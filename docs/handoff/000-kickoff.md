# Задача 000 · Kickoff: библиотека rustinpy

> Исходное задание пользователя, сохранено дословно 2026-10-17.

ЗАДАЧА: создай Python-библиотеку `rustinpy` (шпаргалка по алгоритмам для ICPC) и подготовь её к публикации на PyPI
Ты работаешь как BUILDER. Результат: пакет, который ставится командой `pip install rustinpy`. Язык общения со мной: русский. Код, имена функций и docstring: английский, но у каждой функции есть короткий русский комментарий-подсказка (см. «Стиль функций»).
1. Что это за библиотека
`rustinpy` это шпаргалка (cheat sheet) в виде Python-пакета: готовые, проверенные реализации алгоритмов для спортивного программирования (ICPC). Каждый алгоритм это функция или небольшой класс с понятным докстрингом: что делает, сложность, когда применять, пример вызова, подводные камни.
Главные сценарии использования:

1. Тренировка: `from rustinpy.graph import dijkstra` и сразу использовать.
2. Подготовка TRD (Team Reference Document): быстро посмотреть исходник и скопировать его в документ. На соревновании pip недоступен, поэтому важна самодостаточность каждой функции.
3. Поиск по темам из консоли: `rustinpy list`, `rustinpy show dijkstra`.

Принципы:

* Чистый Python 3.9+, без обязательных зависимостей (numpy/scipy не нужны, они не нужны на контесте).
* Каждая функция самодостаточна: её можно скопировать в файл вместе с её же внутренними вспомогательными функциями и она заработает. Минимум перекрёстных импортов между модулями. Если нужна общая вспомогалка, продублируй её (это шпаргалка, а не фреймворк).
* Никакой рекурсии на больших глубинах: DFS, обход дерева, SCC и подобное пиши итеративно (иначе упадёт на 10^5–10^6 вершин).
* Быстрый ввод-вывод в `rustinpy.io` (`sys.stdin.buffer`).
* Всё типизировано (type hints), есть `py.typed`.

2. Имя пакета и проверка PyPI

* Имя дистрибутива: `rustinpy`, импортируемый пакет: `rustinpy`.
* Первым делом проверь, свободно ли имя на PyPI (`pip index versions rustinpy` или страница `https://pypi.org/project/rustinpy/`). Если занято, остановись и спроси меня, какое имя взять.
* Лицензия MIT. Автор: Mirahmad. Версия начинается с `0.1.0`.

3. Структура репозитория

```
rustinpy/
├── pyproject.toml            # сборка через hatchling или setuptools, без setup.py
├── README.md                 # на русском и английском (см. раздел 8)
├── LICENSE
├── CHANGELOG.md
├── docs/
│   ├── SPEC.md               # спецификация (создай сам по этому промту и согласуй со мной)
│   ├── PROGRESS.md           # что сделано, что дальше
│   └── CATALOG.md            # автогенерируемый каталог всех функций (см. раздел 7)
├── src/rustinpy/
│   ├── __init__.py           # реэкспорт, __version__, функция help()/show()
│   ├── py.typed
│   ├── cli.py                # консольная команда rustinpy
│   ├── io.py
│   ├── interactive.py
│   ├── math/ ...
│   └── ... (модули из раздела 5)
├── tests/                    # pytest, по файлу на модуль
├── scripts/
│   ├── gen_catalog.py        # генерация docs/CATALOG.md
│   └── export_trd.py         # выгрузка выбранных алгоритмов в один .txt/.md для TRD
└── .github/workflows/
    ├── ci.yml                # тесты на 3.9–3.13, ruff, mypy
    └── publish.yml           # публикация через PyPI Trusted Publishing (по тегу v*)

```

4. Стиль функций (ОБЯЗАТЕЛЬНО для каждой)
Формат докстринга (шаблон):

