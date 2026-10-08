#!/usr/bin/env python3
"""Buduje indeksy/artykuly.md z nagłówków plików w zrodla/ i indeksy/.

Dla każdego pliku z polem `artykuly_rodo` zbiera numery artykułów (część przed
pierwszym nawiasem) i grupuje dokumenty według artykułu. Pliki typu `rejestr`
i `artykul` są pomijane – rejestry mają osobne tabele, a artykuły RODO same są
celem indeksu.

Uruchomienie z katalogu głównego repo:  python3 narzedzia/buduj_indeks.py
"""
import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKAN = ["zrodla", "indeksy"]
CEL = os.path.join(ROOT, "indeksy", "artykuly.md")
POMIN_TYPY = {"rejestr", "artykul", "motyw"}

KOLEJNOSC = ["indeks", "akt-wykonawczy", "ustawa", "wyrok", "decyzja", "wytyczne", "projekt"]
ETYKIETY = {
    "indeks": "Tezy",
    "akt-wykonawczy": "Akty wykonawcze",
    "ustawa": "Prawo polskie",
    "wyrok": "Orzecznictwo",
    "decyzja": "Decyzje organów",
    "wytyczne": "Wytyczne",
    "projekt": "Zmiany w przygotowaniu",
}


def naglowek(sciezka):
    with open(sciezka, encoding="utf-8") as f:
        tekst = f.read()
    m = re.match(r"^---\n(.*?)\n---\n", tekst, re.S)
    if not m:
        return None
    pola = {}
    for linia in m.group(1).splitlines():
        if ":" in linia and not linia.startswith(" "):
            k, v = linia.split(":", 1)
            pola[k.strip()] = v.split("#")[0].strip()
    return pola


def artykuly(wartosc):
    wartosc = wartosc.strip().strip("[]")
    wynik = set()
    for el in wartosc.split(","):
        el = el.strip()
        m = re.match(r"(\d+)", el)
        if m:
            wynik.add(int(m.group(1)))
    return wynik


def main():
    indeks = defaultdict(list)
    for katalog in SKAN:
        for sciezka_kat, _, pliki in os.walk(os.path.join(ROOT, katalog)):
            for plik in sorted(pliki):
                if not plik.endswith(".md"):
                    continue
                pelna = os.path.join(sciezka_kat, plik)
                if os.path.abspath(pelna) == os.path.abspath(CEL):
                    continue
                pola = naglowek(pelna)
                if not pola or pola.get("typ") in POMIN_TYPY or "artykuly_rodo" not in pola:
                    continue
                wzgl = os.path.relpath(pelna, os.path.dirname(CEL))
                opis = " ".join(x for x in [pola.get("sygnatura", ""), pola.get("tytul", "")] if x and x != "–")
                for art in artykuly(pola["artykuly_rodo"]):
                    indeks[art].append((pola.get("typ", ""), pola.get("data", ""), opis, wzgl, pola.get("organ", "")))

    linie = [
        "---",
        "id: indeks-artykuly",
        "typ: rejestr",
        "tytul: Indeks – artykuł RODO → źródła",
        "organ: –",
        "status: obowiazuje",
        "artykuly_rodo: []",
        "zrodlo: generowany przez narzedzia/buduj_indeks.py",
        "weryfikacja: generowany automatycznie",
        "---",
        "",
        "# Indeks: artykuł RODO → źródła",
        "",
        "Plik generowany – nie edytować ręcznie. Po dodaniu dokumentu uruchom `python3 narzedzia/buduj_indeks.py`.",
        "Akty wykonawcze: `zrodla/ue/akty-wykonawcze/rejestr.md`. Wytyczne: `zrodla/wytyczne/rejestr.md`.",
        "",
    ]
    for art in sorted(indeks):
        linie.append(f"## Art. {art}")
        linie.append("")
        wpisy = sorted(indeks[art], key=lambda w: (KOLEJNOSC.index(w[0]) if w[0] in KOLEJNOSC else 99, w[1]))
        for typ, data, opis, wzgl, organ in wpisy:
            etykieta = ETYKIETY.get(typ, typ)
            linie.append(f"- {etykieta}: [{opis}]({wzgl}) – {organ}, {data}")
        linie.append("")
    with open(CEL, "w", encoding="utf-8") as f:
        f.write("\n".join(linie))
    print(f"Artykułów w indeksie: {len(indeks)}")


if __name__ == "__main__":
    main()
