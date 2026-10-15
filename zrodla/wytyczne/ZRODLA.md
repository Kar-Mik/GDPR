# Soft law – źródła i zasady importu (etap 2)

Ustalone z użytkownikiem 2026-10-15. Do repozytorium trafiają wyłącznie dokumenty ze stron urzędowych. Tryb sygnalizacyjny: nota z kluczowymi tezami (z numerami punktów źródła) i link – bez pełnych tekstów.

## Zasady

1. **Wersja:** tylko wersja ostateczna (EROD: „Final version”, po konsultacjach). Wersja konsultacyjna → `status: projekt`, tylko sygnalizacja; przy tezach z wersji ostatecznej odnotować, czy wcześniejsza wersja istniała.
2. **Język:** wersja polska; gdy jej nie ma – angielska, z adnotacją `jezyk_tekstu: en` w nagłówku.
3. **Aktualność:** przy każdym dokumencie sprawdzić, czy nie został zastąpiony (np. WP259 → wytyczne 05/2020, WP250 → wytyczne 9/2022). Dokument zastąpiony → `status: uchylony` + wskazanie następcy.
4. **Tezy** – własnymi słowami, z numerem punktu (pkt / akapit) źródła; `weryfikacja` mówi, czy tezę porównano z tekstem.
5. **Nie są źródłem:** komentarze, blogi kancelarii, bazy komercyjne (w tym CMS) – co najwyżej do wyszukania dokumentu.

## Źródła (w kolejności przydatności)

| # | Kategoria | Źródło | Moc / rola w odpowiedzi | Katalog |
|---|---|---|---|---|
| 1 | Wytyczne, rekomendacje, oświadczenia EROD | strona dokumentu na edpb.europa.eu (wersja „Final version”, PDF PL) – np. https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-072020-concepts-controller-and-processor-gdpr_pl | wykładnia EROD (art. 70 RODO), niewiążąca, przyjmowana przez organy i sądy | `wytyczne/edpb/` |
| 2 | Wytyczne WP29 przyjęte przez EROD | lista EROD „Endorsed WP29 Guidelines” – https://www.edpb.europa.eu/endorsed-wp29-guidelines_pl (rozstrzyga, które obowiązują); teksty – archiwum WP29 na ec.europa.eu | jak wyżej | `wytyczne/wp29/` |
| 3 | Raporty EROD – Coordinated Enforcement Framework | edpb.europa.eu | praktyka kontrolna organów UE – materiał do checklist (etap 3) | `wytyczne/edpb-cef/` |
| 4 | Opinie EROD z art. 64 | edpb.europa.eu – w szczególności opinia o polskim wykazie DPIA, kodeksy, BCR | spójność; uzupełnia `zrodla/pl/akty-wykonawcze-uodo/` | `wytyczne/edpb/` |
| 5 | Opinie rzeczników generalnych TSUE | curia.europa.eu | kierunek w sprawach zawisłych | `zrodla/orzecznictwo/tsue/` (pole `typ: opinia-rg`) |
| 6 | UODO – poradniki i wskazówki | uodo.gov.pl – „Poradniki i wskazówki (od 2025 r.)”, „Poradniki i wskazówki (materiały z lat 2018–2020)” | stanowisko polskiego organu; starsze – zaznaczyć datę (sprzed wielu wytycznych EROD) | `wytyczne/uodo/` |
| 7 | UODO – opinie do projektów aktów (art. 57 ust. 1 lit. c RODO), wystąpienia (art. 52 u.o.d.o.), sprawozdania roczne | uodo.gov.pl | sygnały problemów w prawie sektorowym | `wytyczne/uodo/` |
| 8 | Zatwierdzone kodeksy postępowania i certyfikacja | rejestry UODO i EROD | wiążące dla członków kodeksu | `kodeksy-certyfikacja/` |
| 9 | EIOD (EDPS) – opinie legislacyjne (art. 42 rozp. 2018/1725), wytyczne dla instytucji UE, TechDispatch | edps.europa.eu | **punktowo**: cel nowych aktów UE; wytyczne EUDPR pomocniczo tam, gdzie przepisy odpowiadają RODO | `wytyczne/edps/` |
| 10 | Wytyczne organów zagranicznych (CNIL, AP, ICO) | strony organów | tylko ilustracja; ICO – UK GDPR, ostrożnie | `wytyczne/zagraniczne/` |

Pomijamy: sprawozdania roczne EROD i EIOD.

## Dostęp techniczny

Środowisko pracy nie łączy się bezpośrednio z edpb.europa.eu, ec.europa.eu, uodo.gov.pl, edps.europa.eu (stan 2026-10-15). Pobieranie: przez przeglądarkę na komputerze użytkownika albo po dodaniu domen do dozwolonych w ustawieniach.
