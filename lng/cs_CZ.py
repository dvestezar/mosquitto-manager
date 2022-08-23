app_title="Mosquitto manažer"

mainmenu_pwdfile    ="Soubor s hesly "
mainmenu_aclfile    ="ACL soubor     "
mainmenu_ucnt       ="Počet uživatelů"

cnf_nan = "Soubor konfigu nenalzene v adresáři etc/mosquitto"
err="CHYBA"
err_menuid = "Menu musí být list nebo None"
tx_yes="Ano"
tx_no="Ne"
tx_ena="Zapnut"
tx_dis="Vypnut"
notusd="Nepoužito"
ca_ok="Certifikát CA je OK"
ca_err="Certifikát CA nebyl nalezen"

nfo="INFO"
back="Zpět"
yesother="( a=Ano ostatní=Ne )"
keychoice="Stiskni klávesu/y volby"
pressakey="Stiskni klávesu ..."

choiceY="Aa"
choiceQ="Zz"
choiceNew="N"
choiseUserFile="S"
choiceUsers="Uu"
choiceACL="Aa"
choiceResMsq="Rr"
choiceDbgMsq="Dd"
choiceStatsMsq="Ss"
choiceCfgNfo="Cc"
choiceQuittx="Kk"
choiceDelUs="Ss"
choicepwdchng="Hh"
choiceACLnewbl="Nn"
choiceACLnewtp="Nn"
choiceACLdelall="Vv"

user="uživatel"
users_manage="Správa uživatelů"
user_edit="Editace uživatele"
user_new="Nový uživatel"
user_file="Nenalezen soubor s uživately/hesly, vytvořit ?"
user_create="Vytvoř nového uživatele, napiš '"+choiceQ[0]+"' pro zrušení"
user_enter="Napiš nového uživatele (znaky: a-z 0-9 _ ), min. délka je 4 znaky, max 30"
user_lng_err="Minimální délka uživatelského jména jsou 4 znaky"
user_err_word="Zadáno zakázané slovo"
user_err_char="Uživatelské jméno obsahuje zakázané znaky"
user_exists="Uživatel již existuje, vytvoř jiného"
user_mng_acl="Správa ACL uživatelů"
user_del="Opravdu smazat uživatele"

pwd_err_char="Byly použity zakázané znaky v hesle"
pwd_new="Napiš heslo ( znaky: a-z 0-9 _ & # @ * - ) min. délka 6 znaků, max 30"
pwd_chars='znaky'
pwd_lng="Min. délka hesla je 6 znaků"
pwd_again="Napiš heslo znovu pro ověření"
pwd_neq="Hesla se neshodují"
pwd_us="Změna hesla pro uživatele"

menu_users="Uživatelé"
menu_acl="ACL"
menu_res_msq="Restartuj Mosquitto"
menu_dbg_msq="Restartuj Mosquitto do debugu"
menu_delUs="Smazat uživatele"
menu_chngpwd="Změnit heslo"
menu_cfg_nfo="Konfig info"
menu_msq_stat="Mosquitto servis status"

cfg_nfo="""**** Konfig Info ****\n
port: {port}
listener: {lst}
SSL:
    {ca}
    TLS: {tls}

"""

acl_newblock="Vytvoř nový ACL blok pro uživatele"
acl_forusr="Pro uživatele"
acl_line="Řádek"
acl_newtp="Nový topic/pattern"
acl_delall="Smazat celý blok uživatele"
acl_mnglines="Správa řádků ACL pro uživatele"
acl_qdellall="Opravdu smazat všechny řádky ACL pro uživatele"
acl_moavailusr="V souboru hesel není uživatel, který by neměl již vytvořené ACL. Vytvoř nového uživatele a ten se tu zobrazí."
acl_addblforus="přidat pro uživatele"
acl_newusrbl="Vytvořit nový ACL blok pro uživatele"
acl_newusrblnfo="Zobrazeny jsou jen uživatelé, kteří ještě nemají ACL blok vytvořený"
acl_addattr="Přidat atribut"
acl_atrsel="Vybráno"
acl_line_nfo='''INFO:
    $SYS = systémový root topic, používá se jen na začátku cesty '%SYS/....'
    # = na konci cesty znamená cokoliv:
        tj. pth/# akceptuje pth/x pth/y atd.
    - pokud se celý topic path rovná znaku # , tak jsou povoleny všechny topiky - např pro admina
Pro pattern:
    %c = Device ID
    %u = username
    např: 'temp/%c/store'
'''
acl_typepath="Napiš topic (příklad: mytopic/read )"
acl_path_forb="Cesta obsahuje zakázané znaky , povolené a-z A-Z 0-9 a podtržítko, výjimkou je $SYS a u pattern %"+"c %"+"u"
alc_path_lng_er="CHYBA: min délka je jeden znak"
acl_editLine="Upravit ACL řádku"
acl_qattris="Atribut {} je {}"
acl_path_spaces="Cesta nesmí obsahovat mezery"
acl_path_begin="Začátek nesmí obsahovat lomítko"
acl_path_end="Konec nesmí obsahovat lomítko"
acl_typ="Nenalezen typ topic nebo pattern"
acl_add_type="Zvol typ řádku ACL t=Topic ostatní=Pattern"
acl_addtype_sel="Vybrán typ ACL řádku"
acl_line_exists="Uživatel již má tento ACL řádek"
choiceAclAddType="Tt"

choiceACLlineed="Uu"
choiceACLlinedel="Ss"
choiceAttrEna="Zz"
acl_line_ed="Upravit řádek"
acl_line_del="Smazat řádek"
acl_editusrline="ALC úprava řádku pro uživatele {}, řádek: {}"
acl_qline_del="Opravdu smazat řádek"
acl_changeattr="Změnit na: klávesa '"+choiceAttrEna[0]+"'=zapnuto,  ostatní klávesy=vypnuto"
acl_curline="Aktuální řádka"
acl_lineto="Změnit na"

msqt_restart="Restartuji Mosquitto, počkej dokud se nezobrazí: 'Stiskni klávesu ...'"
msqt_rundebug="""Ukončí mosquitto servis a spustí se lokálně se zobrazením debug informací.\r\n
Mosquito ukončíme standartně CTR+C\r\n
Po stisku CTRL+C se zobrazí řádek : Saving in-memory database ...  !!! Vyčkej na ukončení\r\n
Následně se automaticky opět spustí servis mosquitto.\r\n\r\nStiskni klávesu ..."""
msqt_rundebug_run="Ukončuji servis a spouštím debug, čekej (může trvat i minutu) ...."

quittx = "Konec"

needsmenuitem="Položka menu musí být class menuitem, nebo musí být idx string"
menuitem_idx_char="idx musí být znak od 'A' do 'Z'"
menuitem_idx_num="idx musí být číslo vyjátřené textem 00 až 99"
menuitem_idx_err="nepodporovaný formát nebo obsah proměnné idx"