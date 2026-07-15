# IronRoot — diagnostyka — 2026-07-15 16:18 UTC

## Wersja reguł
```
sha256(rules.yaml) : 663fefa307b4747f
reguł              : 32
wykluczeń          : 14
id reguł           : bilp, ciecia-sanitarne, decyzja-srodowiskowa, derogacje, formy-ochrony, info-publiczna, kontrola, krajowy, lasy-prywatne, obrot-ziemia, plan-postepowan, powierzchnie-referencyjne, przetargi-lesne, pul-aneks, pul-decyzja, pul-dokument, pul-kzp, pul-material, pul-ntg, pul-projekt, rdos-inwestycje, rdos-las, rdos-nierozpoznane, rdos-ochrona-przyrody, strefy, tlo-finanse, tlo-obsluga-przetargow, tlo-srodki-zewnetrzne, wykaz-srodowiskowy, zarzadzenia-jednostki, zmiana-strony-krytycznej, zmiana-strony-pozostale
```

## Kubelek NIEZNANE - wzorce do nowych regul

```

── wg rodzaju ──
  dokument        4059
  artykul         1570

── wg szczebla ──
  nadlesnictwo      4485
  rdos               564
  rdlp               501
  ministerstwo        31
  dglp                27
  gdos                21

── 70 NAJCZĘSTSZYCH WZORCÓW (z nich piszemy reguły) ──

      20×  organizacja ruchu droga
          [Nadleśnictwo Karwin] Organizacja ruchu droga nr 1
      19×  oswiadczenie
          [RDLP Toruniu] oświadczenie zał nr 2
      18×  zaproszenie zlozenia oferty
          [Nadleśnictwo Choczewo] Zaproszenie do złożenia oferty na budowę przydomowej oczyszczalni ściekó
      17×  ogloszenie
          [Nadleśnictwo Brzeg] Ogłoszenie
      17×  zdjecie
          [Nadleśnictwo Orneta] Zdjęcie 1
      16×  plan dzialalnosci bydgoszczy
          [RDOŚ Bydgoszcz] Plan działalności Regionalnego Dyrektora Ochrony Środowiska w Bydgoszczy na 202
      15×  przyroda roznorodnosc biologiczna
          [Generalna Dyrekcja Ochrony Środowiska] Przyroda i różnorodność biologiczna
      15×  inwazyjne gatunki obce
          [RDOŚ Białystok] Inwazyjne gatunki obce
      15×  informacja petycjach
          [RDOŚ Warszawa] Informacja o petycjach w 2025 roku
      15×  warunki dostepu sieci
          [RDLP Białymstoku] Warunki dostępu do sieci telekomunikacyjnych
      15×  informacja uniewaznieniu postepowania
          [Nadleśnictwo Pomorze] Informacja o unieważnieniu postępowania
      15×  srodki zewnetrzne
          [Nadleśnictwo Supraśl] Środki zewnętrzne za 2024 rok
      15×  ogloszenie wynikow przetargu
          [Nadleśnictwo Brzeg] Ogłoszenie wyników przetargu
      15×  srodki zewnetrzne wykorzystane
          [Nadleśnictwo Miastko] Środki zewnętrzne wykorzystane w 2011 roku
      15×  otrzymane srodki publiczne
          [Nadleśnictwo Jamy] Otrzymane_środki_publiczne_w_2020
      14×  osrodki rehabilitacji zwierzat
          [Generalna Dyrekcja Ochrony Środowiska] Ośrodki rehabilitacji zwierząt
      14×  sprawozdanie wykonania planu
          [RDOŚ Bydgoszcz] Sprawozdanie z wykonania planu działalności Regionalnego Dyrektora Ochrony Środ
      14×  ogloszenie pisemnym przetargu
          [RDLP Szczecinku] Ogłoszenie_o__II_pisemnym_przetargu_nieograniczonym_-_X-2026r_-_EA23432026
      14×  kwestionariusz osobowy kandydata
          [RDLP Warszawie] załącznik nr 1 - Kwestionariusz osobowy kandydata na pracownika LP referent / s
      14×  parki krajobrazowe
          [Nadleśnictwo Gołdap] Parki Krajobrazowe
      14×  ogloszenie wyniku przetargu
          [Nadleśnictwo Pomorze] Ogłoszenie o wyniku przetargu
      14×  rejestr nieruchomosci
          [Nadleśnictwo Szczebra] Rejestr nieruchomości
      14×  zg.0172.05.2024
          [Nadleśnictwo Starogard] ZG.0172.05.2024 - załącznik 1
      13×  gatunki niebezpieczne
          [RDOŚ Białystok] Gatunki niebezpieczne
      13×  monitoring dane przyrodnicze
          [RDOŚ Białystok] Monitoring i dane przyrodnicze
      13×  mapa obszaru zakwalifikowanego
          [RDLP Zielonej Górze] Mapa obszaru zakwalifikowanego do zabiegu - Nadleśnictwo Gubin
      13×  informacja udzieleniu zamowienia
          [Nadleśnictwo Prószków] informacja_o_udzieleniu_zamówienia_SA.270.1.1.2023
      13×  korzystanie srodkow zewnetrznych
          [Nadleśnictwo Gorlice] Korzystanie ze środków zewnętrznych w 2025 roku
      12×  edukacja przyrodnicza
          [RDOŚ Białystok] Edukacja przyrodnicza
      12×  wniosek udzielenie informacji
          [RDLP Lublinie] Wniosek o udzielenie informacji
      12×  ogloszenie przetargu nieograniczonym
          [Nadleśnictwo Nurzec] Ogłoszenie III o przetargu nieograniczonym na sprzedaż przyczepy asenizacy
      12×  ogloszenie sprzedazy pustostanu
          [Nadleśnictwo Lipusz] Ogłoszenie o sprzedaży pustostanu
      12×  ogloszenia
          [Nadleśnictwo Rudziniec] Załacznik Nr 1 do ogłoszenia
      12×  zapytanie sondaz rynku
          [Nadleśnictwo Pińczów] Zapytanie sondaż rynku
      11×  ogrody botaniczne zoologiczne
          [Generalna Dyrekcja Ochrony Środowiska] Ogrody botaniczne i zoologiczne
      11×  informacja zbiorcza petycjach
          [RDOŚ Białystok] Informacja zbiorcza o petycjach rozpatrzonych w 2025 roku
      11×  informacja rozpatrzonych petycjach
          [RDOŚ Gorzów Wlkp.] Informacja o rozpatrzonych petycjach w 2025 roku
      11×  sprzedaz tusz zwierzyny
          [Nadleśnictwo Olecko] Sprzedaż tusz zwierzyny łownej pozyskanej w OHZ w sezonie łowieckim 2026/2
      11×  kosztorys ofertowy
          [Nadleśnictwo Choczewo] Załącznik nr 3 - kosztorys ofertowy
      11×  informacja rodo
          [Nadleśnictwo Kobiór] Informacja RODO
      11×  wniosek udostepnienie
          [Nadleśnictwo Wisła] Wniosek o udostępnienie
      11×  regulaminu zfss
          [Nadleśnictwo Kaczory] Załącznik nr 1 do Regulaminu ZFŚS str 1
      11×  otrzymane srodki zewnetrzne
          [Nadleśnictwo Osusznica] Otrzymane środki zewnętrzne w 2021 r.
      10×  zbiorcza informacja rozpatrzonych
          [Ministerstwo Klimatu i Środowiska] Zbiorcza informacja o rozpatrzonych petycjach
      10×  projekt umowy
          [RDLP Warszawie] BSP - Projekt umowy
      10×  informacja wyborze oferty
          [RDLP Warszawie] Informacja o wyborze oferty - Bitdefender
      10×  grunty skarbu panstwa
          [RDLP Zielonej Górze] Grunty Skarbu Państwa w zarządzie LP - RDLP Zielona Góra - 2025
      10×  przetarg nieograniczony sprzedaz
          [Nadleśnictwo Łomża] Przetarg nieograniczony na sprzedaż siatki z demontażu grodzeń (materiał uż
      10×  przetarg pisemny nieograniczony
          [Nadleśnictwo Rajgród] Przetarg pisemny nieograniczony na sprzedaż tusz zwierzyny łownej.
      10×  cennik detaliczny drewna
          [Nadleśnictwo Supraśl] Cennik detaliczny drewna
      10×  zestawienie publicznych zewnetrznych
          [Nadleśnictwo Żednia] Zestawienie publicznych zewnętrznych środków finansowych wykorzystanych w 
      10×  informacja zamiarze transakcji
          [Nadleśnictwo Choczewo] Załącznik_nr_1-_Informacja_o_zamiarze_transakcji_zamiany
      10×  protokol wyboru najkorzystniejszej
          [Nadleśnictwo Lipusz] Protokół z wyboru najkorzystniejszej ofert na sprzedaż sprzętu elektronicz
      10×  zakup energii elektrycznej
          [Nadleśnictwo Gidle] Zakup energii elektrycznej na potrzeby obiektów Nadleśnictwa Gidle
      10×  wykonanie dokumentacji projektowej
          [Nadleśnictwo Kędzierzyn] Wykonanie dokumentacji projektowej remontu dostrzegalni przeciwpożarow
      10×  wstepne ogloszenie informacyjne
          [Nadleśnictwo Dynów] Wstępne ogłoszenie informacyjne 2024 2
      10×  sprzedaz srodkow trwalych
          [Nadleśnictwo Mircze] Sprzedaż środków trwałych
      10×  budowa dojazdu pozarowego
          [Nadleśnictwo Radzyń Podlaski] Budowa dojazdu pożarowego nr 29 o długości 1480 mb w leśnictwie T
       9×  petycja zajecie stanowiska
          [RDOŚ Łódź] Petycja o zajęcie stanowiska w sprawie budowy 13 budynków mieszkalnych wielorodzinny
       9×  objasnienia numeracji (kodow)
          [RDLP Warszawie] Objaśnienia numeracji (kodów) HCV
       9×  druk oferty
          [Nadleśnictwo Nurzec] Druk oferty
       9×  cennik detaliczny drewno
          [Nadleśnictwo Lębork] Cennik detaliczny na drewno i stroisz - Załącznik nr 1 do Decyzji 21
       9×  zamowienia poza ustawa
          [Nadleśnictwo Kobiór] Zamówienia poza ustawą Prawo Zamówień Publicznych
       8×  wyszukiwarka zamowien publicznych
          [RDOŚ Białystok] Wyszukiwarka zamówień publicznych
       8×  kontrola zarzadcza
          [RDOŚ Gdańsk] Kontrola zarządcza
       8×  plan kontroli rdos
          [RDOŚ Gdańsk] Plan kontroli RDOŚ w 2026 roku
       8×  odpowiedz petycje
          [RDOŚ Wrocław] odpowiedź na petycję 1
       8×  ogloszenie naborze staz
          [RDLP Białymstoku] Ogłoszenie o naborze na staż 2026 Ogłoszenie_o_naborze_na_staż
       8×  ogloszenie zamiarze sprzedazy
          [RDLP Szczecinku] OGŁOSZENIE O ZAMIARZE SPRZEDAŻY PUSTOSTANU - LOKAL MIESZKALNY W SZCZECINKU
       8×  zalaczniki
          [RDLP Wrocławiu] Załączniki 1-4

```

## Źródła, które nic nie produkują

```

Korpus: 34818 wierszy z 463 źródeł
Źródeł zmapowanych: 463
🔴 ŹRÓDŁA BEZ ANI JEDNEGO WIERSZA: 0


── najwydajniejsze źródła ──
     760  RDOŚ Kraków
     743  Dyrekcja Generalna LP
     698  RDLP Toruniu
     451  Nadleśnictwo Trzcianka
     378  Nadleśnictwo Jamy
     363  Nadleśnictwo Miastko
     332  RDLP Warszawie
     319  Nadleśnictwo Pińczów

── wierszy wg szczebla ──
  nadlesnictwo     29038
  rdlp              2764
  rdos              2083
  dglp               743
  gdos               139
  ministerstwo        51

```