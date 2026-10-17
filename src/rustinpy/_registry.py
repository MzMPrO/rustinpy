"""Registry of algorithms: the @algo decorator and source extraction for show/export.

Реестр алгоритмов: декоратор @algo, поиск по имени и выгрузка самодостаточного исходника.
"""

from __future__ import annotations

import ast
import importlib
import importlib.util
import inspect
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Callable, TypeVar

T = TypeVar("T")

#: Модули с алгоритмами в порядке каталога. Отсутствующие (ещё не написанные) пропускаются.
ALGO_MODULES: tuple[str, ...] = (
    "io",
    "interactive",
    "mathx",
    "ds",
    "graph",
    "tree",
    "dp",
    "strings",
    "roman",
    "bits",
    "geometry",
    "game",
    "introductory",
    "sorting",
    "counting",
    "misc",
)

#: Поля докстринга в обязательном порядке.
DOC_FIELDS: tuple[str, ...] = (
    "When to use",
    "Complexity",
    "Input",
    "Returns",
    "Methods",
    "Pitfalls",
    "Python speed",
    "Idea",
    "Related",
    "CSES",
    "ICPC-UZ",
    "Example",
)


@dataclass(frozen=True)
class AlgoInfo:
    """One registered algorithm (function or class)."""

    module: str
    name: str
    qualname: str
    source_module: str
    obj: object
    tags: tuple[str, ...]
    cses: tuple[str, ...]
    icpc: tuple[str, ...]
    requires: tuple[str, ...]
    complexity: str
    summary: str
    hint: str
    verified: bool
    stub: bool

    @property
    def doc(self) -> str:
        return inspect.getdoc(self.obj) or ""


_REGISTRY: dict[str, AlgoInfo] = {}


def _doc_field(doc: str, field: str) -> str:
    m = re.search(rf"^{re.escape(field)}:\s*(.*)$", doc, re.MULTILINE)
    return m.group(1).strip() if m else ""


def _split_summary(doc: str) -> tuple[str, str]:
    first = doc.strip().splitlines()[0] if doc.strip() else ""
    if "#" in first:
        en, ru = first.split("#", 1)
        return en.strip(), ru.strip()
    return first.strip(), ""


def algo(
    *,
    tags: Sequence[str] = (),
    cses: Sequence[str] = (),
    icpc: Sequence[str] = (),
    requires: Sequence[str] = (),
    verified: bool = True,
    stub: bool = False,
) -> Callable[[T], T]:
    """Register a function or class in the catalog and return it unchanged."""

    def deco(obj: T) -> T:
        source_module = str(getattr(obj, "__module__", ""))
        parts = source_module.split(".")
        module = parts[1] if len(parts) > 1 and parts[0] == "rustinpy" else parts[0]
        name = str(getattr(obj, "__name__", ""))
        doc = inspect.getdoc(obj) or ""
        summary, hint = _split_summary(doc)
        complexity = _doc_field(doc, "Complexity")
        qualname = f"{module}.{name}"
        old = _REGISTRY.get(qualname)
        if old is not None and old.source_module != source_module:
            raise ValueError(
                f"duplicate algorithm {qualname}: {old.source_module} and {source_module}"
            )
        _REGISTRY[qualname] = AlgoInfo(
            module=module,
            name=name,
            qualname=qualname,
            source_module=source_module,
            obj=obj,
            tags=tuple(tags),
            cses=tuple(cses),
            icpc=tuple(icpc),
            requires=tuple(requires),
            complexity=complexity,
            summary=summary,
            hint=hint,
            verified=verified,
            stub=stub,
        )
        return obj

    return deco


def available_modules() -> list[str]:
    """Algorithm modules that exist in this installation."""
    return [m for m in ALGO_MODULES if importlib.util.find_spec(f"rustinpy.{m}") is not None]


def load_all() -> None:
    """Import every algorithm module so that the registry is complete."""
    for m in available_modules():
        importlib.import_module(f"rustinpy.{m}")


def all_algos() -> list[AlgoInfo]:
    load_all()
    order = {m: i for i, m in enumerate(ALGO_MODULES)}
    return sorted(_REGISTRY.values(), key=lambda a: (order.get(a.module, 99), a.qualname))


def resolve(name: str) -> AlgoInfo:
    """Find an algorithm by "name" or "module.name"; ambiguous or unknown -> LookupError."""
    load_all()
    if name in _REGISTRY:
        return _REGISTRY[name]
    matches = [a for a in _REGISTRY.values() if a.name == name]
    if len(matches) == 1:
        return matches[0]
    if matches:
        raise AmbiguousName(name, sorted(a.qualname for a in matches))
    import difflib

    close = difflib.get_close_matches(name, sorted({a.name for a in _REGISTRY.values()}), n=5)
    raise UnknownName(name, close)


