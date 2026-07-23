---
name: raport
description: >
  Składa dzienny raport Leśne Echo w PDF z komentarzem analitycznym i dostarcza go
  użytkownikowi. Użyj, gdy użytkownik prosi o „raport", „PDF", „dzisiejszy raport",
  „złóż raport", „komentarz do raportu", „/raport" w kontekście monitoringu Leśne Echo
  (BIP Lasów Państwowych / RDOŚ / ministerstwo). Czyta gotowe dane z
  reports/RRRR-MM-DD.json, pisze komentarz wg stałej formy, renderuje PDF przez
  tools/render_pdf.py i pokazuje ścieżkę do pliku. NIE commituje do repo
  (sesja jest read-only) — dostarczenie PDF jest wynikiem. Odpowiednik skillu
  Claude (.claude/skills/raport) dla Grok.
---

# Leśne Echo — złożenie dziennego raportu PDF (Grok)

Twoja rola: dołożyć **komentarz analityczny** do gotowych danych i złożyć z tego
czytelny PDF, po czym **dostarczyć go użytkownikowi**. Danych nie generujesz —
robi to automat (collect/classify/report w core, publish) i zapisuje w
`reports/RRRR-MM-DD.json`. Wyglądu nie projektujesz — jest w `templates/raport.html`.
Ty dajesz ocenę i uruchamiasz renderer.

Skill działa w working tree publicznego repo `PiotrBS/ironroot` — tam, gdzie są
`tools/render_pdf.py`, `templates/` i `reports/`. Jeśli sesja stoi w katalogu
silnika (`ironroot-core`), weź świeży JSON z `public/reports/` i renderuj
w katalogu publicznym.

## Zasady nadrzędne

- **Komentarz to cała wartość.** Bez niego PDF jest samą tabelą danych.
- **Opieraj ocenę na danych, nie na przeczuciu.** Wartość przyrodniczą sprawy
  bierzesz z pola `bdl` (gatunek, wiek, powierzchnia, ochronność) oraz z
  `kontekst.obszary` / `zdarzenia[]` (od 0.82), nie z domysłu.
- **Nie jesteś prawnikiem** — przy realnym terminie zaznacz, że potwierdza go prawnik.
- Pełna forma komentarza: `INSTRUKCJE-RAPORT.md` §3 w korzeniu repo publicznego.
- Od **0.82** JSON ma `meta.spraw`, `sekcje.*.zdarzenia[]`, `sprawa_id` — komentarz
  odnosi się do **spraw**, nie do każdego załącznika osobno.
- **Sesja nie ma prawa zapisu do repo (read-only).** Nie próbuj `git commit`
  ani `git push`. Wynikiem jest **dostarczony plik PDF** (plus `komentarz/*.md`
  zapisany lokalnie). Jeśli użytkownik chce mieć pliki w repo, wgra je sam.

## Kroki

1. **Ustal katalog i datę.**
   - Working tree = lokalna kopia **`PiotrBS/ironroot`** (z `tools/render_pdf.py`
     i `templates/raport.html`).
   - Data: domyślnie dziś (UTC) albo data podana przez użytkownika.
   - Plik: `reports/RRRR-MM-DD.json`. Jeśli brak:
     - sprawdź najświeższy dostępny `reports/*.json`;
     - jeśli w ogóle brak `.json` → automat nie opublikował jeszcze warstwy
       strukturalnej; wskaż najbliższy dostępny dzień.

2. **Wczytaj dane.** Przeczytaj `reports/RRRR-MM-DD.json`. Priorytet:
   - `zdrowie` (kanarki, błędy, milczące źródła),
   - `sekcje.obszary_szczegolne`, `sekcje.p1`,
   - `sekcje.p2` / `p3` (skrót do obserwacji),
   - `meta.wersja`, `meta.spraw`, `meta.pozycji`,
   - przy każdej sprawie: `bdl`, `termin`, `snapshot_sha256`, `zdarzenia`, `podmiot`.

3. **Napisz komentarz** do `komentarz/RRRR-MM-DD.md` (utwórz katalog jeśli trzeba)
   **dokładnie** wg formy z `INSTRUKCJE-RAPORT.md` §3:

   ```markdown
   **Jednym zdaniem:** …

   ### Wymaga decyzji
   **[Jednostka] — [sprawa]**

   - **FAKT** — …
   - **ZNACZENIE** — … (BDL jeśli jest)
   - **ZEGAR** — …
   - **OPCJE** — …
   - **NIE WIEM** — …   ← obowiązkowe
   - **DOWÓD** — `hash…`

   ### Obserwacja
   …

   ### Wzorzec
   …   ← tylko gdy trend; inaczej pomiń całą sekcję

   ### Higiena
   …
   ```

   - Zawsze pusta linia przed listą `- **FAKT**` (inaczej PDF spłaszcza listę).
   - Markdown bez polegania na emoji (renderer i tak je czyści).
   - Jeśli P1 puste i kanarki OK — napisz wprost „nic pilnego”.

4. **Zależności renderera** (gdy brak weasyprint/jinja2/markdown):

   ```bash
   pip install -r tools/requirements.txt
   ```

   Na macOS przy błędzie WeasyPrint (Pango/Cairo) doinstaluj systemowe libs
   (Homebrew: `pango` `cairo` `gdk-pixbuf` `libffi`) albo zgłoś błąd użytkownikowi
   z treścią wyjątku — nie udawaj sukcesu.

5. **Złóż PDF:**

   ```bash
   python tools/render_pdf.py --data RRRR-MM-DD
   ```

   Wynik: `raporty-pdf/RRRR-MM-DD.pdf`. Sprawdź, że plik istnieje i ma sensowny rozmiar (> kilku KB).

6. **Dostarcz wynik:**
   - podaj ścieżkę do PDF (względem repo, klikalną jeśli TUI pozwala),
   - w czacie **krótko**: jedno zdanie + liczby (★ / P1 / spraw z BDL / kanarki),
   - **nie** wklejaj całego komentarza ani binariów PDF do czatu.

## Czego nie robić

- Nie commituj i nie pushuj — sesja jest read-only; pliki do repo wgrywa użytkownik.
- Nie edytuj `templates/raport.html` ani `tools/render_pdf.py` w ramach składania raportu.
- Nie przepisuj tabel z JSON-a ręcznie do PDF — renderer robi to sam.
- Nie wrzucaj do PDF treści ze snapshotów HTML (nazwiska) — tylko `reports/*.json`.
- Nie uruchamiaj pełnego `collect` z tego skilla (to job CI / core) — skill składa PDF z gotowych danych.

## Szybka diagnostyka

| Objaw | Co zrobić |
|---|---|
| Brak `reports/*.json` | Pull z `PiotrBS/ironroot` albo przebieg CI/`publish` z core |
| JSON bez `sekcje.p1` | Stary format — i tak czytaj co jest; nie zmyślaj pól |
| WeasyPrint crash | Zależności systemowe; zostaw `komentarz/*.md` i raportuj błąd |
| Puste P1, pełne P3 | Komentarz „nic pilnego” + higiena; nie wymyślaj kryzysu |

## Powiązane pliki

- `INSTRUKCJE-RAPORT.md` — playbook formy komentarza
- `tools/render_pdf.py` — renderer
- `templates/raport.html` — wygląd
- `.claude/skills/raport/SKILL.md` — ten sam proces dla Claude (źródło odpowiednika)
