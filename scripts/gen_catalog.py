"""Generate docs/CATALOG.md from the @algo registry.

    python scripts/gen_catalog.py            # перезаписать docs/CATALOG.md
    python scripts/gen_catalog.py --check    # код возврата 1, если файл устарел

Каталог - производный артефакт: руками не правится, тест test_ac_11 сверяет его с выводом.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rustinpy import __version__
from rustinpy._registry import AlgoInfo, all_algos, load_all

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "docs" / "CATALOG.md"


def _cell(text: str) -> str:
    # вертикальная черта ломает таблицу Markdown
    return text.replace("|", "\\|").strip()


def _status(a: AlgoInfo) -> str:
    if a.stub:
        return "stub"
    return "NV" if not a.verified else ""


def _problems(a: AlgoInfo) -> str:
    parts = [f"CSES: {p}" for p in a.cses if p and not p.startswith("-")]
    parts += [f"ICPC-UZ {p}" for p in a.icpc]
    return "; ".join(parts)


def render() -> str:
    """Return the full text of docs/CATALOG.md."""
    load_all()
    algos = all_algos()
    modules: dict[str, list[AlgoInfo]] = {}
    for a in algos:
        modules.setdefault(a.module, []).append(a)
    nv = sum(1 for a in algos if not a.verified and not a.stub)
    stubs = sum(1 for a in algos if a.stub)
    out = [
        "# Каталог алгоритмов rustinpy",
        "",
        f"Версия {__version__}: {len(algos)} алгоритмов в {len(modules)} модулях, "
        f"из них NOT VERIFIED - {nv}, заглушек - {stubs}.",
        "Файл генерируется командой `python scripts/gen_catalog.py`, руками не правится.",
        "",
        "Статус: пусто - проверено тестами против эталона; `NV` - код проверен тестами, но условие",
        "задачи не сверено (см. docs/PROGRESS.md); `stub` - заглушка с идеей решения.",
        "",
        "| Модуль | Алгоритмов | NV | stub |",
        "|---|---:|---:|---:|",
    ]
    for mod, items in modules.items():
        m_nv = sum(1 for a in items if not a.verified and not a.stub)
        m_stub = sum(1 for a in items if a.stub)
        out.append(f"| [`{mod}`](#{mod}) | {len(items)} | {m_nv} | {m_stub} |")
    for mod, items in modules.items():
        out += [
            "",
            f"## {mod}",
            "",
            "| Имя | Что делает | Сложность | Задачи | Теги | Статус |",
            "|---|---|---|---|---|---|",
        ]
        for a in items:
            desc = a.summary if not a.hint else f"{a.summary} ({a.hint})"
            out.append(
                f"| `{a.name}` | {_cell(desc)} | {_cell(a.complexity)} | {_cell(_problems(a))} "
                f"| {_cell(', '.join(a.tags))} | {_status(a)} |"
            )
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Generate docs/CATALOG.md")
    p.add_argument("--check", action="store_true", help="only compare, do not write")
    args = p.parse_args(argv)
    text = render()
    if args.check:
        current = CATALOG.read_text(encoding="utf-8") if CATALOG.exists() else ""
        if current != text:
            print("docs/CATALOG.md is out of date: run python scripts/gen_catalog.py")
            return 1
        print("docs/CATALOG.md is up to date")
        return 0
    with open(CATALOG, "w", encoding="utf-8", newline="\n") as f:  # LF и на Windows
        f.write(text)
    print(f"written {CATALOG.relative_to(ROOT)}: {text.count(chr(10))} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
