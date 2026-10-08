#!/usr/bin/env python3
"""Zapisuje metadane decyzji Prezesa UODO do zrodla/decyzje-organow/pl-uodo/.

Wejście: narzedzia/dane/uodo_decyzje.json – lista rekordów pobranych z portalu
orzeczenia.uodo.gov.pl (stan 2026-10-08), zweryfikowanych sumą SHA-256 przy przenoszeniu z przeglądarki.
Rekord: [sygnatura, urn, data_ogloszenia, data_publikacji, status, zdarzenia, opis,
         etykiety_taksonomii, kary, artykuly_rodo, flagi]
  zdarzenia: T=trial, D=defended, R=repealed, V=validation (kody portalu) + data, rozdzielone ';'
  kary:      kwoty z sentencji (ekstrakcja automatyczna), rozdzielone ';'
  artykuly:  numery artykułów RODO wskazane w rozstrzygnięciu (ekstrakcja automatyczna)
  flagi:     o = podstawą ustawa z 29.08.1997 r.; p = ustawa z 14.12.2018 r. (przetwarzanie w związku
             ze zwalczaniem przestępczości)

Użycie: python3 narzedzia/import_uodo.py
"""
import json
import os
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DANE = os.path.join(ROOT, "narzedzia", "dane", "uodo_decyzje.json")
SENTENCJE = os.path.join(os.path.dirname(DANE), "uodo_sentencje.json")
SADY = os.path.join(os.path.dirname(DANE), "uodo_sady.json")
SADY_REJESTR = os.path.join(ROOT, "zrodla", "orzecznictwo", "nsa-wsa", "rejestr-uodo.md")
WYDZIAL = {"ii_sa-wa": ("II SA/Wa", "WSA w Warszawie"), "ii_sab-wa": ("II SAB/Wa", "WSA w Warszawie"),
           "iii_osk": ("III OSK", "NSA"), "i_osk": ("I OSK", "NSA"), "i_oz": ("I OZ", "NSA"), "iii_oz": ("III OZ", "NSA")}
SKUTEK = {"defended": "decyzja obroniona", "repealed": "uchylenie przez sąd", "trial": "sprawa w sądzie",
          "validation": "uprawomocnienie"}


def sygnatura_sadu(kod):
    """'2025:ii_sa-wa_124' -> ('II SA/Wa 124/25', 'WSA w Warszawie')"""
    rok, reszta = kod.split(":")
    wydz, nr = reszta.rsplit("_", 1)
    pref, sad = WYDZIAL[wydz]
    return f"{pref} {nr}/{rok[2:]}", sad
OUT = os.path.join(ROOT, "zrodla", "decyzje-organow", "pl-uodo")
PORTAL = "https://orzeczenia.uodo.gov.pl/document/urn:ndoc:gov:pl:uodo:{}/content"
DATA_POBRANIA = "2026-10-08"

ROZSTRZYGNIECIE = {
    "1.10.100": "nakaz", "1.10.101": "odmowa", "1.10.102": "umorzenie", "1.10.103": "upomnienie",
    "1.10.104": "nałożenie kary", "1.10.105": "uchylenie", "1.10.106": "utrzymanie w mocy",
}
OBSZAR = {
    "1.20.100": "Marketing", "1.20.101": "Monitoring", "1.20.102": "BIP", "1.20.103": "Mieszkalnictwo",
    "1.20.104": "DODO", "1.20.106": "Zdrowie", "1.20.107": "Szkolnictwo", "1.20.108": "Finanse",
    "1.20.109": "Telekomunikacja", "1.20.110": "Ubezpieczenia", "1.20.111": "Pozostałe",
}
STATUS = {"final": "prawomocny", "nonfinal": "nieprawomocny", "repealed": "uchylony",
          "partly-final": "czesciowo-prawomocny"}
ZDARZENIE = {
    "T": ("trial", "sprawa w sądzie administracyjnym"),
    "D": ("defended", "decyzja obroniona w sądzie"),
    "R": ("repealed", "uchylenie przez sąd"),
    "V": ("validation", "uprawomocnienie"),
}


def podstawa(flagi):
    if "o" in flagi and "p" in flagi:
        return "ustawa z 29.08.1997 r. o ochronie danych osobowych (przepisy utrzymane art. 175 u.o.d.o.) / ustawa z 14.12.2018 r."
    if "o" in flagi:
        return "ustawa z 29.08.1997 r. o ochronie danych osobowych (sprawa wszczęta przed 25.05.2018)"
    if "p" in flagi:
        return "ustawa z 14.12.2018 r. o ochronie danych osobowych przetwarzanych w związku z zapobieganiem i zwalczaniem przestępczości"
    return "RODO"


