# Changelog — Leśne Echo core

Format: zmiany od najnowszej wersji. Znacznik w kodzie: `LESNE_ECHO_VERSION` w `lesne_echo.py`
(trafia do raportów `.md` / `.json`).

**Schemat numeracji (linia Grok):** baza **0.8 beta** → kolejne poprawki na
**drugim miejscu po przecinku**: `0.81` → `0.82` → `0.83` → …

> Etykiety robocze `0.9` / `0.10` z tej samej sesji były pomyłką względem bazy 0.8.
> Właściwa pierwsza wersja forka Grok to **0.81**.

---

## [0.90 beta] — 2026-07-24

**Chronione wydzielenia — i korekta zawyżonego sygnału.** Backfill pokazał, że
Programy Ochrony Przyrody niosą listy wydzieleń **wyłączonych z użytkowania
rębnego** — sygnał odwrotny do wykazu cięć: nie „tu się tnie", tylko „tego się
NIE tnie".

### Uczciwość ponad efekt

Wcześniej zachwyciłem się „2524 chronionymi wydzieleniami" z Nadl. Torzym.
Zwiad na treści dokumentu pokazał, że **to było zawyżone**:

- fraza „Wyłączenie z użytkowania rębnego" poprzedza **krótkie listy per
  siedlisko** (~15 wydzieleń każda), nie jedną listę na 2524;
- te 2524 to **wszystkie wzmianki** o wydzieleniach w całym dokumencie (granice
  Natura 2000, tabele gatunków, opisy) — nie wydzielenia chronione;
- realnie wyłączonych z użytkowania jest kilkadziesiąt, rozbitych na listy.

Gdyby raport pokazał „2524 chronione", zamieniłby skromny sygnał w wielki
fałszywy. Zamiast tego:

- **rozdzielenie inwentarza od wzmianek:** dokument z opisem drzewostanu
  (gatunek+wiek) pokazuje twarde dane; dokument z samymi adresami mówi wprost
  „wymienia N wydz. (wzmianki)", zamiast udawać, że to inwentarz;
- **sygnał wyłączeń z przykładami, nie z liczbą udającą kompletność:**
  „🛡️ wyłącza wydz. z użytkowania rębnego (m.in. 05-74-d, 09-67-i…)". Płaski
  tekst nie da się wyparsować co do adresu (listy bywają oddzielone prozą,
  rozbite łamaniem wiersza, przerwane nagłówkiem strony) — więc podajemy sygnał,
  nie fałszywą precyzję.

### Kod

- `PROTEKCJA_FRAZA` + `_adresy_chronione()` — adresy z list po frazie ochronnej,
  z naprawą adresów rozbitych łamaniem wiersza („03-\\n223-g" → „03-223-g");
- `streszcz_wydzielenia`: pola `n_chronione` i `chronione` (adresy — do przyszłej
  kontroli krzyżowej: chronione wydzielenie w dokumencie o cięciach = alarm);
- raport: rozdzielenie inwentarza od wzmianek w kartach i tabelach.

### Uwaga wdrożeniowa

Wpisy w cache sprzed 0.90 nie mają pola `chronione` — sygnał ochrony pojawi się
przy nich dopiero po ponownym odczycie (codzienny scan odświeża ~40 dokumentów).
Nowe odczyty mają je od razu.

### Testy

- `tests/test_rules.py` — **45 testów** (42 + wyłączenia z użytkowania, naprawa
  łamania wiersza, nietykanie prozy referencyjnej).

---

## [0.89 beta] — 2026-07-23

**Hartowanie E3a po pierwszym backfillu.** Uruchomienie na 400 dokumentach
pokazało trzy rzeczy, których zwiad na 22 plikach nie mógł pokazać.

### Fałszywe wydzielenia — najpoważniejsze

„Opis taksacyjny — obręb Polkowice cz 2" (**469 stron**) oddawał **7 wydzieleń**.
Prawdziwy wykaz daje tysiące — siedem to szum: numery z nagłówków, zakresy
oddziałów z opisu leśnictw, przypisy. Raport pokazywałby zmyślone dane jako fakt.

Przyczyna (ustalona po zajrzeniu do dokumentu): opis taksacyjny to **formularz
wielokolumnowy**. Numer oddziału, pododdział, lista gatunków i kolumna wieków
stoją w osobnych blokach, powiązanych UKŁADEM STRONY, a nie kolejnością tekstu:

```
239                     ← oddział
n                       ← pododdział
… opis siedliska …
3 OL / 1 BRZ / 1 DB     ← udział + gatunek
16 16 21 29 80 140      ← wieki, osobna kolumna
```

Płaski odczyt tekstu tego nie odtworzy — to zadanie dla ekstrakcji ze
współrzędnymi, czyli **E3b**. Do tego czasu system ma o tym mówić, a nie zgadywać.

- `uklad_wiarygodny()` — ufamy, gdy choć jeden wiersz ma komplet gatunek+wiek
  (układ rozpoznany na pewno) albo gdy samych adresów jest ≥20 (tyle
  przypadkowych dopasowań się nie zdarza). Inaczej zapisujemy **zero**
  i znacznik `uklad_rozpoznany: false`;
- `scan-attachments` liczy takie dokumenty osobno i mówi wprost, czego brakuje:
  „6 dużych dokumentów ma tekst, ale układ wielokolumnowy — potrzebna
  ekstrakcja ze współrzędnymi (E3b)".

### Cisza w logu

PDF-y z BIP bywają technicznie niechlujne (błędne wskaźniki obiektów,
zdublowane wpisy `/Info`). pypdf meldował o tym **setkami linii na dokument**,
topiąc właściwy komunikat przebiegu. To nie są nasze błędy i nic z nimi nie
zrobimy — log pypdf wyciszony do poziomu ERROR.

### Skala z produkcji (400 dokumentów)

| | |
|---|---|
| z wydzieleniami | 8 |
| bez adresu (poprawnie — decyzje, pisma) | 257 |
| skany bez tekstu (mapy) | 133 |
| błędy | 2 |

Najbogatszy plik: **„Wykaz projektowanych cięć rębnych" — 5317 wydzieleń**.
Potwierdza ustalenie ze zwiadu: wartość jest skoncentrowana w wykazach cięć,
nie rozłożona po wszystkich załącznikach.

### Testy

- `tests/test_rules.py` — **42 testy** (41 + próg wiarygodności układu).

---

## [0.88 beta] — 2026-07-23

**E3a — wydzielenia z treści załączników.** Największa dziura projektu zaczyna
się domykać: system wie już nie tylko CO i KIEDY, ale też GDZIE i CO TAM ROŚNIE.

### Zwiad przed budową (i korekta własnego pomiaru)

Zanim powstała linijka kodu, zmierzyłem na 22 żywych PDF-ach z BIP, czy plan
E3 ma sens. Pierwszy pomiar dał „0% dokumentów z oddziałami" — i **był błędny**:
szukałem wzorca „oddz. 128", a BIP zapisuje adresy jako `02-128-k`, do tego
czytałem 25 pierwszych stron, gdy tabele zaczynają się na 214 z 426. Wynik był
na tyle nieprawdopodobny (dokument „Wykaz projektowanych cięć rębnych" MUSI
zawierać wydzielenia), że zajrzałem do środka plików zamiast zaufać liczbie.

Ustalenia, na których stoi ta wersja:

- adres wydzielenia ma **dwa szablony**: `02-128-k` (obręb-oddział-pododdział,
  np. Nadl. Lubin) i `148-b` (obręb tylko w nagłówku sekcji, np. Bystrzyca Kł.);
- **66% PDF-ów ma warstwę tekstową**; reszta to skany, ale prawie wyłącznie
  MAPY — OCR nic by tu nie dał, bo mapę czyta się GIS-em. Odłożenie OCR było
  trafne, skany nie są wąskim gardłem;
- wartość jest **skrajnie skoncentrowana**: decyzja zatwierdzająca to 1–2 strony
  aktu prawnego bez wydzieleń, a cały ładunek siedzi w elaboracie / wykazie
  cięć / opisie taksacyjnym. Jeden taki plik dał **1228 wydzieleń, 1222
  z gatunkiem i wiekiem**, w tym **6 wydzieleń ≥100 lat zaplanowanych do cięcia**
  (115-letnie dęby);
- wiersz tabeli niesie gatunek i wiek WPROST, więc dla tych spraw **BDL nie jest
  już potrzebny** — mamy lepsze źródło: oficjalny zapis planu, a nie rejestr ogólny.

### Co weszło

- `pdf_text()` — tekst z PDF-a, odporny na skany i uszkodzone pliki;
- `extract_wydzielenia()` — oba szablony adresu + pełny wiersz taksacyjny
  (adres, rodzaj cięcia, siedlisko, gatunek, wiek);
