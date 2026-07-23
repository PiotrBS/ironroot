# Jak działa Leśne Echo — po kolei, bez żargonu

Ten dokument jest dla osoby, która widzi projekt pierwszy raz: dziennikarza,
prawnika, organizacji, współpracownika. Nie wymaga wiedzy technicznej.
Opis techniczny znajdziesz w `LESNE-ECHO.md`.

---

## Problem, który rozwiązuje

Kiedy urząd zatwierdza plan wycinki w lesie, ogłasza to na swojej internetowej
tablicy ogłoszeń (Biuletyn Informacji Publicznej, w skrócie BIP). Od dnia
ogłoszenia biegnie termin na odwołanie — i **nikt nikogo o tym nie zawiadamia**.
Trzeba samemu zajrzeć na tablicę.

Problem w tym, że takich tablic jest **467** (430 nadleśnictw, 17 dyrekcji
regionalnych Lasów Państwowych, Ministerstwo Klimatu i Środowiska, regionalne
dyrekcje ochrony środowiska i kilka innych instytucji), a codziennie pojawia się
na nich około tysiąca nowych dokumentów. Człowiek tego nie przejrzy. Kto nie
sprawdza automatycznie — dowiaduje się po terminie.

Leśne Echo robi jedną rzecz: **codziennie rano obchodzi wszystkie tablice
i mówi, co się zmieniło**.

---

## Sztuczka, na której stoi cały program

