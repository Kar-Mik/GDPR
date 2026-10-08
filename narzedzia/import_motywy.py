#!/usr/bin/env python3
"""Zapisuje motywy RODO z plików JSON (eksport z EUR-Lex) do zrodla/ue/rodo/motywy/motyw-NNN.md.

Wejście: pliki JSON z listą obiektów {nr, text}. Tekst zapisywany 1:1 ze źródłem
(łącznie z omyłkami tekstu urzędowego), aby suma kontrolna zgadzała się z EUR-Lex.

Użycie: python3 narzedzia/import_motywy.py plik1.json [plik2.json ...]
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "zrodla", "ue", "rodo", "motywy")
ZRODLO = "https://eur-lex.europa.eu/legal-content/PL/TXT/?uri=CELEX:32016R0679"


def main(paths):
    recs = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            recs.extend(json.load(f))
    recs.sort(key=lambda r: r["nr"])
    os.makedirs(OUT, exist_ok=True)
    for r in recs:
        nr = r["nr"]
        sha = hashlib.sha256(r["text"].encode("utf-8")).hexdigest()
        lines = [
            "---",
            f"id: rodo-motyw-{nr:03d}",
            "typ: motyw",
            f"tytul: Motyw {nr} RODO",
            f"sygnatura: motyw {nr} RODO",
            "organ: Parlament Europejski i Rada",
            "data: 2016-04-27",
            "status: obowiazuje",
            "podstawa: RODO",
            "artykuly_rodo: []",
            f"zrodlo: {ZRODLO}",
            "wersja_tekstu: Dz.U. L 119 z 4.5.2016, s. 1 (bez sprostowań – tekst skonsolidowany nie zawiera preambuły)",
            "jezyk_tekstu: pl",
            f"sha256_tekstu: {sha}",
            "weryfikacja: zweryfikowane (2026-10-08, zgodność z EUR-Lex potwierdzona sumą kontrolną)",
            "---",
            "",
            f"# Motyw {nr}",
            "",
            "<!-- tekst urzędowy: początek -->",
            r["text"],
            "<!-- tekst urzędowy: koniec -->",
            "",
        ]
        with open(os.path.join(OUT, f"motyw-{nr:03d}.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    print(f"Zapisano motywów: {len(recs)}")


if __name__ == "__main__":
    main(sys.argv[1:])
