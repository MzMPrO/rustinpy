"""Общая логика хуков spec-first: статусы спек и состояние шлюза кода.

Статус спеки — строка вида «**Статус:** ЧЕРНОВИК» (можно и «Status: DRAFT»).
Нет строки статуса = ЧЕРНОВИК (безопасное значение по умолчанию).
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

DRAFT, APPROVED, DONE = "DRAFT", "APPROVED", "DONE"

STATUS_WORDS = {
    "ЧЕРНОВИК": DRAFT, "DRAFT": DRAFT,
    "УТВЕРЖДЕНО": APPROVED, "APPROVED": APPROVED,
    "ГОТОВО": DONE, "DONE": DONE,
}
RU_NAME = {DRAFT: "ЧЕРНОВИК", APPROVED: "УТВЕРЖДЕНО", DONE: "ГОТОВО"}

STATUS_RE = re.compile(
    r"^[ \t>*_\-]*(?:Статус|Status)[ \t]*[*_]*[ \t]*:[ \t]*[*_`]*[ \t]*([A-Za-zА-ЯЁа-яё]+)",
    re.MULTILINE | re.IGNORECASE,
)


def read_stdin_json() -> dict:
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def project_root(data: dict | None = None) -> Path:
    root = os.environ.get("CLAUDE_PROJECT_DIR") or (data or {}).get("cwd") or os.getcwd()
    return Path(root).resolve()


def parse_status(text: str | None) -> str:
    if not text:
        return DRAFT
    m = STATUS_RE.search(text)
    if not m:
        return DRAFT
    return STATUS_WORDS.get(m.group(1).upper(), DRAFT)


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return None


def spec_files(root: Path) -> list[Path]:
    """SPEC.md + все спеки фич (файлы, начинающиеся с «_», — шаблоны, их пропускаем)."""
    files = []
    spec = root / "docs" / "SPEC.md"
    if spec.exists():
        files.append(spec)
    feat_dir = root / "docs" / "features"
    if feat_dir.is_dir():
        files += sorted(p for p in feat_dir.glob("*.md") if not p.name.startswith("_"))
    return files


def is_spec_path(root: Path, path: Path) -> bool:
    try:
        rel = path.resolve().relative_to(root)
    except Exception:
        return False
    parts = rel.parts
    if parts == ("docs", "SPEC.md"):
        return True
    return (len(parts) == 3 and parts[0] == "docs" and parts[1] == "features"
            and parts[2].endswith(".md") and not parts[2].startswith("_"))


def gate_state(root: Path) -> tuple[bool, str, list[tuple[Path, str]]]:
    """Возвращает (открыт_ли_шлюз, причина, [(файл, статус), ...])."""
    spec = root / "docs" / "SPEC.md"
    if not spec.exists():
        return False, "нет docs/SPEC.md — начни с интервью (/spec)", []
    statuses = [(p, parse_status(read_text(p))) for p in spec_files(root)]
    drafts = [p for p, s in statuses if s == DRAFT]
    if drafts:
        names = ", ".join(rel(root, p) for p in drafts)
        return False, f"есть неутверждённые спеки: {names}", statuses
    spec_status = dict(statuses).get(spec)
    approved_features = [p for p, s in statuses if s == APPROVED and p != spec]
    if spec_status == APPROVED or approved_features:
        active = [rel(root, p) for p, s in statuses if s == APPROVED]
        return True, "активные спеки: " + ", ".join(active), statuses
    return False, ("MVP закрыт (SPEC.md = ГОТОВО), активной фичи нет — "
                   "новая работа начинается со спеки фичи (/feature)"), statuses


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root)).replace("\\", "/")
    except Exception:
        return str(path)


DEFAULT_CONFIG = {
    "test_command": "python -m pytest -q",
    "lint_command": "python -m ruff check . --extend-exclude .claude",
    "check_ac_in_tests": True,
    "tests_dirs": ["tests"],
    "test_timeout_sec": 600,
}


def load_config(root: Path) -> dict:
    """.claude/spec-first.json — команды тестов и линтера. Меняет только пользователь."""
    cfg = dict(DEFAULT_CONFIG)
    try:
        cfg.update(json.loads((root / ".claude" / "spec-first.json").read_text(encoding="utf-8")))
    except Exception:
        pass
    return cfg


def latest_handoff(root: Path) -> Path | None:
    d = root / "docs" / "handoff"
    files = sorted(p for p in d.glob("*.md")) if d.is_dir() else []
    return files[-1] if files else None


def gate_disabled() -> bool:
    return os.environ.get("SPEC_GATE", "").strip().lower() in {"off", "0", "false", "no"}
