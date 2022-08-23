import msq_mng.jbmenu as jmn,os, msq_mng.lng as mlng,subprocess,msq_mng.helper as hlp,curses,re

lng=mlng.lng

file_users=''
menu=[]
"""uživatelské menu, také seznam userů list of menuitem"""

def generate_users():
    global menu
    r=[]
    if os.path.exists(file_users):
        cnt=1
        x=open(file_users)
        usrs=[]
        for y in x.readlines():
            y=str(y).strip().split(':')
            k=str(cnt)
            if(cnt<10):
                k='0'+k
            r.append( jmn.menuitem(
                k,
                '\t '+lng .user+': '+y[0],
                menu_user_mng,
                y[0]
            ))
            cnt+=1
        r.append( jmn.menuitem(
            lng.choiceNew[0],
            lng.user_new,
            create_user
        ))
        x.close()
    else:
        r.append( jmn.menuitem(
            lng.choiseUserFile[0],
            lng.user_file,
            create_user_file
        ))
    r.append( jmn.menuitem(
        lng.choiceQ[0],
        lng.back
    ))
    menu=r

def menu_users(in_choice):
    """hlavní user menu - seznam uživatelů"""
    i=jmn.menuitem('')
    while i.fn!=None:
        generate_users()
        i=jmn.choice(menu,[lng.users_manage])
        if i.fn!=None:
            i.fn(i)

def menu_user_mng(vi:jmn.menuitem):
    """menu pro managing uživatele"""
    stav=''
    msg=''
    er=''
    i=jmn.menuitem('')
    while i.fn!=None:
        i=jmn.choice(user_mng,[lng.user_edit+': '+vi.us],er)
        if i.fn!=None:
            # musí vrátit tuple(stav,msg) kde stav None=back, true/false=again (false=chyba), msg=None nebo string zobrazeného textu
            stav,msg=i.fn(vi.us)
            if stav==None:
                generate_users()
                return
            elif stav==False:
                er=msg
            else:
                er=''
        else:
            return

def create_user(in_choice):
    win=hlp.win
    er=''
    while True:
        jmn.show(None,[lng.user_create],er)
        win.addstr(lng.user_enter+': ')
        curses.echo()
        nm=str(win.getstr(30),'UTF-8')
        curses.noecho()
        win.addstr('\n')
        if re.search("^[a-z0-9_]+$",nm)!=None:
            if nm in lng.choiceQ:
                return None
            if len(nm)<4:
                er=lng.user_lng_err
            else:
                if nm=='patterns' or nm=='topic':
                    er=lng.user_err_word
                else:
                    f=False
                    for i in menu:
                        if i.us!=None:
                            if i.us==nm:
                                f=True
                    if f:
                        er=lng.user_exists
                    else:
                        #get pwd
                        pwd,ermsg=hlp.enterPwd()
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
    jmn.show(None,[lng.pwd_us+' "'+in_choice+'"'])
    pwd,msg=hlp.enterPwd()
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

def user_delete(in_choice):
    hlp.win.addstr(lng.user_del+' "'+in_choice+'" ? '+lng.yesother+' : ')
    o=hlp.win.getkey()
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

user_mng=[
    jmn.menuitem(lng.choicepwdchng[0],  lng.menu_chngpwd,   user_chng_pwd),
    jmn.menuitem(lng.choiceDelUs[0],    lng.menu_delUs,     user_delete),
    jmn.menuitem(lng.choiceQ[0],        lng.back,           None)
]