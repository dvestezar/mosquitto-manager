import os,re,subprocess,getpass,msq_mng.acl as acl
import msq_mng.getch as getch
import msq_mng.lng as mlng

lng=mlng.lng
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
    ln=lng.line
    x=lng.starline
    print(x)
    print('*** '+lng.app_title+' ***')
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
        print(lng.err_menuid+': ',id)
    if err!='':
        print('!!! '+lng.err+': ',err,'!!!')
        print(ln)
    if info!='':
        print(lng.nfo+': ',info)
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
    print(lng.keychoice+' : ',end='',flush=True)
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
                'tx':'  >>> '+lng .user+': '+y[0],
                'us':y[0],
                'fn':menu_user_mng
            }
            cnt+=1
        _menu['users'][lng.choiceNew[0]]={
            'tx':lng.user_new,
            'us':None,
            'fn':create_user
        }
        x.close()
    else:
        _menu['users'][lng.choiseUserFile[0]]={
            'tx':lng.user_file,
            'us':None,
            'fn':create_user_file
        }
    _menu['users'][lng.choiceQ[0]]={
        'tx':lng.back,
        'us':None,
        'fn':None
    }

def menu_users(in_choice):
    generate_users()
    c=''
    fn=''
    while fn!=None:
        clear()
        c,fn=choice('users',[lng.users_manage])
        if fn!=None and fn!=False:
            fn(c)

def menu_user_mng(in_choice):
    us=_menu['users'][in_choice]
    c=''
    fn=''
    msg=''
    while fn!=None:
        clear()
        c,fn=choice('user_mng',[lng.user_edit+': '+us['us']],msg)
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
        show('',[lng.user_create],er)
        nm=input(lng.user_enter+': ')
        if re.search("^[a-z0-9_]+$",nm)!=None:
            if nm in lng.choiceQ:
                return None
            if len(nm)<4:
                er=lng.user_lng_err
            else:
                if nm=='patterns':
                    er=lng.user_err_word
                else:
                    f=False
                    for y in _menu['users'].keys():
                        if _menu['users'][y]['us']!=None:
                            if _menu['users'][y]['us']==nm:
                                f=True
                    if f:
                        er=lng.user_exists
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
            er=lng.user_err_char


def enterPwd():
    """při chybě vrací (None,'error msg') jinak ('password','')"""
    pwd=getpass.getpass(lng.pwd_new+': ')
    if re.search("^[a-z0-9_&@#*-]+$",pwd)==None:
        return None,lng.pwd_err_char
    else:
        if len(pwd)<6:
            return None,lng.pwd_lng
        else:
            pwd2=getpass.getpass(lng.pwd_again+': ')
            if pwd!=pwd2:
                return None,lng.pwd_neq
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
    show('',[lng.pwd_us+' "'+in_choice+'"'])
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
        c,fn=choice('acl',[lng.user_mng_acl])
        if fn!=None and fn!=False:
            fn(c)
    

def user_delete(in_choice):  
    o=input(lng.user_del+' "'+in_choice+'" ? '+lng.yesother+' : ')
    if o in lng.choiceY:
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
    print(lng.msqt_restart)
    os.system('systemctl restart mosquitto')
    print(lng.pressakey)
    kbd()

_menu={
    'main':{
        lng.choiceUsers[0]:{
            'tx':lng.menu_users,
            'fn':menu_users
        },
        lng.choiceACL[0]:{
            'tx':lng.menu_acl,
            'fn':menu_acl
        },
        lng.choiceResMsq[0]:{
            'tx':lng.menu_res_msq,
            'fn':restart_msqt
        },
        lng.choiceQuittx[0]:{
            'tx':lng.quittx,
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
        lng.choicepwdchng[0]:{
            'tx':lng.menu_chngpwd,
            'fn':user_chng_pwd
        },
        lng.choiceDelUs[0]:{
            'tx':lng.menu_delUs,
            'fn':user_delete
        },
        lng.choiceQ[0]:{
            'tx':lng.back,
            'fn':None
        }
    }
}
