"""Docs and packaging: CATALOG, README, full TRD export, build (AC-10, AC-11, AC-16, AC-17)."""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

import rustinpy
from rustinpy._registry import available_modules

ROOT = Path(__file__).resolve().parent.parent


def load_script(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_ac_11_catalog_matches_generator() -> None:
    gen = load_script("gen_catalog")
    current = (ROOT / "docs" / "CATALOG.md").read_text(encoding="utf-8")
    assert current == gen.render(), "run: python scripts/gen_catalog.py"


def test_ac_11_catalog_lists_every_algorithm() -> None:
    text = (ROOT / "docs" / "CATALOG.md").read_text(encoding="utf-8")
    for a in rustinpy.list_algos():
        assert f"| `{a.name}` |" in text, a.qualname
    for mod in available_modules():
        assert f"## {mod}\n" in text


def test_ac_16_readme_has_ru_and_en_sections() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    ru = ["## Русский", "### Установка", "### Быстрый старт", "### Модули", "### CLI", "### TRD"]
    ru += ["### Ограничения", "### Лицензия"]
    en = ["## English", "### Installation", "### Quick start", "### Modules", "### CLI", "### TRD"]
    en += ["### Limitations", "### License"]
    for heading in ru + en:
        assert f"\n{heading}" in text, heading
    assert text.index("## Русский") < text.index("## English")
    assert "docs/CATALOG.md" in text and "25" in text
    for mod in available_modules():
        assert f"| `{mod}` |" in text, mod


def test_ac_10_export_of_everything_is_valid() -> None:
    for mode in ("full", "none"):
        text = rustinpy.export(modules=available_modules(), docstrings=mode)
        assert "@algo" not in text and "from rustinpy" not in text and "import rustinpy" not in text
        assert all(len(line) <= 100 for line in text.splitlines())
        compile(text, "trd.txt", "exec")
        lines = text.splitlines()
        toc = [ln for ln in lines[1:] if ln.startswith("#  ")]
        assert len(toc) == len(rustinpy.list_algos())
        for line in toc:
            qual, ln = line.split()[2], int(line.split()[-1])
            assert lines[ln - 1] == f"# ==== {qual} ===="


def test_export_trd_script(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    exp = load_script("export_trd")
    out = tmp_path / "trd.txt"
    assert exp.main(["--names", "dijkstra,LCA", "--out", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert "# ==== graph.dijkstra ====" in text and "# ==== tree.LCA ====" in text
    assert "lines" in capsys.readouterr().out
    md = tmp_path / "all.md"
    assert exp.main(["--out", str(md), "--docstrings", "none"]) == 0
    assert md.read_text(encoding="utf-8").startswith("# rustinpy TRD export")
    assert "too long for a TRD" in capsys.readouterr().out


@pytest.mark.slow
def test_ac_17_build_and_twine_check(tmp_path: Path) -> None:
    pytest.importorskip("build")
    pytest.importorskip("twine")
    src = tmp_path / "src"
    shutil.copytree(
        ROOT,
        src,
        ignore=shutil.ignore_patterns(
            ".git", ".venv", "dist", "build", "__pycache__", "*.egg-info"
        ),
    )
    dist = tmp_path / "dist"
    r = subprocess.run(
        [sys.executable, "-m", "build", "--outdir", str(dist), str(src)],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    files = sorted(str(p) for p in dist.iterdir())
    assert any(f.endswith(".whl") for f in files) and any(f.endswith(".tar.gz") for f in files)
    r = subprocess.run(
        [sys.executable, "-m", "twine", "check", "--strict", *files], capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr
