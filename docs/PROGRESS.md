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
| `graph.escalators` | заглушка: условие ICPC-UZ 2023 E |
| `graph.bus_companies` | заглушка: условие CSES Bus Companies не сверено |
| `tree.fix_the_leak` | заглушка: что такое «агенты» и «цепочки» в ICPC-UZ 2025 F |
| `dp.fence_painting` | ICPC-UZ 2023 F: правило соседей (формулы сверены перебором для «соседи различны») |
| `strings.inverse_suffix_array` | формат CSES Inverse Suffix Array (алфавит a..z, вывод) |
| `strings.string_functions` | заглушка: какие функции даёт CSES String Functions |
| `strings.brands` | ICPC-UZ 2023 B: набор гласных (y?) и алфавит |
| `strings.apostrophe_number` | заглушка: правило ICPC-UZ 2024 K |
| `roman.roman_symmetry` | заглушка: условие ICPC-UZ 2023 C |
| `roman.roman_product_unique` | заглушка: условие ICPC-UZ 2024 E |
| `roman.roman_split_min_max` | ICPC-UZ 2025 G: что минимизируется / максимизируется |
| `roman.scroogius_shortest` | заглушка: вторая часть ICPC-UZ 2025 G |
| `bits.k_subset_xors` | CSES K Subset Xors: с кратностями или без |
| `bits.all_subarray_xors` | формат CSES All Subarray Xors |
| `bits.kenobi_skywalker` | заглушка: ограничения ICPC-UZ 2025 K |
| `geometry.robot_path` | CSES Robot Path: условие не сверено; решение O(n^2) (сверено с пошаговой симуляцией) |
| `geometry.line_segments_trace` | заглушка: условие CSES Line Segments Trace |
| `geometry.death_star_min_changes` | заглушка: условие ICPC-UZ 2025 D |
| `geometry.biathlon_route` | ICPC-UZ 2023 K: реализована только базовая версия (TSP по подмножествам) |
| `introductory.monotone_subsequences` | CSES: «монотонная» — только возрастающая или любая |
| `introductory.filling_trominos` | заглушка: условие CSES Filling Trominos |

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

## 2026-10-17 · Этап 2: graph + tree
- **Задание:** docs/handoff/000-kickoff.md, SPEC 4.3 (`rustinpy.graph`, `rustinpy.tree`)
- **Сделано:** `graph` (63): обходы (BFS/итеративный DFS, компоненты, двудольность, циклы, обхват), кратчайшие пути (0-1 BFS, Дейкстра + путь/статистика/купон/состояния/k кратчайших, Беллман-Форд с -INF, отрицательный цикл, High Score, Флойд), DAG (Кан, лекс. минимум, Course Schedule II, подсчёт путей, длиннейший путь, достижимость битсетами), DSU/RollbackDSU/Краскал/Прим, SCC (Тарьян, Косараю, конденсация, Coin Collector, 2-SAT, Reachability Queries), мосты и точки сочленения, Эйлер (Хирхольцер), функциональные графы (подъёмы, Planets Cycles/Queries II), потоки (Диниц, Эдмондс-Карп, min-cut, непересекающиеся пути, min-cost flow), паросочетания (Хопкрофт-Карп, Кун, венгерский), гамильтонов путь, обход конём, Critical Cities, Flight Route Requests, Network Renovation, Strongly Connected / Even Outdegree Edges; `tree` (20): порядок обхода, размеры, диаметр, Tree Distances I/II, центроид, Euler tour, LCA (подъёмы и Euler + sparse table), паросочетание, Counting Paths, Subtree/Path Queries, HLD, центроидная декомпозиция, Fixed-Length Paths I/II, Distinct Colors, изоморфизм (AHU, с корнем и без). Всё без рекурсии (AC-08 проверяет AST)
- **Тесты:** 1442 passed на 3.9 / 3.11 / 3.13 (+3 slow) · ruff ✅ · mypy --strict ✅ · каждая функция graph/tree сверена с перебором (Флойд, перечисление путей/разрезов/паросочетаний/перестановок, удаление вершин и рёбер, рекурсивный эталон DFS); `rustinpy export --modules graph,tree` → 3424 строки, компилируется, ширина ≤ 100
- **Скорость (CPython 3.11):** bfs 2·10⁵/4·10⁵ 0.14 с · dijkstra 0.43 с · scc_tarjan 0.39 с · LCA build + 2·10⁵ запросов (глубина ~4·10⁴) 1.3 с · HLD + 5·10⁴ путей 0.65 с · fixed_length_paths 2·10⁵ 1.6 с, range 1.8 с · Dinic (единичный двудольный, 1.8·10⁵ рёбер) 0.23 с · Хопкрофт-Карп 10⁵+10⁵, 3·10⁵ рёбер 0.84 с · Флойд n=500 10.8 с (Python speed) · гамильтонов путь, полный граф n=18 2.7 с · венгерский 500×500 0.63 с
- **Спеки:** SPEC.md — этап 2 отмечен; отклонения имён от 4.3 без смены смысла: `toposort_smallest_first` вместо `toposort_reverse_trick` (Course Schedule II), `reachability_queries` живёт в `graph/scc.py`, DSU и MST в одном файле `graph/dsu.py` (общий `requires`)
- **Решения:** новых D-записей нет (конвенции D-008 соблюдены)
- **Проблемы / долги:** заглушки `graph.escalators`, `graph.bus_companies`, `tree.fix_the_leak` (этап 5); `knights_tour` — эвристика с перезапусками (проверена на всех 64 стартах 8×8)
- **Ручная проверка:** `rustinpy show dijkstra`, `rustinpy show HLD`, `rustinpy export --modules graph,tree --out trd.txt` — проверить читаемость в TRD
- **Дальше:** этап 3 — `dp`, `strings` (+ `roman`), `bits`

