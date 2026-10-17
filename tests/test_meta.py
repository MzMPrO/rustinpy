"""Meta tests over the whole registry: docstrings, self-containment, no recursion, NOT VERIFIED.

Мета-тесты: проверяют правила раздела 4.1 спеки для каждого алгоритма сразу.
"""

from __future__ import annotations

import ast
import doctest
import importlib
import importlib.metadata
import re
from pathlib import Path

import pytest

from rustinpy._registry import DOC_FIELDS, AlgoInfo, all_algos, source_of
from tests.spec_names import SPEC_NAMES

ROOT = Path(__file__).resolve().parent.parent
ALGOS = all_algos()
IDS = [a.qualname for a in ALGOS]
CYR = re.compile("[а-яА-ЯёЁ]")

# функции, где рекурсия допустима: глубина O(log n)
RECURSION_WHITELIST: set[str] = set()


def test_ac_01_import_and_no_runtime_dependencies() -> None:
    """AC-01: import works, the distribution has no runtime dependencies."""
    import rustinpy

    assert rustinpy.__version__ == "0.1.0"
    reqs = importlib.metadata.requires("rustinpy") or []
    runtime = [r for r in reqs if "extra ==" not in r]
    assert runtime == []


def test_ac_02_every_spec_name_is_registered() -> None:
    """AC-02: every algorithm promised in SPEC 4.3 is registered and importable."""
    registered = {a.qualname for a in ALGOS}
    missing = [
        f"{m}.{n}" for m, names in SPEC_NAMES.items() for n in names if f"{m}.{n}" not in registered
    ]
    assert missing == []
    for a in ALGOS:
        mod = importlib.import_module(f"rustinpy.{a.module}")
        assert getattr(mod, a.name) is a.obj, f"{a.qualname} is not exported by rustinpy.{a.module}"


def test_ac_02_stubs_explain_themselves() -> None:
    """AC-02: stubs are marked NOT VERIFIED and have an Idea section."""
    for a in ALGOS:
        if a.stub:
            assert not a.verified, a.qualname
            assert "Idea:" in a.doc, a.qualname


def _fields(doc: str) -> list[str]:
    names = []
    for line in doc.splitlines():
        m = re.match(r"^([A-Za-z][A-Za-z -]*):(\s|$)", line)
        if m and m.group(1) in DOC_FIELDS:
            names.append(m.group(1))
    return names


@pytest.mark.parametrize("info", ALGOS, ids=IDS)
def test_ac_03_docstring_format(info: AlgoInfo) -> None:
    """AC-03: docstring follows the template of SPEC 4.1."""
    doc = info.doc
    assert doc, "no docstring"
    first = doc.splitlines()[0]
    assert "#" in first and CYR.search(first.split("#", 1)[1]), (
        "summary needs '# русская подсказка'"
    )
    fields = _fields(doc)
    for req in ("When to use", "Complexity", "Example"):
        assert req in fields, f"missing {req}:"
    assert "Returns" in fields or "Methods" in fields, "missing Returns: / Methods:"
    assert "CSES" in fields or "ICPC-UZ" in fields, "missing CSES: / ICPC-UZ:"
    order = [DOC_FIELDS.index(f) for f in fields]
    assert order == sorted(order), f"wrong field order: {fields}"
    assert len(fields) == len(set(fields)), f"duplicated fields: {fields}"
    if info.icpc and not info.stub:
        assert info.verified or "Idea" in fields or "Pitfalls" in fields


@pytest.mark.parametrize("info", ALGOS, ids=IDS)
def test_ac_04_has_doctest(info: AlgoInfo) -> None:
    """AC-04: every algorithm has a doctest example (they run via --doctest-modules)."""
    tests = doctest.DocTestFinder().find(info.obj, info.name)
    assert any(t.examples for t in tests)


def _test_sources() -> str:
    skip = {"test_meta.py", "spec_names.py", "conftest.py"}
    return "\n".join(
        p.read_text(encoding="utf-8")
        for p in (ROOT / "tests").glob("test_*.py")
        if p.name not in skip
    )


def test_ac_05_every_algorithm_has_a_test() -> None:
    """AC-05: each registered algorithm is used in at least one test file."""
    text = _test_sources()
    missing = [a.qualname for a in ALGOS if not re.search(rf"\b{re.escape(a.name)}\b", text)]
    assert missing == []


