import os,re,subprocess,getpass,msq_mng.acl as acl
import msq_mng.getch as getch
kbd=getch._Getch()

clear = lambda: os.system('clear')


last_menuid=None

def show(menu_id,add_tx=[],err='',info=''):
    """zobrazí menu podle menu_id\n
    - menu_id='' tak se zobrazí jen nadpisy, infa a err, menu se nehledá a netiskne
    - add_tx je pole textů, co řádek to zobrazený řádek
    - err pokud<>'' tak je zobrazeno jako error
    - info pokud <>'' tak je zobrazen info řádek"""
    global last_menuid
    ln='--------------------------'
    x='*************************'
    print(x)
    print('*** Mosquitto manager ***')
    print(x)
    last_menuid=None
    if menu_id in _menu.keys() or menu_id=='':
        if len(add_tx)>0:
            for x in add_tx:
                print(x)
            print(ln)
        last_menuid=menu_id
        if menu_id!='':
            for x in _menu[menu_id].keys():
                print (x, '--', _menu[menu_id][x]['tx'] )
            print(ln)
    else:
        print('Menu id not found: ',id)
    if err!='':
        print('!!! ERROR:',err,'!!!')
        print(ln)
    if info!='':
        print('INFO:',info)
        print(ln)

def choice(menu_id,add_tx=[],err='',info=''):
    """zobrazí menu podle menu_id a čeká na vstup, vrací se po volbě z menu\n
    - menu_id='' tak se zobrazí jen nadpisy, infa a err, menu se nehledá a netiskne
    - add_tx je pole textů, co řádek to zobrazený řádek
    - err pokud<>'' tak je zobrazeno jako error
    - info pokud <>'' tak je zobrazen info řádek"""
    show(menu_id,add_tx,err,info)
    if last_menuid==None:
        return None
    # o = input('Enter your choice: ')
    print('Press your choice : ',end='',flush=True)
    o=kbd()
    try:
        if o>='0' and o<='9':
            o=int(o)
            print(str(o),end='',flush=True)
            o2=int(kbd())
            o=str(o)+str(o2)
        else:
            if o>'9':
                o=str(o).upper()
            else:
                o=''
    except:
        o=str(o).upper()
    if o in _menu[menu_id].keys():
        return (o,_menu[menu_id][o]['fn'])
    return '',False

file_users=None
file_acl=None

def generate_users():
    _menu['users']={}
    if os.path.exists(file_users):
        cnt=1
        x=open(file_users)
        usrs=[]
        for y in x.readlines():
            y=str(y).strip().split(':')
            k=str(cnt)
            if(cnt<10):
                k='0'+k
            _menu['users'][k]={
                'tx':'  >>> user: '+y[0],
                'us':y[0],
                'fn':menu_user_mng
            }
            cnt+=1
        _menu['users']['N']={
            'tx':'New user',
            'us':None,
            'fn':create_user
        }
        x.close()
    else:
        _menu['users']['F']={
            'tx':'Users file not found - create ?',
            'us':None,
            'fn':create_user_file
        }
    _menu['users']['Q']={
        'tx':'Back',
        'us':None,
        'fn':None
    }

def menu_users(in_choice):
    generate_users()
    c=''
    fn=''
    while fn!=None:
        clear()
        c,fn=choice('users',['Manage users'])
        if fn!=None and fn!=False:
            fn(c)

def menu_user_mng(in_choice):
    us=_menu['users'][in_choice]
    c=''
    fn=''
    msg=''
    while fn!=None:
        clear()
        c,fn=choice('user_mng',['Edit selected user: '+us['us']],msg)
        if fn!=None:
            # musí vrátit tuple(stav,msg) kde stav None=back, true/false=again (false=chyba), msg=None nebo string zobrazeného textu
            if fn!=False:
                stav,msg=fn(us['us'])
                if stav==None:
                    generate_users()
                    return
            else:
                er=msg
        else:
            return
            

def create_user(in_choice):
    er=''
    while True:
        clear()
        show('',['Create new user, type Q for exit'],er)
        nm=input('Enter new user name ( a-z 0-9 _ ), min length 4: ')
        if re.search("^[a-z0-9_]+$",nm)!=None:
            if nm=='Q' or nm=='q':
                return None
            if len(nm)<4:
                er='wrong length'
            else:
                if nm=='patterns':
                    er='Username contains forbidden word'
                else:
                    f=False
                    for y in _menu['users'].keys():
                        if _menu['users'][y]['us']!=None:
                            if _menu['users'][y]['us']==nm:
                                f=True
                    if f:
                        er="User exists, type another"
                    else:
                        #get pwd
                        pwd,ermsg=enterPwd()
                        if pwd==None:
                            er=ermsg
                        else:
                            cmd='mosquitto_passwd -b '+file_users+' "'+nm+'" "'+pwd+'"'
                            p = subprocess.Popen([cmd], shell=True , stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
                            p.wait()
                            out = p.stdout.read()
                            if p.returncode!=0:
                                er=out
                            else:
                                generate_users()
                                return True
        else:
            er="found wong character in name"


def enterPwd():
    """při chybě vrací (None,'error msg') jinak ('password','')"""
    pwd=getpass.getpass('Enter password ( a-z 0-9 _ & # @ * - ) min length 6: ')
    if re.search("^[a-z0-9_&@#*-]+$",pwd)==None:
        return None,"found frong chars in password"
    else:
        if len(pwd)<6:
            return None,'Min password length: 6'
        else:
            pwd2=getpass.getpass('Enter password again: ')
            if pwd!=pwd2:
                return None,'Passwords not equal'
            else:
                return pwd,''

def create_user_file(in_choice):
    cmd='touch '+file_users
    p = subprocess.Popen([cmd], shell=True , stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    p.wait()
    out = p.stdout.read()
    if p.returncode!=0:
        return False
    else:
        generate_users()
        return None

def user_chng_pwd(in_choice):
    clear()
    show('',['Change password for user "'+in_choice+'"'])
    pwd,msg=enterPwd()
    if pwd==None:
        return False,msg
    else:
        #change
        cmd='mosquitto_passwd -D '+file_users+' "'+in_choice+'"'
        p = subprocess.Popen([cmd], shell=True , stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        p.wait()
        out = p.stdout.read()
        if p.returncode!=0:
            return False,out

        cmd='mosquitto_passwd -b '+file_users+' "'+in_choice+'" "'+pwd+'"'
        p = subprocess.Popen([cmd], shell=True , stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        p.wait()
        out = p.stdout.read()
        if p.returncode!=0:
            return False,out
        else:
            generate_users()
            return None,None

def menu_acl(in_choice):
    generate_users()
    c=''
    fn=''
    while fn!=None:
        acl.generate_ACL()
        clear()
        c,fn=choice('acl',['Manage users ACL'])
        if fn!=None and fn!=False:
            fn(c)
    

def user_delete(in_choice):  
    o=input('Realy delete user "'+in_choice+'" ? (y=Yes, other=No) : ')
    if o=='y' or o=='Y':
        cmd='mosquitto_passwd -D '+file_users+' "'+in_choice+'"'
        p = subprocess.Popen([cmd], shell=True , stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        p.wait()
        out = p.stdout.read()
        if p.returncode!=0:
            return False,out
        else:
            generate_users()
            return None,''
    return True,''

def restart_msqt(c):
    print('Restarting, wait for message: Press any key.')
    os.system('systemctl restart mosquitto')
    print('Press any key')
    kbd()

_menu={
    'main':{
        'U':{
            'tx':'Users',
            'fn':menu_users
        },
        'A':{
            'tx':'ACL',
            'fn':menu_acl
        },
        'R':{
            'tx':'Restart mosquito',
            'fn':restart_msqt
        },
        'Q':{
            'tx':'Exit',
            'fn':None
        }
    },
    'users':{
    },
    'acl':{
    },
    'acl_edit':{
    },
    'acl_new_userblock':{
    },
    'acl_line_menu':{
    },
    'user_mng':{
        'C':{
            'tx':'Change password',
            'fn':user_chng_pwd
        },
        'D':{
            'tx':'Delete user',
            'fn':user_delete
        },
        'Q':{
            'tx':'Back',
            'fn':None
        }
    }
}
