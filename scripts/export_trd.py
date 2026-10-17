"""Collect algorithms into one file for a team reference document (TRD).

    python scripts/export_trd.py --out trd.txt                    # все модули
    python scripts/export_trd.py --modules graph,tree --out trd.md --docstrings none
    python scripts/export_trd.py --names dijkstra,LCA,Dinic --out trd.txt

Тонкая обёртка над rustinpy.export (то же, что `rustinpy export`), плюс оценка объёма:
правила ICPC - до 25 страниц A4, печать с одной стороны.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rustinpy._api import export
from rustinpy._registry import available_modules

LINES_PER_PAGE = 2 * 90  # грубо: две колонки по ~90 строк моноширинного 7-8 pt на A4


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Export rustinpy algorithms for a TRD")
    p.add_argument("--modules", help="comma separated; default: all modules")
    p.add_argument("--names", help="comma separated algorithm names")
    p.add_argument("--out", "-o", required=True, help="output file, .txt or .md")
    p.add_argument("--docstrings", choices=["full", "short", "none"], default="short")
    args = p.parse_args(argv)
    names = [x.strip() for x in (args.names or "").split(",") if x.strip()]
    modules = [x.strip() for x in (args.modules or "").split(",") if x.strip()]
    if not names and not modules:
        modules = available_modules()
    out = Path(args.out)
    fmt = "md" if out.suffix.lower() == ".md" else "txt"
    text = export(names, modules=modules, docstrings=args.docstrings, fmt=fmt)
    with open(out, "w", encoding="utf-8", newline="\n") as f:  # LF и на Windows
        f.write(text)
    lines = text.count("\n")
    pages = -(-lines // LINES_PER_PAGE)
    print(f"written {out}: {lines} lines, ~{pages} A4 pages in two columns (limit 25)")
    if pages > 25:
        hint = "" if args.docstrings == "none" else " or use --docstrings none"
        print(f"too long for a TRD: pick fewer modules / names{hint}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
