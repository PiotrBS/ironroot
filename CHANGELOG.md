# Changelog — IronRoot core

Format: zmiany od najnowszej wersji. Znacznik w kodzie: `IROOT_VERSION` w `ironroot.py`
(trafia do raportów `.md` / `.json`).

**Schemat numeracji (linia Grok):** baza **0.8 beta** → kolejne poprawki na
**drugim miejscu po przecinku**: `0.81` → `0.82` → …

> Etykiety robocze `0.9` / `0.10` z tej samej sesji były pomyłką względem bazy 0.8.
> Właściwa pierwsza wersja forka Grok to **0.81**.

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
