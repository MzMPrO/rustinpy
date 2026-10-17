"""User-facing helpers: show, search, list_algos, help, export.

Пользовательские функции: просмотр исходника, поиск, список, экспорт для TRD.
"""

from __future__ import annotations

import ast

from rustinpy._registry import (
    ALGO_MODULES,
    AlgoInfo,
    all_algos,
    resolve,
    source_of,
    source_parts,
)

__all__ = ["export", "help", "list_algos", "search", "show"]


def list_algos(module: str | None = None, *, tag: str | None = None) -> list[AlgoInfo]:
    """All registered algorithms, optionally filtered by module and tag."""
    out = all_algos()
    if module is not None:
        out = [a for a in out if a.module == module]
    if tag is not None:
        out = [a for a in out if tag in a.tags]
    return out


def show(name: str, *, raw: bool = False) -> None:
    """Print the self-contained source of an algorithm (raw=True: decorator kept, no deps)."""
    info = resolve(name)
    print(source_of(info, with_requires=not raw, strip_decorator=not raw), end="")


def _score(a: AlgoInfo, q: str) -> int:
    q = q.lower()
    score = 0
    if q == a.name.lower():
        score += 100
    if q in a.name.lower():
        score += 40
    if any(q in t.lower() for t in a.tags):
        score += 30
    if any(q in c.lower() for c in a.cses + a.icpc):
        score += 25
    if q in a.summary.lower() or q in a.hint.lower():
        score += 20
    if q in a.doc.lower():
        score += 5
    return score


def search(query: str, *, module: str | None = None, quiet: bool = False) -> list[AlgoInfo]:
    """Search by name, tags, problem names and docstrings; prints and returns the matches."""
    words = query.split()
    scored: list[tuple[int, AlgoInfo]] = []
    for a in list_algos(module):
        parts = [_score(a, w) for w in words] or [0]
        if all(p > 0 for p in parts):
            scored.append((sum(parts), a))
    scored.sort(key=lambda t: (-t[0], t[1].qualname))
    found = [a for _, a in scored]
    if not quiet:
        for a in found:
            print(format_row(a))
        if not found:
            print(f"nothing found for {query!r}")
    return found


def format_row(a: AlgoInfo) -> str:
    flags = ("" if a.verified else " [NOT VERIFIED]") + (" [stub]" if a.stub else "")
    cx = f"  [{a.complexity}]" if a.complexity else ""
    return f"{a.qualname:<40} {a.summary}{cx}{flags}"


def help(name: str | None = None) -> None:
    """Overview of modules, or the docstring of one algorithm."""
    if name is not None:
        info = resolve(name)
        print(f"{info.qualname}\n\n{info.doc}")
        return
    algos = all_algos()
    print("rustinpy - ICPC / CSES algorithms cheat sheet")
    print("usage: rustinpy.show(name), rustinpy.search(query), rustinpy.list_algos(module)\n")
    for m in ALGO_MODULES:
        n = sum(1 for a in algos if a.module == m)
        if n:
            print(f"  rustinpy.{m:<14} {n:>4} algorithms")


# ---------------------------------------------------------------- export for TRD


def _rewrite_docstrings(code: str, mode: str) -> str:
    """mode: full | short (first line + Complexity) | none."""
    if mode == "full":
        return code
    tree = ast.parse(code)
    lines = code.splitlines()
    repl: list[tuple[int, int, list[str]]] = []
    top = {id(n) for n in tree.body}
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        body = node.body
        if not (
            body
            and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)
        ):
            continue
        ds = body[0]
        start, end = ds.lineno, ds.end_lineno or ds.lineno
        indent = lines[start - 1][: len(lines[start - 1]) - len(lines[start - 1].lstrip())]
        text = str(ds.value.value).strip() if isinstance(ds.value, ast.Constant) else ""
        new: list[str] = []
        if mode == "short" and id(node) in top:
            first = text.splitlines()[0] if text else ""
            cx = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("Complexity:")]
            new = [f'{indent}"""{first}']
            if cx:
                new.append(f"{indent}{cx[0]}")
            new[-1] += '"""'
        elif len(body) == 1:
            new = [f"{indent}..."]  # тело только из докстринга
        repl.append((start, end, new))
    for start, end, new in sorted(repl, reverse=True):
        lines[start - 1 : end] = new
    return "\n".join(lines)


def export(
    names: list[str] | None = None,
    *,
    modules: list[str] | None = None,
    docstrings: str = "short",
    fmt: str = "txt",
) -> str:
    """Collect algorithms into one TRD-ready text (txt or md) with a table of contents."""
    if docstrings not in ("full", "short", "none"):
        raise ValueError("docstrings must be full, short or none")
    picked: list[AlgoInfo] = []
    if modules:
        for m in modules:
            got = list_algos(m)
            if not got:
                raise LookupError(f"unknown or empty module {m!r}")
            picked.extend(got)
    for n in names or []:
        picked.append(resolve(n))
    picked = list({a.qualname: a for a in picked}.values())
    if not picked:
        raise ValueError("nothing to export: give modules or names")

    blocks: list[tuple[str, str]] = []
    all_imports: list[str] = []
    for a in picked:
        imports, code = source_parts(a)
        all_imports.extend(imports)
        blocks.append((a.qualname, _rewrite_docstrings(code, docstrings)))
    imports = sorted(set(all_imports), key=lambda s: (s.startswith("from"), s))

    md = fmt == "md"
    header = ["from __future__ import annotations", *imports]
    body: list[str] = []
    starts: list[int] = []  # смещение начала блока внутри body
    for qual, code in blocks:
        starts.append(len(body))
        if md:
            body += [f"## {qual}", "", "```python", *code.splitlines(), "```", ""]
        else:
            body += [f"# ==== {qual} ====", *code.splitlines(), "", ""]

    out: list[str] = []
    if md:
        out += ["# rustinpy TRD export", ""]
        out += [f"{i}. {qual}" for i, (qual, _) in enumerate(blocks, 1)]
        out += ["", "```python", *header, "```", ""]
        out += body
    else:
        width = max(len(q) for q, _ in blocks)
        first_body_line = 1 + len(blocks) + 1 + len(header) + 2 + 1  # 1-based
        out.append("# rustinpy TRD export - contents:")
        for i, ((qual, _), st) in enumerate(zip(blocks, starts), 1):
            out.append(f"#  {i:>3}. {qual:<{width}}  line {first_body_line + st}")
        out.append("")
        out += [*header, "", ""]
        out += body
    return "\n".join(out).rstrip() + "\n"