```python
def dijkstra(n: int, adj: list[list[tuple[int, int]]], src: int) -> list[int]:
    """Shortest paths from src, non-negative weights.   # Кратчайшие пути из src.

    When to use:  single-source shortest path, weights >= 0.   # Когда применять
    Complexity:   O((n + m) log n)
    Input:        adj[u] = [(v, w), ...], 0-indexed vertices.
    Returns:      dist[v], or INF (= 1 << 60) if unreachable.
    Pitfalls:     do not use with negative edges -> bellman_ford.   # Подводные камни
    Related:      bellman_ford, zero_one_bfs, floyd_warshall.
    CSES:         Shortest Routes I (1671).
    Example:
        >>> adj = [[(1, 5)], [(2, 1)], []]
        >>> dijkstra(3, adj, 0)
        [0, 5, 6]
    """

```

Требования:

* Блок `Example:` обязан быть рабочим doctest (`pytest --doctest-modules` проходит).
* Строка `CSES:` / `ICPC-UZ:` со ссылкой на задачу, где алгоритм нужен (названия берём из раздела 5).
* Внутри тела: короткие русские комментарии к ключевым шагам, чтобы можно было читать как конспект.
* Индексация везде 0-based, если в докстринге не сказано иное. Значения INF фиксированы в модуле.
* Модуль по умолчанию `MOD = 998244353`, но функции принимают `mod` параметром (в задаче 2025 B модуль составной, 2112025, поэтому обратные элементы там не работают; отметь это в `nCr`).

5. Содержимое: ВСЕ алгоритмы, которые нужно реализовать
Источники: полный список CSES Problem Set (17 разделов) плюс темы задач ICPC Uzbekistan Regional 2023, 2024, 2025. Реализуй всё ниже. Если алгоритм покрывает несколько задач, одной реализации достаточно.
5.1 `rustinpy.io`, `rustinpy.interactive`

* Быстрый ввод: `read_int`, `read_ints`, `read_str`, обёртка над `sys.stdin.buffer`.
* Быстрый вывод: накопление в список, `sys.stdout.write`.
* Интерактив (ICPC-UZ 2023 I, 2024 F, 2024 J, 2025 J): `ask(query) -> reply` с обязательным `flush`, обработка `-1`/EOF, шаблон бинарного поиска по ответу, шаблон 2D-поиска по прямоугольнику (2024 F: 10^9 × 10^9, 125 запросов), заметка про адаптивный интерактор.

5.2 `rustinpy.introductory` (CSES Introductory + Construction)

* Gray code, Tower of Hanoi (ходы), перебор перестановок строки, `next_permutation`, подмножества (bitmask), N ферзей, обход сетки (бэктрекинг).
* Конструктивы: Prüfer code (кодирование и декодирование), de Bruijn sequence, Inverse Inversions, Monotone Subsequences, Chess Tournament (граф степеней), Trominos.

5.3 `rustinpy.sorting` (Sorting and Searching)

* Бинарный поиск по ответу (универсальный шаблон `bisect_answer(lo, hi, ok)`), два указателя, sweep line по событиям, scheduling (Movie Festival I/II, Room Allocation).
* Nested ranges, Josephus (I и II, формула и структура), Sliding Window Median/Cost.
* Subarray sums (префиксные суммы + словарь), monotonic stack/deque (Nearest Smaller Values).
* Meet in the middle.

5.4 `rustinpy.dp`

* Knapsack 0/1, неограниченный, подсчёт способов (Coin Combinations I/II), Edit Distance, LCS, LIS за n log n (строго и нестрого, с восстановлением), Money Sums (bitset).
* DP по подотрезкам (Rectangle Cutting, Removal Game).
* Bitmask DP (Elevator Rides, Hamiltonian Flights), DP по профилю (Counting Tilings).
* Digit DP (Counting Numbers; ICPC-UZ 2024 D «Deep Numbers»).
* Оптимизации: Convex Hull Trick (Li Chao и монотонный), Divide & Conquer optimization, Knuth optimization (Houses and Schools, Knuth Division).
* Подсчёт раскрасок с ограничениями соседей (ICPC-UZ 2023 F «Fence Painting»: сегменты нулей между закрашенными, формулы по концам).

5.5 `rustinpy.graph`

