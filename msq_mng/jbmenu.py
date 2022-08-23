import msq_mng.lng as mlng,curses
import msq_mng.helper as hlp

ver:str=""
"""Pokud nastavíme tak se zobrazí verze př. ver='1.15.30'"""
lng=mlng.lng

class JBMenuException(Exception):
    pass
class JBMenuItemException(Exception):
    pass

class menuitem:
    idx:str=''
    """klávesa volby nebo textové číslo 00-99 je to kopie key, pokud ='' tak se při stisku ignoruje"""
    tx:str=''
    """Zobrazený text, pokud = '' tak se zobrazí prázdný řádek"""
    fn=None
    """funkce pro zpracování nebo None"""
    us:str=None
    """uživatel pomocná proměnná"""
    exists:bool=False
    """pomocná proménná - user exists - když je v ACL řádek pro uživatel který není v heslech"""
    selected:bool=False
    """Selected menu"""

    aclLine=None
    """řádek ACL"""

    def __init__(self,idx,tx:str='',fn=None,us:str=None,exists:bool=None,aclLine=None) -> None:
        """vytvoří objekt menuitem

        Args:
            idx (menuitem|str): pokud '' tak vytvoří prázdný objekt s fn='', používá se jako init před vstupem do while, jinak char nebo číslo volby
            tx (str, optional): zobrazený text. Defaults to ''.
            fn (_type_, optional): funkce. Defaults to None.
            us (str, optional): uživatel. Defaults to None.
            exists (bool, optional): user exists. Defaults to None.

        Raises:
            JBMenuItemException: chyba vytvoření
        """
        if type(idx)==str:
            self.idx=idx.upper()
            if len(self.idx)==1 and (self.idx<'A' or self.idx>'Z'):
                raise JBMenuItemException(lng.menuitem_idx_char)
            elif len(self.idx)==1 and self.idx>='A' and self.idx<='Z':
                pass
            elif len(self.idx)==2:
                try:
                    x=int(self.idx)
                except:
                    raise JBMenuItemException(lng.menuitem_idx_num)
                if x<0 or x>99:
                    raise JBMenuItemException(lng.menuitem_idx_num)
            elif self.idx=='':
                fn=''
            else:
                raise JBMenuItemException(lng.menuitem_idx_err)
            self.tx=tx
            self.fn=fn
            self.us=us
            self.exists=exists
            self.aclLine=aclLine
        elif type(idx)==menuitem:
            self.idx=idx.idx
            self.tx=idx.tx
            self.fn=idx.fn
            self.us=idx.us
            self.exists=idx.exists
        else:
            raise JBMenuItemException(lng.needsmenuitem)

    def getMenuTx(self)->str:
        return self.idx + ' -- ' + self.tx


def show(menu:list,add_tx=[],err='',info='',menusel_idx:str=''):
    """zobrazí menu podle menu_id\n
    - menu=None tak se zobrazí jen nadpisy, infa a err, menu se netiskne
    - add_tx je pole textů, co řádek to zobrazený řádek
    - err pokud<>'' tak je zobrazeno jako error
    - info pokud <>'' tak je zobrazen info řádek
    - menusel_idx pokud se rovná idx v menuitem tak je řádek zobrazen inverzně"""
    win=hlp.win
    v=ver
    if v!='': v=' v.: '+v
    tit='***   '+lng.app_title+v+'   ***'
    itms=[]
    itms.append( [None,'*'] )
    itms.append( [curses.A_UNDERLINE,tit] )
    itms.append( [None,'*'] )
    itms.append( [None,''] )
    if menu==None or type(menu)==list:
        if len(add_tx)>0:
            for x in add_tx:
                itms.append([None,x])
            itms.append( [None,'-'] )
        if menu!=None:
            for x in menu:
                # x=menuitem(x)
                if x.tx=='':
                    itms.append([None,''])
                else:
                    if menusel_idx==x.idx:
                        itms.append( [curses.A_REVERSE, ' '+x.getMenuTx()+' '] )
                    else:
                        itms.append( [None, ' '+x.getMenuTx()+' '] )
            itms.append( [None,'-'] )
    else:
        raise Exception(lng.err_menuid)
    if err!='':
        itms.append( [None,'!!! '+lng.err+': '+err+' !!!'] )
        itms.append( [None,'-'] )
    if info!='':
        itms.append( [None,lng.nfo+': '+info])
        itms.append( [None,'-'] )
    
    lln=0
    for i in itms:
        x=len(i[1])
        if lln<x: lln=x

    sline=("{:*>"+str(lln)+"}").format('')
    mline=("{:->"+str(lln)+"}").format('')

    win.clear()
    toln="{: <"+str(lln)+"}"
    for i in itms:
        if i[1]=='' or i[1]==None:
            pass
        elif i[1]=='*':
            win.addstr(sline)
        elif i[1]=='-':
            win.addstr(mline)
        else:
            if i[0]==None:
                win.addstr(toln.format(i[1]))
            else:
                win.addstr(toln.format(i[1]),i[0])
        win.addstr('\n')
    win.refresh()

def choice(menu:list,add_tx=[],err='',info='')->menuitem:
    """zobrazí menu podle menu_id a čeká na vstup, vrací se po volbě z menu\n
    - menu=None tak se zobrazí jen nadpisy, infa a err, menu se netiskne
    - add_tx je pole textů, co řádek to zobrazený řádek
    - err pokud<>'' tak je zobrazeno jako error
    - info pokud <>'' tak je zobrazen info řádek"""
    win=hlp.win
    s=None
    sel=0
    ln=len(menu)-1
    while True:
        show(menu,add_tx,err,info,menu[sel].idx)
        win.addstr(lng.keychoice+' : ')
        y,x=win.getyx()
        o=win.getkey()
        win.refresh()
        try:
            if o>='0' and o<='9':
                o=int(o)
                win.addstr(y,x,str(o))
                o2=int(win.getkey())
                o=str(o)+str(o2)
            elif o=='KEY_UP':
                sel-=1
                if sel<0: sel=ln
            elif o=='KEY_DOWN':
                sel+=1
                if sel>ln: sel=0
            elif o=='\n':
                return menu[sel]
            else:
                if o>'9':
                    o=str(o).upper()
                else:
                    o=''
        except:
            o=str(o).upper()
        for i in menu:
            if i.idx==o:
                return i
        
