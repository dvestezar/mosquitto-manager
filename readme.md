# MQTT - Mosquitto manager
Jednoduchý konzolový manažer pro mosquitto broker na Ubuntu. Podpora jazykových souborů.
Testováno na Ubuntu 20+, Python 3+

Používá curses

Edituje soubory **passwd** a **aclfile**, pokud nejsou, tak doporučuji vytvořit. Samozřejmostí je spuštění scriptu jako root.

## Co umím
1. *Správa uživatelů v passwd*
    1. Přidání uživatele
    1. Editace hesla uživatele
    1. Smazání uživatele
1. *Správa ACL pro uživatele*
    1. Přidání ACL bloku pro uživatele
    1. Přidání topic/pattern řádku do bloku uživatele
    1. Smazání topic/pattern řádku uživatele
    1. Editace topic/pattern řádku uživatele
    1. Umí smazat celý ACL blok uživatele
    1. Editace bloku global - pracuje jako s uživatelem '* all'
1. *Restart mosqitto brokeru*
1. *Sputit mosquitto s aktivním výpisem - debug*
1. *Zobrazit základní info z konfigu*

Po jakékoliv editaci doporučuji restart mosquitta pro zavedení nové konfigurace, oba soubory jsou totiž konfigurací a ne live data v databázi.

Editace řádků ACL : zeptá se na atribut read a write a následně se zadá cesta. Jak je uvedeno v dokumentaci, zadání obou read a write nebo jejich nezadání vyjde nastejno

PS: úmyslem nebylo něco poskytnout celému světu s čistými kódy, ale něco funkčního rychle sesmolit. To rychlé nakonec nebylo zas tak rychlé a došlo nakonec k větší změně na verzi 2.+ Komu se ale chce, tak může apku přeložit pro celý svět a třeba i očistit kód ;) To že jsem to sem dal je jen malinké plus pro toho kdo apku případně využije.