#!/usr/bin/env python3
"""Zapisuje ustawę z 10 maja 2018 r. o ochronie danych osobowych do zrodla/pl/ustawa-odo-2018/.

Wejście: narzedzia/dane/uodo2018_tj2019.json – artykuły tekstu jednolitego (Dz.U. 2019 poz. 1781)
pobrane z api.sejm.gov.pl (ELI DU/2019/1781, text.html); zgodność każdego artykułu ze źródłem
potwierdzona sumą SHA-256 policzoną w przeglądarce na oryginalnym HTML.

Na tekst jednolity nanoszone są zmiany z 2026 r. (ZMIANY_2026) przepisane z PDF Dziennika Ustaw.
Tekst między znacznikami `<!-- tekst urzędowy -->` jest kopią źródła 1:1 (indeksy górne zapisane
znakami Unicode, np. „art. 23¹”, „6⁰⁰”).

Użycie: python3 narzedzia/import_ustawa.py
"""
import hashlib
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DANE = os.path.join(ROOT, "narzedzia", "dane", "uodo2018_tj2019.json")
OUT = os.path.join(ROOT, "zrodla", "pl", "ustawa-odo-2018")
ELI_AKT = "https://api.sejm.gov.pl/eli/acts/DU/2018/1000"
ELI_TJ = "https://api.sejm.gov.pl/eli/acts/DU/2019/1781/text.html"
ISAP = "https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU20180001000"
DATA_IMPORTU = "2026-10-08"

ROZDZIALY = [
    ("1", "Rozdział 1 – Przepisy ogólne"),
    ("8", "Rozdział 2 – Wyznaczanie inspektora ochrony danych"),
    ("12", "Rozdział 3 – Warunki i tryb udzielania akredytacji podmiotowi certyfikującemu"),
    ("15", "Rozdział 4 – Warunki i tryb dokonywania certyfikacji"),
    ("27", "Rozdział 5 – Opracowywanie i zatwierdzanie kodeksu postępowania oraz warunki i tryb akredytacji podmiotu monitorującego jego przestrzeganie"),
    ("34", "Rozdział 6 – Prezes Urzędu"),
    ("60", "Rozdział 7 – Postępowanie w sprawie naruszenia przepisów o ochronie danych osobowych"),
    ("75", "Rozdział 8 – Europejska współpraca administracyjna"),
    ("78", "Rozdział 9 – Kontrola przestrzegania przepisów o ochronie danych osobowych"),
    ("92", "Rozdział 10 – Odpowiedzialność cywilna i postępowanie przed sądem"),
    ("101", "Rozdział 11 – Przepisy o administracyjnych karach pieniężnych i przepisy karne"),
    ("109-157", "Rozdział 12 – Zmiany w przepisach"),
    ("158", "Rozdział 13 – Przepisy przejściowe i dostosowujące"),
    ("175", "Rozdział 14 – Przepisy końcowe"),
]

