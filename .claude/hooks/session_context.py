#!/usr/bin/env python3
"""SessionStart-хук spec-first: в начале каждой сессии (и после /clear, /compact, resume)
добавляет в контекст короткую сводку: шлюз кода, статусы спек, последние записи журнала, git.
Всё, что печатается в stdout, Claude Code добавляет в контекст сессии.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import (  # noqa: E402
    RU_NAME, gate_disabled, gate_state, latest_handoff, project_root, read_stdin_json, read_text, rel,
)

MAX_PROGRESS_LINES = 25


def last_progress_entries(root: Path, count: int = 2) -> list[str]:
    text = read_text(root / "docs" / "PROGRESS.md")
    if not text:
        return []
    sections, current = [], []
    for line in text.splitlines():
        if line.startswith("## "):
            if current:
                sections.append(current)
            current = [line]
        elif current:
            current.append(line)
    if current:
        sections.append(current)
    lines = [ln for sec in sections[-count:] for ln in sec if ln.strip()]
    return lines[-MAX_PROGRESS_LINES:]


def git_log(root: Path) -> list[str]:
    try:
        out = subprocess.run(
            ["git", "log", "--oneline", "-3"], cwd=root, capture_output=True, text=True, timeout=3,
            check=False
        )
        return out.stdout.strip().splitlines() if out.returncode == 0 else []
    except Exception:
        return []


def main() -> None:
    data = read_stdin_json()
    root = project_root(data)
    source = data.get("source", "startup")
    out = ["[spec-first] Состояние проекта (сгенерировано хуком)"]

    if not (root / "docs" / "SPEC.md").exists():
        out.append("docs/SPEC.md нет. Любая работа начинается с интервью и ТЗ (/spec).")
        print("\n".join(out))
        return

    is_open, reason, statuses = gate_state(root)
    if gate_disabled():
        out.append("Шлюз кода: ОТКЛЮЧЁН пользователем (SPEC_GATE=off). Правила workflow всё равно действуют.")
    else:
        out.append(f"Шлюз кода: {'ОТКРЫТ' if is_open else 'ЗАКРЫТ'} — {reason}")

    not_done = [(p, s) for p, s in statuses if RU_NAME[s] != "ГОТОВО"]
    if not_done:
        out.append("Спеки в работе: " + "; ".join(f"{rel(root, p)} [{RU_NAME[s]}]" for p, s in not_done))

    handoff = latest_handoff(root)
    if handoff:
        out.append(f"Последнее задание архитектора: {rel(root, handoff)}")

    progress = last_progress_entries(root)
    if progress:
        out.append("Последние записи docs/PROGRESS.md:")
        out += ["  " + ln for ln in progress]

    commits = git_log(root)
    if commits:
        out.append("Последние коммиты: " + " | ".join(commits))

    if source == "compact":
        out.append("Контекст был сжат. Перед продолжением перечитай активную спеку и правила из CLAUDE.md.")
    out.append("Роль: Строитель (скилл spec-first, references/builder.md). Код — только по утверждённой "
               "спеке, тесты на каждый AC, после этапа — /done (тесты → журнал → commit + push → отчёт).")
    print("\n".join(out))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[spec-first] ошибка хука session_context: {exc}", file=sys.stderr)
        sys.exit(1)
