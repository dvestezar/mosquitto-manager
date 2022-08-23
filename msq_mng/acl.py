import re, msq_mng.users as usr, msq_mng.lng as mlng,msq_mng.jbmenu as jml,msq_mng.helper as hlp,curses
from typing import Tuple

lng=mlng.lng
file_acl=None
aclMenu=[]
aclUsers={}

allBlock='* all'

class c_aclline:
    """inicializuj a pak nastav pomocí parse nebo jednotlicých proměnný, pokud nastavejeme proměnné tak path nastavujeme jako poslední"""
    __typ:str=None
    __r:bool=None
    __w:bool=None
    __path:str=None

    def parse(self,tx:str)->str:
        """parsuje řádek ze souboru ACL
        
        vrací None pokud ok, text při chybě"""
        t=''
        r=False
        w=False
        if tx.startswith('topic '):
            tx=tx[6:]
            t="t"
            r,w,tx=self.__get_rw(tx)
        elif tx.startswith('pattern '):
            tx=tx[8:]
            t="p"
            r,w,tx=self.__get_rw(tx)
        else:
            return lng.acl_typ

        if r==w:
            r=False
            w=False
        self.__typ=t
        self.__r=r
        self.__w=w
        return self.set_path(tx)

    def __str__(self) -> str:
        """získá řádek do souboru ACL"""
        r=self.typ+" "
        a=self.attrs
        r+=a
        r+="" if a=="" else " "
        return r+self.__path

    @property
    def typ(self)->str:
        return "topic" if self.__typ=='t' else "pattern"
    @typ.setter
    def typ(self,val):
        if val=='pattern' or val=='p':
            self.__typ='p'
        elif val=='topic' or val=='t':
            self.__typ='t'
    @property
    def isReadOnly(self)->bool:
        return self.__r and not self.__w
    @property
    def isWriteOnly(self)->bool:
        return self.__w and not self.__r
    @property
    def attrs(self):
        """vrátí '', 'read' nebo 'write' podle nastavení"""
        if (self.__w and self.__r) or (not self.__w and not self.__r):
            return ""
        return "read" if self.__r else "write"
    @property
    def path(self)->str:
        return self.__path

    def __get_rw(self,l:str):
        """vrací (read:bool,write:bool, cleaned_text:str)"""
        r=False
        w=False
        if l.startswith('read '):
            r=True
            l=l[5:]
        if l.startswith('write '):
            w=True
            l=l[6:]
        if r==False and l.startswith('read '):
            r=True
            l=l[5:]
        if r==True and w==True:
            r=False
            w=False
        return r,w,l
    def __checkPathItem(self,tx:str,pattern:bool)->bool:
        if pattern:
            if tx=='%u': return True
            if tx=='%c': return True
        return re.search('^\w+$',tx)!=None

    def set_path(self,tx:str)->str:
        """nastaví cestu, před tím je nutné !!!! nastavit typ !!! podle aktuálního typu se testuje cesta

        Args:
            tx (str): cesta

        Returns:
            str: None pokud OK, jinak text chyby
        """
        if tx=='#':
            self.__path=tx
            return None
        patern=self.__typ=='p'
        tx=str(tx).split('/')
        ln=len(tx)
        for i in range(ln):
            x=tx[i].strip()
            if tx[i]!=x:
                return lng.acl_path_spaces
            tx[i]=x
            
            if i==0:
                if tx[0]=='':
                    return lng.acl_path_begin
                if tx[0]!='$SYS' and not self.__checkPathItem(tx[0],patern):
                    return lng.acl_path_forb
            elif i==(ln-1):
                if tx[i]=='':
                    return lng.acl_path_end
                if tx[i]!='#':
                    if not self.__checkPathItem(tx[i],patern):
                        return lng.acl_path_end    
            else:
                if not self.__checkPathItem(tx[i],patern):
                    return lng.acl_path_end
        self.__path='/'.join(tx)

    def set_writeOnly(self):
        self.__r=False
        self.__w=True
    def set_readOnly(self):
        self.__r=True
        self.__w=False


def menu_acl(in_choice):
    """hlavní menu ACL"""
    usr.generate_users()
    i=jml.menuitem('')
    while i.fn!=None:
        generate_ACL()
        i=jml.choice(aclMenu,[lng.user_mng_acl])
        if i.fn!=None and i.fn!=False:
            i.fn(i)

