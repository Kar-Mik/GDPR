# Konwencja metadanych

Każdy plik źródłowy zaczyna się nagłówkiem YAML. Skill czyta go, zanim użyje treści, i na jego podstawie podaje status na początku odpowiedzi.

```yaml
---
id: tsue-c-13-16                 # unikalny identyfikator (prefiks: rodo-, akt-, pl-, tsue-, nsa-, uodo-, at-dsb-, edpb-, zmiana-)
typ: wyrok                       # artykul | motyw | akt-wykonawczy | ustawa | wyrok | decyzja | wytyczne | projekt
tytul: Rīgas satiksme
sygnatura: C-13/16               # sygnatura, CELEX lub numer decyzji
organ: TSUE                      # TSUE | NSA | WSA | UODO | DSB (AT) | EROD | Komisja | Sejm …
data: 2017-05-04                 # data wydania / przyjęcia
status: prawomocny               # obowiązuje | uchylony | zmieniony | wchodzi-w-zycie | prawomocny | nieprawomocny | wydana (decyzje EROD) | projekt | brak-aktu
obowiazuje_od:                   # dla aktów: data stosowania
podstawa: dyrektywa 95/46        # akt, na którego gruncie wydano (dyrektywa 95/46 | RODO | …)
artykuly_rodo: [6(1)(f)]         # artykuły RODO, których dotyczy (dla wyroków z dyr. 95/46 – odpowiedniki w RODO)
zrodlo: https://curia.europa.eu/juris/liste.jsf?num=C-13/16
jezyk_tekstu: pl
weryfikacja: niezweryfikowane    # zweryfikowane (data) | niezweryfikowane
---
```

## Pola obowiązkowe

`id`, `typ`, `tytul`, `organ`, `data`, `status`, `artykuly_rodo`, `zrodlo`, `weryfikacja`.

## Zasady

- **Wyroki wydane na gruncie dyrektywy 95/46** mają `podstawa: dyrektywa 95/46`, a w `artykuly_rodo` wpisuje się odpowiedniki w RODO. Skill zaznacza w odpowiedzi, że orzeczenie zachowuje aktualność na gruncie RODO.
- **Decyzje zagranicznych organów** są ilustracją wykładni, nie wiążą w Polsce – skill przedstawia je jako przykład praktyki.
- **`status: wchodzi-w-zycie`** – przepis ogłoszony w dzienniku urzędowym, jeszcze nieobowiązujący; data wejścia w życie w `obowiazuje_od`.
- **Przepisy polskie zmienione po tekście jednolitym** mają pola `wersja_tekstu` (skąd pochodzi brzmienie) i `ostatnia_zmiana` (data wejścia w życie ostatniej zmiany), a w treści sekcję „Historia zmian” z poprzednim brzmieniem.
- **`status: brak-aktu`** oznacza, że RODO przewiduje akt (wykonawczy, delegowany), ale go nie wydano. To też informacja dla odpowiedzi.
- Zmiana statusu (uchylenie, nowelizacja) wymaga aktualizacji pliku i rejestru katalogu w tym samym commicie.
