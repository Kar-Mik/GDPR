#!/usr/bin/env python3
"""Generuje pliki wyroków TSUE (zrodla/orzecznictwo/tsue/) z danych zweryfikowanych w EUR-Lex.

Sentencje: plik JSON {CELEX: tekst} – tekst 1:1 z EUR-Lex (twarde spacje zamienione
na zwykłe), suma SHA-256 zapisywana w nagłówku.

Użycie: python3 narzedzia/buduj_tsue.py sentencje.json
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "zrodla", "orzecznictwo", "tsue")
WERYF = "zweryfikowane (2026-10-08, sentencja i punkty uzasadnienia z tekstem PL w EUR-Lex)"

# celex, sygnatura, nazwa, data, izba, ecli, podstawa, artykuly_rodo, teza, punkty uzasadnienia
CASES = [
    ("62012CJ0131", "C-131/12", "Google Spain i Google", "2014-05-13", "wielka izba", "ECLI:EU:C:2014:317",
     "dyrektywa 95/46", ["3(1)", "4(2)", "4(7)", "17", "21"],
     "Działalność wyszukiwarki (indeksowanie, przechowywanie, udostępnianie wyników) jest przetwarzaniem danych, a jej operator – administratorem. Prawo UE ma zastosowanie, gdy operator ma w państwie członkowskim oddział sprzedający reklamy skierowane do jego mieszkańców. Osoba może żądać usunięcia z wyników wyszukiwania po jej imieniu i nazwisku linków do stron z informacjami o niej, nawet gdy publikacja na tych stronach jest zgodna z prawem; jej prawa z art. 7 i 8 Karty co do zasady przeważają nad interesem operatora i odbiorców, chyba że uzasadnia to np. rola tej osoby w życiu publicznym (prawo do bycia zapomnianym).",
     []),
    ("62013CJ0212", "C-212/13", "Ryneš", "2014-12-11", "czwarta izba", "ECLI:EU:C:2014:2428",
     "dyrektywa 95/46", ["2(2)(c)", "6(1)(f)"],
     "Kamera zainstalowana przez osobę fizyczną na domu rodzinnym, nagrywająca w sposób ciągły obraz osób i obejmująca również przestrzeń publiczną, nie jest przetwarzaniem w ramach czynności o czysto osobistym lub domowym charakterze. Właściciel jest administratorem; jego uzasadniony interes (ochrona mienia, zdrowia i życia) może zostać uwzględniony w ramach podstawy z art. 7 lit. f dyrektywy (odpowiednik art. 6 ust. 1 lit. f RODO).",
     ["34 – uzasadnione interesy administratora (ochrona własności, zdrowia i życia) można uwzględnić m.in. na podstawie art. 7 lit. f dyrektywy"]),
    ("62014CJ0362", "C-362/14", "Schrems (I)", "2015-10-06", "wielka izba", "ECLI:EU:C:2015:650",
     "dyrektywa 95/46", ["45", "58", "77"],
     "Decyzja Komisji o odpowiednim stopniu ochrony nie stoi na przeszkodzie temu, by organ nadzorczy rozpatrzył skargę osoby podnoszącej, że prawo i praktyka państwa trzeciego nie zapewniają odpowiedniej ochrony. Decyzja 2000/520 (Safe Harbour) jest nieważna. Stwierdzić nieważność decyzji Komisji może wyłącznie Trybunał – sądy krajowe i organy nadzorcze nie mogą tego zrobić samodzielnie.",
     ["61 – wyłącznie Trybunał jest właściwy do stwierdzenia nieważności aktu Unii, takiego jak decyzja o adekwatności", "62 – sądy krajowe i organy nadzorcze nie mogą samodzielnie stwierdzić nieważności takiej decyzji"]),
    ("62014CJ0582", "C-582/14", "Breyer", "2016-10-19", "druga izba", "ECLI:EU:C:2016:779",
     "dyrektywa 95/46", ["4(1)", "6(1)(f)"],
     "Dynamiczny adres IP rejestrowany przez operatora strony internetowej jest dla niego daną osobową, jeżeli dysponuje on środkami prawnymi pozwalającymi zidentyfikować użytkownika dzięki dodatkowym informacjom posiadanym przez dostawcę internetu. Art. 7 lit. f dyrektywy stoi na przeszkodzie przepisom krajowym, które z góry zawężają możliwość przetwarzania danych bez zgody i wykluczają wyważenie interesów.",
     []),
    ("62016CJ0013", "C-13/16", "Rīgas satiksme", "2017-05-04", "druga izba", "ECLI:EU:C:2017:336",
     "dyrektywa 95/46", ["6(1)(f)"],
     "Sentencja: art. 7 lit. f dyrektywy nie nakłada obowiązku przekazania danych osobowych osobie trzeciej w celu dochodzenia przez nią odszkodowania, ale nie stoi na przeszkodzie takiemu przekazaniu na podstawie prawa krajowego. Uzasadnienie (pkt 28) formułuje trzy kumulatywne przesłanki przetwarzania na podstawie prawnie uzasadnionego interesu: (1) realizacja uzasadnionego interesu administratora lub osoby trzeciej, (2) niezbędność przetwarzania do realizacji tego interesu, (3) brak pierwszeństwa praw i wolności osoby, której dane dotyczą. To podstawa testu LIA.",
     ["28 – trzy kumulatywne przesłanki legalności przetwarzania na podstawie art. 7 lit. f dyrektywy (test LIA)"]),
    ("62016CJ0210", "C-210/16", "Wirtschaftsakademie Schleswig-Holstein", "2018-06-05", "wielka izba", "ECLI:EU:C:2018:388",
     "dyrektywa 95/46", ["4(7)", "26"],
     "Administrator fanpage’a na portalu społecznościowym jest (współ)administratorem danych odwiedzających w rozumieniu art. 2 lit. d dyrektywy. Wspólna odpowiedzialność nie wymaga, by każdy ze współadministratorów miał dostęp do danych. Pkt 2–3 sentencji dotyczą właściwości organów nadzorczych na gruncie dyrektywy – na gruncie RODO zastąpione mechanizmem kompleksowej współpracy (art. 56, 60).",
     ["38 – dyrektywa nie wymaga, by przy wspólnej odpowiedzialności każdy z podmiotów miał dostęp do danych osobowych"]),
    ("62017CJ0040", "C-40/17", "Fashion ID", "2019-07-29", "druga izba", "ECLI:EU:C:2019:629",
     "dyrektywa 95/46", ["4(7)", "26", "6(1)(a)", "6(1)(f)", "13", "80"],
     "Operator strony z wtyczką społecznościową (np. „Lubię to”) jest administratorem tylko w zakresie zbierania i ujawniania danych przez transmisję – tam, gdzie rzeczywiście określa cele i sposoby. Każdy z podmiotów musi realizować własny uzasadniony interes. Zgodę dla tych operacji uzyskuje operator strony, na nim ciąży też obowiązek informacyjny w tym zakresie. Prawo krajowe może przyznać stowarzyszeniom konsumenckim legitymację procesową w sprawach naruszeń ochrony danych.",
     []),
    ("62017CJ0673", "C-673/17", "Planet49", "2019-10-01", "wielka izba", "ECLI:EU:C:2019:801",
     "dyrektywa 95/46, dyrektywa 2002/58, RODO", ["4(11)", "6(1)(a)", "7"],
     "Zgoda na cookies wyrażona przez domyślnie zaznaczone okienko, które trzeba odznaczyć, nie jest ważna. Wykładnia jest taka sama niezależnie od tego, czy informacje w urządzeniu końcowym są danymi osobowymi. Informacja dla użytkownika obejmuje okres funkcjonowania cookies i to, czy osoby trzecie mogą uzyskać do nich dostęp.",
     []),
    ("62018CJ0708", "C-708/18", "TK / Asociaţia de Proprietari bloc M5A-ScaraA", "2019-12-11", "trzecia izba", "ECLI:EU:C:2019:1064",
     "dyrektywa 95/46", ["5(1)(c)", "6(1)(f)"],
     "Monitoring wizyjny części wspólnych budynku mieszkalnego w celu ochrony osób i mienia może być prowadzony bez zgody osób, których dane dotyczą, na podstawie prawnie uzasadnionego interesu, jeżeli spełnione są przesłanki art. 7 lit. f dyrektywy – co ocenia sąd krajowy (niezbędność, minimalizacja, wyważenie).",
     []),
    ("62018CJ0311", "C-311/18", "Facebook Ireland i Schrems (Schrems II)", "2020-07-16", "wielka izba", "ECLI:EU:C:2020:559",
     "RODO", ["2", "44", "45", "46(1)", "46(2)(c)", "58(2)"],
     "RODO obejmuje przekazanie danych podmiotowi w państwie trzecim, nawet jeśli mogą one tam być przetwarzane przez organy do celów bezpieczeństwa. SCC muszą zapewnić ochronę merytorycznie równoważną unijnej – ocenia się postanowienia umowne i system prawny państwa trzeciego (dostęp organów publicznych). Organ nadzorczy musi zawiesić lub zakazać transferu na SCC, jeśli klauzule nie mogą być przestrzegane, a ochrony nie da się zapewnić innymi środkami. Decyzja 2010/87 (SCC) pozostała ważna; decyzja 2016/1250 (Tarcza Prywatności) jest nieważna.",
     []),
    ("62020CJ0184", "C-184/20", "OT / Vyriausioji tarnybinės etikos komisija", "2022-08-01", "wielka izba", "ECLI:EU:C:2022:601",
     "dyrektywa 95/46, RODO", ["6(1)(c)", "6(3)", "9(1)"],
     "Publikacja w internecie oświadczeń o interesach prywatnych jest nieproporcjonalna w zakresie danych osób bliskich i wszystkich transakcji powyżej 3000 EUR. Dane mogące pośrednio ujawnić orientację seksualną (np. imię partnera) są danymi szczególnej kategorii w rozumieniu art. 9 ust. 1 RODO.",
     []),
    ("62021CJ0154", "C-154/21", "Österreichische Post (odbiorcy)", "2023-01-12", "pierwsza izba", "ECLI:EU:C:2023:3",
     "RODO", ["15(1)(c)", "12(5)"],
     "W ramach prawa dostępu administrator musi podać tożsamość konkretnych odbiorców, którym ujawniono dane, a nie tylko ich kategorie – chyba że identyfikacja odbiorców jest niemożliwa albo żądanie jest ewidentnie nieuzasadnione lub nadmierne (art. 12 ust. 5).",
     []),
    ("62021CJ0300", "C-300/21", "Österreichische Post (odszkodowanie)", "2023-05-04", "trzecia izba", "ECLI:EU:C:2023:370",
     "RODO", ["82"],
     "Samo naruszenie RODO nie wystarcza do przyznania odszkodowania – potrzebne są szkoda i związek przyczynowy. Nie można uzależniać odszkodowania za szkodę niemajątkową od osiągnięcia określonego stopnia wagi. Wysokość odszkodowania ustala się według prawa krajowego, z poszanowaniem zasad równoważności i skuteczności.",
     []),
    ("62021CJ0487", "C-487/21", "F.F. / Österreichische Datenschutzbehörde (kopia)", "2023-05-04", "pierwsza izba", "ECLI:EU:C:2023:369",
     "RODO", ["15(1)", "15(3)"],
     "Prawo do kopii oznacza wierną i zrozumiałą reprodukcję wszystkich danych. Obejmuje kopie fragmentów dokumentów, całych dokumentów lub wyciągów z baz danych, jeżeli jest to niezbędne do skutecznego wykonywania praw, z uwzględnieniem praw innych osób. „Informacje” w art. 15 ust. 3 zd. trzecie to wyłącznie dane osobowe, których kopię trzeba dostarczyć.",
     []),
    ("62021CJ0252", "C-252/21", "Meta Platforms i in. / Bundeskartellamt", "2023-07-04", "wielka izba", "ECLI:EU:C:2023:537",
     "RODO", ["4(11)", "6(1)(a)", "6(1)(b)", "6(1)(c)", "6(1)(d)", "6(1)(e)", "6(1)(f)", "9(1)", "9(2)(a)", "9(2)(e)", "51"],
     "Organ ochrony konkurencji może w sprawie o nadużycie pozycji dominującej stwierdzić niezgodność z RODO, z zachowaniem lojalnej współpracy z organami nadzorczymi. Zbieranie danych z przeglądania stron i aplikacji powiązanych z kategoriami z art. 9 ust. 1 jest przetwarzaniem danych szczególnych kategorii; samo przeglądanie nie oznacza ich „oczywistego upublicznienia”. Art. 6 ust. 1 lit. b obejmuje tylko przetwarzanie obiektywnie niezbędne do głównego celu umowy. Lit. f wymaga wskazania interesu, ścisłej niezbędności i wyważenia; użytkownik nie może racjonalnie spodziewać się przetwarzania bez zgody w celu personalizacji reklamy, więc takie przetwarzanie nie mieści się w lit. f (pkt 117). Pozycja dominująca nie wyklucza ważnej zgody, ale jest istotna przy ocenie jej dobrowolności.",
     ["115–117 – personalizacja reklamy: marketing bezpośredni może być uzasadnionym interesem (motyw 47), ale użytkownik nie może racjonalnie spodziewać się przetwarzania bez zgody w tym celu; interesy użytkownika przeważają"]),
    ("62021CJ0807", "C-807/21", "Deutsche Wohnen", "2023-12-05", "wielka izba", "ECLI:EU:C:2023:950",
     "RODO", ["58(2)(i)", "83"],
     "Kara z art. 83 wobec osoby prawnej nie może być uzależniona od uprzedniego przypisania naruszenia zidentyfikowanej osobie fizycznej. Kara wymaga wykazania naruszenia umyślnego lub nieumyślnego. Przy ustalaniu wysokości kary wobec przedsiębiorstwa stosuje się pojęcie przedsiębiorstwa (jednostki gospodarczej) z prawa konkurencji (art. 101 i 102 TFUE).",
     ["56–59 – pojęcie przedsiębiorstwa jako jednostki gospodarczej; kara ustalana według rzeczywistych możliwości ekonomicznych adresata"]),
    ("62021CJ0683", "C-683/21", "Nacionalinis visuomenės sveikatos centras", "2023-12-05", "wielka izba", "ECLI:EU:C:2023:949",
     "RODO", ["4(2)", "4(7)", "26", "83"],
     "Administratorem może być podmiot, który zlecił opracowanie aplikacji i uczestniczył w określaniu celów i sposobów przetwarzania, nawet jeśli sam nie przetwarzał danych, nie wyraził zgody na publiczne udostępnienie i nie nabył aplikacji – chyba że wyraźnie się temu sprzeciwił. Współadministrowanie nie wymaga uzgodnień między podmiotami. Testowanie systemów na danych osobowych jest przetwarzaniem (chyba że dane są zanonimizowane lub fikcyjne). Kara wymaga zawinienia; można ją nałożyć na administratora za przetwarzanie przez podmiot przetwarzający, chyba że ten działał we własnych celach lub poza ramami określonymi przez administratora.",
     []),
    ("62021CJ0634", "C-634/21", "OQ / SCHUFA Holding (scoring)", "2023-12-07", "pierwsza izba", "ECLI:EU:C:2023:957",
     "RODO", ["22(1)"],
     "Zautomatyzowane wyliczenie przez biuro informacji kredytowej wartości prawdopodobieństwa (scoringu) jest zautomatyzowanym podejmowaniem decyzji w rozumieniu art. 22 ust. 1, jeżeli od tej wartości w decydujący sposób zależy, czy strona trzecia nawiąże, wykona lub zakończy umowę z tą osobą.",
     []),
    ("62022CJ0026", "C-26/22, C-64/22", "UF i AB / SCHUFA Holding (zwolnienie z długów)", "2023-12-07", "pierwsza izba", "ECLI:EU:C:2023:958",
     "RODO", ["5(1)(a)", "6(1)(f)", "17(1)(c)", "17(1)(d)", "21(1)", "78(1)"],
     "Decyzja organu nadzorczego w sprawie skargi podlega pełnej kontroli sądowej. Prywatne biuro informacji kredytowej nie może przechowywać danych o zwolnieniu z długów pochodzących z rejestru publicznego dłużej niż ten rejestr. Osoba wnosząca sprzeciw (art. 21 ust. 1) może żądać usunięcia danych, jeżeli brak nadrzędnych prawnie uzasadnionych podstaw; dane przetwarzane niezgodnie z prawem trzeba usunąć bez zbędnej zwłoki.",
     []),
    ("62022CJ0604", "C-604/22", "IAB Europe", "2024-03-07", "czwarta izba", "ECLI:EU:C:2024:214",
     "RODO", ["4(1)", "4(7)", "26(1)"],
     "TC String jest daną osobową, jeżeli rozsądnie prawdopodobnymi sposobami można go powiązać z identyfikatorem, np. adresem IP – nawet gdy organizacja sektorowa sama nie ma dostępu do danych. Organizacja ustalająca ramy (TCF) może być współadministratorem bez bezpośredniego dostępu do danych, ale jej odpowiedzialność nie rozciąga się automatycznie na dalsze przetwarzanie przez osoby trzecie do celów reklamy ukierunkowanej.",
     []),
    ("62022CJ0621", "C-621/22", "Koninklijke Nederlandse Lawn Tennis Bond (KNLTB)", "2024-10-04", "dziewiąta izba", "ECLI:EU:C:2024:858",
     "RODO", ["6(1)(f)"],
     "Interes czysto komercyjny (odpłatne ujawnienie danych członków związku sportowego sponsorom) może być prawnie uzasadnionym interesem, jeżeli jest zgodny z prawem – nie musi być określony ustawowo. Przetwarzanie musi być ściśle niezbędne, a interesy i prawa członków nie mogą mieć nadrzędnego charakteru.",
     []),
    ("62023CJ0413", "C-413/23 P", "EIOD / SRB", "2025-09-04", "pierwsza izba", "ECLI:EU:C:2025:645",
     "rozporządzenie 2018/1725", ["4(1)", "4(5)", "11", "13", "14"],
     "Sentencja: uchylenie wyroku Sądu (T-557/20) i przekazanie sprawy do ponownego rozpoznania. Tezy z uzasadnienia: dla administratora, który ma dodatkowe informacje, dane spseudonimizowane pozostają danymi osobowymi (pkt 76); dla odbiorcy mogą nie być danymi osobowymi, jeżeli nie może znieść pseudonimizacji ani zidentyfikować osoby innymi sposobami (pkt 77, 86); dane spseudonimizowane nie są więc w każdym przypadku i dla każdego danymi osobowymi. Obowiązek informacyjny (w tym o odbiorcach) ocenia się w momencie zbierania danych i z punktu widzenia administratora (pkt 111). Wyrok na gruncie rozporządzenia 2018/1725 – definicje tożsame z RODO.",
     ["76 – dla administratora dysponującego dodatkowymi informacjami dane spseudonimizowane zachowują charakter danych osobowych", "77 – dla odbiorcy mogą nie mieć tego charakteru, jeśli nie może znieść środków pseudonimizacji ani zidentyfikować osoby innymi sposobami", "86 – dane spseudonimizowane nie stanowią w każdym wypadku i dla każdej osoby danych osobowych", "111 – identyfikowalność dla celów obowiązku informacyjnego ocenia się w momencie zbierania danych i z punktu widzenia administratora"]),
]


def slug(syg):
    return syg.lower().replace(", ", "-").replace("/", "-").replace(" ", "-")


def main(sent_path):
    sent = json.load(open(sent_path, encoding="utf-8"))
    rows = []
    for celex, syg, nazwa, data, izba, ecli, podstawa, arts, teza, punkty in CASES:
        s = slug(syg)
        tekst = sent[celex]
        sha = hashlib.sha256(tekst.encode("utf-8")).hexdigest()
        note = ""
        if "95/46" in podstawa and "RODO" not in podstawa:
            note = "\n\n**Podstawa:** wyrok wydany na gruncie dyrektywy 95/46; zachowuje aktualność dla wskazanych odpowiedników w RODO."
        elif "2018/1725" in podstawa:
            note = "\n\n**Podstawa:** wyrok na gruncie rozporządzenia 2018/1725 (instytucje UE); definicje są tożsame z RODO."
        pkt = ""
        if punkty:
            pkt = "\n## Kluczowe punkty uzasadnienia\n\n" + "\n".join(f"- pkt {p}" for p in punkty) + "\n"
        content = f"""---
