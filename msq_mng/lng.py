import os,argparse,importlib,locale

def init(): 
    global lng
    parser = argparse.ArgumentParser(description="Mosquitto Manager",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-l", "--lng", default="sys", help="default is system language, cs_CZ if not found language file",action="store_true")
    args = parser.parse_args()
    a = vars(args)
    v_lng=a['lng']

    if v_lng=='sys':
        v_lng,x=locale.getdefaultlocale()

    if not os.path.exists('lng/'+v_lng+'.py'):
        v_lng='cs_CZ'
        if not os.path.exists('lng/'+v_lng+'.py'):
            raise Exception("Language file not found: "+v_lng)

    return importlib.import_module('lng.'+v_lng)

lng=init()