#!/usr/bin/env python3
"""Generuje sygnalizacyjne noty wyroków TSUE dotyczących RODO oraz rejestr zbiorczy.

Dane wejściowe (narzedzia/dane/):
- tsue_wszystkie.py  – WYROKI (celex, sygnatura, nazwa, data, skład, ECLI, artykuły, teza)
                       i POMINIETE (wyroki z listy EUR-Lex bez wykładni RODO co do istoty);
- tsue_metadane.json – dla każdego CELEX: sygnatura, ECLI, data, skład, SHA-256 sentencji
                       i jej długość, odczytane z EUR-Lex (strona PL dokumentu);
- tsue_zawisle.json  – sprawy zawisłe (opcjonalnie).

Noty NIE zawierają tekstu sentencji – tylko tezę (streszczenie własne), metadane i link.
Wyroki opracowane wcześniej z pełną sentencją (buduj_tsue.py) nie są nadpisywane.

Użycie: python3 narzedzia/buduj_tsue_rodo.py
"""
import importlib.util
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DANE = os.path.join(ROOT, "narzedzia", "dane")
OUT = os.path.join(ROOT, "zrodla", "orzecznictwo", "tsue")
DZIS = "2026-10-15"
WERYF = (f"sygnatura, data, skład, ECLI i sentencja sprawdzone w EUR-Lex ({DZIS}); "
         "teza – streszczenie własne sentencji; tekst sentencji nie jest kopiowany (suma SHA-256 w nagłówku)")
MIESIACE = ("stycznia lutego marca kwietnia maja czerwca lipca sierpnia "
            "września października listopada grudnia").split()


def wczytaj_wyroki():
    spec = importlib.util.spec_from_file_location("tsue_wszystkie", os.path.join(DANE, "tsue_wszystkie.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.WYROKI, mod.POMINIETE


def iso(data_pl):
    d, m, r = data_pl.split()
    return f"{r}-{MIESIACE.index(m) + 1:02d}-{int(d):02d}"


def slug(syg):
    return re.sub(r"-+", "-", syg.lower().replace(", ", "-").replace("/", "-").replace(" ", "-"))


def naglowek(sciezka):
    tekst = open(sciezka, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", tekst, re.S)
    pola = {}
    for linia in m.group(1).splitlines():
        if ":" in linia and not linia.startswith(" "):
            k, v = linia.split(":", 1)
            pola[k.strip()] = v.strip()
    return pola


def main():
    wyroki, pominiete = wczytaj_wyroki()
    meta = {x[0]: x for x in json.load(open(os.path.join(DANE, "tsue_metadane.json"), encoding="utf-8"))}
    sciezka_zaw = os.path.join(DANE, "tsue_zawisle.json")
    zawisle = json.load(open(sciezka_zaw, encoding="utf-8")) if os.path.exists(sciezka_zaw) else []

    istniejace = {}
    for plik in os.listdir(OUT):
        if plik.endswith(".md") and plik not in ("rejestr.md", "rejestr-rodo.md"):
            p = naglowek(os.path.join(OUT, plik))
            istniejace[p.get("celex")] = (plik, p)

    wiersze = []
    for celex, syg, nazwa, data, izba, ecli, arts, teza in wyroki:
        m = meta[celex]
        # kontrola zgodności z EUR-Lex
        assert m[2] == ecli, (celex, m[2], ecli)
        assert iso(m[3]) == data, (celex, m[3], data)
        assert m[6] > 0, celex
        if celex in istniejace and istniejace[celex][1].get("weryfikacja", "").startswith("zweryfikowane"):
            raise SystemExit(f"{celex} ma już pełną notę – usuń z WYROKI")
        s = slug(syg)
        jezyk = "fr" if "FR" in m[4] else "pl"
        uwaga_jez = ("\n\n**Uwaga:** brak polskiej wersji wyroku w EUR-Lex – teza na podstawie wersji francuskiej."
                     if jezyk == "fr" else "")
        tekst = f"""---
id: tsue-{s}
typ: wyrok
tytul: {nazwa}
sygnatura: {syg}
organ: TSUE ({izba})
data: {data}
ecli: {ecli}
celex: {celex}
status: prawomocny
podstawa: RODO
artykuly_rodo: [{", ".join(arts)}]
zrodlo: https://eur-lex.europa.eu/legal-content/PL/TXT/?uri=CELEX:{celex}
jezyk_tekstu: {jezyk}
sha256_sentencji: {m[5]}
weryfikacja: {WERYF}
---

# {syg} {nazwa} ({data})

**{ecli}** · TSUE, {izba}

## Teza (streszczenie sentencji – sygnalizacyjnie)

{teza}{uwaga_jez}

## Tekst

Sentencja i uzasadnienie: [EUR-Lex – CELEX {celex}](https://eur-lex.europa.eu/legal-content/PL/TXT/?uri=CELEX:{celex}). Przed powołaniem się na wyrok przeczytaj sentencję i odpowiednie punkty uzasadnienia.
"""
        with open(os.path.join(OUT, s + ".md"), "w", encoding="utf-8") as f:
            f.write(tekst)
        wiersze.append((data, f"| {data} | [{syg}]({s}.md) | {nazwa} | {', '.join(arts)} |"))

    # wyroki z pełną notą (buduj_tsue.py) – tylko te na gruncie RODO
    for celex, (plik, p) in istniejace.items():
        if "RODO" not in p.get("podstawa", ""):
            continue
        arts = p.get("artykuly_rodo", "").strip("[]")
        wiersze.append((p["data"], f"| {p['data']} | [{p['sygnatura']}]({plik}) ★ | {p['tytul']} | {arts} |"))

    wiersze.sort()
    pom = "\n".join(f"- {v}" for _, v in sorted(pominiete.items()))
    zaw = ""
    if zawisle:
        zaw = ("\n## Sprawy zawisłe (pytania prejudycjalne bez wyroku)\n\n"
               "Stan wg EUR-Lex na " + DZIS + ". Sygnał, że kwestia może zostać rozstrzygnięta – sprawdź stan sprawy "
               "w CURIA przed udzieleniem odpowiedzi.\n\n"
               "| Sprawa | Wpływ | Sąd odsyłający / przedmiot | Link |\n|---|---|---|---|\n"
               + "\n".join(f"| {z[1]} | {z[2]} | {z[3]} | https://eur-lex.europa.eu/legal-content/PL/TXT/?uri=CELEX:{z[0]} |"
                           for z in zawisle) + "\n")
    rejestr = f"""---
id: tsue-rejestr-rodo
typ: rejestr
tytul: Wyroki TSUE na gruncie RODO – rejestr zbiorczy
organ: TSUE
data: {DZIS}
status: obowiazuje
artykuly_rodo: []
zrodlo: https://eur-lex.europa.eu/legal-content/PL/ALL/?uri=CELEX:32016R0679
weryfikacja: {WERYF}
---

# Wyroki TSUE na gruncie RODO

Lista wyroków, w których Trybunał dokonał wykładni RODO (EUR-Lex: „Interpreted by” dla CELEX 32016R0679 oraz pytania prejudycjalne z wydanym wyrokiem). Stan na {DZIS}: {len(wiersze)} wyroków.

- ★ – nota pełna (sentencja w brzmieniu urzędowym, punkty uzasadnienia): zob. [`rejestr.md`](rejestr.md).
- Pozostałe – nota sygnalizacyjna: teza (streszczenie własne sentencji), metadane, suma SHA-256 sentencji, link do EUR-Lex. **Przed powołaniem się na wyrok przeczytaj sentencję i uzasadnienie.**
- Wyroki wiodące sprzed RODO (dyrektywa 95/46) – tylko w [`rejestr.md`](rejestr.md).

| Data | Sygnatura | Nazwa | Artykuły RODO |
|---|---|---|---|
""" + "\n".join(w for _, w in wiersze) + f"""

## Pominięte (na liście EUR-Lex, ale bez wykładni RODO co do istoty)

{pom}
{zaw}"""
    with open(os.path.join(OUT, "rejestr-rodo.md"), "w", encoding="utf-8") as f:
        f.write(rejestr)
    print(f"noty: {len(wyroki)}, rejestr: {len(wiersze)}, pominięte: {len(pominiete)}, zawisłe: {len(zawisle)}")


if __name__ == "__main__":
    main()