def generate_ACL():
    global aclMenu,aclUsers
    m={allBlock:[]}
    u=[]
    f=open(file_acl)
    lu=allBlock
    cnt=1
    for l in f.readlines():
        l=l.strip()
        if l.startswith('topic ') or l.startswith('pattern '):
            r=c_aclline()
            l=r.parse(str(l).strip())
            if l==None:
                if lu not in m.keys():
                    m[lu]=[]
                m[lu].append( r )
        elif l.startswith('user '):
            lu=l[5:]
        elif l=='':
            lu=allBlock

        x=lu
        f=False
        for xx in u:
            if xx.us==x:
                f=True
                break
        if not f:
            u.append(jml.menuitem(
                '{:>02}'.format(cnt),
                '  >>> '+lng.acl_forusr+': '+x,
                acl_user_menu,
                x,
                user_exists(x)
            ))
            cnt+=1

    u.append(jml.menuitem(
        lng.choiceACLnewbl[0],
        lng.acl_newblock,
        add_user_block
    ))
    u.append(jml.menuitem(
        lng.choiceQ[0],
        lng.back
    ))

    aclMenu=u
    aclUsers=m

def user_exists(user)->bool:
    if user==allBlock:
        return True
    for x in usr.menu:
        if x.us==user:
            return True
    return False

def acl_user_menu(c:jml.menuitem):
    """menu s vypsanými acl uživatele"""
    i=jml.menuitem('')
    while i.fn!=None:
        m=[]
        cnt=1
        if len(aclUsers[c.us])>0:
            for x in aclUsers[c.us]:
                m.append(jml.menuitem(
                    '{:>02}'.format(cnt),
                    '   : '+str(x),
                    edit_user_topic,
                    c.us,
                    aclLine=x
                ))
                cnt+=1

        m.append(jml.menuitem(
            lng.choiceACLnewtp[0],
            lng.acl_newtp,
            add_user_topic,
            c.us
        ))
        m.append(jml.menuitem(
            lng.choiceACLdelall[0],
            lng.acl_delall,
            del_all_acl,
            c.us
        ))
        m.append(jml.menuitem(
            lng.choiceQ[0],
            lng.back
        ))

        i=jml.choice(m,[lng.acl_mnglines+': '+c.us])
        if i.fn!=None:
            c.aclLine=i.aclLine
            if i.fn(c)==False:
                acl_save()
                return
        acl_save()

def del_all_acl(c:jml.menuitem):
    hlp.win.addstr(lng.acl_qdellall+' "'+c.us+'"? '+lng.yesother+' : ')
    o=hlp.win.getkey()
    if o in lng.choiceY:
        if c.us==allBlock:
            aclUsers[allBlock]=[]
        else:
            del(aclUsers[c.us])
        acl_save()
        return False

def add_user_block(i:jml.menuitem):
    #get users from pwd
    u_pwd=[allBlock]
    for x in usr.menu:
        if x.us!=None:
            u_pwd.append(x.us)

    #get users from acl
    u_acl=[]
    for x in aclUsers:
        u_acl.append(x)

    #show menu for intersects user
    u_m=list(set(u_acl) ^ set(u_pwd))

    if len(u_m)==0:
        hlp.win.addstr('\n!!! '+lng.acl_moavailusr+'\n')
        hlp.win.getkey()
    else:
        #make menu and select new section for user
        i=jml.menuitem('')
        while i.fn!=None:
            cnt=1
            m=[]
            for x in u_m:
                m.append(jml.menuitem(
                    '{:>02}'.format(cnt),
                    '  >>> '+lng.acl_addblforus+':  '+x,
                    make_user_block,
                    x
                ))
                cnt+=1
        
            m.append(jml.menuitem(
                lng.choiceQ[0],
                lng.back
            ))

            i=jml.choice(m,[lng.acl_newusrbl,lng.acl_newusrblnfo])
            if i.fn!=None:
                if i.fn(i)==True:
                    return