id: tsue-{s}
typ: wyrok
tytul: {nazwa}
sygnatura: {syg}
organ: TSUE ({izba})
data: {data}
ecli: {ecli}
celex: {celex}
status: prawomocny
podstawa: {podstawa}
artykuly_rodo: [{", ".join(arts)}]
zrodlo: https://eur-lex.europa.eu/legal-content/PL/TXT/?uri=CELEX:{celex}
jezyk_tekstu: pl
sha256_sentencji: {sha}
weryfikacja: {WERYF}
---

# {syg} {nazwa} ({data})

**{ecli}** · TSUE, {izba}

## Teza

{teza}{note}
{pkt}
## Sentencja

Trybunał orzeka, co następuje:

<!-- tekst urzędowy: początek -->
{tekst}
<!-- tekst urzędowy: koniec -->
"""
        with open(os.path.join(OUT, s + ".md"), "w", encoding="utf-8") as f:
            f.write(content)
        rows.append(f"| [{syg}]({s}.md) | {nazwa} | {data} | {izba} | {ecli} | {podstawa} | {', '.join(arts)} |")

    with open(os.path.join(OUT, "rejestr.md"), "w", encoding="utf-8") as f:
        f.write(f"""---
id: tsue-rejestr
typ: rejestr
tytul: Wyroki wiodące TSUE – rejestr
organ: TSUE
data: 2026-10-08
status: obowiazuje
artykuly_rodo: []
zrodlo: https://eur-lex.europa.eu
weryfikacja: {WERYF}
---

# Wyroki wiodące TSUE

Etap 1 obejmuje wyłącznie wyroki wiodące. Każdy plik zawiera tezę (własnymi słowami), kluczowe punkty uzasadnienia oraz sentencję w brzmieniu z EUR-Lex (suma SHA-256 w nagłówku). Gdy teza wynika z uzasadnienia, a nie z sentencji, plik wskazuje numer punktu.

| Sygnatura | Nazwa | Data | Skład | ECLI | Podstawa | Artykuły RODO |
|---|---|---|---|---|---|---|
""" + "\n".join(rows) + "\n")
    print(len(rows))


if __name__ == "__main__":
    main(sys.argv[1])
