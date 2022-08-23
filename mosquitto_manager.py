import curses
import os, msq_mng.lng as mlng, msq_mng.helper as hlp,msq_mng.jbmenu as jmn, msq_mng.users as usr,msq_mng.acl as acl
from curses import wrapper

ver="2.0.0"
lng=mlng.lng

msqt_root='/etc/mosquitto/'
cnf_file=msqt_root+'mosquitto.conf'
hlp.cnf_file=cnf_file
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
def getinfo(x=None):
    global lns
    hlp.win.clear()
    lst=findprop(lns,'listener')
    if lst==None: lst=lng.notusd
    port=findprop(lns,'port')
    if port==None: port=lng.notusd
    tls=lng.notusd
    ca=findprop(lns,'cafile')
    if ca==None:
        ca=lng.notusd
    else:
        if os.path.exists(ca):
            ca=lng.ca_ok
        else:
            ca=lng.err+': '+lng.ca_err
        tls=findprop(lns,'tls_version')
        if tls==None: tls=lng.notusd

    hlp.win.addstr(lng.cfg_nfo.format(lst=lst,port=port,tls=tls,ca=ca))
    hlp.win.addstr('\n'+lng.pressakey)
    hlp.win.refresh()
    hlp.win.getkey()


if not os.path.exists(cnf_file):
    raise Exception(lng.cnf_nan)

jmn.ver=ver
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

usr.file_users=findprop(lns,'password_file')
acl.file_acl=findprop(lns,'acl_file')

main_menu=[
    jmn.menuitem(lng.choiceUsers[0],    lng.menu_users,     usr.menu_users),
    jmn.menuitem(lng.choiceACL[0],      lng.menu_acl,       acl.menu_acl),
    jmn.menuitem(lng.choiceResMsq[0],   lng.menu_res_msq,   hlp.restart_msqt),
    jmn.menuitem(lng.choiceDbgMsq[0],   lng.menu_dbg_msq,   'debug'),
    jmn.menuitem(lng.choiceStatsMsq[0], lng.menu_msq_stat,   'status'),
    jmn.menuitem(lng.choiceCfgNfo[0],   lng.menu_cfg_nfo,   getinfo),

    jmn.menuitem(lng.choiceQuittx[0],lng.quittx,None)
]

def run(win:curses.window):
    hlp.win=win

    i=jmn.menuitem('')
    usr.generate_users()
    while i.fn!=None:
        i=jmn.choice(main_menu,[
            '- '+lng.mainmenu_pwdfile +' : '+usr.file_users,
            '- '+lng.mainmenu_aclfile +' : '+acl.file_acl,
            '- '+lng.mainmenu_ucnt    +' : '+str(len(usr.menu)-2)
        ])
        if i.fn!=None:
            if i.fn=='debug' or i.fn=='status':
                return i.fn
            else:
                i.fn(i.idx)

    return None

x=''
while x!=None:
    x=wrapper(run)
    if x=='debug':
        hlp.msqt_run_debug()
    elif x=='status':
        hlp.msqt_status()

