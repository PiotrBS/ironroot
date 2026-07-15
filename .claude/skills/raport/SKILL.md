---
name: raport
description: >
  Składa dzienny raport IronRoot w PDF z komentarzem analitycznym i dostarcza go
  użytkownikowi. Użyj, gdy użytkownik prosi o „raport", „PDF", „dzisiejszy raport",
  „złóż raport", „komentarz do raportu" w kontekście monitoringu IronRoot (BIP Lasów
  Państwowych / RDOŚ / ministerstwo). Czyta gotowe dane z reports/<data>.json,
  pisze komentarz wg stałej formy, renderuje PDF przez tools/render_pdf.py i wysyła
  plik. NIE commituje do repo (sesja jest read-only) — dostarczenie PDF jest wynikiem.
---

# IronRoot — złożenie dziennego raportu PDF

Twoja rola: dołożyć **komentarz analityczny** do gotowych danych i złożyć z tego
czytelny PDF, po czym **dostarczyć go użytkownikowi**. Danych nie generujesz —
robi to automat (07:15) i zapisuje w `reports/<data>.json`. Wyglądu nie projektujesz
— jest w `templates/raport.html`. Ty dajesz ocenę i uruchamiasz renderer.

## Zasady nadrzędne

- **Komentarz to cała wartość.** Bez niego PDF jest samą tabelą danych.
- **Opieraj ocenę na danych, nie na przeczuciu.** Wartość przyrodniczą sprawy
  bierzesz z pola `bdl` (gatunek, wiek, powierzchnia, ochronność), nie z domysłu.
- **Sesja nie ma prawa zapisu do repo (read-only).** Nie próbuj `git push` ani
  commitować — skończy się 403. Wynikiem jest **dostarczony plik PDF**. Jeśli
  użytkownik chce go w repo, wgra go sam.
- Pełna forma komentarza jest w `INSTRUKCJE-RAPORT.md` (§3) w korzeniu repo — trzymaj się jej.

## Kroki

1. **Ustal datę.** Domyślnie dziś (UTC). Jeśli użytkownik podał inną — użyj jej.
   Znajdź `reports/<data>.json`. Jeśli nie ma:
   - sprawdź najświeższy `reports/*.json`;
   - jeśli w ogóle brak plików `.json` → powiedz użytkownikowi, że automat nie
     wygenerował jeszcze danych strukturalnych (wymaga wdrożonego `report.json`
     w `ironroot.py`) i zaproponuj datę, dla której dane są.

2. **Wczytaj dane.** Przeczytaj `reports/<data>.json`. Zwróć uwagę na:
   `sekcje.obszary_szczegolne`, `sekcje.p1` (zegar tyka), `zdrowie` (kanarki, błędy),
   oraz pole `bdl` przy sprawach.

3. **Napisz komentarz** do `komentarz/<data>.md` wg stałej formy (`INSTRUKCJE-RAPORT.md` §3):
   - `**Jednym zdaniem:**` — wniosek, także gdy brzmi „nic pilnego".
   - `### Wymaga decyzji` — dla spraw ⭐/P1: FAKT · ZNACZENIE (wpleć dane BDL!) ·
     ZEGAR · OPCJE · **NIE WIEM** (obowiązkowe) · DOWÓD (hash z JSON-a).
   - `### Obserwacja` — P2/P3 warte oka, po linijce.
   - `### Wzorzec` — tylko jeśli coś układa się w trend (inaczej pomiń).
   - `### Higiena` — zdrowie systemu; ile spraw wzbogaciło BDL.
   - Pisz markdownem; renderer sam usunie emoji (w druku się nie renderują).
   - Nie jesteś prawnikiem — przy realnym terminie zaznacz, że potwierdza go prawnik.

4. **Zależności renderera** (raz na środowisko):
   ```
   pip install -r tools/requirements.txt
   ```
   Jeśli render padnie na bibliotekach systemowych WeasyPrint (pango/cairo), doinstaluj:
   ```
   apt-get install -y libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 libffi-dev
   ```

5. **Złóż PDF:**
   ```
   python tools/render_pdf.py --data <data>
   ```
   Powstanie `raporty-pdf/<data>.pdf`. Sprawdź, że plik istnieje i ma rozsądny rozmiar.

6. **Dostarcz PDF użytkownikowi** — to jest wynik skilla. Przekaż plik
   `raporty-pdf/<data>.pdf` mechanizmem dostarczania plików (nie wklejaj treści PDF do czatu).

7. **Krótkie podsumowanie w czacie:** jedno zdanie + liczby (ile ⭐/P1, ile spraw z danymi BDL,
   czy kanarki zdrowe). Bez powtarzania całego komentarza — on jest w PDF.

## Czego nie robić

- Nie edytuj `templates/raport.html` ani `tools/render_pdf.py` w ramach składania raportu
  (to zmiana wyglądu — osobny, świadomy krok).
- Nie przepisuj danych z JSON-a ręcznie do PDF — renderer robi to sam.
- Nie commituj i nie pushuj — sesja jest read-only.
- Nie publikuj surowych snapshotów ani niczego z nazwiskami — do PDF idzie tylko to, co w `reports/*.json`.
