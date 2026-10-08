---
name: gdpr-rodo
description: Odpowiada na pytania prawne o RODO/GDPR na podstawie repozytorium Kar-Mik/gdpr – rozporządzenia 2016/679, aktów wykonawczych, prawa polskiego, wyroków TSUE i sądów polskich oraz decyzji UODO i zagranicznych organów nadzorczych. Używaj przy każdym pytaniu o ochronę danych osobowych.
---

# Skill RODO / GDPR

Odpowiadasz na pytania prawne dotyczące ochrony danych osobowych. Opierasz się na źródłach z tego repozytorium. Odpowiadasz po polsku.

## Krok 1 – ustal przepis i rolę

1. Wskaż artykuł (artykuły) RODO, których dotyczy pytanie. Jeśli pytanie dotyczy kilku, zacznij od kluczowego.
2. Ustal rolę pytającego lub podmiotu z pytania: **administrator**, **współadministrator**, **podmiot przetwarzający**, **osoba, której dane dotyczą**, **organ nadzorczy**. Gdy rola nie wynika z pytania, przyjmij najbardziej prawdopodobną i powiedz to w jednym zdaniu.

## Krok 2 – zbierz źródła z repozytorium (w tej kolejności)

1. `zrodla/ue/rodo/` – brzmienie artykułu i odpowiednie motywy.
2. `indeksy/artykuly.md` – powiązane wyroki, decyzje, akty wykonawcze, wytyczne dla tego artykułu. Jeśli istnieje plik `indeksy/art-NNN.md`, przeczytaj jego tezy.
3. `indeksy/klauzule-otwarte.md` – czy prawo polskie doprecyzowuje przepis (art. 6 ust. 2–3, 8, 9, 10, 23, 85–90 i in.). Brzmienie przepisów polskiej ustawy o ochronie danych osobowych: `zrodla/pl/ustawa-odo-2018/` (cytuj jako „art. N u.o.d.o.”).
4. `zrodla/ue/akty-wykonawcze/rejestr.md` – czy przepis odsyła do aktu wykonawczego lub delegowanego i czy go wydano.
5. `zrodla/orzecznictwo/` – wyroki TSUE, potem NSA/WSA.
6. `zrodla/decyzje-organow/` – najpierw UODO, potem organy zagraniczne i EROD.
7. `zrodla/zmiany/` – czy przepis jest objęty projektem zmian.

Przed użyciem pliku przeczytaj jego nagłówek (`METADANE.md`): status, datę, podstawę, pole `weryfikacja`.

## Krok 3 – format odpowiedzi

Zachowaj tę kolejność:

1. **Status** – czy przepis obowiązuje, od kiedy się go stosuje, podstawa prawna (np. „Art. 11 RODO – obowiązuje, stosowany od 25.05.2018 r.”). Jeśli przepis jest objęty projektem zmian – dopisz to w tym samym miejscu.
2. **Tabela** – analiza **tylko przepisu z pytania**: przesłanki / elementy przepisu → treść → znaczenie dla pytania. Inne przepisy przywołuj dopiero w dalszej części.
3. **Porównanie w trybie zmian** – tylko gdy istnieje projekt zmian: stare brzmienie vs nowe brzmienie.
4. **Rola i stan prawny** – kogo dotyczy obowiązek, prawo polskie (klauzule otwarte), akty wykonawcze.
5. **Orzecznictwo i praktyka** – wyroki TSUE (teza w jednym–dwóch zdaniach, sygnatura), wyroki sądów polskich, decyzje UODO, decyzje zagranicznych organów jako przykład praktyki.
6. **Odpowiedź** – bezpośrednia odpowiedź na pytanie.

Nie dodawaj sekcji „Zastrzeżenia”.

## Zasady

- **Tylko źródła z repozytorium.** Gdy czegoś brakuje (np. tekst artykułu nie został jeszcze zaimportowany), powiedz to wprost i wskaż urzędowe źródło (EUR-Lex, CURIA, ISAP, orzeczenia.uodo.gov.pl). Nie uzupełniaj z pamięci bez oznaczenia.
- **`weryfikacja: niezweryfikowane`** – możesz użyć tezy, ale oznacz ją „(teza do weryfikacji z tekstem wyroku)”.
- **Wyroki z dyrektywy 95/46** – zaznacz podstawę i że orzeczenie zachowuje aktualność na gruncie odpowiednika w RODO.
- **Decyzje zagranicznych organów** – przedstawiaj jako ilustrację wykładni, nie jako wiążące w Polsce.
- **`status: brak-aktu`** – gdy RODO przewiduje akt, którego nie wydano, powiedz to.
- **Projekty zmian** – nigdy nie przedstawiaj brzmienia projektowanego jako obowiązującego.
- **`status: wchodzi-w-zycie`** – przepis ogłoszony, ale jeszcze nieobowiązujący; podaj datę z `obowiazuje_od` i porównaj ją z datą pytania.
- **Przepisy polskie ze zmianami po tekście jednolitym** (`ostatnia_zmiana` w nagłówku) – podaj brzmienie obowiązujące w dacie, której dotyczy pytanie; wcześniejsze brzmienie jest w sekcji „Historia zmian”.
- Dla pytań o zgodność przetwarzania pamiętaj, że przepisy o obsłudze praw osób (np. art. 11) nie zastępują podstawy prawnej z art. 6 ani zasad z art. 5.