- `warto_skanowac()` — celownik po tytule i klasie. Celowo BEZ gołego
  „zestawienie": łapało „Zestawienie otrzymanych dotacji" (307 szt.);
- `scan-attachments [--limit N] [--minuty M]` — czytanie z budżetem czasu,
  zapis po każdym dokumencie (przerwanie nie gubi godzin pracy), kolejność
  **nowości → archiwum, P1 → P3**;
- w `collect`: załączniki P1 czytane z bajtów, które i tak pobieramy dla hasha
  — **zero dodatkowych zapytań** do BIP;
- w raporcie: wiersz „🌲 Drzewostan (z dokumentu)" w kartach, kolumna
  w tabelach P2/P3, licznik w sekcji zdrowia, pełne dane w JSON.

### Streszczenie zamiast kopii tabeli (poprawka w trakcie)

Pierwsza wersja zapisywała pełną listę wydzieleń — przy 1228 wierszach to
110 kB na dokument, czyli **kilkadziesiąt MB w repo** dla całego archiwum.
Dokładnie to, czego projekt unika. Cache trzyma więc SYGNAŁ, nie duplikat:
liczbę wydzieleń, histogram gatunków, zakres wieku, **pełne dane drzewostanów
≥100 lat** i numery oddziałów do BDL. Zmierzone: **13,9 kB na 17 dokumentów**
(~1,6 MB dla całego archiwum). Sama tabela zostaje w dokumencie, którego hash
mamy w manifeście.

### pypdf zamiast pdfplumber

Zmierzone na tym samym PUL-u (17 MB, 432 str.): **28 s wobec 64 s**, przy
identycznym wyniku (1228 wydzieleń). pypdf jest lżejszy, czysto pythonowy
i też na MIT. Nadal świadomie NIE pymupdf — najszybszy, ale AGPL.

### Naprawione przy okazji

- **Wyjście w UTF-8.** `print` z emoji wywalał `UnicodeEncodeError` na polskiej
  konsoli Windows (cp1250) — ten sam rodzaj błędu co odczyty w 0.86, tylko po
  stronie zapisu. Teraz `stdout`/`stderr` są przestawiane na UTF-8 na starcie.

### Workflow

- codzienny przebieg: `scan-attachments --limit 40 --minuty 12`, krok
  **nieblokujący** (jak `bdl-enrich`) — nie ma prawa zatrzymać raportu;
- nowy tryb ręczny **`scan`** — backfill archiwum z budżetem 60 min.

### Testy

- `tests/test_rules.py` — **41 testów** (35 + oba szablony adresu, starodrzew,
  odporność na śmieci, celownik tytułów, odporność `pdf_text`).

---

## [0.87 beta] — 2026-07-23

**Zmiana nazwy programu: IronRoot → Leśne Echo.**

Do wersji 0.86 włącznie program nazywał się **IronRoot** (znacznik `IRoot 0.8x
beta`). Wpisy historyczne poniżej opisują te same wydania — zmieniła się nazwa,
nie historia.

### Co się zmieniło

| | było | jest |
|---|---|---|
| Silnik | `ironroot.py` | `lesne_echo.py` |
| Ramy projektu | `IRONROOT.md` | `LESNE-ECHO.md` |
| Workflow | `.github/workflows/ironroot.yml` | `lesne-echo.yml` |
| Znacznik wersji | `IROOT_VERSION` = „IRoot 0.86 beta" | `LESNE_ECHO_VERSION` = „Leśne Echo 0.87 beta" |
| Tytuł raportu | „IronRoot — raport dzienny" | „Leśne Echo — raport dzienny" |
| Podpis bota (UA) | `IronRoot/1.0` | `LesneEcho/1.0` |
| Autor commitów automatu | `ironroot` | `lesne-echo` |

Pliki przeniesione przez `git mv`, więc **historia zmian się zachowała**
(`git log --follow lesne_echo.py` pokazuje pełne dzieje silnika).

### Czego świadomie NIE ruszono

- **Nazwy repozytoriów** (`PiotrBS/ironroot-core`, `PiotrBS/ironroot`) — zmiana
  po stronie GitHuba wymaga ręcznej akcji i unieważniłaby dotychczasowe linki.
  Sekret `PUBLIC_REPO` działa bez zmian.