# Odnośniki tekstu jednolitego dotyczące brzmienia artykułów (bez odnośników o publikatorach innych ustaw).
ODN3 = "ustawa z dnia 21 lutego 2019 r. o zmianie niektórych ustaw w związku z zapewnieniem stosowania rozporządzenia 2016/679 (Dz.U. poz. 730), w życie 2019-05-04"
ODN7 = "ustawa z dnia 3 lipca 2018 r. – Przepisy wprowadzające ustawę – Prawo o szkolnictwie wyższym i nauce (Dz.U. poz. 1669), w życie 2018-10-01"
PRZYPISY = {
    "5a": ["Dodany przez art. 161 pkt 1 ustawy z dnia 21 lutego 2019 r. o zmianie niektórych ustaw w związku z zapewnieniem stosowania rozporządzenia Parlamentu Europejskiego i Rady (UE) 2016/679 z dnia 27 kwietnia 2016 r. w sprawie ochrony osób fizycznych w związku z przetwarzaniem danych osobowych i w sprawie swobodnego przepływu takich danych oraz uchylenia dyrektywy 95/46/WE (ogólne rozporządzenie o ochronie danych) (Dz. U. poz. 730), która weszła w życie z dniem 4 maja 2019 r."],
    "6a": [f"Dodany przez art. 161 pkt 2 ustawy, o której mowa w odnośniku 3. [odnośnik 3: {ODN3}]"],
    "11a": [f"Dodany przez art. 161 pkt 3 ustawy, o której mowa w odnośniku 3. [odnośnik 3: {ODN3}]"],
    "48": [f"Ust. 7 pkt 4 – w brzmieniu ustalonym przez art. 168 pkt 1 ustawy z dnia 3 lipca 2018 r. - Przepisy wprowadzające ustawę - Prawo o szkolnictwie wyższym i nauce (Dz. U. poz. 1669), która weszła w życie z dniem 1 października 2018 r."],
    "57": [f"Ust. 1 – w brzmieniu ustalonym przez art. 161 pkt 4 ustawy, o której mowa w odnośniku 3. [odnośnik 3: {ODN3}]"],
    "85": [f"Ust. 7 – w brzmieniu ustalonym przez art. 168 pkt 2 ustawy, o której mowa w odnośniku 7. [odnośnik 7: {ODN7}]"],
    "101a": [f"Dodany przez art. 161 pkt 5 ustawy, o której mowa w odnośniku 3. [odnośnik 3: {ODN3}]"],
    "108": [f"Oznaczenie ust. 1 nadane przez art. 161 pkt 6 ustawy, o której mowa w odnośniku 3. [odnośnik 3: {ODN3}]",
            f"Ust. 2 dodany przez art. 161 pkt 6 ustawy, o której mowa w odnośniku 3. [odnośnik 3: {ODN3}]"],
    "109-157": ["Zamieszczone w obwieszczeniu (przepisy zmieniające inne ustawy – pominięte w tekście jednolitym)."],
    "175": ["Przepisy art. 1, art. 2, art. 3 ust. 1, art. 4-7, art. 14-22, art. 23-28, art. 31 oraz rozdziały 4, 5 i 7 ustawy z dnia 29 sierpnia 1997 r. o ochronie danych osobowych zachowane w mocy na podstawie art. 175 ustawy z dnia 10 maja 2018 r. o ochronie danych osobowych (Dz. U. poz. 1000) utraciły moc z dniem 6 lutego 2019 r. na podstawie art. 107 ustawy z dnia 14 grudnia 2018 r. o ochronie danych osobowych przetwarzanych w związku z zapobieganiem i zwalczaniem przestępczości (Dz. U. z 2019 r. poz. 125), która weszła w życie z dniem 6 lutego 2019 r."],
}
DODANE_2019 = {"5a", "6a", "11a", "101a"}

