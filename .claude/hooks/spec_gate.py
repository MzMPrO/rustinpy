#!/usr/bin/env python3
"""PreToolUse-хук spec-first («шлюз кода»).

Что делает:
1. Не даёт Claude трогать .claude/hooks и .claude/settings*.json (иначе шлюз можно отключить).
2. Не даёт Claude самому поставить спеке статус УТВЕРЖДЕНО — это делает только пользователь
   словом «утверждаю» (хук approve.py). ГОТОВО можно ставить только утверждённой спеке.
3. Пока шлюз закрыт (см. spec_common.gate_state), блокирует запись любых файлов, кроме *.md и docs/.
4. Для Bash — эвристика: блокирует команды, которые явно пишут файлы, пока шлюз закрыт.
5. Статус ГОТОВО пропускает, только если все AC отмечены, у каждого автоматизированного AC
   есть тест с его ID, а линтер и тесты из .claude/spec-first.json зелёные.
6. Всегда блокирует опасные git-команды: --no-verify, force-push, reset --hard, clean -f.

Выход с кодом 2 = блокировка; текст из stderr получает Claude.
Аварийное отключение шлюза кода: запустить Claude Code с переменной окружения SPEC_GATE=off.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_common import (  # noqa: E402
    APPROVED, DONE, RU_NAME, gate_disabled, gate_state, is_spec_path, load_config,
    parse_status, project_root, read_stdin_json, read_text,
)

FILE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
PROTECTED_RE = re.compile(r"^\.claude/(hooks/|settings(\.local)?\.json$|spec-first\.json$)")
AC_LINE_RE = re.compile(r"^[ \t]*[-*][ \t]*\[([ xX])\][ \t]*\**(AC-\d+(?:-\d+)*)\b(.*)$", re.MULTILINE)
MANUAL_RE = re.compile(r"\((?:ручная|manual)\)|\[manual\]", re.IGNORECASE)
DANGEROUS_GIT = [
    (r"--no-verify\b", "--no-verify обходит pre-commit и тесты"),
    (r"\bgit\s+commit\b[^\n;&|]*\s-n\b", "git commit -n обходит pre-commit"),
    (r"\bgit\s+push\b[^\n;&|]*\s(?:-f\b|--force\b|--force-with-lease\b)", "force-push переписывает историю на GitHub"),
    (r"\bgit\s+reset\b[^\n;&|]*--hard\b", "reset --hard безвозвратно удаляет незакоммиченную работу"),
    (r"\bgit\s+clean\b[^\n;&|]*\s-[a-zA-Z]*f", "git clean -f безвозвратно удаляет файлы"),
    (r"\bgit\s+checkout\s+(?:--\s+)?\.(?:\s|$)", "checkout . затирает незакоммиченные изменения"),
]

BASH_WRITE_PATTERNS = [
    r"(?<![0-9&<>])>{1,2}(?!\s*(?:&|/dev/null))",   # перенаправление в файл
    r"\btee\b",
    r"\bsed\s+(?:-[a-zA-Z]*i|--in-place)",
    r"\bperl\s+-[a-zA-Z]*i",
    r"\b(?:cp|mv|rm|touch|ln)\s",
    r"\bgit\s+(?:apply|am|restore|checkout\s+--)",
    r"\bpatch\b",
    r"\b(?:django-admin|manage\.py)\s+(?:startproject|startapp)",
    r"\balembic\s+revision",
    r"\b(?:npm|yarn|pnpm)\s+(?:init|create)\b",
    r"\b(?:uv|poetry)\s+(?:init|new)\b",
    r"\bcookiecutter\b",
    r"open\([^)]*,\s*['\"][wax]",
    r"\.write_text\(|\.write\(",
]
CODE_EXT_RE = re.compile(
    r"\.(py|pyi|js|jsx|ts|tsx|vue|html|css|scss|json|ya?ml|toml|ini|cfg|sql|sh|env|go|rs|java|kt|dart|php|rb)\b"
    r"|Dockerfile|docker-compose|Makefile|requirements",
    re.IGNORECASE,
)


def block(message: str) -> None:
    print(f"[spec-first] {message}", file=sys.stderr)
    sys.exit(2)


def next_step(reason: str) -> str:
    if reason.startswith("MVP закрыт"):
        action = ("Создай спеку фичи в docs/features/ (как /feature), проведи короткое интервью "
                  "и попроси пользователя ответить «утверждаю NNN».")
    elif reason.startswith("нет docs/SPEC.md"):
        action = "Начни с интервью и ТЗ (/spec)."
    else:
        action = ("Доведи спеку до конца (интервью, «Открытые вопросы» пусты), покажи пользователю "
                  "резюме и попроси ответить «утверждаю».")
    return "Что делать: " + action + " Не обходи блокировку через Bash или другие имена файлов."


def new_content(tool: str, ti: dict, old: str | None) -> str | None:
    if tool == "Write":
        return ti.get("content", "")
    if tool == "Edit":
        base = old or ""
        o, n = ti.get("old_string", ""), ti.get("new_string", "")
        if not o:
            return base + n
        return base.replace(o, n) if ti.get("replace_all") else base.replace(o, n, 1)
    if tool == "MultiEdit":
        text = old or ""
        for e in ti.get("edits", []) or []:
            o, n = e.get("old_string", ""), e.get("new_string", "")
            if not o:
                text += n
            else:
                text = text.replace(o, n) if e.get("replace_all") else text.replace(o, n, 1)
        return text
    return None


def check_spec_transition(tool: str, ti: dict, path: Path, relpath: str, root: Path) -> None:
    old_text = read_text(path)
    new_text = new_content(tool, ti, old_text)
    if new_text is None:
        return
    old_status = parse_status(old_text) if old_text is not None else None
    new_status = parse_status(new_text)
    if new_status == APPROVED and old_status != APPROVED:
        block(
            f"Статус УТВЕРЖДЕНО в {relpath} ставит только пользователь. "
            "Оставь статус ЧЕРНОВИК, покажи пользователю краткое резюме спеки и попроси "
            "ответить «утверждаю» — хук approve.py сам поменяет статус."
        )
    if new_status == DONE and old_status not in (APPROVED, DONE):
        was = RU_NAME.get(old_status, "нет файла")
        block(
            f"ГОТОВО можно ставить только утверждённой спеке, а {relpath} сейчас в статусе «{was}». "
            "Сначала спеку должен утвердить пользователь."
        )
    if new_status == DONE and old_status == APPROVED:
        verify_done(root, new_text, relpath)


def tests_corpus(root: Path, dirs: list[str]) -> str:
    chunks = []
    for d in dirs:
        base = root / d
        if base.is_dir():
            for f in base.rglob("*.py"):
                chunks.append(read_text(f) or "")
    return "\n".join(chunks)


def has_ac_test(ac_id: str, corpus: str) -> bool:
    raw = re.compile(r"(?<![A-Za-z0-9])" + re.escape(ac_id) + r"(?![0-9])", re.IGNORECASE)
    snake = re.compile(r"(?<![A-Za-z0-9])" + re.escape(ac_id.lower().replace("-", "_")) + r"(?![0-9])",
                       re.IGNORECASE)
    return bool(raw.search(corpus) or snake.search(corpus))


def run_check(root: Path, name: str, cmd: str, timeout: int) -> None:
    try:
        res = subprocess.run(cmd, shell=True, cwd=root, capture_output=True, text=True, timeout=timeout,
                             check=False)
    except subprocess.TimeoutExpired:
        block(f"ГОТОВО не поставлен: проверка «{cmd}» не уложилась в {timeout} сек.")
    if res.returncode == 0:
        return
    tail = "\n".join((res.stdout + "\n" + res.stderr).strip().splitlines()[-40:])
    hint = ""
    if res.returncode == 5 and "pytest" in cmd:
        hint = "\nPytest не нашёл ни одного теста — этап без тестов не закрывается."
    elif res.returncode in (127, 9009) or "No such file" in tail or "not found" in tail.lower():
        hint = ("\nКоманда не найдена: создай окружение .venv и поставь dev-зависимости (git.md, этап 0). "
                "Если проекту нужна другая команда — попроси пользователя поправить .claude/spec-first.json.")
    block(f"ГОТОВО не поставлен: {name} (код {res.returncode}). Команда: {cmd}\n{tail}{hint}\n"
          "Исправь код или тесты по-честному (не ослабляя проверки) и попробуй снова.")


def verify_done(root: Path, new_text: str, relpath: str) -> None:
    cfg = load_config(root)
    items = AC_LINE_RE.findall(new_text)
    if not items:
        block(f"ГОТОВО не поставлен: в {relpath} нет критериев приёмки в формате «- [x] AC-01: …». "
              "Без проверяемых критериев нельзя доказать, что работа сделана.")
    unchecked = [ac for mark, ac, _ in items if mark == " "]
    if unchecked:
        block(f"ГОТОВО не поставлен: не отмечены {', '.join(unchecked)}. Ручные AC отмечаются только "
              "после подтверждения пользователя.")
    if cfg.get("check_ac_in_tests", True):
        corpus = tests_corpus(root, cfg.get("tests_dirs") or ["tests"])
        auto = [ac for _, ac, rest in items if not MANUAL_RE.search(rest)]
        missing = [ac for ac in auto if not has_ac_test(ac, corpus)]
        if missing:
            block(f"ГОТОВО не поставлен: нет тестов для {', '.join(missing)}. Добавь тест с ID в имени "
                  "(test_ac_07_…) или в докстринге («AC-07»). Если критерий правда нельзя автоматизировать — "
                  "согласуй с пользователем пометку (ручная).")
    timeout = int(cfg.get("test_timeout_sec") or 600)
    for name in ("lint_command", "test_command"):
        if cfg.get(name):
            label = "линтер не прошёл" if name == "lint_command" else "тесты не прошли"
            run_check(root, label, cfg[name], timeout)


def handle_file_tool(tool: str, ti: dict, root: Path) -> None:
    raw = ti.get("file_path") or ti.get("notebook_path")
    if not raw:
        return
    path = Path(raw)
    if not path.is_absolute():
        path = root / path
    try:
        relpath = str(path.resolve().relative_to(root)).replace("\\", "/")
    except Exception:
        return  # файл вне проекта — не наша зона

    if PROTECTED_RE.match(relpath):
        block(
            f"{relpath} — служебный файл шлюза spec-first, Claude его не меняет. "
            "Если правка действительно нужна, попроси пользователя сделать её вручную."
        )

    if is_spec_path(root, path):
        check_spec_transition(tool, ti, path, relpath, root)
        return

    if relpath.lower().endswith(".md") or relpath.startswith("docs/"):
        return  # документацию и ТЗ можно писать всегда

    if gate_disabled():
        return
    is_open, reason, _ = gate_state(root)
    if not is_open:
        block(f"Запись кода заблокирована: {reason}. Файл: {relpath}.\n{next_step(reason)}")


def handle_bash(ti: dict, root: Path) -> None:
    cmd = ti.get("command", "") or ""
    for pattern, why in DANGEROUS_GIT:
        if re.search(pattern, cmd):
            block(f"Опасная git-команда заблокирована: {why}. Если это действительно нужно — объясни "
                  "пользователю зачем, и пусть он выполнит команду сам.")
    writes = any(re.search(p, cmd) for p in BASH_WRITE_PATTERNS)
    if not writes:
        return
    if re.search(r"\.claude[/\\](?:hooks|settings|spec-first\.json)", cmd):
        block("Команда меняет служебные файлы шлюза (.claude/hooks, settings, spec-first.json). "
              "Это делает только пользователь вручную.")
    if re.search(r"docs[/\\](?:SPEC\.md|features)", cmd):
        block("Спеки меняй через инструменты Edit/Write, а не через Bash — так проверяются переходы статусов.")
    if re.search(r"УТВЕРЖДЕНО|APPROVED", cmd, re.IGNORECASE):
        block("Статус УТВЕРЖДЕНО ставит только пользователь словом «утверждаю».")
    if gate_disabled():
        return
    is_open, reason, _ = gate_state(root)
    if is_open:
        return
    touches_only_docs = re.search(r"docs[/\\]|\.md\b", cmd) and not CODE_EXT_RE.search(cmd)
    if not touches_only_docs:
        block(
            f"Команда похожа на запись файлов, а шлюз кода закрыт: {reason}.\n"
            "Пока спека не утверждена, можно читать проект и писать только docs/ и *.md. "
            + next_step(reason)
        )


def main() -> None:
    data = read_stdin_json()
    tool = data.get("tool_name", "")
    ti = data.get("tool_input", {}) or {}
    root = project_root(data)
    if tool in FILE_TOOLS:
        handle_file_tool(tool, ti, root)
    elif tool == "Bash":
        handle_bash(ti, root)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # не валим сессию из-за бага в хуке
        print(f"[spec-first] ошибка хука spec_gate: {exc}", file=sys.stderr)
        sys.exit(1)
