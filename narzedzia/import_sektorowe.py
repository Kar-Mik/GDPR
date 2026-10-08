#!/usr/bin/env python3
"""Zapisuje wybrane przepisy sektorowe do zrodla/pl/:

- Kodeks pracy, art. 22¹–22³ (dane kandydatów i pracowników, kontrola trzeźwości, monitoring) –
  z tekstu jednolitego Dz.U. 2026 poz. 1245 (PDF z api.sejm.gov.pl, warstwa tekstowa; stan prawny
  na 27.08.2026 z uwzględnieniem zmian wymienionych w obwieszczeniu),
- Prawo komunikacji elektronicznej, art. 398–400 (marketing bezpośredni, cookies, zgoda) –
  z tekstu Dz.U. 2024 poz. 1221 (HTML z api.sejm.gov.pl); akty zmieniające PKE (Dz.U. 2025 poz. 637, 820;
  2026 poz. 252, 815, 1296) sprawdzone – żaden nie zmienia art. 398–400.

Dane wejściowe: narzedzia/dane/kp_art22.json, narzedzia/dane/pke_art398_400.json (przeniesione z przeglądarki,
zgodność potwierdzona sumą SHA-256). KOREKTY – błędy warstwy tekstowej PDF poprawione jawnie.

Użycie: python3 narzedzia/import_sektorowe.py
"""
import hashlib
import json
import re
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DANE = os.path.join(ROOT, "narzedzia", "dane")
DATA_IMPORTU = "2026-10-08"

SUP2ASCII = str.maketrans({"¹": "1", "²": "2", "³": "3", "ᵃ": "a", "ᵇ": "b", "ᶜ": "c", "ᵈ": "d", "ᵉ": "e", "ᶠ": "f", "ᵍ": "g", "ʰ": "h"})

# Błędy warstwy tekstowej PDF (sklejone wyrazy, niezamieniony indeks górny) – poprawione względem obrazu strony.
KOREKTY = [("niepóźniej", "nie później"), ("22¹g", "22¹ᵍ")]

KP_RODO = {
    "22¹": "[6(1)(b), 6(1)(c), 88]",
    "22¹ᵃ": "[6(1)(a), 7, 10, 88]",
    "22¹ᵇ": "[9(1), 9(2)(a), 9(2)(b), 9(4), 88]",
    "22¹ᶜ": "[5(1)(e), 6(1)(c), 9(2)(b), 88]",
    "22¹ᵈ": "[6(1)(c), 9(2)(b), 88]",
    "22¹ᵉ": "[5(1)(e), 6(1)(c), 9(2)(b), 88]",
    "22¹ᶠ": "[6(1)(c), 9(2)(b), 88]",
    "22¹ᵍ": "[88]",
    "22¹ʰ": "[88]",
    "22²": "[5(1)(c), 5(1)(e), 6(1)(c), 12, 13, 88]",
    "22³": "[5(1)(c), 6(1)(c), 88]",
}
KP_TEMAT = {
    "22¹": "dane osobowe kandydata i pracownika – katalog",
    "22¹ᵃ": "zgoda kandydata/pracownika jako podstawa przetwarzania",
    "22¹ᵇ": "dane szczególnych kategorii i biometria pracownika",
    "22¹ᶜ": "kontrola trzeźwości",
    "22¹ᵈ": "niedopuszczenie do pracy po kontroli trzeźwości",
    "22¹ᵉ": "kontrola na obecność środków działających podobnie do alkoholu",
    "22¹ᶠ": "niedopuszczenie do pracy – środki podobne do alkoholu",
    "22¹ᵍ": "upoważnienie do rozporządzenia (badania trzeźwości)",
    "22¹ʰ": "kontrola trzeźwości – osoby zatrudnione na innej podstawie",
    "22²": "monitoring wizyjny",
    "22³": "monitoring poczty elektronicznej i inne formy monitoringu",
}
PKE_RODO = {"398": "[6(1)(a), 7, 21(2)]", "399": "[4(11), 6(1)(a), 7, 95]", "400": "[4(11), 7, 8]"}
PKE_TEMAT = {"398": "zakaz marketingu bezpośredniego bez zgody (telefon, e-mail, systemy wywołujące)",
             "399": "cookies – przechowywanie informacji i dostęp do urządzenia końcowego",
             "400": "zgoda – odesłanie do przepisów o ochronie danych osobowych"}


def popraw(s):
    for a, b in KOREKTY:
        s = s.replace(a, b)
    return s


def zapisz(katalog, plik, linie):
    os.makedirs(katalog, exist_ok=True)
    with open(os.path.join(katalog, plik), "w", encoding="utf-8") as f:
        f.write("\n".join(linie))


