"""AC-09, AC-10: CLI and Python helpers show / search / list / export."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

import rustinpy
from rustinpy.cli import main


def test_ac_09_list(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["list"]) == 0
    out = capsys.readouterr().out
    assert "[mathx]" in out and "mathx.modpow" in out
    assert main(["list", "--module", "io"]) == 0
    out = capsys.readouterr().out
    assert "io.FastReader" in out and "mathx." not in out
    assert main(["list", "--unverified"]) == 0
    assert "NOT VERIFIED" in capsys.readouterr().out
    assert main(["list", "--module", "nope"]) == 1


def test_ac_09_show_strips_decorator_and_adds_requires(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["show", "factorize"]) == 0
    out = capsys.readouterr().out
    assert "@algo" not in out and "rustinpy" not in out
    assert "def is_prime" in out and "def pollard_rho" in out and "def factorize" in out
    assert out.index("def is_prime") < out.index("def factorize")
    assert "import random" in out
    assert main(["show", "factorize", "--raw"]) == 0
    raw = capsys.readouterr().out
    assert "@algo" in raw and "def is_prime" not in raw


def test_ac_09_show_unknown_and_close_matches(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["show", "factorise"]) == 1
    assert "factorize" in capsys.readouterr().err


def test_ac_09_search(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["search", "fibonacci"]) == 0
    out = capsys.readouterr().out
    assert "mathx.fib" in out
    assert main(["search", "zzzzqqq"]) == 1


def test_ac_09_python_api(capsys: pytest.CaptureFixture[str]) -> None:
    found = rustinpy.search("prime", quiet=True)
    assert any(a.name == "is_prime" for a in found)
    rustinpy.show("modinv")
    out = capsys.readouterr().out
    assert "def ext_gcd" in out and "def modinv" in out
    assert {a.module for a in rustinpy.list_algos()} >= {"io", "interactive", "mathx"}
    assert all(a.module == "mathx" for a in rustinpy.list_algos("mathx"))
    rustinpy.help()
    assert "rustinpy.mathx" in capsys.readouterr().out
    rustinpy.help("fib")
    assert "fast doubling" in capsys.readouterr().out


def test_ac_10_export_txt(tmp_path: Path) -> None:
    out = tmp_path / "trd.txt"
    assert main(["export", "--modules", "io", "--names", "fib,modinv", "--out", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert text.startswith("# rustinpy TRD export - contents:")
    assert "@algo" not in text and "from rustinpy" not in text
    assert all(len(line) <= 100 for line in text.splitlines())
    compile(text, "trd.txt", "exec")  # весь файл - корректный Python
    lines = text.splitlines()
    # номера строк в оглавлении указывают на заголовки блоков
    for line in lines[1:]:
        if not line.startswith("#  "):
            break
        qual, ln = line.split()[2], int(line.split()[-1])
        assert lines[ln - 1] == f"# ==== {qual} ===="


def test_ac_10_export_md_and_docstring_modes(tmp_path: Path) -> None:
    md = rustinpy.export(["fib"], fmt="md", docstrings="full")
    assert md.startswith("# rustinpy TRD export") and "```python" in md and ">>>" in md
    short = rustinpy.export(["fib"], docstrings="short")
    assert "Complexity:   O(log n)" in short and ">>>" not in short
    none = rustinpy.export(["fib"], docstrings="none")
    assert '"""' not in none
    compile(none, "x", "exec")
    with pytest.raises(ValueError):
        rustinpy.export([])
    out = tmp_path / "t.md"
    assert main(["export", "--names", "fib", "--out", str(out)]) == 0
    assert out.read_text(encoding="utf-8").startswith("# rustinpy TRD export")


def test_ac_09_installed_command_runs() -> None:
    r = subprocess.run(
        [sys.executable, "-m", "rustinpy.cli", "--version"], capture_output=True, text=True
    )
    assert r.returncode == 0 and "0.1.0" in r.stdout