class AmbiguousName(LookupError):
    def __init__(self, name: str, options: list[str]) -> None:
        super().__init__(f"ambiguous name {name!r}: " + ", ".join(options))
        self.options = options


class UnknownName(LookupError):
    def __init__(self, name: str, close: list[str]) -> None:
        hint = f"; did you mean: {', '.join(close)}" if close else ""
        super().__init__(f"unknown algorithm {name!r}{hint}")
        self.close = close


# ---------------------------------------------------------------- source extraction

_Node = ast.stmt


def _module_index(source_module: str) -> tuple[list[str], dict[str, _Node], list[_Node]]:
    mod = sys.modules[source_module]
    src = inspect.getsource(mod)
    tree = ast.parse(src)
    defs: dict[str, _Node] = {}
    imports: list[_Node] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defs[node.name] = node
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    defs[t.id] = node
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            defs[node.target.id] = node
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(node)
    return src.splitlines(), defs, imports


def _is_algo_decorator(dec: ast.expr) -> bool:
    target = dec.func if isinstance(dec, ast.Call) else dec
    return isinstance(target, ast.Name) and target.id == "algo"


def _node_lines(lines: list[str], node: _Node, strip_decorator: bool) -> list[str]:
    start = node.lineno
    decorators = getattr(node, "decorator_list", [])
    kept = [d for d in decorators if not (strip_decorator and _is_algo_decorator(d))]
    if kept:
        start = min(d.lineno for d in kept)
    elif decorators and not strip_decorator:
        start = min(d.lineno for d in decorators)
    end = node.end_lineno or node.lineno
    return lines[start - 1 : end]


def _ordered_requires(info: AlgoInfo) -> list[tuple[str, str]]:
    """Transitive requires as (source_module, name) in dependency order."""
    out: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    # стек вместо рекурсии: (модуль, имя, раскрыт ли уже)
    stack: list[tuple[str, str, bool]] = [
        (info.source_module, r, False) for r in reversed(info.requires)
    ]
    by_key = {(a.source_module, a.name): a for a in _REGISTRY.values()}
    visiting: set[tuple[str, str]] = set()  # защита от циклов в requires
    root = (info.source_module, info.name)
    while stack:
        mod, name, expanded = stack.pop()
        key = (mod, name)
        if key in seen or key == root:
            continue
        sub = by_key.get(key)
        if expanded or sub is None or not sub.requires:
            seen.add(key)
            out.append(key)
            continue
        if key in visiting:
            continue
        visiting.add(key)
        stack.append((mod, name, True))
        for r in reversed(sub.requires):
            if (mod, r) not in seen and (mod, r) not in visiting:
                stack.append((mod, r, False))
    return out


def _needed_imports(code: str, imports: list[_Node]) -> list[str]:
    """Top-level stdlib imports of the module whose names are used in code."""
    out: list[str] = []
    for node in imports:
        if isinstance(node, ast.ImportFrom):
            if node.module == "__future__" or (node.module or "").startswith("rustinpy"):
                continue
            names = [a for a in node.names if re.search(rf"\b{a.asname or a.name}\b", code)]
            if names:
                parts = [f"{a.name} as {a.asname}" if a.asname else a.name for a in names]
                out.append(f"from {node.module} import {', '.join(parts)}")
        elif isinstance(node, ast.Import):
            for a in node.names:
                if a.name.startswith("rustinpy"):
                    continue
                bound = a.asname or a.name.split(".")[0]
                if re.search(rf"\b{re.escape(bound)}\b", code):
                    out.append(f"import {a.name} as {a.asname}" if a.asname else f"import {a.name}")
    return out


def source_parts(
    info: AlgoInfo, *, with_requires: bool = True, strip_decorator: bool = True
) -> tuple[list[str], str]:
    """Return (imports, code) of a self-contained snippet for the algorithm."""
    load_all()
    chunks: list[str] = []
    keys = _ordered_requires(info) if with_requires else []
    keys.append((info.source_module, info.name))
    imports: list[_Node] = []
    for mod, name in keys:
        lines, defs, imports_m = _module_index(mod)
        node = defs.get(name)
        if node is None:
            raise LookupError(f"{name!r} not found at top level of {mod}")
        chunks.append("\n".join(_node_lines(lines, node, strip_decorator)))
        imports.extend(imports_m)
    code = "\n\n\n".join(chunks)
    imp = list(dict.fromkeys(_needed_imports(code, imports)))
    return imp, code


def source_of(info: AlgoInfo, *, with_requires: bool = True, strip_decorator: bool = True) -> str:
    """Self-contained source: imports + required helpers + the algorithm itself."""
    imports, code = source_parts(info, with_requires=with_requires, strip_decorator=strip_decorator)
    head = ["from __future__ import annotations", *imports]
    return "\n".join(head) + "\n\n\n" + code + "\n"