* BFS, DFS (итеративный), 0-1 BFS (ICPC-UZ 2024 I), Dijkstra, Bellman-Ford (+ поиск отрицательного цикла с выводом), Floyd-Warshall, Dijkstra на состояниях «вершина + терминал».
* Топологическая сортировка (Kahn), подсчёт путей на DAG, самый длинный путь.
* DSU (rank + path compression, откат/rollback-версия), Kruskal, Prim.
* SCC (Tarjan и Kosaraju, итеративные), конденсация, 2-SAT (Giant Pizza), мосты и точки сочленения.
* Эйлеров путь и цикл (неориентированный и ориентированный), Hierholzer.
* Функциональные графы: binary lifting по функции, Planets Cycles/Queries (ICPC-UZ 2023 E «Escalators»: граф движения, цикл или выход, запросы с изменением одной вершины).
* Потоки: Dinic, Edmonds-Karp, min-cut (восстановление разреза), реберно-непересекающиеся пути, Hopcroft-Karp, паросочетание по Куну, назначение задач (Hungarian).
* Hamiltonian path (bitmask), Knight's Tour (эвристика Варнсдорфа), Graph Girth, Shortest cycle.
* Advanced: Tree Isomorphism (хеширование AHU), Critical Cities (dominators упрощённо), Flight Route Requests, Network Renovation, Bus Companies, Strongly Connected Edges, Even Outdegree Edges.

5.6 `rustinpy.tree`

* Диаметр, центроид, subtree sizes, Euler tour (tin/tout), LCA (binary lifting и Euler + sparse table), расстояния в дереве, rerooting DP (Tree Distances I/II), Tree Matching, Counting Paths (разности на дереве), HLD + сегментное дерево (Path Queries I/II), Centroid decomposition (Fixed-Length Paths I/II), Distinct Colors (small-to-large / Euler + offline), Subtree Queries.
* ICPC-UZ 2025 F «Fix the Leak»: дерево родителей `p_i < i`, удаление ровно k «агентов» с цепочками, минимизация листьев. Реализуй решение и опиши идею в докстринге.

5.7 `rustinpy.ds` (Range Queries и структуры данных)

* Prefix sums 1D/2D, Fenwick (точечное обновление, обновление на отрезке, 2D, поиск k-го), Sparse Table (min/max/gcd), Segment Tree (несколько вариантов: сумма, min, max-subarray-sum, с lazy: assign/add/sum, «слияние узлов» для хранения префикс/суффикс/лучшая серия). ICPC-UZ 2025 H «Headquarter Reforms»: инверсия отрезка и подсчёт суммы по сериям единиц.
* Persistent segment tree, Merge Sort Tree, Wavelet/offline k-th, Mo's algorithm (+ с обновлениями), sqrt decomposition, Treap/implicit treap (Cut and Paste, Substring Reversals), Order statistics tree.
* Distinct Values Queries (offline + BIT), Movie Festival Queries, Missing Coin Sum Queries.
* Dynamic Connectivity (offline, divide & conquer + rollback DSU), New Roads Queries.
* Isotonic regression / PAV (ICPC-UZ 2023 L: монотонная подгонка по МНК с запросами, сумма квадратов как дробь по модулю).
* Монотонная очередь, «стек минимумов», скользящее окно (Sliding Window Sum/Min/Xor/Or/Distinct/ Mode/Mex/Median/Cost/Inversions).
* Mex на подотрезках (ICPC-UZ 2025 E «Exclusions»: f(k) для разбиения на k блоков).
* Эффективная проверка условия «нет повторов на отрезках» с удалением букв (ICPC-UZ 2023 G «Generic Strings»: бинарный поиск по ответу или два указателя).

5.8 `rustinpy.mathx` (в пакете назови `rustinpy.mathx`, чтобы не конфликтовать со `math`)

