---
id: pl-rejestr
typ: rejestr
tytul: Prawo polskie – rejestr aktów
organ: Sejm RP
data: 2026-10-08
status: obowiazuje
artykuly_rodo: [6(2), 6(3), 8(1), 9(2), 9(4), 10, 23, 37, 58, 83(7), 84, 85, 86, 87, 88, 89, 90]
zrodlo: https://isap.sejm.gov.pl
weryfikacja: niezweryfikowane
---

# Prawo polskie

Teksty jednolite i aktualne publikatory (Dz.U.) potwierdzać w ISAP / api.sejm.gov.pl (ELI) przy imporcie.

## Ustawy ogólne

| Akt | Relacja do RODO | Stan w repo |
|---|---|---|
| Ustawa z 10.05.2018 r. o ochronie danych osobowych (t.j. Dz.U. 2019 poz. 1781, zm. Dz.U. 2026 poz. 252, 548, 1003) | organ nadzorczy (UODO), postępowanie, kary dla sektora publicznego (art. 83 ust. 7), akredytacja i certyfikacja | **zaimportowana** – [`ustawa-odo-2018/`](ustawa-odo-2018/) (art. 1–176 + art. 59a od 2026-10-28) |
| Ustawa z 21.02.2019 r. o zmianie niektórych ustaw w związku z zapewnieniem stosowania RODO (Dz.U. 2019 poz. 730) | dostosowanie ok. 160 ustaw sektorowych (m.in. KP art. 22¹–22³) | **nie importujemy** – ustawa zmieniająca; jej zmiany są w tekstach jednolitych zmienionych ustaw. ELI: https://api.sejm.gov.pl/eli/acts/DU/2019/730 |
| Ustawa z 14.12.2018 r. o ochronie danych osobowych przetwarzanych w związku z zapobieganiem i zwalczaniem przestępczości (Dz.U. 2019 poz. 125; t.j. Dz.U. 2023 poz. 1206) | implementacja dyrektywy 2016/680 (policja, prokuratura, sądy w sprawach karnych, służby) – RODO się nie stosuje | **sygnalizacyjnie** – tylko odesłanie: https://api.sejm.gov.pl/eli/acts/DU/2023/1206 |
| Konstytucja RP – art. 47, 51 | prawo do prywatności, autonomia informacyjna | do importu |
| Komunikat Prezesa UODO z 17.06.2019 r. – wykaz operacji wymagających DPIA (M.P. 2019 poz. 666) | art. 35 ust. 4 RODO | **zaimportowany** – [`akty-wykonawcze-uodo/`](akty-wykonawcze-uodo/rejestr.md) |

## Przepisy sektorowe (najczęściej przywoływane)

| Akt | Zakres | Klauzula RODO |
|---|---|---|
| Kodeks pracy – art. 22¹–22³ (t.j. Dz.U. 2026 poz. 1245) | dane kandydatów i pracowników, zgoda, dane szczególne i biometria, kontrola trzeźwości, monitoring wizyjny i poczty | art. 88 – **zaimportowany**: [`kodeks-pracy/`](kodeks-pracy/README.md) |
| Prawo komunikacji elektronicznej (Dz.U. 2024 poz. 1221 ze zm.) – art. 398–400 | marketing bezpośredni, cookies, zgoda | art. 95 (ePrivacy) – **zaimportowany**: [`prawo-komunikacji-elektronicznej/`](prawo-komunikacji-elektronicznej/README.md) |
| Ustawa o świadczeniu usług drogą elektroniczną (t.j. Dz.U. 2024 poz. 1513 ze zm.) | dane usługobiorców, definicja informacji handlowej (do art. 398 PKE) | art. 6 ust. 1 lit. c |
| Prawo bankowe – art. 105a | tajemnica bankowa, ocena zdolności kredytowej, profilowanie | art. 6 ust. 1 lit. c, art. 22 ust. 2 lit. b |
| Ustawa o prawach pacjenta i Rzeczniku Praw Pacjenta | dokumentacja medyczna | art. 9 ust. 2 lit. h |
| Ustawa o ochronie sygnalistów | dane sygnalistów i osób, których dotyczy zgłoszenie | art. 6 ust. 1 lit. c, art. 23 |