def kp():
    d = json.load(open(os.path.join(DANE, "kp_art22.json"), encoding="utf-8"))
    out = os.path.join(ROOT, "zrodla", "pl", "kodeks-pracy")
    pliki = []
    for num, paras in d["arts"]:
        tekst = [popraw(p) for p in paras]
        tekst[0] = re.sub(r"^Art\. \S+\.\s*", "", tekst[0])
        body = "\n".join(tekst)
        sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
        przypisy = sorted({k for k in d["foots"] if f"⁽{k}⁾" in body}, key=int)
        nazwa = "art-22-" + num[2:].translate(SUP2ASCII) + ".md"
        linie = [
            "---",
            f"id: pl-kp-{nazwa[:-3]}",
            "typ: ustawa",
            f'tytul: "Art. {num} Kodeksu pracy – {KP_TEMAT[num]}"',
            f"sygnatura: art. {num} KP",
            "organ: Sejm RP",
            "data: 1974-06-26",
            "status: obowiazuje",
            "podstawa: RODO",
            f"artykuly_rodo: {KP_RODO[num]}",
            "akt: ustawa z dnia 26 czerwca 1974 r. – Kodeks pracy (t.j. Dz.U. 2026 poz. 1245)",
            "zrodlo: https://api.sejm.gov.pl/eli/acts/DU/2026/1245",
            "wersja_tekstu: Dz.U. 2026 poz. 1245 (tekst jednolity, stan prawny na 27.08.2026)",
            "jezyk_tekstu: pl",
            f"sha256_tekstu: {sha}",
            f'weryfikacja: "zweryfikowane ({DATA_IMPORTU}) – tekst z warstwy tekstowej PDF tekstu jednolitego; korekty sklejonych wyrazów opisane w README"',
            "---",
            "",
            f"# Art. {num} Kodeksu pracy",
            "",
            f"*{KP_TEMAT[num]}*",
            "",
            "<!-- tekst urzędowy: początek -->",
            body,
            "<!-- tekst urzędowy: koniec -->",
            "",
        ]
        if przypisy:
            linie += ["## Przypisy tekstu jednolitego", ""]
            for k in przypisy:
                t = d["foots"][k]
                if "odnośniku 10" in t:
                    t += " [ustawa z odnośnika 10: ustawa z dnia 4 czerwca 2025 r. o zmianie ustawy – Kodeks pracy (Dz. U. poz. 807), w życie 24.12.2025 r.]"
                linie.append(f"- ⁽{k}⁾ {t}")
            linie.append("")
        zapisz(out, nazwa, linie)
        pliki.append((num, nazwa))
    return pliki


def pke():
    d = json.load(open(os.path.join(DANE, "pke_art398_400.json"), encoding="utf-8"))
    out = os.path.join(ROOT, "zrodla", "pl", "prawo-komunikacji-elektronicznej")
    pliki = []
    for num in ["398", "399", "400"]:
        paras = d[num]
        paras = [re.sub(r"^Art\. \d+\.\s*", "", paras[0])] + paras[1:]
        paras = [x for x in paras if x]
        body = "\n".join(paras)
        sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
        linie = [
            "---",
            f"id: pl-pke-art-{num}",
            "typ: ustawa",
            f'tytul: "Art. {num} Prawa komunikacji elektronicznej – {PKE_TEMAT[num]}"',
            f"sygnatura: art. {num} PKE",
            "organ: Sejm RP",
            "data: 2024-07-12",
            "status: obowiazuje",
            "obowiazuje_od: 2024-11-10",
            "podstawa: dyrektywa 2002/58 (ePrivacy)",
            f"artykuly_rodo: {PKE_RODO[num]}",
            "akt: ustawa z dnia 12 lipca 2024 r. – Prawo komunikacji elektronicznej (Dz.U. 2024 poz. 1221 ze zm.)",
            "zrodlo: https://api.sejm.gov.pl/eli/acts/DU/2024/1221",
            "wersja_tekstu: Dz.U. 2024 poz. 1221 (tekst pierwotny; zmiany do 2026-10-08 nie dotyczą art. 398–400)",
            "jezyk_tekstu: pl",
            f"sha256_tekstu: {sha}",
            f"weryfikacja: zweryfikowane ({DATA_IMPORTU}, api.sejm.gov.pl ELI text.html)",
            "---",
            "",
            f"# Art. {num} Prawa komunikacji elektronicznej",
            "",
            f"*{PKE_TEMAT[num]}*",
            "",
            "<!-- tekst urzędowy: początek -->",
            body,
            "<!-- tekst urzędowy: koniec -->",
            "",
        ]
        zapisz(out, f"art-{num}.md", linie)
        pliki.append((num, f"art-{num}.md"))
    return pliki


if __name__ == "__main__":
    a = kp()
    b = pke()
    print("KP:", [n for _, n in a])
    print("PKE:", [n for _, n in b])