* `modpow`, `modinv` (ext. gcd), `ext_gcd`, `crt`, `nCr` (факториалы + обратные, плюс Паскаль для составного модуля), `nPr`, multinomial, Catalan, Stirling (1-го и 2-го рода), Bell, Derangements (Christmas Party), Burnside (Counting Necklaces/Grids), inclusion-exclusion (Prime Multiples, Counting Coprime Pairs).
* Решето Эратосфена, линейное решето (spf, φ, μ), сегментированное решето, факторизация, Miller-Rabin (детерминированный для < 2^64) и Pollard rho (ICPC-UZ 2024 E: до 10^18, 2·10^5 запросов), `next_prime`, делители, sum of divisors, `divisor_analysis`.
* Блоки `floor(n/i)` (ICPC-UZ 2023 J: сумма φ или подсчёт взаимно простых пар, 2025 C «Count The Sum Of GCD»).
* Матричная экспонента, линейные рекуррентности (Kitamasa / Berlekamp-Massey), быстрый Фибоначчи (doubling), Цекендорф (представление в Фибоначчи, подсчёт представлений различными числами Фибоначчи, ICPC-UZ 2023 H, 2025 J).
* FFT/NTT (умножение многочленов, свёртка), Gaussian elimination (по модулю и вещественная), System of Linear Equations (CSES), Sum of Four Squares.
* Вероятности/мат. ожидание (Dice Probability, Moving Robots, Candy Lottery), игры.
* Подсчёт строк с минимальным числом смен цифр, мультиномиальные коэффициенты (ICPC-UZ 2025 B: перестановки цифр, модуль 2112025).
* Подсчёт «глубоких» чисел (2024 D: не простое и нет простой подпоследовательности цифр, n до 10^6; запиши в докстринге идею: запрещённые цифры/короткие простые шаблоны).
* Подсчёт игр длины n (2025 I «Infinite Game»: DP по (сумма mod 3, последняя цифра), матрица перехода).
* Подсчёт вероятностей и K для порога (2023 D: `K = ceil(ln(1-p)/ln(1-q))` с аккуратной точностью).

5.9 `rustinpy.bits` (Bitwise)

* Counting Bits, Maximum Xor Subarray (trie), xor basis (линейный базис над GF(2)), Maximum Xor Subset, Number of Subset Xors, K Subset Xors, SOS DP (subset-sum DP), And Subset Count, Hamming Distance.
* FWHT (быстрое преобразование Уолша-Адамара, XOR/AND/OR-свёртка), ICPC-UZ 2025 K «Kenobi and Skywalker»: значения до 511, запросы «есть ли подмножество из c элементов с xor x» (DP по `cnt[x][parity]` или свёртка).

5.10 `rustinpy.strings`

* Z-function, prefix function (KMP), borders, periods, минимальный циклический сдвиг (Booth / Duval), Manacher (All Palindromes), polynomial hashing (одинарный и двойной, 2^61−1), trie, Aho-Corasick, suffix array (O(n log n)) + LCP (Kasai), suffix automaton (Distinct Substrings, Substring Order I/II, Repeating Substring, Substring Distribution), Palindrome Queries (hash + BIT), String Functions, Inverse Suffix Array, Burrows-Wheeler transform, Distinct Subsequences, Shortest Subsequence, Required Substring (DP + KMP).
* Римские цифры (`rustinpy.roman`): `to_roman(n)`, `from_roman(s)`, `is_valid_roman(s)`, три задачи ICPC-UZ: 2023 C (симметрии), 2024 E (единственность представления в виде произведения римских чисел > 1, n до 10^18), 2025 G «Governor Scroogius» (максимальная и минимальная разбивка строки на корректные римские числа, разность n, кратчайшая лексикографически минимальная строка).
* Простые строковые задачи: 2023 B «Brands» (вставка минимального числа букв для чередования гласных/согласных, лексикографически минимально), 2024 K (апострофы в числах).

5.11 `rustinpy.geometry`

* Point/Vector, cross, dot, ориентация, Point Location Test, пересечение отрезков (+ точки пересечения), площадь многоугольника (знаковая), point in polygon, Pick (Polygon Lattice Points), convex hull (Andrew monotone chain), closest pair (divide & conquer и sweep line), maximum/all Manhattan distances (поворот на 45°), Intersection Points (sweep line), Area of Rectangles (segment tree + sweep), Robot Path, Lines and Queries (CHT / Li Chao), Line Segments Trace.
* 3D: детерминант, объёмы, «лежат ли в одной плоскости с началом координат» (ICPC-UZ 2025 D «Death Star N»: минимальное число искажаемых координат, перебор подмножеств, `det == 0` как многочлен по искажаемым переменным).
* Маршрут биатлониста (ICPC-UZ 2023 K: минимальная длина без самопересечений, пары стрельбищ, геометрия + DP по подмножествам или паросочетание): опиши в докстринге, что это «трудная» задача и реализуй базовую версию (проверка пересечений + DP по подмножествам для малых N).