## 2026-10-17 · Этап 3: dp + strings + roman + bits
- **Задание:** docs/handoff/000-kickoff.md, SPEC 4.3 (`dp`, `strings`, `roman`, `bits`)
- **Сделано:** `dp` (30): монеты и кубики, рюкзаки 0/1 / неограниченный / ограниченный (двоичное разбиение), Array Description, Counting Towers, edit distance, LCS с восстановлением, LIS (строго / нестрого, с восстановлением), число возрастающих подпоследовательностей, Money Sums (битсет), Rectangle Cutting, Removal Game, Projects, Elevator Rides, Hamiltonian Flights, Counting Tilings (broken profile), digit DP (Counting Numbers), Li Chao, монотонный CHT, D&C-оптимизация (итеративная), Houses and Schools, оптимизация Кнута, Fence Painting (NV); `strings` (29): Z, префикс-функция, KMP, границы, периоды, минимальный сдвиг, Линдон, Required Substring (автомат КМП), хеши 2^61-1 и двойной, Palindrome Queries, бор, Word Combinations, Ахо-Корасик (count / first_pos), суффиксный массив + Kasai, различные подстроки, суффиксный автомат (k-я подстрока с повторами и без, длиннейший повтор, распределение длин), обратный SA, BWT и обратный, Манакер, All Palindromes, Distinct Subsequences, Shortest Subsequence, Brands (NV); `roman` (7); `bits` (22): popcount, Counting Bits, xor-бор, xor-базис (k-й, представимость), K Subset Xors, All Subarray Xors (FWHT), xor-пирамида, SOS DP, SOS Bit Problem, And Subset Count, Hamming Distance, FWHT xor/and/or и свёртки
- **Тесты:** 2004 passed на 3.9 / 3.11 / 3.13 (+4 slow) · ruff ✅ · mypy --strict ✅ · перебор для каждой функции (все подмножества / разбиения / строки, рекурсивные эталоны, `str.find`, `sorted` суффиксов, множества подстрок); тесты нашли реальный баг `suffix_array` (ранги через `ord` ломали упаковку ключа) и семь моих неверных ожиданий в doctest — исправлено
- **Скорость (CPython 3.11):** suffix_array 10⁵ 0.22 с / 10⁶ 4.3 с · SuffixAutomaton 10⁵ 0.21 с · z 10⁶ 0.23 с · манакер 10⁶ 0.75 с · counting_tilings 10×1000 0.66 с · elevator n=18 0.62 с, n=20 2.8 с · hamiltonian_flights полный n=18 0.5 с · knapsack_01 1000×10⁵ 13 с (Python speed) · Кнут n=2000 1.6 с · FWHT 2²⁰ 1.5 с · SOS 2²⁰ 1.2 с
- **Спеки:** SPEC.md — этап 3 отмечен; отклонение: suffix_array за O(n log² n) с сортировкой в C (D-009)
- **Решения:** D-009
- **Проблемы / долги:** заглушки `string_functions`, `apostrophe_number`, `roman_symmetry`, `roman_product_unique`, `scroogius_shortest`, `kenobi_skywalker` (этап 5); `houses_and_schools` при n·k > ~3·10⁵ медленный
- **Ручная проверка:** `rustinpy show SuffixAutomaton`, `rustinpy search palindrome`, `rustinpy export --modules dp,strings --out trd.txt`
- **Дальше:** этап 4 — `geometry`, `game`, `introductory`, `sorting`