# Powiązanie z artykułami RODO – opracowanie własne na podstawie odesłań w treści przepisu.
RODO = {
    "1": "[2, 3]", "2": "[85]", "3": "[13(3), 23]", "4": "[14, 23]", "5": "[15, 23]", "5a": "[15, 23]",
    "6": "[2(2)]", "6a": "[9, 10]", "8": "[37]", "9": "[37(1)(a)]", "10": "[37(7)]", "11": "[37(7)]",
    "11a": "[37]", "12": "[43]", "13": "[43(3)]", "14": "[43]", "15": "[42]", "16": "[42(5)]",
    "17": "[42]", "18": "[42]", "19": "[42]", "20": "[42]", "21": "[42]", "22": "[42(7)]", "23": "[42(8)]",
    "24": "[42]", "25": "[42]", "26": "[42]", "27": "[40]", "28": "[41]", "29": "[41]", "30": "[41]",
    "31": "[41]", "32": "[41(5)]", "33": "[41]", "34": "[51, 53, 54]", "35": "[54]", "36": "[53]",
    "37": "[52(3)]", "38": "[52]", "45": "[52(4)]", "46": "[54(2)]", "50": "[59]", "51": "[36(4)]",
    "52": "[58(3)(b)]", "53": "[28(8), 40, 46(2)(d)]", "54": "[35(4), 35(5)]", "55": "[33]",
    "56": "[46(3), 47]", "57": "[36]", "58": "[58]", "59": "[91]", "60": "[57(1)(f), 58, 77]",
    "61": "[80(1)]", "64": "[58(1)]", "65": "[58(1)]", "68": "[58(1)]", "69": "[58(1)(a)]",
    "70": "[58(2)(f)]", "71": "[40(9), 45(3), 45(5), 46(2)(c), 58(5)]", "72": "[83(2)]", "73": "[58]",
    "74": "[83(8)]", "75": "[61(8), 62(7), 66(1)]", "76": "[60, 61]", "77": "[62]", "78": "[57(1)(h), 58(1)(b)]",
    "79": "[62]", "84": "[58(1)(e), 58(1)(f)]", "92": "[79, 82]", "93": "[79, 82]", "94": "[79, 82]",
    "95": "[79, 82]", "96": "[79, 82]", "97": "[82]", "98": "[80]", "99": "[79, 82]", "100": "[79, 82]",
    "101": "[83]", "101a": "[83]", "102": "[83(7)]", "103": "[83]", "104": "[83]", "105": "[83]",
    "106": "[83]", "107": "[84]", "108": "[84]", "158": "[37]", "172": "[35(4)]",
}

# Zmiany ustawy po tekście jednolitym z 2019 r. (stan na DATA_IMPORTU, wg ELI DU/2018/1000).
Z252 = "art. 16 ustawy z dnia 23 stycznia 2026 r. o zmianie ustawy o krajowym systemie cyberbezpieczeństwa oraz niektórych innych ustaw (Dz.U. 2026 poz. 252)"
Z548 = "art. 38 ustawy z dnia 27 marca 2026 r. o zarządzaniu danymi (Dz.U. 2026 poz. 548)"
Z1003 = "art. 123 ustawy z dnia 3 lipca 2026 r. o systemach sztucznej inteligencji (Dz.U. 2026 poz. 1003)"

ART104_NOWY = (
    "1. Środki z administracyjnej kary pieniężnej stanowią dochód budżetu państwa, z uwzględnieniem ust. 2.\n"
    "2. Środki z administracyjnej kary pieniężnej nałożonej za naruszenie art. 5 ust. 1 lit. f, art. 25 ust. 1 i 2, "
    "art. 28 ust. 3 lit. c oraz art. 32 ust. 1 i 2 rozporządzenia 2016/679 stanowią w 50 % dochód budżetu państwa, "
    "a w 50 % dochód Funduszu Cyberbezpieczeństwa, o którym mowa w art. 2 ustawy z dnia 2 grudnia 2021 r. o szczególnych "
    "zasadach wynagradzania osób realizujących zadania z zakresu cyberbezpieczeństwa (Dz. U. z 2024 r. poz. 1662, "
    "z 2025 r. poz. 1017 oraz z 2026 r. poz. 252)."
)
ART34_UST2A = (
    "2a. Prezes Urzędu jest organem właściwym do spraw:\n"
    "1) usług pośrednictwa danych, o którym mowa w art. 13 rozporządzenia Parlamentu Europejskiego i Rady (UE) 2022/868 "
    "z dnia 30 maja 2022 r. w sprawie europejskiego zarządzania danymi i zmieniającego rozporządzenie (UE) 2018/1724 "
    "(akt w sprawie zarządzania danymi) (Dz. Urz. UE L 152 z 03.06.2022, str. 1, z późn. zm.);\n"
    "2) rejestracji organizacji altruizmu danych, o którym mowa w art. 23 rozporządzenia Parlamentu Europejskiego i Rady (UE) "
    "2022/868 z dnia 30 maja 2022 r. w sprawie europejskiego zarządzania danymi i zmieniającego rozporządzenie (UE) 2018/1724 "
    "(akt w sprawie zarządzania danymi);\n"
    "3) naruszeń obowiązków, o których mowa w art. 5 ust. 14 lub art. 31 rozporządzenia Parlamentu Europejskiego i Rady (UE) "
    "2022/868 z dnia 30 maja 2022 r. w sprawie europejskiego zarządzania danymi i zmieniającego rozporządzenie (UE) 2018/1724 "
    "(akt w sprawie zarządzania danymi), dotyczących przekazywania danych nieosobowych do państw trzecich."
)
ART59A = "Prezes Urzędu współpracuje z Komisją Rozwoju i Bezpieczeństwa Sztucznej Inteligencji."


