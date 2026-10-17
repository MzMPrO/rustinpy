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

## 2026-10-17 · Проект инициализирован (spec-first)
- **Сделано:** созданы CLAUDE.md, docs/SPEC.md (ЧЕРНОВИК), DECISIONS.md, PROGRESS.md, команды и хуки
- **Дальше:** ТЗ с архитектором в claude.ai (→ KICKOFF.md) или здесь через /spec