## 2026-10-17 · Этап 4: geometry + game + introductory + sorting
- **Задание:** docs/handoff/000-kickoff.md, SPEC 4.3
- **Сделано:** `geometry` (26): Point, cross / dot / orientation, Point Location, точка на отрезке, пересечение отрезков (+ точка пересечения дробями), площадь, точка в многоугольнике, Пик, выпуклая оболочка (с коллинеарными и без), ближайшая пара (D&C снизу вверх и сканирование), манхэттенские расстояния, Intersection Points, Area of Rectangles, Robot Path (NV, O(n²)), Li Chao на максимум, det3 / объём / компланарность, биатлонист — базовая версия (NV, TSP), 2 заглушки; `game` (9): mex, Ним, Ним с ограничением, поддавки, игры вычитания, Гранди на DAG, Stair Game, Grundy's Game, Another Game; `introductory` (28): все задачи Introductory из SPEC (Коллатц, спираль, два коня, два множества, нули факториала, кучи монет, палиндром, яблоки, цифры, красивая перестановка, String Reorder, Mex Grid, ходы коня, код Грея, Ханой, перестановки, подмаски, ферзи, Grid Path Description) + конструктивы (Прюфер, де Брёйн, Inverse Inversions, Monotone Subsequences (NV), Chess Tournament, заглушка Filling Trominos); `sorting` (37): бинпоиски, два указателя, сканирование, расписания (Movie Festival I/II, Room Allocation), суммы 2/3/4, Кадане и версия с длиной, медиана, Missing Coin Sum, Collecting Numbers, Playlist, Towers, Traffic Lights, Иосиф (формула, порядок, запросы), вложенные отрезки, Factory Machines, Tasks and Deadlines, Reading Books, Array Division, подмассивы (сумма x, делимость, ≤ k различных), ближайшие меньшие, встреча посередине, медиана и стоимость скользящего окна (две кучи с ленивым удалением)
- **Тесты:** 2643 passed на 3.9 / 3.11 / 3.13 (+5 slow) · ruff ✅ · mypy --strict ✅ · полный перебор игр (дерево игры с мемоизацией), сетки целых точек и Пик для многоугольников, пошаговая симуляция робота, перестановки для расписаний / Иосифа / ферзей / конструктивов
- **Скорость (CPython 3.11):** convex_hull 2·10⁵ 0.46 с · closest_pair 2·10⁵ 1.6 с (сканирование 0.27 с) · area_of_rectangles 10⁵ 2.3 с · sliding_window_median 2·10⁵ 0.35 с · josephus_order 2·10⁵ 0.55 с · concert_tickets 2·10⁵ 0.21 с · meet_in_middle n=40 0.58 с
- **Спеки:** SPEC.md — этап 4 отмечен
- **Решения:** новых нет
- **Проблемы / долги:** `robot_path` O(n²) (для полных ограничений CSES нужна заметающая прямая); заглушки `line_segments_trace`, `death_star_min_changes`, `filling_trominos`; полный перебор 7×7 в `grid_path_description` занимает минуты
- **Ручная проверка:** `rustinpy show convex_hull`, `rustinpy search josephus`, `rustinpy export --modules geometry,sorting --out trd.txt`
- **Дальше:** этап 5 — `counting`, `misc`, сверка условий ICPC-UZ (Q-1), README RU/EN, CATALOG, export_trd, чек-лист публикации