5.12 `rustinpy.game` (Game Theory)

* Nim I/II, Sprague-Grundy (общий подсчёт grundy через mex), Stair Game, Grundy's Game, Stick Game, Another Game, misère Nim.

5.13 `rustinpy.counting` (Counting Problems, Additional Problems I/II)

* Подсчёт подсеток (Filled Subgrid Count и аналоги, стек), Counting Bishops, Counting Permutations, Permutation Inversions, Counting Reorders, Grid Completion, Raab Game, Functional Graph Distribution, Empty String, Counting Sequences, Tournament Graph Distribution (реализуй хотя бы базовые формулы и DP; для самых редких задач допускается «заглушка с ссылкой на CSES и описанием идеи»).
* Additional Problems I/II: Maximum Building I/II (гистограмма), Cyclic Array, Sorting Methods, Bubble Sort Rounds, Programmers and Artists, Coding Company, Two Stacks Sorting, Stick Divisions, Swap Round Sorting, Binary Subsequences, School Excursion, Coin Grid, Coin Arrangement, Grid Puzzle I/II, Book Shop II и другие. Приоритет у тех, что есть в списке «Что чаще всего встречается».

5.14 `rustinpy.misc` (мелкие задачи ICPC-UZ, где нужна быстрая реализация)

* 2023 A «Attacks Number» (минимум успешных атак при ходах 2 и 3 очка).
* 2024 A «A+Branding» (минимум совместных задач по структуре A/B/C).
* 2024 B «Big Deadline» (подсчёт порядков двух исполнителей: D-задачи раньше T-задач; подсчёт по модулю 998244353).
* 2024 C «Certainly Best» (уникальные непустые подмножества друзей, минимальная суммарная мощность).
* 2024 G «Great Sign» (минимальное максимальное число с представлением всех b цифр ровно по разу).
* 2024 H «Hidden Pieces» (шахматная туманная видимость, симуляция).
* 2024 L «Laura and Arrays» (случайные данные, максимум скалярного произведения; жадность по случайности).
* 2025 A «A Problems and A Balloons» (простая), 2025 L «Limit The Arrow» (f(i) для всех i, DP/структура), 2025 M «Minimum Number of Tasks» (простая, но аккуратно).
* Для каждой: отдельная функция + докстринг с формулировкой в 1–2 строки, идеей решения и сложностью. Если решение мне неизвестно или сложное, напиши честный комментарий `# NOT VERIFIED` вместо выдумки.

6. Тесты и качество (обязательно)

* `pytest`, покрытие каждого публичного алгоритма минимум одним тестом.
* Для всего нетривиального пиши brute-force и сравнивай на случайных малых данных (например, Dijkstra против Floyd, сегментное дерево против наивного массива, LCA против прямого подъёма, Dinic против перебора разрезов на малых графах, Pollard rho против пробного деления, FWHT против наивной свёртки, суффиксный массив против сортировки суффиксов, Aho-Corasick против `str.find`).
* Тесты на производительность (маркер `slow`): типичные пределы 2·10^5 / 10^6 должны укладываться в разумное время на CPython (оцени и зафиксируй). Если алгоритм в чистом Python заведомо не успеет (например, 10^6 с лишним лог), отметь это в докстринге строкой `Python speed:`.
* `ruff` (lint + format), `mypy --strict` для публичного API.
* Doctest в каждом докстринге проходит.
* CI: GitHub Actions на Python 3.9–3.13.

7. Служебные возможности

