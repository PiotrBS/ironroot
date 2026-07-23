# Audyt Leśne Echo 0.9 — po naprawach

> **Uwaga numeracji:** ten audyt powstał w sesji oznaczanej roboczo „0.9”. Właściwa wersja forka Grok względem bazy 0.8 to **Leśne Echo 0.81 beta** (katalogi: `ironroot-core-grok`, `ironroot-grok`).


**Data:** 2026-07-19  
**Wersja (historyczna etykieta sesji):** 0.9 → właściwa **Leśne Echo 0.81 beta**  
**Katalog:** `ironroot-core-grok` (kopia `ironroot-core` + poprawki)  
**Zakres:** ponowna weryfikacja po P0 z audytu 0.8; **bez** zmian publish key.

---

## 1. Podsumowanie

| Obszar | 0.8 | 0.9 | Status |
|---|---|---|---|
| Fałszywe P1 na „miejscach postoju” | **TAK** | **NIE** (0 w korpusie) | ✅ naprawione |
| Fałszywe „leśn. X” z Nadleśnictwa | **TAK** | **NIE** | ✅ naprawione |
| Szum „Zmiana w BIP” w raporcie | ~48% nowości | −99 pozycji / 7 dni | ✅ złagodzone |
| Decyzje PUL w P1 | OK | OK | ✅ bez regresji |
| Ostoja / strefy gatunków | (psute przez postoju) | 20 tytułów → `strefy` | ✅ działa |
| Testy reguł | 0 | **15/15** | ✅ dodane |
| PUBLISH_KEY / deploy SSH | bug nazw | **bez zmian** | ⏸ odłożone |
| Grupowanie spraw | brak | brak | ⏳ backlog |
| BDL produkcyjnie | szkic | szkic | ⏳ backlog |

**Werdykt (obecnie 0.81):** krytyczne fałszywe alarmy P0 usunięte; raport czytelniejszy; pipeline lokalny (`classify --rebuild` → `report` → `publish`) działa. Nadaje się do dalszej pracy operacyjnej; publish key i grupowanie spraw — osobne etapy.

---

## 2. Testy automatyczne

```bash
cd ironroot-core-grok
python tests/test_rules.py
# → 15/15 passed
```

Pokrycie:

- postoju / MPP → wykluczone, nie `strefy`
- ostoja / strefa ochronna → nadal P1 ochrona
- Nadleśnictwa Pieńsk → brak `adres.lesnictwo`
- leśnictwo Zarzecze → `adres.lesnictwo == Zarzecze`
- PUL decyzja / informacja o zatwierdzeniu → `pul-decyzja` P1
- `report_worthy` dla dokumentów, szumu, zmian stron

---

## 3. Rebuild korpusu i raport

```text
Sklasyfikowano 34837 (przebudowa całej historii)
  … szum 1459 (w tym MPP/postoju) …
reports/… P1: 4  · obszary szczególne: 3
okno 7d: 235 pozycji → 136 report_worthy (−99)
postoju jako P1: 0
```

### Sekcja 🔴 Zegar tyka (0.9) — wyłącznie realne PUL

- RDLP Wrocław: Pieńsk, Lubin, Milicz (informacje o zatwierdzeniu)
- Nadleśnictwo Milicz: Zatwierdzenie PUL  
- **Brak** „Wykaz miejsc postoju” / „Mapa miejsc postoju”

### Lokalizacja

- `RDLP Wrocławiu` **bez** fałszywego `→ leśn. Pieńsk`

### Obszary szczególne

- Rezerwat Wąwóz Homole, Natura 2000 Babia Góra, Rezerwat Wodospad Wilczki — bez regresji

---

## 4. Architektura (bez zmian koncepcyjnych)

Nadal aktualne i **poprawne** decyzje z 0.8:

1. Zapisuj wszystko → filtruj osobno (`classify --rebuild`)
2. Zdrowie systemu w raporcie (kanarki)
3. Dual-repo (snapshoty prywatnie, hashe publicznie)
4. Model BIP: załączniki LP + artykuły RDOŚ + metryka

### Nowa warstwa w 0.9

```
classified.jsonl  ──report_worthy()──►  sekcje 1–5 raportu
       │
       └── (pełny) ──────────────────►  korpus / diagnostyka / unknowns
```

---

## 5. Wąskie gardła — status

| Wąskie gardło | Status 0.9 | Komentarz |
|---|---|---|
| Collect ~23 min (delay×strony/4) | bez zmian | nie ruszane w tej iteracji |
| `health_summary` skanuje cały korpus | bez zmian | backlog wydajności |
| Monolit 2.2k LOC | bez zmian | OK na 0.9 |
| Workflow SSH secret name | **świadomie nietknięte** | `PUBLISH_KEY` vs `PUBLIC_DEPLOY_KEY` |
| Brak grupowania spraw | bez zmian | nadal 4 karty na PUL Wrocław |
| BDL | bez zmian | kolumna często „—” |
| Alert push (ntfy) | brak | protokół opisuje, kod nie |

---

## 6. Rekomendacje następne (priorytet)

1. **Publish key** — ujednolicić nazwę sekretu w workflow (osobna sesja).
2. **Grupowanie spraw** w `cmd_report` (jedna karta PUL + oś czasu załączników).
3. **pytest w CI** — krok `python tests/test_rules.py` przed collect.
4. Nie sleepować na HTTP 304 / opóźnić tylko body 200.
5. Indeks `last_seen` zamiast pełnego `corpus_read()` w health.

---

## 7. Pliki zmienione w 0.9

```
lesne_echo.py                 IROOT_VERSION, report_worthy, filtr w cmd_report
config/rules.yaml           ostoj, exclusions MPP/dróg
config/obszary.yaml         lesnictwo lookbehind + formy fleksyjne
tests/test_rules.py         NOWE — 15 testów
README.md                   opis 0.9
CHANGELOG.md                NOWE
AUDYT-0.9.md                TEN PLIK
LESNE-ECHO.md                 korekta opisu terminów
reports/, LATEST.md, public/  przebudowane classify+report
```

**Nie ruszane:** `.github/workflows/ironroot.yml` (publish key), BDL, collect/fetcher.
