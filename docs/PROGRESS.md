# Журнал проекта: rustinpy

История от начала до конца. Новые записи добавляются В КОНЕЦ файла, по одной на сессию или задачу.
Если файл длиннее ~300 строк, старые записи уходят в docs/history/PROGRESS-ГГГГ-ММ.md,
а здесь остаётся сводка.

Формат записи:

    ## ГГГГ-ММ-ДД · Что за сессия (коротко)
    - **Задание:** docs/handoff/NNN-….md
    - **Сделано:** …
    - **Тесты:** N passed, покрытие X% · линтер ✅ · закрыты AC-…
    - **Спеки:** что утверждено, изменено или закрыто
    - **Решения:** D-00X (если были)
    - **Проблемы / долги:** … (включая каждый skip/xfail с причиной)
    - **Ручная проверка:** что пользователь должен проверить руками
    - **Дальше:** конкретный следующий шаг

---

## NOT VERIFIED — что проверить руками (живой список, обновляется каждый этап)

Алгоритм с `verified=False`: код или формула проверены тестами, но условие задачи не сверено
(или это заглушка). Тест `test_ac_13` следит, чтобы список совпадал с кодом.

| Алгоритм | Что не проверено |
|---|---|
| `interactive.find_hidden_rectangle` | тип запроса в ICPC-UZ 2024 F («пересекает ли» / «сколько клеток») |
| `interactive.kth_highest_score` | формат взаимодействия CSES K-th Highest Score |
| `interactive.colored_chairs` | формат взаимодействия CSES Colored Chairs |
| `interactive.permuted_binary_strings` | заглушка: условие CSES не сверено |
| `interactive.inversion_sorting` | заглушка: условие CSES не сверено |
| `mathx.phi_prefix_sum` | условие ICPC-UZ 2023 J (что именно суммировать) |
| `mathx.coprime_pairs_up_to` | 2023 J: упорядоченные или неупорядоченные пары |
| `mathx.gcd_sum_pairs` | условие ICPC-UZ 2025 C |
| `mathx.count_fib_representations` | условия ICPC-UZ 2023 H / 2025 J |
| `mathx.min_trials_for_probability` | условие и требования к точности ICPC-UZ 2023 D |
| `mathx.min_digit_changes_count` | заглушка: условие ICPC-UZ 2025 B |
| `mathx.deep_numbers_count` | заглушка: условие ICPC-UZ 2024 D |
| `mathx.infinite_game_count` | заглушка: правила игры ICPC-UZ 2025 I |
| `ds.SegTreeFlipRuns` | ICPC-UZ 2025 H: какая функция от длины серии единиц (сейчас L(L+1)/2) |
| `ds.isotonic_sse_mod` | ICPC-UZ 2023 L: какие запросы; реализована только подгонка и SSE |
| `ds.exclusions` | заглушка: определение f(k) в ICPC-UZ 2025 E |
| `ds.generic_strings` | заглушка: условие ICPC-UZ 2023 G |

## 2026-10-17 · Проект инициализирован (spec-first)
- **Сделано:** созданы CLAUDE.md, docs/SPEC.md (ЧЕРНОВИК), DECISIONS.md, PROGRESS.md, команды и хуки
- **Дальше:** ТЗ с архитектором в claude.ai (→ KICKOFF.md) или здесь через /spec

## 2026-10-17 · Спека утверждена, этап 1: каркас + io + interactive + mathx + ds
- **Задание:** docs/handoff/000-kickoff.md; спека — docs/SPEC.md (УТВЕРЖДЕНО, Q-1…Q-5 по умолчанию)
- **Сделано:** имя `rustinpy` свободно на PyPI/TestPyPI; реестр `@algo` с выгрузкой самодостаточного кода через AST (`_registry.py`), `show/search/list_algos/help/export` (`_api.py`), CLI `rustinpy list|show|search|export`; `io` (8), `interactive` (9), `mathx` (69), `ds` (55) — 140 алгоритмов; CI (3.9–3.13 + windows, ruff, mypy, build), `publish.yml` (Trusted Publishing: ручной запуск → TestPyPI, тег `v*` → PyPI), pre-commit (ruff 0.17.1, поиск токенов)
- **Тесты:** 908 passed на 3.9 / 3.11 / 3.13 (+2 slow) · ruff ✅ · mypy --strict ✅ · `python -m build` + `twine check --strict` ✅ · wheel в чистом venv: 0 зависимостей ✅ · AC-01, AC-12 закрыты; AC-03…AC-09, AC-13, AC-14 выполняются для готовых модулей
- **Скорость (CPython 3.11, эта машина, шум ±50%):** Fenwick 4·10⁵ оп. 1.4 с · SegTree(min) 4·10⁵ оп. 3.1 с · LazySegAddSum 4·10⁵ оп. 12.9 с (Python speed) · SortedList 3·10⁵ оп. 2.0 с · distinct_values_queries 2·10⁵ 1.5 с · sieve(10⁷) 0.07 с · linear_sieve(2·10⁶) 0.5 с · Comb(10⁶) 0.25 с · convolution 2·10⁵×2·10⁵ 1.6–1.9 с (decimal) · convolution_ntt 5·10⁴ 2.5 с · phi_prefix_sum(10⁹) 1.75 с
- **Спеки:** SPEC.md — этап 1 отмечен; мелкие отклонения сигнатур от 4.3 (без смены смысла): `FastReader.next_int()` и т.д. вместо `.int()` (имя метода `int` ломает mypy), `pizzeria_queries` принимает 3-кортежи `("?", k, 0)`, добавлен `convolution_ntt` (D-007), `SegTreeFlipRuns` считает Σ L(L+1)/2 (NOT VERIFIED)
- **Решения:** D-002 (реестр + AST), D-003 (mypy под 3.10), D-004 (закреплённые ruff/mypy), D-005 (cp1251), D-006 (ICPC-UZ без условий — заглушки), D-007 (свёртка через decimal)
- **Проблемы / долги:** ленивые деревья медленные в CPython (~30 мкс/оп., документировано); тесты в песочнице Claude Code требуют `--basetemp` в scratchpad; GitHub-репозиторий не создан (нужен ник владельца) — CI ещё ни разу не запускался
- **Ручная проверка:** `pip install -e .` и `rustinpy list`, `rustinpy show factorize`, `rustinpy export --modules ds --out trd.txt` — открыть trd.txt, глянуть читаемость; просмотреть таблицу NOT VERIFIED выше
- **Дальше:** этап 2 — `graph`, `tree`
