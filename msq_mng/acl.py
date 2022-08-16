import msq_mng.menus as menus, msq_mng.getch as getch, re
import msq_mng.lng as mlng

lng=mlng.lng

kbd=getch._Getch()
content={}

class menu:
    @staticmethod
    def get():
        return menus._menu['acl']
    @staticmethod
    def set(val):
        menus._menu['acl']=val

def generate_ACL():
    global content
    m={
        '*':[],
        '_':[]
    }
    u={

    }
    f=open(menus.file_acl)
    lu='*'
    cnt=1

    for l in f.readlines():
        l=str(l).strip()
        if l.startswith('topic '):
            l=l[6:]
            r,w,l=get_rw(l)
            if lu not in m.keys():
                m[lu]=[]
            m[lu].append( ['t',l,r,w] )
        elif l.startswith('user '):
            lu=l[5:]
        elif l=='':
            lu='*'
        elif l.startswith('pattern '):
            l=l[8:]
            r,w,l=get_rw(l)
            m['_'].append( ['p',l,r,w] )
            lu='_'

        x=lu
        if x=='*':
            x='* all'
        if x=='_':
            x='* patterns'
        f=False
        for xx in u.keys():
            if u[xx]['us']==x:
                f=True
                break
        if not f:
            u['{:>02}'.format(cnt)]={
                'tx':'  >>> '+lng.acl_forusr+': '+x,
                'us':x,
                'idx':lu,
                'fn':acl_user_menu,
                'exists':user_exists(x)
            }
            cnt+=1

    u[lng.choiceACLnewbl[0]]={
        'tx':lng.acl_newblock,
        'us':None,
        'fn':add_user_block,
        'exists':None
    }
    u[lng.choiceQ[0]]={
        'tx':lng.back,
        'us':None,
        'fn':None,
        'exists':None
    }

    menu.set(u)
    content=m

    # print(u)
    # print(m)
    # kbd()

def user_exists(user)->bool:
    if user=='all' or user=='patterns':
        return True
    for x in menus._menu['users'].keys():
        u=menus._menu['users'][x]
        if u['us']==user:
            return True
    return False

def acl_user_menu(c):
    user=menus._menu['acl'][c]
    nfo=content[user['idx']]

    c=''
    fn=''
    while fn!=None:
        m={
        }

        cnt=1
        if len(content[user['idx']])>0:
            for x in content[user['idx']]:
                p,l,r,w=x
                m['{:>02}'.format(cnt)]={
                    'tx':'  >>> '+lng.acl_line+': '+('read ' if r else '') + ('write ' if w else '') + l ,
                    'us':user,
                    'line':x,
                    'fn':edit_user_topic
                }
                cnt+=1


        m[lng.choiceACLnewtp[0]]={
            'tx':lng.acl_newtp,
            'us':user,
            'fn':add_user_topic
        }
        m[lng.choiceACLdelall[0]]={
            'tx':lng.acl_delall,
            'us':user,
            'fn':del_all_acl
        }
        m[lng.choiceQ[0]]={
            'tx':lng.back,
            'us':None,
            'fn':None,
            'exists':None
        }
        menus._menu['acl_edit']=m

        menus.clear()
        c,fn=menus.choice('acl_edit',[lng.acl_mnglines+': '+user['us']])
        if fn!=None and fn!=False:
            if fn(user,c)==False:
                acl_save()
                return
        acl_save()

def del_all_acl(user,c=None):
    print(lng.acl_qdellall+' "'+user['us']+'"? '+lng.yesother+' : ')
    o=kbd()
    if o in lng.choiceY:
        if user['idx']=='*' or user['idx']=='_':
            content[user['idx']]=[]
        else:
            del(content[user['idx']])
        acl_save()
        return False

def get_rw(l:str):
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

def add_user_block(c):
    #get users from pwd
    u_pwd=[]
    for x in menus._menu['users'].keys():
        u=menus._menu['users'][x]['us']
        if u!=None:
            u_pwd.append(u)

    #get users from acl
    u_acl=[]
    for x in content.keys():
        if x!='*' and x!='_':
            u_acl.append(x)

    #show menu for intersects user
    u_m=list(set(u_acl) ^ set(u_pwd))

    if len(u_m)==0:
        print(lng.acl_moavailusr)
        kbd()
    else:
        #make menu and select new section for user
        c=''
        fn=''
        while fn!=None:
            cnt=1
            m={}
            for x in u_m:
                m['{:>02}'.format(cnt)]={
                    'tx':'  >>> '+lng.acl_addblforus+':  '+x,
                    'us':x,
                    'fn':make_user_block
                }
                cnt+=1
        
            m[lng.choiceQ[0]]={
                'tx':lng.back,
                'us':None,
                'fn':None
            }
            menus._menu['acl_new_userblock']=m

            menus.clear()
            c,fn=menus.choice('acl_new_userblock',[lng.acl_newusrbl,lng.acl_newusrblnfo])
            if fn!=None and fn!=False:
                if fn(m[c]['us'])==True:
                    return