* `rustinpy.show("dijkstra")` печатает исходный код функции с комментариями (через `inspect.getsource`).
* `rustinpy.search("lca")` ищет по названию, тегам и докстрингам и печатает список подходящих.
* CLI (`[project.scripts] rustinpy = "rustinpy.cli:main"`):
   * `rustinpy list [--module graph]` список алгоритмов по модулям,
   * `rustinpy show <name>` исходник,
   * `rustinpy search <query>`,
   * `rustinpy export --modules graph,tree --out trd.txt` собирает выбранные алгоритмы в один текстовый файл для вставки в TRD (моноширинный, без лишнего, с оглавлением).
* Реестр: декоратор `@algo(tags=[...], cses=[...], icpc=[...])`, который регистрирует функцию в каталоге. `scripts/gen_catalog.py` строит `docs/CATALOG.md` (таблица: модуль, имя, сложность, задачи CSES/ICPC-UZ, теги).

8. README (русский + английский)
Содержит: что это, установка (`pip install rustinpy`), быстрый старт (3–4 примера), таблицу модулей, ссылку на `docs/CATALOG.md`, примеры CLI, раздел «Как использовать для TRD» (правила ICPC/NERC: до 25 страниц A4 с одной стороны; библиотека помогает подготовить, а не заменяет собственный TRD), раздел «Ограничения» (скорость CPython, некоторые алгоритмы упрощены), лицензия.
9. Порядок работы (спека прежде кода)

1. Сначала создай `docs/SPEC.md` (модули, список функций, сигнатуры) и покажи мне на подтверждение. Не пиши код, пока я не одобрю.
2. Работай этапами и после каждого этапа коммить и обновляй `docs/PROGRESS.md`:
   * Этап 1: каркас (pyproject, CLI, реестр, io, interactive, CI) + `mathx` и `ds`.
   * Этап 2: `graph`, `tree`.
   * Этап 3: `dp`, `strings` (+ roman), `bits`.
   * Этап 4: `geometry`, `game`, `introductory`, `sorting`.
   * Этап 5: `counting`, `misc`, README, каталог.
3. Каждая зафиксированная идея «NOT VERIFIED» перечислена в `docs/PROGRESS.md`, чтобы я знал, что проверять руками. Не выдумывай решения. Если не уверен, так и пиши.
4. Git: осмысленные коммиты (`feat(graph): add dinic`), без `git add -A` без проверки, не коммить `dist/`, `.venv`, токены.

10. Публикация на PyPI (аккуратно)

* Сборка: `python -m build`, проверка: `twine check dist/*`.
* Сначала TestPyPI. Установи оттуда в чистое окружение и прогони тесты (`pip install -i https://test.pypi.org/simple/ rustinpy`).
* Основная публикация: PyPI Trusted Publishing через GitHub Actions (`publish.yml`, триггер на тег `v*`), без токенов в репозитории. Если Trusted Publishing не настроен, используй токен из переменной окружения `PYPI_API_TOKEN`; никогда не вписывай токены в файлы, коммиты или логи.
* НЕ публикуй на PyPI самостоятельно. Подготовь всё и дай мне чек-лист из точных шагов (регистрация проекта, настройка Trusted Publisher, создание тега). Публикация только после моей явной команды.
* Закрепи версию: `0.1.0`; дальше SemVer, записи в `CHANGELOG.md`.

11. Критерии готовности

* [ ] `pip install .` в чистом venv работает, `import rustinpy` без ошибок, зависимостей нет.
* [ ] Все алгоритмы из раздела 5 реализованы, либо явно помечены `NOT VERIFIED` / заглушкой с причиной.
* [ ] Каждый алгоритм: докстринг по шаблону, doctest, тест; нетривиальные проверены brute-force.
* [ ] `rustinpy list/show/search/export` работают.
* [ ] `docs/CATALOG.md` сгенерирован, README готов на двух языках.
* [ ] `ruff`, `mypy`, `pytest` зелёные на Python 3.9–3.13.
* [ ] `twine check` проходит, пакет установился из TestPyPI.
* [ ] Чек-лист публикации на PyPI выдан мне, публикации ещё нет.

Начни с проверки имени `rustinpy` на PyPI и создания `docs/SPEC.md`.
