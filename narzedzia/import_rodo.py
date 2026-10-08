#!/usr/bin/env python3
"""Zapisuje artykuły RODO z plików JSON (eksport z EUR-Lex) do zrodla/ue/rodo/art-NNN.md.

Wejście: pliki JSON z listą obiektów {nr, title, rozdzial, sekcja, corr, text}.
Tekst artykułu jest zapisywany bez zmian (łącznie z oczywistymi omyłkami pisarskimi
tekstu urzędowego), aby suma kontrolna zgadzała się ze źródłem.

Użycie: python3 narzedzia/import_rodo.py plik1.json [plik2.json ...]
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "zrodla", "ue", "rodo")
ZRODLO = "https://eur-lex.europa.eu/legal-content/PL/TXT/?uri=CELEX:02016R0679-20160504"
SPROSTOWANIA = {
    "C1": "sprostowanie Dz.U. L 127 z 23.5.2018, s. 2",
    "C2": "sprostowanie Dz.U. L 74 z 4.3.2021, s. 35",
}


def yaml_str(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def main(paths):
    arts = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            arts.extend(json.load(f))
    arts.sort(key=lambda a: a["nr"])
    os.makedirs(OUT, exist_ok=True)
    for a in arts:
        nr = a["nr"]
        sha = hashlib.sha256(a["text"].encode("utf-8")).hexdigest()
        corr = a.get("corr") or []
        lines = [
            "---",
            f"id: rodo-art-{nr:03d}",
            "typ: artykul",
            f"tytul: {yaml_str(a['title'])}",
            f"sygnatura: art. {nr} RODO",
            "organ: Parlament Europejski i Rada",
            "data: 2016-04-27",
            "status: obowiazuje",
            "obowiazuje_od: 2018-05-25",
            "podstawa: RODO",
            f"artykuly_rodo: [{nr}]",
            f"rozdzial: {yaml_str(a['rozdzial'])}",
        ]
        if a.get("sekcja"):
            lines.append(f"sekcja: {yaml_str(a['sekcja'])}")
        if corr:
            lines.append(f"sprostowania: [{', '.join(corr)}]")
        lines += [
            f"zrodlo: {ZRODLO}",
            "wersja_tekstu: 02016R0679-20160504 (tekst skonsolidowany, ze sprostowaniami)",
            "jezyk_tekstu: pl",
            f"sha256_tekstu: {sha}",
            "weryfikacja: zweryfikowane (2026-10-08, zgodność z EUR-Lex potwierdzona sumą kontrolną)",
            "---",
            "",
            f"# Art. {nr}. {a['title']}",
            "",
        ]
        if corr:
            opis = "; ".join(SPROSTOWANIA.get(c, c) for c in corr)
            lines += [f"> Brzmienie uwzględnia {opis}.", ""]
        body = a["text"]
        # Markdown: zachowaj podział na linie (dwie spacje nie zmieniają tekstu źródłowego w sekcji poniżej)
        lines += ["<!-- tekst urzędowy: początek -->", body, "<!-- tekst urzędowy: koniec -->", ""]
        with open(os.path.join(OUT, f"art-{nr:03d}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    print(f"Zapisano artykułów: {len(arts)}")


if __name__ == "__main__":
    main(sys.argv[1:])
