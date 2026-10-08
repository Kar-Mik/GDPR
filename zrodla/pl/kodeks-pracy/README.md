# Kodeks pracy – przepisy o danych osobowych (art. 22¹–22³)

- **Źródło:** tekst jednolity – obwieszczenie Marszałka Sejmu z 1.09.2026 r. (Dz.U. 2026 poz. 1245), stan prawny na 27.08.2026 z uwzględnieniem zmian wymienionych w obwieszczeniu. PDF z api.sejm.gov.pl (ELI DU/2026/1245) – HTML dla tego tekstu jednolitego nie jest publikowany.
- **Klauzula RODO:** art. 88 (zatrudnienie); art. 9 ust. 2 lit. b i ust. 4 (biometria, dane szczególne); art. 6 ust. 1 lit. c.
- **Generator:** `narzedzia/import_sektorowe.py`, dane: `narzedzia/dane/kp_art22.json` (zgodność przeniesienia potwierdzona SHA-256).

| Plik | Przepis | Zakres |
|---|---|---|
| [art-22-1.md](art-22-1.md) | art. 22¹ | katalog danych kandydata i pracownika (§ 1 pkt 6 w brzmieniu od 24.12.2025 – bez informacji o wynagrodzeniu) |
| [art-22-1a.md](art-22-1a.md) | art. 22¹ᵃ | zgoda jako podstawa (bez danych z art. 10 RODO), zakaz niekorzystnego traktowania |
| [art-22-1b.md](art-22-1b.md) | art. 22¹ᵇ | dane z art. 9 RODO – tylko z inicjatywy pracownika; biometria do kontroli dostępu |
| [art-22-1c.md](art-22-1c.md) – [art-22-1h.md](art-22-1h.md) | art. 22¹ᶜ–22¹ʰ | kontrola trzeźwości i na obecność środków podobnych do alkoholu (od 21.02.2023), retencja wyników, zastosowanie do niepracowników |
| [art-22-2.md](art-22-2.md) | art. 22² | monitoring wizyjny (cele, pomieszczenia wyłączone, 3 miesiące, informowanie; § 8 zmieniony od 27.01.2026) |
| [art-22-3.md](art-22-3.md) | art. 22³ | monitoring poczty elektronicznej i inne formy monitoringu |

## Korekty warstwy tekstowej PDF

Warstwa tekstowa PDF skleja niektóre wyrazy. Poprawiono jawnie (`KOREKTY` w generatorze):
- „niepóźniej” → „nie później” (art. 22¹ᶜ § 11, art. 22² § 7 i § 9),
- „22¹g” → „22¹ᵍ” (niezamieniony indeks górny w art. 22¹ᶜ § 3 i art. 22¹ʰ).

Indeksy górne zapisano znakami Unicode (np. „22¹ᵃ”, „§ 1¹”). Odnośniki tekstu jednolitego oznaczono „⁽14⁾” i podano pod tekstem artykułu.

## Poza zakresem (sygnalizacyjnie)

Inne przepisy KP dotyczące danych (np. dokumentacja pracownicza, praca zdalna) nie zostały zaimportowane – sprawdzić w tekście jednolitym: https://api.sejm.gov.pl/eli/acts/DU/2026/1245/text.pdf
