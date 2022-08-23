import msq_mng.lng as mlng,os,curses,re,os

win:curses.window=None
lng=mlng.lng
cnf_file=None

def restart_msqt(c):
    win.clear()
    win.addstr(lng.msqt_restart+'\n')
    win.refresh()
    os.system('systemctl restart mosquitto')
    win.clear()
    win.addstr(lng.pressakey+'\n')
    win.refresh()
    win.getkey()

def clearConsole():
    if os.name=='nt':
        os.system('cls')
    else:
        os.system('clear')    

def msqt_run_debug(c=None):
    clearConsole()
    print(lng.msqt_rundebug+'\r\n')
    win.getkey()
    clearConsole()
    print(lng.msqt_rundebug_run+'\r\n')
    os.system('systemctl stop mosquitto')
    os.system('mosquitto -c {} -v'.format(cnf_file))
    os.system('systemctl start mosquitto')

def msqt_status(c=None):
    clearConsole()
    os.system('systemctl status mosquitto')
    print('\r\n'+lng.pressakey)
    win.getkey()

def enterPwd():
    """při chybě vrací (None,'error msg') jinak ('password','')"""
    curses.noecho()
    win.addstr(lng.pwd_new+': ')
    y,x=win.getyx()
    pwd=_enterpwd()
    if re.search("^[a-z0-9_&@#*-]+$",pwd)==None:
        return None,lng.pwd_err_char
    else:
        if len(pwd)<6:
            return None,lng.pwd_lng
        else:
            win.addstr(lng.pwd_again+': ')
            pwd2=_enterpwd()
            if pwd!=pwd2:
                return None,lng.pwd_neq
            else:
                return pwd,''

def _enterpwd(maxlength:int=30)->str:
    y,x=win.getyx()
    pwd=''
    while True:
        ch=win.getkey()
        if len(ch)==1:
            if ch>=' ' and ch<='z' and ch!='"' and ch!="'":
                pwd+=ch
                s=lng.pwd_chars+(" {}: {:*>"+str(len(pwd))+"}").format(len(pwd),'')
                win.addstr(y,x, s )
                if len(pwd)==maxlength:
                    win.addstr('\n')
                    return pwd
            elif ch=='\n':
                win.addstr('\n')
                return pwd