def input_acl_topic_line() -> Tuple[c_aclline,str]:
    """vstup pro zadání ACL řádky,
    
    vrací tuple (acl_line,msg) kde msg=None je vše ok, jinak onsahuje msg text chyby"""
    aline=c_aclline()

    hlp.win.addstr(lng.acl_add_type+' : ')
    t=hlp.win.getkey()
    aline.typ='t' if t in lng.choiceAclAddType else 'p'
    hlp.win.addstr(lng.acl_addtype_sel+': ' + aline.typ + '\n',curses.A_REVERSE)

    hlp.win.addstr(lng.acl_addattr+' "read" '+lng.yesother+' : ')
    r=hlp.win.getkey()
    r=( r in lng.choiceY )
    hlp.win.addstr(lng.acl_atrsel+': ' + (lng.tx_yes if r else lng.tx_no) + '\n',curses.A_REVERSE)
    
    hlp.win.addstr(lng.acl_addattr+' "write" '+lng.yesother+' : ')
    w=hlp.win.getkey()
    w=( w in lng.choiceY )
    hlp.win.addstr(lng.acl_atrsel+': ' + (lng.tx_yes if w else lng.tx_no) + '\n',curses.A_REVERSE)
    
    if w==r:
        r=False
        w=False
    else:
        if r:aline.set_readOnly()
        if w:aline.set_writeOnly()

    hlp.win.addstr('\n')
    hlp.win.addstr(lng.acl_line_nfo)
    hlp.win.addstr('\n')
    hlp.win.addstr(lng.acl_typepath+': ')

    curses.echo()
    o=str(hlp.win.getstr(30),'UTF-8')
    curses.noecho()
    o=str(o).strip()

    x=aline.set_path(o)
    return aline,x

def __checkUserTopicExists(user:str,aclline:c_aclline)->bool:
    """vrací true pokud aclline již existuje v uživatelově bloku"""
    r=str(aclline)
    if len(aclUsers[user])==0:
        return False
    for f in aclUsers[user]:
        if str(f)==r:
            return True
    return False

def add_user_topic(user):
    if type(user) is jml.menuitem:
        user=user.us

    jml.show(None,['Vytvoření bloku pro uživatele: '+user])

    aline,msg=input_acl_topic_line()
    if msg!=None:
        hlp.win.addstr('!!! '+lng.err+': '+lng.acl_path_forb+' - '+msg)
        hlp.win.getkey()
    else:
        if not user in aclUsers.keys():
            aclUsers[user]=[]
        if __checkUserTopicExists(user,aline):
            hlp.win.addstr('!!! '+lng.err+': '+lng.acl_line_exists)
            hlp.win.getkey()
            return
        aclUsers[user].append(aline)
        acl_save()
        return True

def make_user_block(i:jml.menuitem):
    return add_user_topic(i.us)

def acl_save():
    o=''

    #all
    if allBlock in aclUsers.keys():
        if len(aclUsers[allBlock])>0:
            for x in aclUsers[allBlock]:
                x=str(x)
                o+=x+"\r\n"
            o+="\r\n"

    #users
    for x in aclUsers.keys():
        if x!=allBlock:
            if len(aclUsers[x])>0:
                o+='user '+x+"\r\n"
                for y in aclUsers[x]:
                    y=str(y)
                    o+=y+"\r\n"
                o+="\r\n"

    f=open(file_acl,'w')
    f.write(o)
    f.close()
    
def edit_user_topic(i:jml.menuitem):
    r=i.aclLine
    m=[]
    m.append(jml.menuitem(
        lng.choiceACLlineed[0],
        lng.acl_line_ed,
        acl_editLine,
        i.us,
        aclLine=r
    ))
    m.append(jml.menuitem(
        lng.choiceACLlinedel[0],
        lng.acl_line_del,
        acl_delLine,
        i.us,
        aclLine=r
    ))
    m.append(jml.menuitem(
        lng.choiceQ[0],
        lng.back
    ))
    i=jml.menuitem('')
    while i.fn!=None:
        i=jml.choice(m,[ lng.acl_editusrline.format(i.us,str(r))] )
        if i.fn!=None:
            if i.fn(i)==True:
                return
    

def acl_delLine(i:jml.menuitem):
    hlp.win.addstr('\n'+lng.acl_qline_del+'? '+lng.yesother)
    o=hlp.win.getkey()
    if o in lng.choiceY:
        r=str(i.aclLine)
        for f in range(len(aclUsers[i.us])):
            if str(aclUsers[i.us][f])==r:
                del(aclUsers[i.us][f])
                return True

def acl_editLine(i:jml.menuitem):
    r=str(i.aclLine)
    for f in range(len(aclUsers[i.us])):
        if str(aclUsers[i.us][f])==r:
            aline=None
            jml.show(None,[lng.acl_editusrline.format(i.us,str(r)),lng.acl_editLine])
            aline,msg=input_acl_topic_line()
            if msg!=None:
                hlp.win.addstr('\n!!! '+lng.err+' - '+lng.alc_path_lng_er+' : '+msg)
                hlp.win.getkey()
                return False
            else:
                if __checkUserTopicExists(i.us,aline):
                    hlp.win.addstr('!!! '+lng.err+': '+lng.acl_line_exists)
                    hlp.win.getkey()
                    return False
                aclUsers[i.us][f]=aline
                return True
