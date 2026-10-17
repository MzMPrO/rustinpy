#!/usr/bin/env python3
"""UserPromptSubmit-хук spec-first: утверждение спеки человеком.

Пользователь пишет в Claude Code сообщение, начинающееся со слова:
    утверждаю            — утвердить единственный черновик
    утверждаю 004        — утвердить docs/features/004-*.md
    утверждаю тз         — утвердить docs/SPEC.md
    утверждаю всё        — утвердить все черновики
(также: approve / approved)

Хук сам меняет статус ЧЕРНОВИК → УТВЕРЖДЕНО, ставит дату и печатает в stdout
сообщение, которое Claude Code добавляет в контекст. Claude этот статус поставить не может.
Если после «утверждаю» идут условия («утверждаю, но поменяй …») — НЕ утверждает.
"""
from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import (  # noqa: E402
    DRAFT, STATUS_RE, parse_status, project_root, read_stdin_json, read_text, rel, spec_files,
)

TRIGGER_RE = re.compile(r"^\s*(утверждаю|утверждено|approved?)\b(.*)$", re.IGNORECASE | re.DOTALL)
CONDITION_RE = re.compile(
    r"\b(но|только|кроме|если|поменя|измени|исправ|добав|убер|однако|but|except|change|fix)",
    re.IGNORECASE,
)
ALL_WORDS = {"всё", "все", "all"}
SPEC_WORDS = {"тз", "spec", "спек", "спеку", "spec.md", "проект"}
STAMP_RE = re.compile(r"^[ \t>*_\-]*Утверждено[ \t]*[*_]*[ \t]*:.*$", re.MULTILINE)


def say(text: str) -> None:
    print(f"[spec-first] {text}")
    sys.exit(0)


def approve_file(path: Path, now: str) -> None:
    text = read_text(path) or ""
    m = STATUS_RE.search(text)
    word = "APPROVED" if m and m.group(1).isascii() else "УТВЕРЖДЕНО"
    stamp = f"> **Утверждено:** {now} (пользователем)"
    if m:
        text = text[: m.start(1)] + word + text[m.end(1):]
        if STAMP_RE.search(text):
            text = STAMP_RE.sub(stamp, text, count=1)
        else:
            line_end = text.find("\n", m.start(1))
            line_end = len(text) if line_end == -1 else line_end
            text = text[:line_end] + "\n" + stamp + text[line_end:]
    else:
        text = f"> **Статус:** {word}\n{stamp}\n\n" + text
    if "История изменений" in text:
        text = text.rstrip("\n") + f"\n- {now} — утверждено пользователем\n"
    path.write_text(text, encoding="utf-8")


def main() -> None:
    data = read_stdin_json()
    prompt = data.get("prompt", "") or ""
    m = TRIGGER_RE.match(prompt)
    if not m:
        sys.exit(0)

    root = project_root(data)
    rest = m.group(2).strip(" \t\n.,!:;—-")
    if len(rest) > 40 or CONDITION_RE.search(rest):
        say(
            "Пользователь начал с «утверждаю», но добавил условия — автоматически НЕ утверждено. "
            "Внеси правки в спеку (статус остаётся ЧЕРНОВИК), покажи, что изменилось, и попроси "
            "утвердить ещё раз одним словом «утверждаю»."
        )

    drafts = [p for p in spec_files(root) if parse_status(read_text(p)) == DRAFT]
    if not drafts:
        say("Пользователь написал «утверждаю», но черновиков спек нет — утверждать нечего. "
            "Уточни у пользователя, что он имел в виду.")

    token = (rest.split() or [""])[0].strip(".,!:;").lower()
    by_name = [p for p in drafts if token and token in p.name.lower()]
    if token in ALL_WORDS:
        chosen = drafts
    elif token in SPEC_WORDS:
        chosen = [p for p in drafts if p.name == "SPEC.md"]
    elif token.isdigit() or by_name:
        chosen = by_name
    else:
        chosen = drafts  # «утверждаю» или «утверждаю, отлично» — без указания цели
        if len(drafts) > 1:
            names = ", ".join(rel(root, p) for p in drafts)
            say(f"Черновиков несколько ({names}), ничего не утверждено. Попроси пользователя "
                "уточнить: «утверждаю 004», «утверждаю тз» или «утверждаю всё».")

    if not chosen:
        names = ", ".join(rel(root, p) for p in drafts)
        say(f"Не нашёл черновик по «{rest}». Черновики сейчас: {names}. Ничего не утверждено.")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    for p in chosen:
        approve_file(p, now)
    names = ", ".join(rel(root, p) for p in chosen)
    say(
        f"Пользователь УТВЕРДИЛ: {names} ({now}). Статус выставлен хуком. "
        "Можно приступать к реализации строго по плану из спеки. Если по ходу появится "
        "что-то, меняющее поведение, — остановись и уточни."
    )


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(f"[spec-first] ошибка хука approve: {exc}", file=sys.stderr)
        sys.exit(1)
