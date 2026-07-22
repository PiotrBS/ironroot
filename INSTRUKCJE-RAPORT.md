# IronRoot — instrukcja składania raportu PDF (dla modelu)

Ten plik jest **playbookiem dla modelu językowego**. Automat generuje surowe dane
codziennie o 07:15; model raz dziennie zagląda tutaj, pisze komentarz i składa
z tego czytelny PDF. Model nie rysuje raportu — dokłada **wyłącznie komentarz**.
Wygląd jest zamrożony w szablonie, żeby każdy dzień wyglądał tak samo.

---

## 1. Co gdzie leży

| ścieżka | co to | kto tworzy |
|---|---|---|
| `reports/RRRR-MM-DD.json` | **dane** raportu (struktura: sprawy, priorytety, BDL, hashe) | automat (07:15) |
| `reports/RRRR-MM-DD.md` | ten sam raport w markdownie (do czytania) | automat |
| `komentarz/RRRR-MM-DD.md` | **Twój komentarz** — TYLKO treść, wg §3 | **model (Ty)** |
| `templates/raport.html` | szablon wizualny — **nie ruszaj** | stały |
| `tools/render_pdf.py` | renderer: dane + komentarz + szablon → PDF | stały |
| `raporty-pdf/RRRR-MM-DD.pdf` | gotowy PDF | renderer |

Wszystko żyje w repo **publicznym** (`PiotrBS/ironroot`). Surowe snapshoty stron
(z nazwiskami urzędników) są w repo prywatnym i tu nie trafiają.

---

## 2. Procedura (krok po kroku)

1. Ustal datę dzisiejszego raportu `RRRR-MM-DD` (najświeższy plik w `reports/`).
2. Przeczytaj `reports/RRRR-MM-DD.json` — to jest źródło prawdy o sprawach.
   Zwróć uwagę na: `sekcje.obszary_szczegolne`, `sekcje.p1` (zegar tyka),
   `zdrowie` (kanarki, błędy), oraz pole `bdl` przy sprawach (gatunek/wiek/ochronność).
3. Napisz komentarz do `komentarz/RRRR-MM-DD.md` wg **stałej formy** (§3).
4. Zainstaluj zależności (raz na środowisko): `pip install -r tools/requirements.txt`.
5. Złóż PDF:
   ```
   python tools/render_pdf.py --data RRRR-MM-DD
   ```
   (skrót ustawia wszystkie ścieżki; równoważnie `--json ... --komentarz ... --out ...`).
6. Sprawdź, że powstał `raporty-pdf/RRRR-MM-DD.pdf`, i przekaż go użytkownikowi.
7. **Nie commituj i nie pushuj** — sesja modelu jest read-only. Wynikiem pracy
   jest dostarczony PDF (plus `komentarz/*.md` zapisany lokalnie). Jeśli pliki
   mają trafić do repo, wgrywa je użytkownik.

---

## 3. Stała forma komentarza (to jest cała wartość raportu)

Trzymaj się dokładnie tej struktury — bez niej po miesiącu nikt tego nie czyta.
Jest zgodna z `PROTOKOL.md` §4 w repo prywatnym. Pisz **markdownem**; renderer
sam usunie ewentualne emoji (w PDF się nie renderują — znaczenie ma tekst).

> ⚠ **Zawsze zostawiaj pustą linię przed listą punktowaną.** Renderer
> (`markdown` + rozszerzenie `nl2br`) bez pustej linii między poprzednim akapitem
> a `- pierwszym punktem` NIE rozpozna listy — w PDF wyjdzie płaski tekst z
> myślnikami zamiast punktorów. Widać to dokładnie we wzorcu niżej: pusta linia
> jest MIĘDZY `**[Jednostka] — [sprawa]**` a `- **FAKT**`, nie od razu po niej.

```markdown
**Jednym zdaniem:** [wniosek — także gdy brzmi „nic pilnego"]

### Wymaga decyzji
**[Jednostka] — [sprawa]**

- **FAKT** — co dokładnie opublikowano i kiedy (data z metryki BIP)
- **ZNACZENIE** — co to zmienia; TU wpleć dane BDL, jeśli są (gatunek, wiek,
  powierzchnia, ochronność) — to one odróżniają 148-letni dąb od sosny z lat 70.
- **ZEGAR** — ile dni, od czego liczone, co się stanie po terminie
- **OPCJE** — 2–3 możliwe ruchy, z kosztem każdego
- **NIE WIEM** — czego brakuje do oceny (sekcja OBOWIĄZKOWA)
- **DOWÓD** — hash snapshotu (pole `snapshot_sha256` z JSON-a)

### Obserwacja
[jedna linijka na sprawę — P2/P3, które warto mieć na oku]

### Wzorzec
[tylko jeśli coś układa się w trend — inaczej pomiń tę sekcję]

### Higiena
[zdrowie systemu z pola `zdrowie`: kanarki, błędy; ile spraw wzbogaciło BDL]
```

Zasady:
- **„NIE WIEM" jest obowiązkowe.** Komentarz bez niego udaje pewność, której nie ma.
- Nie oceniaj wartości przyrodniczej z powietrza — opieraj się na danych BDL z JSON-a.
  Gdy sprawa nie ma `bdl` (brak adresu oddziałowego), powiedz to wprost.
- Nie jesteś prawnikiem — przy realnym terminie procesowym zaznacz, że potwierdza go prawnik.
- Jeśli sekcja `p1` jest pusta i nic się nie pali — napisz to krótko. Cisza to też informacja.

---

## 4. Czego nie robić

- Nie edytuj `templates/raport.html` ani `tools/render_pdf.py` w ramach dziennej rutyny
  (to zmiana wyglądu — rób ją świadomie i osobno).
- Nie przepisuj danych z JSON-a ręcznie do PDF — renderer robi to sam. Twoja rola to komentarz.
- Nie publikuj surowych snapshotów ani niczego z nazwiskami — do PDF idzie tylko to, co w `reports/*.json`.

---

## 5. Gdyby coś nie zadziałało

- `Brak danych raportu: reports/...json` → automat jeszcze nie wygenerował raportu na tę datę;
  sprawdź najświeższą datę w `reports/`.
- Błąd importu `weasyprint`/`markdown` → `pip install -r tools/requirements.txt`.
- PDF powstał, ale bez komentarza → nie znaleziono `komentarz/<data>.md`; sprawdź nazwę pliku.
