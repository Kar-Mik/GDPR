# GDPR – baza wiedzy dla skilla RODO

Repozytorium przechowuje źródła prawa ochrony danych osobowych, z których korzysta skill `gdpr-rodo` (instrukcje w [`SKILL.md`](SKILL.md)). Skill odpowiada na pytania prawne na podstawie RODO, prawa polskiego, orzecznictwa TSUE i sądów polskich oraz decyzji organów nadzorczych.

**Etap 1 (bieżący):** odpowiedzi na pytania prawne.
**Etap 2:** soft law (wytyczne EROD/WP29, poradniki UODO), kodeksy postępowania i certyfikacja.
**Etap 3:** zmiany w przygotowaniu (Digital Omnibus) w trybie „stare vs nowe brzmienie”; później moduł sprawdzania dokumentów i checklisty wdrożeniowe.

## Struktura

```
SKILL.md                     instrukcje skilla (format odpowiedzi, kolejność źródeł)
METADANE.md                  konwencja nagłówka (frontmatter) każdego pliku źródłowego
zrodla/
  ue/
    rodo/                    RODO – artykuły i motywy (art-001.md … art-099.md, motywy/)
    akty-wykonawcze/         akty wydane na podstawie RODO + odesłania bez aktu
    inne/                    ePrivacy, dyr. 2016/680, rozp. 2018/1725, rozp. 2025/2518, KPP, TFUE
  pl/
    ustawa-odo-2018/         ustawa o ochronie danych osobowych (art-001.md … art-176.md)
    akty-wykonawcze-uodo/    komunikaty Prezesa UODO (wykaz DPIA), rozporządzenia RM, uchwały o powołaniu Prezesa
    kodeks-pracy/            KP art. 22¹–22³ (dane pracowników, monitoring, kontrola trzeźwości)
    prawo-komunikacji-elektronicznej/  PKE art. 398–400 (marketing, cookies)
    rejestr.md               ustawy sektorowe – rejestr
  orzecznictwo/
    tsue/                    wyroki wiodące (RODO i dyrektywa 95/46)
    nsa-wsa/                 sygnatury wyroków WSA/NSA w sprawach decyzji UODO (rejestr-uodo.md)
  decyzje-organow/
    pl-uodo/                 decyzje Prezesa UODO (RRRR/…, rejestr.md)
    at-dsb/                  austriacka Datenschutzbehörde
    edpb-art65/              wiążące decyzje EROD
    …                        kolejne organy: kod państwa + skrót organu
  wytyczne/                  soft law (etap 2) – źródła i zasady: wytyczne/ZRODLA.md
  kodeksy-certyfikacja/      kodeksy postępowania, certyfikacja (etap 2)
  zmiany/                    projekty zmian (etap 3)
indeksy/
  artykuly.md                artykuł RODO → orzeczenia, decyzje, wytyczne, akty
  klauzule-otwarte.md        klauzule otwarte RODO → przepisy polskie
  art-011.md                 przykład tezy indeksowej (art. 11)
```

## Stan bazy

| Obszar | Stan |
|---|---|
| Tekst RODO | art. 1–99 (wersja skonsolidowana ze sprostowaniami) i motywy 1–173 – zaimportowane i zweryfikowane sumą kontrolną |
| Akty wykonawcze | rejestr gotowy (przegląd EUR-Lex z 2026-10-08) |
| Wyroki TSUE | 22 wyroki wiodące – zweryfikowane z EUR-Lex: ECLI, skład, sentencja (suma SHA-256), kluczowe punkty uzasadnienia |
| Wyroki NSA/WSA | 108 sygnatur w sprawach 84 decyzji UODO ze skutkiem wg portalu UODO – sygnalizacyjnie, bez tekstów (odesłanie do CBOSA) |
| Decyzje organów | UODO – 585 decyzji (metadane: status, kara, rozstrzygnięcie, artykuły RODO, sygnatury wyroków; skróty sentencji 136 decyzji z karą; bez pełnych tekstów); EROD – 12 wiążących decyzji (art. 65, 66 ust. 2) – noty; DSB (AT) – Tesla Sentry; bazy zewnętrzne (CMS, EROD) – tylko przypomnienie |
| Prawo polskie | ustawa o ochronie danych osobowych z 2018 r. – zaimportowana (tekst jednolity 2019 + zmiany z 2026 r.), zweryfikowana sumą kontrolną; komunikat Prezesa UODO – wykaz operacji wymagających DPIA (M.P. 2019 poz. 666); Kodeks pracy art. 22¹–22³ (t.j. 2026) i Prawo komunikacji elektronicznej art. 398–400 – zaimportowane; pozostałe ustawy sektorowe – rejestr |
| Soft law, kodeksy | etap 2 |
| Digital Omnibus | notatka o stanie prac |

## Zasady

1. Każdy plik ma nagłówek zgodny z [`METADANE.md`](METADANE.md) – status, daty, źródło URL, powiązane artykuły.
2. Teksty aktów pochodzą wyłącznie ze źródeł urzędowych (EUR-Lex, ISAP/Dziennik Ustaw/api.sejm.gov.pl, CURIA, orzeczenia.uodo.gov.pl, strony organów).
3. Streszczenia orzeczeń i decyzji są pisane własnymi słowami; pole `weryfikacja` mówi, czy zostały sprawdzone z tekstem źródłowym.
4. Nowy dokument = nowy plik + wpis w rejestrze katalogu + wpis w `indeksy/artykuly.md`.