def add_user_topic(user,c=None):
    if type(user) is dict:
        user=user['idx']
    print('\r\n')
    
    print(lng.acl_addattr+' "read" '+lng.yesother+' : ')
    r=kbd()
    r=( r in lng.choiceY )
    print(lng.acl_atrsel+': ' + (lng.tx_yes if r else lng.tx_no) )
    
    print(lng.acl_addattr+' "write" '+lng.yesother+' : ')
    w=kbd()
    w=( w in lng.choiceY )
    print(lng.acl_atrsel+': ' + (lng.tx_yes if w else lng.tx_no) )
    
    print('\r\n'+lng.acl_line_nfo1)
    print('\r\n'+lng.acl_line_nfo2)
    o=input('\r\n'+lng.acl_typepath+': ')
    o=str(o).strip()
    if re.match('[ *+-]',o)!=None:
        print(lng.acl_path_forb)
        kbd()
    else:
        if len(o)<1:
            print(lng.alc_path_lng_er)
            kbd()
            return
        else:
            content[user].append(['t',o,r,w])
            acl_save()
            return True

def make_user_block(user):
    content[user]=[]
    return add_user_topic(user)

def acl_save():
    o=''

    #all
    if '*' in content.keys():
        if len(content['*'])>0:
            for x in content['*']:
                p,l,r,w=x
                o+='topic '
                if r:
                    o+='read '
                if w:
                    o+='write '
                o+=l+"\r\n"
            o+="\r\n"

    #users
    for x in content.keys():
        if x!='*' and x!='_':
            if len(content[x])>0:
                o+='user '+x+"\r\n"
                for y in content[x]:
                    p,l,r,w=y
                    o+='topic '
                    if r:
                        o+='read '
                    if w:
                        o+='write '
                    o+=l+"\r\n"
                o+="\r\n"

    #patterns
    if '_' in content.keys():
        if len(content['_'])>0:
            for x in content['_']:
                p,l,r,w=x
                o+='pattern '
                if r:
                    o+='read '
                if w:
                    o+='write '
                o+=l+"\r\n"
            o+="\r\n"

    f=open(menus.file_acl,'w')
    f.write(o)
    f.close()
    
def edit_user_topic(user,c):
    nfo=menus._menu['acl_edit'][c]

    # nfo['us']={'tx': '  user: test', 'us': 'test', 'idx': 'test', 'fn': <function acl_user_menu at 0x7f72047fc040>, 'exists': True}
    # nfo['line']=['t', 'test/topic', False, False]  l,r,w
    # menus._menu['acl_line_menu']
    m={}

    m[lng.choiceACLlineed[0]]={
        'tx':lng.acl_line_ed,
        'fn':acl_editLine
    }
    m[lng.choiceACLlinedel[0]]={
        'tx':lng.acl_line_del,
        'fn':acl_delLine
    }
    m[lng.choiceQ[0]]={
        'tx':lng.back,
        'fn':None
    }
    menus._menu['acl_line_menu']=m

    choice=''
    fn=''
    while fn!=None:
        menus.clear()
        c,fn=menus.choice('acl_line_menu',[ lng.acl_editusrline.format(nfo['us']['us'],nfo['line'][1]) ] )
        if fn!=None and fn!=False:
            if fn(nfo)==True:
                return
    

def acl_delLine(nfo):
    print('\r\n'+lng.acl_qline_del+'? '+lng.yesother)
    o=kbd()
    if o in lng.choiceY:
        for idx, i in enumerate(content[nfo['us']['idx']]):
            if i==nfo['line']:
                del(content[nfo['us']['idx']][idx])
                return True

def acl_editLine(nfo):
    for idx, i in enumerate(content[nfo['us']['idx']]):
        if i==nfo['line']:
            print('\r\n'+lng.acl_editLine)
            
            print(lng.acl_qattris.format('"read"', lng.tx_ena if i[2] else lng.tx_dis))
            print(lng.acl_changeattr)
            r=kbd() in lng.choiceAttrEna

            print('\r\n'+lng.acl_qattris.format('"write"', lng.tx_ena if i[3] else lng.tx_dis))
            print(lng.acl_changeattr)
            w=kbd() in lng.choiceAttrEna

            print(lng.acl_curline+': '+i[1])
            o=input(lng.acl_lineto+': ')
            o=str(o).strip()

            if len(o)<1:
                print(lng.alc_path_lng_er)
                kbd()
                return
            else:        
                content[nfo['us']['idx']][idx]=[ i[0], o, r, w ]
                return True
    