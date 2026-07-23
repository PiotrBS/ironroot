# IronRoot — raporty publiczne

Obywatelski monitoring Biuletynów Informacji Publicznej: nadleśnictw i dyrekcji Lasów Państwowych, regionalnych dyrekcji ochrony środowiska (RDOŚ) oraz Ministerstwa Klimatu i Środowiska — to tam zapadają decyzje zatwierdzające plany urządzenia lasu, od których biegnie termin na skargę.

**Pierwszy raz tutaj?** Zacznij od [`JAK-TO-DZIALA.md`](JAK-TO-DZIALA.md) — opis działania monitoringu bez żargonu technicznego.

Co tu jest:

- `reports/` — raport z każdego dnia (`.md` do czytania, `.json` dla narzędzi),
- `sprawy/` — notatki o sprawach w toku,
- `MANIFEST.jsonl` — rejestr snapshotów stron BIP: hash SHA-256, czas pobrania i data publikacji podana przez urząd. Gdy treść strony zmieni się albo zniknie, hash pozwala wykazać, co było opublikowane i kiedy zostało zarchiwizowane.

Surowych kopii stron nie publikujemy — zawierają dane osobowe (nazwiska urzędników, wnioskodawców). W repozytorium są hashe i metadane; kopie źródłowe udostępniamy uprawnionym podmiotom na uzasadnione żądanie. Tytuły dokumentów przechodzą przed publikacją przez automatyczną anonimizację.

Dane pochodzą z informacji publicznej. Robot odwiedza strony z poszanowaniem robots.txt i przedstawia się User-Agentem z danymi kontaktowymi.
