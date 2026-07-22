# Changelog — IronRoot core

Format: zmiany od najnowszej wersji. Znacznik w kodzie: `IROOT_VERSION` w `ironroot.py`
(trafia do raportów `.md` / `.json`).

**Schemat numeracji (linia Grok):** baza **0.8 beta** → kolejne poprawki na
**drugim miejscu po przecinku**: `0.81` → `0.82` → `0.83` → …

> Etykiety robocze `0.9` / `0.10` z tej samej sesji były pomyłką względem bazy 0.8.
> Właściwa pierwsza wersja forka Grok to **0.81**.

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
- Teksty: IRONROOT.md (zdublowana numeracja sekcji, nieaktualne „37 kandydatów"),
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

- **Tytuły wracają:** raport `# IronRoot — raport dzienny — <data>` (+ wersja
  w podtytule), BUNDLE `# IronRoot — wyciąg do analizy — <data>`. Commit
  `136c566` podmienił je na sam znacznik wersji („IRoot 0.83 beta — data")
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

Baza: **IRoot 0.8 beta** (upstream `ironroot-core` przed pracą Grok).

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

- `IROOT_VERSION = "IRoot 0.81 beta"`
- `report_worthy()` w `cmd_report`
- `tests/test_rules.py` — 15 testów złotych przypadków

### Dokumentacja

- `README.md`, `CHANGELOG.md`, `AUDYT-0.9.md` (audyt reguł; numer w nazwie pliku = sesja audytu)
- `IRONROOT.md` §8 — terminy od metryki BIP

### Świadomie odłożone

- Bug workflow `PUBLISH_KEY` vs `PUBLIC_DEPLOY_KEY`
- Grupowanie spraw, BDL produkcyjnie, ntfy

### Weryfikacja

```text
python tests/test_rules.py          → 15/15 OK
python ironroot.py classify --rebuild
python ironroot.py report --days 7
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