To jest najważniejsza rzecz do zrozumienia. Te tablice **nie mają zakładki
„co nowego"**. Nie ma listy ogłoszeń ani powiadomień. Jest zestaw stałych stron
(„Plan urządzenia lasu", „Ochrona przyrody", „Zarządzenia") i gdy coś się dzieje,
urząd **dopisuje do istniejącej strony** kolejny załącznik.

To tak, jakby na korkowej tablicy nikt nie wieszał nowych kartek w widocznym
miejscu, tylko dopinał je do kartek już wiszących. Jedyny sposób, żeby zauważyć
zmianę, to **pamiętać, jak tablica wyglądała wczoraj** i porównać.
I dokładnie to program robi.

---

## Jeden dzień z życia programu — sześć kroków

### 1. Mapa terenu (raz w tygodniu, w poniedziałek)

Zanim cokolwiek zbierze, program musi wiedzieć, gdzie szukać. Odwiedza każdą
z 467 instytucji i sporządza **plan budynku**: jakie strony ma dana jednostka,
które z nich są istotne (plan urządzenia lasu, ochrona przyrody, przetargi,
kontrole).

Robi to raz w tygodniu, bo urzędy zmieniają układ stron — dodają sekcje,
zmieniają nazwy. Mapa sprzed miesiąca prowadziłaby w ślepe zaułki.

Na koniec podaje **pokrycie** — ile jednostek udało się zmapować. Jeśli spadnie
poniżej 90%, program krzyczy, zamiast udawać, że wszystko gra.

### 2. Obchód (codziennie rano)

Program odwiedza około **5,5 tysiąca stron** (w niedzielę robi obchód pełny —
12 tysięcy). Przy każdej stronie:

**Najpierw pyta grzecznie: „zmieniło się coś od ostatniego razu?"** Jeśli nie,
serwer odpowiada „nie" i nie przysyła treści. Dzięki temu program prawie nie
obciąża urzędowych serwerów — po pierwszym przebiegu większość odpowiedzi to
właśnie „bez zmian". Przedstawia się też z imienia i podanym kontaktem oraz
przestrzega reguł, które strona ustala dla robotów. To nie jest grzecznościowy
detal: bot, który młóci serwery, zostanie zablokowany i traci się narzędzie
razem z wiarygodnością.

**Jeśli coś się zmieniło**, program czyta stronę i wyciąga trzy rzeczy:

- **dokumenty** (załączniki — tak publikują Lasy Państwowe),
- **artykuły** (osobne podstrony — tak publikują dyrekcje ochrony środowiska
  i ministerstwo),
- **sam fakt, że strona została zmieniona** — bo to też jest sygnał.

Przy okazji odczytuje **urzędową metrykę strony** — oficjalną datę udostępnienia.
To ważne: terminy liczy się od tej daty, a nie od chwili, w której program
zajrzał na stronę.

Obowiązują tu dwie zasady:

**Zapisuje wszystko, niczego nie odrzuca.** Nawet rzeczy z pozoru nieistotne.
Powód jest praktyczny: każdy filtr na starcie jest niedoskonały. Gdyby program
odrzucał na wejściu, błąd w regule kasowałby ogłoszenie bezpowrotnie i nikt by
się o tym nie dowiedział. Skoro zapisuje wszystko — poprawiona reguła może
przejrzeć całą historię wstecz i odzyskać przeoczone sprawy.

**Pierwsza wizyta na stronie to „fotografia stanu zastanego", nie nowość.** Gdy
program wchodzi gdzieś po raz pierwszy i widzi 300 archiwalnych ogłoszeń, nie
zgłasza ich jako nowin. Inaczej po każdym rozszerzeniu monitoringu dostawałbyś
lawinę fałszywych alarmów i przestałbyś czytać raporty.

### 3. Sortowanie (klasyfikacja)

Zebrane tytuły przechodzą przez **słownik reguł** — kilkadziesiąt wzorców, które
rozpoznają, o czym jest dokument, i nadają mu wagę:

| Waga | Znaczenie | Reakcja |
|---|---|---|
| **P1** | zegar tyka albo skutek nieodwracalny | dni, nie tygodnie |
| **P2** | okno wpływu otwarte — można złożyć uwagi | dzień–dwa |
| **P3** | sygnał wyprzedzający (np. przetarg poprzedza piłę o miesiące) | zapisz, obserwuj |
| **P4** | tło — warto wiedzieć, nie ma co reagować | — |
| **nieznane** | reguły nie rozpoznały | materiał na nowe reguły, nie śmieć |

Jest tu jeden mechanizm wart uwagi: **eskalacja przyrodnicza**. Jeśli dokument
dotyczy rezerwatu, parku narodowego albo starodrzewu, ląduje na szczycie raportu
**niezależnie od tego, jak niewinnie brzmi tytuł**. Bo miejsce znaczy więcej
niż nagłówek.

### 4. Sprawdzenie, co tam naprawdę rośnie

Sam tytuł „cięcia sanitarne w leśnictwie Zarzecze" nie mówi, czy chodzi
o stuletnią buczynę przy rezerwacie, czy o sosnę z lat 70. A to jest różnica
między sprawą wartą walki a rutyną.

Jeśli w dokumencie jest **adres leśny** (nadleśnictwo + numer oddziału), program
pyta państwowy **Bank Danych o Lasach**: jaki gatunek, w jakim wieku, jaka
powierzchnia, czy las ma status ochronny. Te dane trafiają wprost do raportu.

### 5. Raport

Program pisze raport dnia. Najważniejsza decyzja: **jednostką raportu jest
sprawa, nie ogłoszenie**. Pięć publikacji o jednym planie urządzenia lasu to
jedna pozycja z osią czasu — inaczej po miesiącu miałbyś 400 wierszy
i przestałbyś je czytać. Zmęczenie alertami zabija takie systemy szybciej niż
błędy techniczne.

Raport zawsze ma ten sam układ, a **zaczyna się od zdrowia systemu**, nie od
treści. Dopiero potem: obszary szczególne, sprawy z biegnącym terminem, okno
wpływu, sygnały wyprzedzające, kubełek nierozpoznanych i miejsce na komentarz
analityka.

### 6. Publikacja

Gotowy raport trafia do **publicznego repozytorium** — razem z notatkami
o sprawach w toku i rejestrem „odcisków palca" dokumentów. Surowe kopie stron
zostają w części prywatnej.

---

## Trzy zabezpieczenia, które warto znać

**Kanarki.** Program zna kilka źródeł, o których wie, że publikują regularnie.
Jeśli takie źródło milczy — to nie jest cisza w lesie, to **awaria**. Bo
największym ryzykiem tego systemu nie jest błąd, tylko **cisza wyglądająca jak
spokój**: zepsuty odczyt strony daje dokładnie ten sam efekt co brak wydarzeń —
pusty raport. Można przez miesiące żyć w przekonaniu, że nic się nie dzieje.

**Odciski palca dokumentów.** Dla najważniejszych spraw program zapisuje kopię
strony i wylicza jej **cyfrowy odcisk** (SHA-256) — krótki ciąg znaków, który
zmienia się przy każdej, choćby najdrobniejszej zmianie treści. Gdyby dokument
później zniknął albo został po cichu podmieniony, odcisk zapisany w publicznym
rejestrze dowodzi, co i kiedy było opublikowane.

**Dwa repozytoria.** Prywatne trzyma kod i surowe kopie stron — te zawierają
nazwiska urzędników i wnioskodawców. Publiczne dostaje raporty i odciski palca,
bez danych osobowych (tytuły dokumentów przechodzą dodatkowo przez automatyczne
usuwanie nazwisk). Dowód czasowy zostaje, ryzyko prawne znika.

---

## Kto to wszystko uruchamia

Nikt. Program mieszka w chmurze i **odpala się sam raz na dobę** — nie trzeba
trzymać włączonego komputera. Cały obchód trwa około pół godziny (w niedzielę
półtorej), po czym raport pojawia się w repozytorium.

Człowiek ma do tego zajrzeć rano na dziesięć sekund: sprawdzić, czy zdrowie
systemu jest w porządku i czy sekcja „zegar tyka" jest pusta. Jeśli tak —
zamyka i idzie dalej. Jeśli nie — wtedy zaczyna się praca analityka.

---

## Czego Leśne Echo NIE robi

- **Nie ocenia wartości przyrodniczej za człowieka.** Podaje gatunek i wiek
  drzewostanu; osąd, czy sprawa jest warta walki, należy do człowieka.
- **Nie liczy terminów wiążąco.** Terminy w raporcie to budzik, nie kalendarz.
  Termin procesowy potwierdza prawnik.
- **Nie zastępuje legitymacji procesowej.** Skargę na plan urządzenia lasu może
  wnieść organizacja z udokumentowanym stażem. Leśne Echo ten staż buduje —
  ale go nie zastąpi.
- **Nie działa sam z siebie w sprawie.** Jest narzędziem obserwacyjnym.
  Decyzje podejmują ludzie.
