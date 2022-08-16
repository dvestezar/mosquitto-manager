# Mosquitto manager
Jednoduchý konzolový manažer pro mosquitto broker na Ubuntu. 
Testováno na Ubuntu 20+, Python 3+

Edituje soubory **passwd** a **aclfile**, pokud nejsou, tak doporučuji vytvořit. Samozřejmostí je spuštění scriptu jako root.

## Co umím
1. *Správa uživatelů v passwd*
    1. Přidání uživatele
    1. Editace hesla uživatele
    1. Smazání uživatele
1. *Správa ACL pro uživatele*
    1. Přidání ACL bloku pro uživatele
    1. Přidání topic řádku do bloku uživatele
    1. Smazání topic řádku uživatele
    1. Editace topic řádku uživatele
    1. Umí smazat celý blok uživatele
    1. Editace bloku : pattern/s
    1. Editace bloku : global
1. *Restart mosqitto brokeru*

Po jakékoliv editaci doporučuji restart mosquitta pro zavedení nové konfigurace :D oba soubory jsou totiž konfigurací a ne live data v databázi.

Editace řádků ACL : zeptá se na atribut read a write a následně se zadá cesta/topic. Jak je uvedeno v dokumentaci, pokud zadáme read a write, tak je to to samé jako by jsme je neuvedli. 

PS: úmyslem nebylo něco poskytnout celému světu, nebo čisté kódy ale něco funkčního rychle sesmolit. Komu se chce tak může přeložit pro celý svět a očistit kód ;) To že jsem to sem dal je jen malinké plus pro toho kdo využije.