- **Skrzynka kontaktowa bota** (`ironroot_contact@pm.me`) — działa i jest
  podana urzędom w User-Agencie. Bot bez odbieranego kontaktu traci
  wiarygodność, więc zmieniamy nazwę, a adres zostaje.
- **Opublikowane raporty** (`reports/`, `MANIFEST.jsonl`, snapshoty) — to
  datowane dokumenty. Przepisywanie ich wstecz byłoby fałszowaniem zapisu.
  Nowa nazwa pojawia się w raportach od najbliższego przebiegu.

### Weryfikacja

```text
python tests/test_rules.py   → 35/35 (import z lesne_echo działa)
py_compile lesne_echo.py, build_sources.py, tools/render_pdf.py → OK
YAML: 5 configów + workflow → OK
wywołań `lesne_echo.py` w workflow: 30
```

---

## [0.86 beta] — 2026-07-23

Naprawa defektów wykrytych podczas weryfikacji pierwszego przebiegu na 0.85.
Wszystkie trzy potwierdzone na żywych danych (przebieg 2026-07-23, 225 spraw).

### BDL — poszlaka przestaje udawać fakt

`bdl_info` szukał adresu leśnego w trzech miejscach, ale wynik podawał zawsze
tak samo — jakby należał do tej sprawy. Skutek w produkcji: *„Załącznik nr 2
Mapa przedmiotu dzierżawy"* (klasa `grunty`, **własny adres pusty**) dostawał
25 wydzieleń w wieku 0–167 lat, zaciągniętych z sąsiedniego dokumentu na tej
samej stronie BIP — i raport pokazywał je jako drzewostan tej sprawy.