def sha(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def nazwa_pliku(nr):
    if "-" in nr:
        a, b = nr.split("-")
        return f"art-{int(a):03d}-{int(b):03d}.md"
    num = "".join(c for c in nr if c.isdigit())
    lit = nr[len(num):]
    return f"art-{int(num):03d}{lit}.md"


def zapisz(nr, rozdzial, tekst, *, status="obowiazuje", obowiazuje_od="2018-05-25", wersja, weryfikacja,
           przypisy=(), dodatkowe_sekcje="", ostatnia_zmiana=None):
    lines = [
        "---",
        f"id: pl-uodo2018-art-{nr}",
        "typ: ustawa",
        f'tytul: "Art. {nr} ustawy o ochronie danych osobowych"',
        f"sygnatura: art. {nr} u.o.d.o.",
        "organ: Sejm RP",
        "data: 2018-05-10",
        f"status: {status}",
        f"obowiazuje_od: {obowiazuje_od}",
        "podstawa: RODO",
        f"artykuly_rodo: {RODO.get(nr, '[]')}",
        f'rozdzial: "{rozdzial}"',
        "akt: ustawa z dnia 10 maja 2018 r. o ochronie danych osobowych (Dz.U. 2018 poz. 1000; t.j. Dz.U. 2019 poz. 1781, zm. Dz.U. 2026 poz. 252, 548, 1003)",
        f"zrodlo: {ELI_AKT}",
        f"wersja_tekstu: {wersja}",
        "jezyk_tekstu: pl",
        f"sha256_tekstu: {sha(tekst)}",
    ]
    if ostatnia_zmiana:
        lines.append(f"ostatnia_zmiana: {ostatnia_zmiana}")
    lines.append(f"weryfikacja: {weryfikacja}")
    lines += ["---", "", f"# Art. {nr}", "", f"*{rozdzial}*", "",
              "<!-- tekst urzędowy: początek -->", tekst, "<!-- tekst urzędowy: koniec -->", ""]
    if przypisy:
        lines += ["## Przypisy tekstu jednolitego", ""] + [f"- {p}" for p in przypisy] + [""]
    if dodatkowe_sekcje:
        lines += [dodatkowe_sekcje, ""]
    with open(os.path.join(OUT, nazwa_pliku(nr)), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    with open(DANE, encoding="utf-8") as f:
        recs = json.load(f)
    os.makedirs(OUT, exist_ok=True)
    starty = dict(ROZDZIALY)
    rozdzial = None
    WER_TJ = "Dz.U. 2019 poz. 1781 (tekst jednolity, api.sejm.gov.pl ELI)"
    WERYF_TJ = f"zweryfikowane ({DATA_IMPORTU}, zgodność z tekstem jednolitym w api.sejm.gov.pl potwierdzona sumą kontrolną)"
    WERYF_ZM = (f"zweryfikowane ({DATA_IMPORTU}): część z tekstu jednolitego – suma kontrolna zgodna z api.sejm.gov.pl; "
                "zmiana z 2026 r. – przepisana z PDF Dziennika Ustaw (łamanie wierszy i przenoszenie wyrazów usunięte)")
    n = 0
    for r in recs:
        nr, tekst = r["nr"], r["text"]
        if nr in starty:
            rozdzial = starty[nr]
        od = "2019-05-04" if nr in DODANE_2019 else "2018-05-25"
        przyp = PRZYPISY.get(nr, [])

        if nr == "34":
            linie = tekst.split("\n")
            idx = next(i for i, l in enumerate(linie) if l.startswith("3. "))
            nowy = "\n".join(linie[:idx] + [ART34_UST2A] + linie[idx:])
            hist = ("## Historia zmian\n\n"
                    f"- **2026-07-23** – dodano ust. 2a: {Z548}; ustawa weszła w życie po 3 miesiącach od ogłoszenia.\n"
                    "- Do 2026-07-22 przepis obowiązywał bez ust. 2a (tekst jednolity Dz.U. 2019 poz. 1781, "
                    f"sha256 brzmienia sprzed zmiany: `{sha(tekst)}`).\n\n"
                    "Ust. 2a – przypis aktu zmieniającego do rozporządzenia 2022/868: zmiany ogłoszone w Dz. Urz. UE L 132 "
                    "z 17.05.2023, str. 89 oraz Dz. Urz. UE L 2023/90204 z 21.12.2023.")
            zapisz(nr, rozdzial, nowy, wersja=f"{WER_TJ} + ust. 2a z Dz.U. 2026 poz. 548 (naniesione w repo)",
                   weryfikacja=WERYF_ZM, przypisy=przyp, dodatkowe_sekcje=hist, ostatnia_zmiana="2026-07-23")
        elif nr == "104":
            hist = ("## Historia zmian\n\n"
                    f"- **2026-04-03** – nowe brzmienie: {Z252}; ustawa weszła w życie po miesiącu od ogłoszenia.\n\n"
                    "### Brzmienie do 2026-04-02 (tekst jednolity Dz.U. 2019 poz. 1781)\n\n"
                    f"> {tekst}\n\n"
                    f"sha256 brzmienia sprzed zmiany: `{sha(tekst)}`")
            zapisz(nr, rozdzial, ART104_NOWY, wersja="Dz.U. 2026 poz. 252, art. 16 (nowe brzmienie; naniesione w repo)",
                   weryfikacja=WERYF_ZM, przypisy=przyp, dodatkowe_sekcje=hist, ostatnia_zmiana="2026-04-03")
        else:
            zapisz(nr, rozdzial, tekst, obowiazuje_od=od, wersja=WER_TJ, weryfikacja=WERYF_TJ, przypisy=przyp)
        n += 1
        if nr == "59":
            hist = ("## Historia zmian\n\n"
                    f"- Dodany przez {Z1003}. Rozdział 9 tej ustawy („Zmiany w przepisach”) wchodzi w życie po upływie "
                    "3 miesięcy od dnia ogłoszenia (art. 127 pkt 2) – według ELI: **2026-10-28**.\n"
                    "- Komisja Rozwoju i Bezpieczeństwa Sztucznej Inteligencji jest organem nadzoru rynku w zakresie systemów AI "
                    "w rozumieniu art. 70 ust. 1 rozporządzenia (UE) 2024/1689 (AI Act) i pojedynczym punktem kontaktowym "
                    "(art. 5 ust. 1–2 ustawy o systemach sztucznej inteligencji).")
            zapisz("59a", starty["34"], ART59A, status="wchodzi-w-zycie", obowiazuje_od="2026-10-28",
                   wersja="Dz.U. 2026 poz. 1003, art. 123 (naniesione w repo)",
                   weryfikacja=f"zweryfikowane ({DATA_IMPORTU}, przepisane z PDF Dziennika Ustaw)",
                   dodatkowe_sekcje=hist)
            n += 1
    print(f"Zapisano plików: {n}")


if __name__ == "__main__":
    main()