def yq(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    with open(DANE, encoding="utf-8") as f:
        recs = json.load(f)
    with open(SENTENCJE, encoding="utf-8") as f:
        sentencje = json.load(f)
    with open(SADY, encoding="utf-8") as f:
        sady = defaultdict(list)
        for syg_d, uzycie, data_z, kod in json.load(f):
            sady[syg_d].append((data_z.strip(), uzycie, *sygnatura_sadu(kod)))
    plik_decyzji = {}
    lata = Counter()
    rejestr = defaultdict(list)
    for (syg, urn, d_ogl, d_pub, status, zdarz, opis, etyk, kary, arts, flagi) in recs:
        rok_urn, nazwa = urn.split(":")
        rok = d_ogl[:4]
        lata[rok] += 1
        katalog = os.path.join(OUT, rok)
        os.makedirs(katalog, exist_ok=True)
        plik = f"{nazwa}-{rok_urn}.md"
        etykiety = [e for e in etyk.split(",") if e]
        rozs = [ROZSTRZYGNIECIE[e] for e in etykiety if e in ROZSTRZYGNIECIE]
        obsz = [OBSZAR[e] for e in etykiety if e in OBSZAR]
        kary_l = [k.strip() for k in kary.split(";") if k.strip()]
        arts_l = [a for a in arts.split(",") if a]
        pods = podstawa(flagi)
        rodo = pods == "RODO"
        zdarzenia = []
        for z in [z.strip() for z in zdarz.split(";") if z.strip()]:
            kod, data = z[0], z[1:].strip()
            zdarzenia.append((data, ZDARZENIE[kod][0], ZDARZENIE[kod][1]))
        tytul = ", ".join(rozs) if rozs else "decyzja"
        if kary_l:
            tytul += " (" + " + ".join(kary_l) + ")"
        if rodo and arts_l:
            tytul += " – art. " + ", ".join(arts_l) + " RODO"
        elif not rodo:
            tytul += " – " + ("ustawa z 1997 r." if "o" in flagi else "ustawa z 2018 r. (przestępczość)")
        link = PORTAL.format(urn)
        lines = [
            "---",
            f"id: uodo-{rok_urn}-{nazwa}",
            "typ: decyzja",
            f"tytul: {yq(tytul)}",
            f"sygnatura: {yq(syg)}",
            "organ: Prezes UODO",
            f"data: {d_ogl}",
            f"data_publikacji: {d_pub}",
            f"status: {STATUS[status]}",
            f"podstawa: {yq(pods)}",
            f"artykuly_rodo: [{', '.join(arts_l) if rodo else ''}]",
            f"rozstrzygniecie: [{', '.join(rozs)}]",
            f"obszar: [{', '.join(obsz)}]",
        ]
        if kary_l:
            lines.append(f"kara: {yq('; '.join(kary_l))}")
        lines += [
            f"zrodlo: {link}",
            "jezyk_tekstu: pl",
            f"weryfikacja: {yq(f'metadane z portalu orzeczenia.uodo.gov.pl ({DATA_POBRANIA}); kwoty kar i artykuły RODO wyodrębnione automatycznie z sentencji – niezweryfikowane z pełnym tekstem')}",
            "---",
            "",
            f"# Decyzja Prezesa UODO {syg}",
            "",
            "| | |",
            "|---|---|",
            f"| Data wydania (ogłoszenia) | {d_ogl} |",
            f"| Publikacja na portalu | {d_pub} |",
            f"| Status (portal) | {STATUS[status]} |",
            f"| Rozstrzygnięcie | {', '.join(rozs) or '–'} |",
            f"| Kara | {'; '.join(kary_l) or '–'} |",
            f"| Podstawa | {pods} |",
            f"| Artykuły RODO w rozstrzygnięciu | {', '.join(arts_l) if (rodo and arts_l) else '–'} |",
            f"| Obszar (portal) | {', '.join(obsz) or '–'} |",
            "",
            "## Opis (portal UODO)",
            "",
            f"> {opis}",
            "",
        ]
        if zdarzenia:
            lines += ["## Losy decyzji (portal UODO)", ""]
            for data, kod, opis_z in zdarzenia:
                lines.append(f"- {data} – {opis_z} (`{kod}`)")
            lines.append("")
        if sady.get(syg):
            lines += ["## Sądy administracyjne (portal UODO)", ""]
            for data_z, uzycie, syg_s, sad in sorted(sady[syg]):
                lines.append(f"- {sad}, {syg_s} – {SKUTEK[uzycie]} ({data_z}); tekst: CBOSA https://orzeczenia.nsa.gov.pl (wyszukaj sygnaturę)")
            lines.append("")
        plik_decyzji[syg] = f"{rok}/{plik}"
        if syg in sentencje:
            lines += [
                "## Sentencja (skrót – sygnalizacyjnie)",
                "",
                "*Fragment rozstrzygnięcia: tytuł rozporządzenia skrócony do „rozporządzenia 2016/679”, "
                "zapis „(słownie: …)” usunięty, tekst ucięty do ok. 700 znaków ([…]). "
                "Do opinii – pełny tekst pod linkiem.*",
                "",
            ]
            lines += ["> " + l if l else ">" for l in sentencje[syg].split("\n")]
            lines.append("")
        lines += [
            "## Pełny tekst",
            "",
            f"Nie zaimportowano. Tekst decyzji: {link}",
            "",
        ]
        with open(os.path.join(katalog, plik), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        rejestr[rok].append((d_ogl, syg, f"{rok}/{plik}", ", ".join(rozs) or "–", "; ".join(kary_l) or "",
                             ", ".join(arts_l) if (rodo and arts_l) else ("1997" if "o" in flagi else ("2018-P" if "p" in flagi else "")),
                             STATUS[status]))

    # rejestr
    n_kar = sum(1 for r in recs if r[8])
    w = [
        "---",
        "id: pl-uodo-rejestr",
        "typ: rejestr",
        "tytul: Decyzje Prezesa UODO – rejestr",
        "organ: Prezes UODO",
        f"data: {DATA_POBRANIA}",
        "status: obowiazuje",
        "artykuly_rodo: []",
        "zrodlo: https://orzeczenia.uodo.gov.pl",
        f"weryfikacja: metadane z portalu ({DATA_POBRANIA}), przeniesienie zweryfikowane sumą kontrolną",
        "---",
        "",
        "# Decyzje Prezesa UODO – rejestr",
        "",
        f"Stan portalu orzeczenia.uodo.gov.pl na {DATA_POBRANIA}: **{len(recs)} decyzji** "
        f"({', '.join(f'{k}: {v}' for k, v in sorted(lata.items()))}), w tym {n_kar} z kwotą kary w sentencji.",
        "",
        "Kolumna „Art.” – artykuły RODO wskazane w rozstrzygnięciu (ekstrakcja automatyczna); "
        "„1997” – decyzja na podstawie ustawy z 1997 r.; „2018-P” – ustawa z 14.12.2018 r. (przestępczość).",
        "",
    ]
    for rok in sorted(rejestr, reverse=True):
        w += [f"## {rok}", "", "| Data | Sygnatura | Rozstrzygnięcie | Kara | Art. | Status |", "|---|---|---|---|---|---|"]
        for d, syg, p, rz, k, a, st in sorted(rejestr[rok], reverse=True):
            w.append(f"| {d} | [{syg}]({p}) | {rz} | {k} | {a} | {st} |")
        w.append("")
    with open(os.path.join(OUT, "rejestr.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(w))
    # rejestr wyroków sądów administracyjnych
    wiersze = []
    for syg_d, lst in sady.items():
        for data_z, uzycie, syg_s, sad in lst:
            wiersze.append((data_z, syg_s, sad, SKUTEK[uzycie], syg_d))
    w2 = [
        "---",
        "id: nsa-wsa-rejestr-uodo",
        "typ: rejestr",
        "tytul: Wyroki sądów administracyjnych w sprawach decyzji Prezesa UODO – rejestr",
        "organ: WSA w Warszawie / NSA",
        f"data: {DATA_POBRANIA}",
        "status: obowiazuje",
        "artykuly_rodo: []",
        "zrodlo: https://orzeczenia.uodo.gov.pl",
        f"weryfikacja: {yq(f'powiązania decyzja–sygnatura z portalu UODO ({DATA_POBRANIA}); treści wyroków nie importowano')}",
        "---",
        "",
        "# Sądy administracyjne – sprawy decyzji Prezesa UODO",
        "",
        f"Powiązania z portalu orzeczenia.uodo.gov.pl: **{len(wiersze)} zdarzeń**, {len({w[1] for w in wiersze})} sygnatur, {len(sady)} decyzji. "
        "Sygnatura odtworzona z identyfikatora portalu (np. `2025:ii_sa-wa_124` → II SA/Wa 124/25). "
        "Data – data zdarzenia w portalu (zwykle data orzeczenia). Skutek – kod portalu UODO (`defended`, `repealed`, `trial`, `validation`), "
        "a nie odczyt sentencji wyroku. Teksty wyroków: CBOSA https://orzeczenia.nsa.gov.pl – wyszukać sygnaturę.",
        "",
        "Sygnalizacyjnie: przy decyzji z wyrokiem skill podaje sygnaturę i skutek oraz odsyła do CBOSA. Tez wyroków nie ma w repozytorium.",
        "",
        "| Data | Sygnatura | Sąd | Skutek (portal) | Decyzja UODO |",
        "|---|---|---|---|---|",
    ]
    for data_z, syg_s, sad, sk, syg_d in sorted(wiersze, reverse=True):
        link = os.path.relpath(os.path.join(OUT, plik_decyzji[syg_d]), os.path.dirname(SADY_REJESTR)) if syg_d in plik_decyzji else ""
        w2.append(f"| {data_z} | {syg_s} | {sad} | {sk} | " + (f"[{syg_d}]({link})" if link else syg_d) + " |")
    with open(SADY_REJESTR, "w", encoding="utf-8") as f:
        f.write("\n".join(w2) + "\n")
    print(f"Zapisano decyzji: {len(recs)}")


if __name__ == "__main__":
    main()