@pytest.mark.parametrize("info", ALGOS, ids=IDS)
def test_ac_07_exported_source_is_self_contained(info: AlgoInfo) -> None:
    """AC-07: exported snippet runs its own doctest without the rustinpy package."""
    code = source_of(info)
    assert "rustinpy" not in code.replace("rustinpy -", ""), "snippet mentions rustinpy"
    ns: dict[str, object] = {"__name__": f"standalone_{info.name}"}
    exec(compile(code, f"<{info.qualname}>", "exec"), ns)
    obj = ns[info.name]
    finder = doctest.DocTestFinder(recurse=True)
    runner = doctest.DocTestRunner(optionflags=doctest.NORMALIZE_WHITESPACE)
    for t in finder.find(obj, info.name, globs=ns):
        for ex in t.examples:
            assert "rustinpy" not in ex.source, "doctest imports rustinpy"
        runner.run(t, out=lambda s: None)
    res = runner.summarize(verbose=False)
    assert res.failed == 0, f"{res.failed} doctest failures in standalone snippet"


def _recursive_calls(tree: ast.AST) -> list[str]:
    bad = []
    # метод нельзя вызвать по голому имени: для методов считаем только self.<имя>(...)
    methods = {
        id(item)
        for cls in ast.walk(tree)
        if isinstance(cls, ast.ClassDef)
        for item in cls.body
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Call):
                    f = sub.func
                    if isinstance(f, ast.Name) and f.id == node.name and id(node) not in methods:
                        bad.append(node.name)
                    elif (
                        isinstance(f, ast.Attribute)
                        and isinstance(f.value, ast.Name)
                        and f.value.id == "self"
                        and f.attr == node.name
                    ):
                        bad.append(node.name)
    return bad


@pytest.mark.parametrize("info", ALGOS, ids=IDS)
def test_ac_08_no_recursion(info: AlgoInfo) -> None:
    """AC-08: no function calls itself (except whitelisted O(log n) depth)."""
    if info.qualname in RECURSION_WHITELIST:
        return
    tree = ast.parse(source_of(info))
    assert _recursive_calls(tree) == []


@pytest.mark.parametrize("info", ALGOS, ids=IDS)
def test_ac_08_comments_in_russian(info: AlgoInfo) -> None:
    """AC-08 (style): non-trivial bodies carry Russian comments on key steps."""
    code = source_of(info, with_requires=False)
    tree = ast.parse(code)
    node = tree.body[-1]
    body_lines = (node.end_lineno or 0) - node.lineno
    doc_lines = info.doc.count("\n") + 3
    if body_lines - doc_lines >= 10:
        comments = [ln for ln in code.splitlines() if "#" in ln and CYR.search(ln.split("#", 1)[1])]
        assert len(comments) >= 2, "add short Russian comments to key steps"


def test_ac_09_sources_are_printable_on_windows_console() -> None:
    """AC-09: sources use only cp1251-encodable characters (show works in a Russian console)."""
    for p in (ROOT / "src" / "rustinpy").rglob("*.py"):
        text = p.read_text(encoding="utf-8")
        try:
            text.encode("cp1251")
        except UnicodeEncodeError as e:
            bad = text[e.start : e.end]
            line = text[: e.start].count("\n") + 1
            pytest.fail(f"{p.name}:{line}: character {bad!r} is not in cp1251")


PY39_FORBIDDEN = {
    r"\.bit_count\(": "int.bit_count is 3.10+: use bin(x).count('1')",
    r"\bpairwise\(|import.*\bpairwise\b": "itertools.pairwise is 3.10+",
    r"\bzip\(.*\bstrict=": "zip(strict=...) is 3.10+",
    r"^\s*match\s+\S.*:\s*$": "match statement is 3.10+",
    r"\bbisect_\w+\([^)]*\bkey=": "bisect key= is 3.10+",
}


def test_ac_14_sources_avoid_python310_only_features() -> None:
    """AC-14: mypy checks against 3.10, so 3.9-incompatible APIs are caught here."""
    for p in (ROOT / "src" / "rustinpy").rglob("*.py"):
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            code = line.split("#", 1)[0]
            for pat, why in PY39_FORBIDDEN.items():
                assert not re.search(pat, code), f"{p.name}:{i}: {why}"
        assert "from __future__ import annotations" in p.read_text(encoding="utf-8"), p.name


def test_ac_13_not_verified_is_listed_in_progress() -> None:
    """AC-13: every NOT VERIFIED algorithm is marked in code and listed in docs/PROGRESS.md."""
    progress = (ROOT / "docs" / "PROGRESS.md").read_text(encoding="utf-8")
    m = re.search(r"## NOT VERIFIED.*?\n(.*?)(?:\n## |\Z)", progress, re.S)
    assert m, "docs/PROGRESS.md needs a '## NOT VERIFIED' section"
    listed = set(re.findall(r"`([a-z_]+\.[A-Za-z_0-9]+)`", m.group(1)))
    unverified = {a.qualname for a in ALGOS if not a.verified}
    assert unverified == listed
    for a in ALGOS:
        has_mark = "NOT VERIFIED" in source_of(a, with_requires=False)
        assert has_mark == (not a.verified), a.qualname
