# Decyzje Prezesa UODO

- **Źródło:** portal orzeczenia.uodo.gov.pl (filtr „Rozporządzenie o Ochronie Danych Osobowych”), stan na 2026-10-08.
- **Zakres:** wszystkie **585 decyzji** opublikowanych na portalu (2018–2026) – metadane; dla **136 decyzji z karą** także skrót sentencji (sygnalizacyjnie). Pełnych tekstów nie importowano.
- **Rejestr z tabelą wszystkich decyzji:** [`rejestr.md`](rejestr.md). Pliki: `RRRR/<sygnatura>-<rok sprawy>.md`, gdzie `RRRR` to rok wydania decyzji.
- **Dane wejściowe:** `narzedzia/dane/uodo_decyzje.json`, `narzedzia/dane/uodo_sentencje.json`; generator: `narzedzia/import_uodo.py`.

## Co zawiera plik decyzji

| Pole | Skąd | Wiarygodność |
|---|---|---|
| `sygnatura`, `data`, `data_publikacji` | metadane portalu | wysoka |
| `status` (prawomocny / nieprawomocny / uchylony / częściowo prawomocny) | status dokumentu w portalu | wysoka, na dzień pobrania |
| „Losy decyzji” | zdarzenia portalu: `trial` (sprawa w sądzie), `defended` (decyzja obroniona w sądzie – skarga oddalona), `repealed` (uchylenie przez sąd), `validation` (uprawomocnienie) | daty z portalu; opisy kodów – interpretacja własna |
| `rozstrzygniecie`, `obszar` | taksonomia portalu (rodzaj decyzji, obszar) | średnia – zdarzają się błędne przypisania |
| „Opis (portal UODO)” | tytuł/teza nadana przez UODO na portalu | treść UODO; zdarzają się niezgodności z rozstrzygnięciem |
| `kara` | kwoty „w wysokości / w kwocie … zł” wyszukane w sentencji | **ekstrakcja automatyczna** – kilka kwot = kilka kar (np. administrator i podmiot przetwarzający) albo kary za odrębne naruszenia |
| `artykuly_rodo` | numery artykułów, przy których w rozstrzygnięciu pada „rozporządzenia 2016/679” / „RODO” | **ekstrakcja automatyczna** – może być niepełna (np. pomija naruszenie art. 6 wymienione w liście z art. 9); brak przy decyzjach o niewykonaniu nakazu |
| „Sentencja (skrót)” – tylko decyzje z karą | rozstrzygnięcie z portalu: tytuł RODO skrócony do „rozporządzenia 2016/679”, „(słownie: …)” usunięte, ucięte do ok. 700 znaków | tekst UODO, ale **niepełny** – służy do zorientowania się, czego dotyczy kara; nie cytować jako całej sentencji. Przy decyzjach wieloadresatowych początek bywa listą stron, a w jednej (DS.523.4750.2023) fragment zaczyna się w środku wyliczenia |
| `podstawa` | RODO albo ustawa z 1997 r. (sprawy sprzed 25.05.2018) albo ustawa z 14.12.2018 r. (policja, prokuratura, sądy w sprawach karnych) | wykryta z podstawy prawnej w sentencji |

| „Sądy administracyjne” – 84 decyzje | sygnatury WSA/NSA z identyfikatorów zdarzeń portalu | sygnatury – wysoka; skutek – kod portalu (zob. [`rejestr-uodo.md`](../../orzecznictwo/nsa-wsa/rejestr-uodo.md)) |

Przy odpowiedzi skill przytacza decyzję jako: sygnatura, data, rozstrzygnięcie, kara, status – i odsyła do pełnego tekstu na portalu. Kwoty i artykuły przed użyciem w opinii warto potwierdzić w tekście decyzji.

## Znane rozbieżności w danych portalu

- W kilku decyzjach opis mówi o karze, a taksonomia wskazuje upomnienie (np. DKE.561.14.2022, DKN.5131.14.2021) – rozstrzyga sentencja.
- ZSOŚS.421.25.2019 – kara oznaczona w taksonomii, kwoty nie znaleziono automatycznie (sprawa z ustawy z 2018 r. – przestępczość).
- Sygnatura „ZSPR.421.2.2019 ZSPR.405.67.2019” – ponowna decyzja w sprawie Morele.net (2024) po uchyleniu decyzji z 2019 r.

## Następne kroki (do decyzji użytkownika)

1. Pełne teksty wybranych decyzji z tezami do `indeksy/`.
