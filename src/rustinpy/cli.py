"""Command line interface: rustinpy list | show | search | export.

Консольная команда rustinpy.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rustinpy import __version__
from rustinpy._api import export, format_row, list_algos, search, show
from rustinpy._registry import AmbiguousName, UnknownName, available_modules


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="rustinpy", description="ICPC / CSES algorithms cheat sheet")
    p.add_argument("--version", action="version", version=f"rustinpy {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("list", help="list algorithms by module")
    pl.add_argument("--module", "-m")
    pl.add_argument("--tag", "-t")
    pl.add_argument("--unverified", action="store_true", help="only NOT VERIFIED / stubs")

    ps = sub.add_parser("show", help="print source code")
    ps.add_argument("name")
    ps.add_argument("--raw", action="store_true", help="keep @algo, no dependencies")

    pq = sub.add_parser("search", help="search by name, tags, problems and docstrings")
    pq.add_argument("query", nargs="+")
    pq.add_argument("--module", "-m")

    pe = sub.add_parser("export", help="collect algorithms into one file for a TRD")
    pe.add_argument("--modules", help="comma separated, e.g. graph,tree")
    pe.add_argument("--names", help="comma separated, e.g. dijkstra,LCA")
    pe.add_argument("--out", "-o", required=True, help="output file (.txt or .md)")
    pe.add_argument("--docstrings", choices=["full", "short", "none"], default="short")
    return p


def _split(s: str | None) -> list[str]:
    return [x.strip() for x in s.split(",") if x.strip()] if s else []


def main(argv: list[str] | None = None) -> int:
    """Entry point of the ``rustinpy`` command; returns the exit code."""
    # консоль Windows (cp1251/cp866) не должна падать на редких символах;
    # в файл или pipe пишем UTF-8, чтобы кириллица не портилась
    for stream in (sys.stdout, sys.stderr):
        reconf = getattr(stream, "reconfigure", None)
        if reconf is not None:
            tty = getattr(stream, "isatty", lambda: False)()
            reconf(errors="replace") if tty else reconf(encoding="utf-8", errors="replace")
    args = _build_parser().parse_args(argv)
    try:
        if args.cmd == "list":
            if args.module and args.module not in available_modules():
                print(
                    f"unknown module {args.module!r}; available: " + ", ".join(available_modules()),
                    file=sys.stderr,
                )
                return 1
            algos = list_algos(args.module, tag=args.tag)
            if args.unverified:
                algos = [a for a in algos if not a.verified or a.stub]
            current = None
            for a in algos:
                if a.module != current:
                    current = a.module
                    print(f"\n[{current}]")
                print("  " + format_row(a))
            print(f"\n{len(algos)} algorithms")
            return 0
        if args.cmd == "show":
            show(args.name, raw=args.raw)
            return 0
        if args.cmd == "search":
            found = search(" ".join(args.query), module=args.module)
            return 0 if found else 1
        if args.cmd == "export":
            fmt = "md" if args.out.lower().endswith(".md") else "txt"
            text = export(
                _split(args.names),
                modules=_split(args.modules),
                docstrings=args.docstrings,
                fmt=fmt,
            )
            Path(args.out).write_text(text, encoding="utf-8")
            print(f"written {args.out}: {text.count(chr(10))} lines")
            return 0
    except AmbiguousName as e:
        print(str(e), file=sys.stderr)
        return 2
    except (UnknownName, LookupError, ValueError) as e:
        print(str(e), file=sys.stderr)
        return 1
    return 1  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
