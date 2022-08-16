import msq_mng.menus as menus, msq_mng.getch as getch, re

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
                'tx':'  >>> for user: '+x,
                'us':x,
                'idx':lu,
                'fn':acl_user_menu,
                'exists':user_exists(x)
            }
            cnt+=1

    u['N']={
        'tx':'Add user block',
        'us':None,
        'fn':add_user_block,
        'exists':None
    }
    u['Q']={
        'tx':'Back',
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
                    'tx':'  >>> Line: '+('read ' if r else '') + ('write ' if w else '') + l ,
                    'us':user,
                    'line':x,
                    'fn':edit_user_topic
                }
                cnt+=1


        m['N']={
            'tx':'New topic/pattern',
            'us':user,
            'fn':add_user_topic
        }
        m['D']={
            'tx':'Delete all',
            'us':user,
            'fn':del_all_acl
        }
        m['Q']={
            'tx':'Back',
            'us':None,
            'fn':None,
            'exists':None
        }
        menus._menu['acl_edit']=m

        menus.clear()
        c,fn=menus.choice('acl_edit',['Manage user lines ACL for: '+user['us']])
        if fn!=None and fn!=False:
            if fn(user,c)==False:
                acl_save()
                return
        acl_save()

def del_all_acl(user,c=None):
    print('Realy delete all for user "'+user['us']+'"? (y=Yes other=No) : ')
    o=kbd()
    if o=='y' or o=='Y':
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
        print('All users from password file have his block. You have to add new user to password file - Users menu.')
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
                    'tx':'  >>> add for user:  '+x,
                    'us':x,
                    'fn':make_user_block
                }
                cnt+=1
        
            m['Q']={
                'tx':'Back',
                'us':None,
                'fn':None
            }
            menus._menu['acl_new_userblock']=m

            menus.clear()
            c,fn=menus.choice('acl_new_userblock',['New user block','Select available user for add'])
            if fn!=None and fn!=False:
                if fn(m[c]['us'])==True:
                    return

def add_user_topic(user,c=None):
    if type(user) is dict:
        user=user['idx']
    print('\r\n')
    print('Add topic atribute "read" y=Yes other=No')
    r=kbd()
    r=( r=='y' or r=='Y' )
    print('Add topic atribute "write" y=Yes other=No')
    w=kbd()
    w=( w=='y' or w=='Y' )
    print('\r\n$SYS = system root topic, %%c = user ID, %%u = user name, # = at end is anything = pth/# accept pth/x pth/y etc.')
    print('\r\nIf topic path = # = all is granted')
    o=input('\r\nType topic path (example: mytopic/read ): ')
    o=str(o).strip()
    if re.match('[ *+-]',o)!=None:
        print('path include forbidden chars ( space * + - )')
        kbd()
    else:
        if len(o)<1:
            print('ERROR min length of path is 1')
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

    m['E']={
        'tx':'Edit line',
        'fn':acl_editLine
    }
    m['D']={
        'tx':'Delete Line',
        'fn':acl_delLine
    }
    m['Q']={
        'tx':'Back',
        'fn':None
    }
    menus._menu['acl_line_menu']=m

    choice=''
    fn=''
    while fn!=None:
        menus.clear()
        c,fn=menus.choice('acl_line_menu',['Edit user "'+nfo['us']['us']+'" block line : '+nfo['line'][1]])
        if fn!=None and fn!=False:
            if fn(nfo)==True:
                return
    

def acl_delLine(nfo):
    print('\r\nDelete line? (y=Yes other=No)')
    o=kbd()
    if o=='y' or o=='Y':
        for idx, i in enumerate(content[nfo['us']['idx']]):
            if i==nfo['line']:
                del(content[nfo['us']['idx']][idx])
                return True

def acl_editLine(nfo):
    for idx, i in enumerate(content[nfo['us']['idx']]):
        if i==nfo['line']:
            print('\r\nEdit line')
            
            print('Attribute "read" is ', 'enabled' if i[2] else 'disabled')
            print('Change to "e"=enabled other key=disabled')
            r=kbd()=='e'

            print('\r\nAttribute "write" is ', 'enabled' if i[3] else 'disabled')
            print('Change to "e"=enabled other key=disabled')
            w=kbd()=='e'

            print('Curren path is: '+i[1])
            o=input('Change to : ')
            o=str(o).strip()

            if len(o)<1:
                print('Min length of path is 1')
                kbd()
                return
            else:        
                content[nfo['us']['idx']][idx]=[ i[0], o, r, w ]
                return True
    