- wynik niesie teraz pole `dopasowanie`: `wlasny` · `zdarzenie` · `strona`,
- `strona` = **poszlaka**: karta dostaje jawne ostrzeżenie („adres pochodzi
  z innego dokumentu na tej samej stronie, nie z tej sprawy"), tabela — znacznik `?`,
- sekcja 0 liczy trafienia pewne i poszlaki **osobno**. Uczciwy obraz na dziś:
  `z drzewostanem 0 · poszlaka ze strony 2` (wcześniej raportowane jako 2 trafienia).

### Dowód, który istniał, ale był niewidoczny

Snapshot jest fotografią CAŁEJ strony BIP, a hash trafiał tylko do wiersza,
który go wywołał. Gdy na jednej stronie RDLP leżały decyzje PUL dla kilku
nadleśnictw, sprawa obok pokazywała „dowód: —", choć dowód był w manifeście
(realny przypadek: PUL Manowo).

- `collect`: hash dostaje **każdy** wiersz z tej strony,
- `report`: sprawa bez własnego hasha wskazuje snapshot z tej samej strony
  **i tego samego dnia** (para strona+dzień — hash sprzed tygodnia nie dowodzi
  dokumentu, który doszedł wczoraj). Działa **wstecz**, na zebranym korpusie.
- Efekt: spraw z dowodem **39 → 64** (+64%) na tym samym zestawie danych.

### Kodowanie — narzędzia nie dało się uruchomić na Windowsie

Sześć odczytów JSON (`bdl_cache`, `http_cache`, `pages_seen`, `sources_state`)
szło bez `encoding="utf-8"`, więc Python brał kodowanie systemowe. Na Linuksie
w CI działało; na polskim Windowsie `report` wywalał się na pierwszym „ż"
w nazwie nadleśnictwa (`UnicodeDecodeError`, cp1250). Błąd był niewidoczny,
dopóki nikt nie uruchomił silnika lokalnie.

### Weryfikacja

```text
python tests/test_rules.py            → 35/35
python lesne_echo.py classify --rebuild → 58 368 wierszy
python lesne_echo.py report --days 7    → 225 spraw (identycznie jak automat 0.85)
```

Liczby spraw, priorytetów i klas bez zmian względem 0.85 — naprawy dotyczą
wyłącznie rzetelności prezentacji i przypisania dowodu.

---

## [0.85 beta] — 2026-07-22

Druga część audytu: naprawy wymagające żywej sieci (Python zainstalowany
lokalnie, testy uruchamiane realnie) + zabezpieczenia RODO i porządki w tekstach.

### Pokrycie źródeł — odzyskane 3 nadleśnictwa i RDOŚ Białystok

- **Adapter bip2** (stary BIP LP, `bip2.lasy.gov.pl`): Jagiełek i Żmigród nie
  mają profilu na gov.pl (przekierowania na stronę główną portalu / własną
  domenę) i publikują wyłącznie na bip2. Silnik rozumie teraz oba schematy:
  `unit_prefix()` (gov.pl `/web/<slug>` i bip2 `/pl/bip/dg/<rdlp>/<nadl>`),
  pliki `px_…` jako załączniki (z czyszczeniem doklejanych metadanych
  ".PDF … (4.0MB)"), sekcje z podkreślnikami w CORE_SECTIONS
  (`plan_urzadzania_lasu` — przez "a"!). Zweryfikowane na żywo: Jagiełek
  21 sekcji / 11 kluczowych, Żmigród 22 / 11.
- **Fallback dziurawych profili gov.pl:** strona główna Janowa Lubelskiego
  zwraca 404 albo miękko przekierowuje na gov.pl, choć podstrony żyją.
  `discover_sections` próbuje wtedy `kontakt` / `co-robimy` / `mapa-strony` —
  menu jednostki wisi na każdej żywej podstronie. Zweryfikowane: 28 sekcji / 12.
- **Status 998 — „przekierowanie poza BIP":** sekcja „Archiwum (stary BIP)"
  RDOŚ Białystok to drogowskaz na martwą domenę `bip.bialystok.rdos.gov.pl`.
  Fetcher rozpoznaje redirect na obcy host przy padającym połączeniu; collect
  pomija bez alarmu — koniec z wiecznym „błędów: 1" w sekcji zdrowia.

### RODO

- `anonimizuj()`: imię i nazwisko po wyzwalaczu („na wniosek…", „Pana/Pani…")
  znika ze WSZYSTKIEGO, co publikowane (raporty, BUNDLE, diagnostyka, manifest);
  korpus i snapshoty w repo prywatnym zachowują oryginał. Garda na nazwy
  instytucji („na wniosek Nadleśnictwa Milicz" zostaje). Uwaga językowa:
  rdzeń to `wnios\w+`, bo mianownik „wniosek" ma ruchome „e".
- Skan obecnych publikacji (manifest, raporty, diagnostyka): zero trafień —
  anonimizacja działa na przyszłość, nie było czego czyścić wstecz.
- README repo publicznego przepisane: uczciwie o tym, co hash dowodzi,
  o danych osobowych i o anonimizacji tytułów.

### Dowody i manifest

- **Hash załącznika P1:** przy snapshocie strony silnik pobiera też sam PLIK
  dokumentu, hashuje go i wpisuje do manifestu (`rodzaj: zalacznik`). Plik
  zostaje w repo prywatnym tylko gdy mały (≤3 MB przed kompresją); większe mają
  sam hash — dowód bez puchnięcia repo.
- Manifest publiczny: deduplikacja identycznych wierszy. Zbadany duplikat
  `483dc1c1…` (dwa adresy RDOŚ Rzeszów, jeden hash) okazał się prawdziwy —
  dwa URL-e serwują tę samą treść; oba wpisy zostają.

### Wydajność i higiena

- `collect` strumieniowo (`as_completed` zamiast `gather`) — pełny obchód nie
  trzyma już w pamięci wszystkich 12 tys. odpowiedzi HTML naraz.
- `tools/requirements.txt` (renderer PDF): wersje przypięte `==` —
  deterministyczny renderer nie może zależeć od pływających bibliotek.
- Skille ujednolicone: polityka **read-only** (bez commit/push z sesji modelu)
  obowiązuje w `.claude`, `.grok` i `INSTRUKCJE-RAPORT.md` §2.7.
- Teksty: LESNE-ECHO.md (zdublowana numeracja sekcji, nieaktualne „37 kandydatów"),
  PROTOKOL.md (numery sekcji raportu po 0.82), nagłówek diagnostyki bez
  połamanych znaków, README obu repo.
- `sprawy/`: założone pierwsze karty — 3× PUL (Pieńsk, Lubin, Milicz;
  orientacyjny koniec okna 2026-08-13), Wąwóz Homole, Babia Góra PZO,
  Wodospad Wilczki.

### Testy

- `tests/test_rules.py` — **35 testów** (33 + anonimizacja osób / nietykanie
  instytucji), wszystkie uruchomione lokalnie: 35/35. Adapter bip2 i fallback
  gov.pl zweryfikowane dodatkowo na żywych stronach.

---

## [0.84 beta] — 2026-07-22

Audyt linii Grok (Claude): odkręcenie niezamierzonych zmian + naprawa błędów
grupowania i baseline. Szczegóły audytu w rozmowie; poniżej co weszło do kodu.

### Odkręcone (niezamierzone zmiany linii Grok)

- **Tytuły wracają:** raport `# Leśne Echo — raport dzienny — <data>` (+ wersja
  w podtytule), BUNDLE `# Leśne Echo — wyciąg do analizy — <data>`. Commit
  `136c566` podmienił je na sam znacznik wersji („Leśne Echo 0.83 beta — data")
  przy okazji commitu danych.
- **Przywrócone komentarze** wycięte w 0.82/0.83: rationale WAGA 3 (sąsiedztwo
  nazwy i typu — fałszywy pozytyw „starodrzew BUKOWY"/„Puszcza BUKOWA"),
  WAGA 2 (wielkie litery), nagłówek `analiza()`, opis sekcji „W skrócie".
- **`bdl_info`:** usunięty martwy blok (`pass`) i komentarz o niezaimplementowanym
  kroku 4; funkcja nie zwraca już wyniku przypadkowego ostatniego lookupu —
  przy braku trafienia wraca PIERWSZY niepusty wynik (powód braku z adresu
  własnego sprawy).
- Wiersz diagnostyki BDL wchodzi DO listy sekcji „0. Zdrowie" (insert przed
  pustą linią), a nie luzem za sekcją.

### Naprawione błędy (silnik)

- **Artykuły ≠ jedna sprawa:** grupowanie po `(page_url, rule_id)` obejmuje
  już tylko załączniki/edycje strony. Artykuły z jednej strony-rocznika RDOŚ
  zlewały się w jedną sprawę (raport 2026-07-21: 6 RÓŻNYCH inwestycji jako
  jedna karta P1 z jedną osią czasu).
- **Znak sprawy jako klucz:** publikacje z tym samym znakiem („znak:
  OO.4220.249.2026.TP") łączą się w jedną sprawę między stronami i miesiącami.
- **Starodrzew bez zlewania:** generyczny znacznik „★ starodrzew…" nie jest już
  kluczem sprawy — sprawy z różnych nadleśnictw przestały się sklejać.
- **Baseline po błędzie:** strona, której pierwsza wizyta skończyła się błędem
  HTTP, nie była już oznaczana jako „widziana"; po udanej wizycie jej stan
  zastany szedłby do raportu jako lawina „nowości". Teraz do `pages_seen`
  trafiają tylko strony faktycznie przeczytane (200 z treścią / 304).
- **Ekstrakcja oddziału:** „w oddziale 12 na terenie" dawało pododdział „12na"
  (śmieciowe klucze w cache BDL). Litery po spacji tylko, gdy nie są polskim
  słówkiem; przyklejone („14a") bez zmian.
- `podmiot_nadlesnictwa`: obcięcie samotnego „z" na końcu nazwy dwuczłonowej
  („Stary Sącz z [dnia…]") — klucze `pul|` przestają się rozjeżdżać.
- `publish`: MANIFEST.jsonl sortowany po `fetched_utc` + kończący `\n`
  (stabilna chronologia pliku dowodowego); kopiuje też CHANGELOG/VERSION/AUDYT
  do `public/` (rozjazd: publiczne VERSION mówiło 0.82 przy raportach 0.83).
- robots.txt pobierany z podpisanym User-Agentem (jak strony treści).
- Fetcher: pusty `str(ReadTimeout)` dawał w health `error:""` — teraz
  zapisujemy przynajmniej nazwę wyjątku (diagnoza rdos-bialystok).

### Reguły (wymaga `classify --rebuild`!)

- **Znak OO./00.4220 przestaje być P1.** Wzorce znaku przeniesione z reguły
  `decyzja-srodowiskowa` (P1, snapshot, termin 14 dni) do `rdos-inwestycje`
  (P4 tło) — zgodnie z projektem sekcji I („OO. = inwestycje → tło").
  Wprowadzone w 0.82 wbrew komentarzom pliku; skutek widoczny w raportach:
  karta „Zegar tyka" z 6 fermami/drogami. Test odwrócony.
- Wykluczenie „organizacja ruchu": `stal` → `\bstal` („ustalono"/„została"
  łapały się na substring).
- Wykluczenie postoju z gardą `\A(?!.*zakaz wstepu)` — „Zakaz wstępu do lasu
  i postoju pojazdów" to sygnał o zamknięciu lasu, nie szum parkingowy.
- `przetargi-lesne`: `\boddzial(?!ywan)\w* \d+` — „prognoza ODDZIAŁYWANIA
  2026" wpadała jako przetarg.
- `obszary.yaml` fallback oddziału z tą samą gardą przyimka co silnik.

### Workflow / narzędzia

- **Uporządkowany tor publikacji.** Env eksportował `PUBLISH_KEY`, a skrypty
  czytały `PUBLIC_DEPLOY_KEY` — tor SSH nigdy nie działał. Stan faktyczny
  (ustalony w 0.85): deploy key nigdy nie był skonfigurowany, publikacja od
  początku chodzi na `PUBLIC_TOKEN`, który jest dziś BEZTERMINOWY — token to
  droga podstawowa, deploy key zostaje jako opcja (sekret `PUBLIC_DEPLOY_KEY`
  z kluczem SSH, gdyby kiedyś był potrzebny). Martwe odwołanie do
  `PUBLISH_KEY` usunięte z env.
- Testy reguł uruchamiane w CI przed zbieraniem (rekomendacja AUDYT-0.9).
- `LATEST.json` dołączony do dziennego commita (był zamrożony na 2026-07-19).
- Inputy `workflow_dispatch` przekazywane przez env (bez interpolacji w shellu).
- `build_sources.py`: strażnik przed nadpisaniem zweryfikowanych źródeł
  (ponowne uruchomienie cofałoby naprawione adresy RDLP); `--force` wymusza.
- `requirements.txt`: usunięty nieużywany `feedparser`.
- `bdl.yaml`: usunięty nieczytany klucz `wiek_rebnosci` (sekcja deklaruje
  „klucze używane w kodzie").

### Testy

- `tests/test_rules.py` — **33 testy** (29 z 0.83 + artykuły osobno, znak
  sprawy, starodrzew, przyimek po numerze oddziału; odwrócony
  `test_rdos_oo_inwestycja`).

### Nadal poza zakresem

- E5 alert (ntfy/mail), E3 treść załączników; rdos-bialystok (martwa sekcja
  archiwum — wymaga diagnozy na żywym gov.pl); trzy nadleśnictwa z HTTP 200
  i zerem sekcji (janow-lubelski, jagielek, zmigrod — inny szablon strony?).

### BDL — brak danych w raporcie

**Diagnoza:** WFS BDL działa (cache: 100% trafień gdy jest oddział). Problemem
było **brak numeru oddziału w tytułach BIP** w oknie raportu + lookup tylko po
tytule wiersza (bez strony, bez dual-key).

**Naprawy:**
- `extract_adres_lesny()` — warianty „oddz.14a”, „oddział 14 bx”, „wydzielenie…”, wiele oddziałów
- `bdl_lookup` — klucz pełny i numeryczny; lista `oddzialy`
- `bdl-enrich` faza A: dociąga oddziały z treści/strony BIP (priorytet: najnowsze URL)
- report: BDL ze **sprawy → zdarzenia → inne wiersze tej samej strony** (także baseline)
- sekcja 0: `🌳 BDL: z drzewostanem X · … · brak oddziału w BIP Y`
- karta: przy adresie bez trafienia — jawny powód zamiast milczenia

**Limit:** większość nowości BIP **nie podaje oddziału** w tytule ani na stronie
listy; pełne tabele są w PDF („Wydzielenia objęte zadaniem”) — to etap E3 (treść
załączników), nie zamknięty w 0.83.

---

## [0.82 beta] — 2026-07-19

Plan: `PLAN-JAKOSC-0.82.md` — epiki **E1** (sprawy) + **E2** (słownik nieznanych).

### E1 — jednostką raportu jest sprawa

- `group_sprawy()` / `sprawa_group_key()` / `podmiot_nadlesnictwa()`
- Klucze: obszar chroniony (waga≥2) · `pul|<nadleśnictwo>` · `page_url+rule_id` · wiersz
- `cmd_report`: sekcje 1–5 po sprawach; karta P1 z **osią czasu** gdy `n_zdarzen>1`
- JSON: `sprawa_id`, `zdarzenia[]`, meta `spraw` + `pozycji`
- Przykład: RDLP Wrocław 3 PUL + załącznik Milicz → **3 sprawy** (Milicz z 2 publikacjami)

### E2 — domknięcie kubełka „nieznane”

- `formy-ochrony`: `zespol\w* przyrodniczo…` (fleksja „Zespoły”)
- `przetargi-lesne`: wydzielenia+pozyskanie/masa; unieważnienie/info przetargu
- `decyzja-srodowiskowa`: OO. / znak 00.4220…
- `obrot-ziemia`: rejestr nieruchomości (nie tylko „leśnych”)
- exclusions: oświadczenie wykluczenia, meble/dach/kruszywo, cennik sadzonek, PR „jeden las…”
- **Fix Classifier:** exclusions na **samym tytule** (wzorce `^…$` nie widzą URL)

### Testy

- `tests/test_rules.py` — **27 testów** (0.81 + E1 + E2)

### Weryfikacja (okno 7 dni, po rebuild)

| Metryka | 0.81 | 0.82 |
|---|---|---|
| Publikacje → raport | ~136 wierszy | **126 → 76 spraw** |
| P1 (zegar) | 4–7 wierszy | **4 sprawy** (3 PUL + 1 OOŚ grupa) |
| Nieznane w raporcie | 16 | **0** |
| Testy | 15 | **27/27** |

### Nadal poza zakresem

- E4 BDL diagnostyka, E5 alert, E3 PDF, publish key

---

## [0.81 beta] — 2026-07-19

Fork katalogów z sufiksem **`-grok`** (bez `v2` w nazwie):

| Katalog | Rola |
|---|---|
| `ironroot-core-grok/` | silnik + korpus (to repo) |
| `ironroot-grok/` | kopia publicznych raportów |

Baza: **Leśne Echo 0.8 beta** (upstream `ironroot-core` przed pracą Grok).

### Naprawione błędy (P0)

| ID | Problem | Skutek w 0.8 | Naprawa |
|---|---|---|---|
| **A** | Wzorzec `ostoj\w*` matchował **postoju** (parking leśny) | Fałszywe **P1** „Strefy ochrony gatunków” na wykazach MPP | `osto(?:ja\|i\|je)`; wykluczenia MPP / `postoj*` / dróg |
| **B** | `[Ll]eśnictw…` matchowało podciąg w **Nadleśnictwa** | Raport: `→ leśn. Pieńsk` przy decyzji PUL | `(?<![Nn]ad)` + formy *leśnictwie/a/o/u* |
| **C** | Sekcje P2/P3 zalane „Zmiana w BIP: …” | ~48% nowości w oknie 7 dni = szum | `report_worthy()` — `kind=zmiana` tylko przy klasie merytorycznej lub P≤2 |

### Reguły i konfiguracja

- `config/rules.yaml` — ostoja, exclusions postoju/MPP/dróg
- `config/obszary.yaml` — `adres_lesny.lesnictwo` z lookbehind

### Kod

- `LESNE_ECHO_VERSION = "Leśne Echo 0.81 beta"`
- `report_worthy()` w `cmd_report`
- `tests/test_rules.py` — 15 testów złotych przypadków

### Dokumentacja

- `README.md`, `CHANGELOG.md`, `AUDYT-0.9.md` (audyt reguł; numer w nazwie pliku = sesja audytu)
- `LESNE-ECHO.md` §8 — terminy od metryki BIP

### Świadomie odłożone

- Bug workflow `PUBLISH_KEY` vs `PUBLIC_DEPLOY_KEY`
- Grupowanie spraw, BDL produkcyjnie, ntfy

### Weryfikacja

```text
python tests/test_rules.py          → 15/15 OK
python lesne_echo.py classify --rebuild
python lesne_echo.py report --days 7
```

| Metryka | 0.8 | 0.81 |
|---|---|---|
| „postoju” jako P1 | tak | **0** |
| Fałszywe `leśn.` z Nadleśnictwa | tak | **brak** |
| Okno 7d → raport | ~235 | **~136** (−szum `zmiana`) |
| Decyzje PUL P1 | OK | bez regresji |

---

## [0.8 beta] — upstream

Linia produkcyjna przed forkiem Grok: collect/classify/report, dual-repo,
baseline per strona, kanarki, snapshoty P1/P2, szkic BDL, workflow GitHub Actions.
Katalog: `ironroot-core/` → GitHub `PiotrBS/ironroot-core`.
