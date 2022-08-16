import os,time,importlib
import msq_mng.lng as mlng
lng=mlng.lng

msqt_root='/etc/mosquitto/'

def getlines(from_lines,to_lines):
    for x in from_lines:
        y=str(x).strip()
        if not y.startswith('#') and y!='':
            to_lines.append(y)

def findprop(from_lines,cmd:str)->str:
    cmd+=' '
    for x in from_lines:
        if x.startswith(cmd):
            return x.replace(cmd,'')
    return None

cnf_file=msqt_root+'mosquitto.conf'
if not os.path.exists(cnf_file):
    raise Exception('config not found')

lns=[]
cnf=open(cnf_file)
getlines(cnf.readlines(),lns)
cnf.close()
del(cnf)

file_pwd=None
file_acl=None
include_dir=findprop(lns,'include_dir')
inc_fls=[]
if include_dir!=None:
    if os.path.exists(include_dir):
        x=os.listdir(include_dir)
        for y in x:
            if y.endswith('.conf'):
                inc_fls.append(y)

if len(inc_fls)>0:
    for f in inc_fls:
        x=open(include_dir+'/'+f)
        getlines(x.readlines(),lns)
        x.close()

import msq_mng.menus as menus
menus.file_users=findprop(lns,'password_file')
menus.file_acl=findprop(lns,'acl_file')


choice=''
fn=''
while fn!=None:
    menus.generate_users()
    menus.clear()
    choice,fn=menus.choice('main',[
        '- '+lng.mainmenu_pwdfile +' : '+menus.file_users,
        '- '+lng.mainmenu_aclfile +' : '+menus.file_acl,
        '- '+lng.mainmenu_ucnt    +' : '+str(len(menus._menu['users'])-2)
    ])
    if fn!=None and fn!=False:
        fn(choice)
    
menus.clear()
print(lng.quittx)