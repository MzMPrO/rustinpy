# rustinpy

**RU:** шпаргалка алгоритмов для ICPC и CSES в виде Python-пакета. ·
**EN:** an ICPC / CSES algorithms cheat sheet as a Python package — [English below](#english).

```bash
pip install rustinpy
rustinpy show dijkstra
```

---

## Русский

### Что это

`rustinpy` — около 450 самодостаточных функций и классов на чистом Python 3.9+ (только
стандартная библиотека) по темам CSES Problem Set и задачам ICPC Uzbekistan 2023–2025.
У каждой функции есть докстринг-конспект («когда применять», сложность, подводные камни,
задачи CSES / ICPC-UZ), русская подсказка в первой строке и работающий doctest. Всё проверено
тестами против перебора на случайных данных.

Для чего пакет нужен:
- **тренировка** — импортировать готовую функцию и сосредоточиться на задаче;
- **поиск** — быстро найти нужный алгоритм и посмотреть его исходник;
- **TRD** — собрать выбранные алгоритмы в один файл для командного справочника.

### Установка

```bash
pip install rustinpy
```

Нужен Python 3.9–3.13, зависимостей нет. Для разработки:
`pip install -e ".[dev]"` в клоне репозитория.

### Быстрый старт

```python
from rustinpy.graph import dijkstra
from rustinpy.mathx import Comb

adj = [[(1, 4), (2, 1)], [(3, 1)], [(1, 2), (3, 5)], []]
print(dijkstra(4, adj, 0))  # [0, 3, 1, 4]

c = Comb(10**6)  # факториалы по модулю 998244353
print(c.nCr(10, 3))  # 120

import rustinpy

rustinpy.search("lca")  # найти по имени, тегам, задачам и докстрингам
rustinpy.show("LCA")  # исходник вместе с нужными константами и вспомогалками
rustinpy.help("dijkstra")  # докстринг-конспект
```

Соглашения: индексация с 0, отрезки полуинтервалами `[l, r)`, `INF = 1 << 60`,
`MOD = 998244353`, `MOD7 = 10**9 + 7`. Функции принимают данные аргументами и не читают stdin.
Быстрый ввод-вывод — в `rustinpy.io` (`rustinpy show fast_io_template`).

### Модули

| Модуль | Что внутри |
|---|---|
| `io` | быстрый ввод-вывод, шаблон решения |
| `interactive` | шаблоны интерактивных задач (`make_ask`, бинпоиск по ответам) |
| `mathx` | модульная арифметика, комбинаторика, решёта, Миллер-Рабин и Поллард, φ и μ, матрицы, свёртки (NTT, через decimal), Гаусс, вероятности |
| `ds` | префиксные суммы, Фенвик, sparse table, деревья отрезков (ленивые, персистентные), Мо, декартово дерево, SortedList, оффлайн-запросы, окна |
| `graph` | обходы, кратчайшие пути, DAG, DSU и MST, SCC и 2-SAT, мосты, Эйлер, функциональные графы, потоки, паросочетания |
| `tree` | диаметр, LCA, HLD, центроиды, Euler tour, изоморфизм |
| `dp` | рюкзаки, LIS/LCS, DP по маскам, профилю и цифрам, CHT/Li Chao, D&C и Кнут |
| `strings` | Z, префикс-функция, хеши, бор, Ахо-Корасик, суффиксный массив и автомат, Манакер, BWT |
| `roman` | римские числа и задачи ICPC-UZ на них |
| `bits` | битовые трюки, xor-базис, SOS DP, преобразования Уолша-Адамара |
| `geometry` | точная геометрия на целых: оболочка, ближайшая пара, сканирование, 3D |
| `game` | Ним, Шпраг-Гранди |
| `introductory` | вводные задачи CSES и конструктивы (Прюфер, де Брёйн, Грей) |
| `sorting` | бинпоиск по ответу, два указателя, расписания, Иосиф, скользящая медиана |
| `counting` | подсчёты и конструктивы CSES: слоны, турниры, функциональные графы, Кёниг, потоки на сетке |
| `misc` | короткие задачи ICPC-UZ |

Полный список с асимптотикой, задачами и статусом проверки — [docs/CATALOG.md](https://github.com/MzMPrO/rustinpy/blob/main/docs/CATALOG.md).

### CLI

```bash
rustinpy list                          # все алгоритмы по модулям
rustinpy list --module graph --tag flow
rustinpy list --unverified             # что помечено NOT VERIFIED или заглушка
rustinpy search suffix                 # поиск
rustinpy show dijkstra                 # исходник без @algo, с зависимостями
rustinpy show graph.dijkstra --raw     # как в пакете
rustinpy export --modules graph,tree --out trd.txt
rustinpy export --names dijkstra,LCA,Dinic --out trd.md --docstrings none
rustinpy --version
```

`export` собирает один файл: оглавление с номерами строк, общая шапка импортов stdlib, затем
блоки `# ==== модуль.имя ====`. Ширина строки ≤ 100 символов, `@algo` и импорты `rustinpy`
вырезаны, константы и вспомогалки подставлены. `--docstrings full|short|none` (по умолчанию
`short`: первая строка и сложность).

### TRD (командный справочник)

На ICPC можно взять распечатанный справочник: **до 25 страниц A4, печать с одной стороны**
(проверьте правила своего соревнования). `rustinpy` помогает его подготовить, но не заменяет:
отбирать алгоритмы, которые команда понимает и умеет применять, и проверять распечатку нужно
самим.

```bash
python scripts/export_trd.py --modules graph,tree,strings --out trd.txt --docstrings none
```

Скрипт печатает число строк и грубую оценку страниц (две колонки мелкого моноширинного
шрифта). Весь пакет целиком в 25 страниц не помещается: выбирайте модули и имена. Каждый блок
самодостаточен, его можно вставить в решение как есть.

### Ограничения

- Это CPython: часть алгоритмов медленнее ориентира контеста. Такие места помечены строкой
  `Python speed:` в докстринге, замеры — в [docs/PROGRESS.md](https://github.com/MzMPrO/rustinpy/blob/main/docs/PROGRESS.md).
- Условия задач ICPC Uzbekistan 2023–2025 в открытом доступе не найдены. Решения по ним
  (и несколько задач CSES, условие которых восстановлено по памяти) помечены `NOT VERIFIED`,
  неясные — заглушками с идеей решения. Список — в docs/PROGRESS.md и
  `rustinpy list --unverified`.
- Без рекурсии (кроме глубины O(log n)), но глубокие структуры в Python всё равно требуют
  памяти: на больших n следите за лимитом.
- Тесты гоняются на CPython 3.9–3.13; PyPy не проверялся.

### Лицензия

MIT, © Mirahmad. См. [LICENSE](https://github.com/MzMPrO/rustinpy/blob/main/LICENSE).

---

## English

### What it is

`rustinpy` is about 450 self-contained functions and classes in pure Python 3.9+ (standard
library only) covering the CSES Problem Set topics and ICPC Uzbekistan 2023–2025 problems.
Every function has a cheat-sheet docstring (when to use, complexity, pitfalls, CSES / ICPC-UZ
problems), a Russian hint on the first line and a working doctest. Everything is tested against
brute force on random data.

Use it for:
- **practice**: import a ready function and focus on the problem;
- **lookup**: find an algorithm quickly and read its source;
- **TRD**: collect selected algorithms into a single file for the team reference document.

### Installation

```bash
pip install rustinpy
```

Python 3.9–3.13, no dependencies. For development: `pip install -e ".[dev]"` in a clone.

### Quick start

```python
from rustinpy.graph import dijkstra
from rustinpy.mathx import Comb

adj = [[(1, 4), (2, 1)], [(3, 1)], [(1, 2), (3, 5)], []]
print(dijkstra(4, adj, 0))  # [0, 3, 1, 4]

c = Comb(10**6)  # factorials modulo 998244353
print(c.nCr(10, 3))  # 120

import rustinpy

rustinpy.search("lca")  # search names, tags, problems and docstrings
rustinpy.show("LCA")  # source together with the constants and helpers it needs
rustinpy.help("dijkstra")  # the cheat-sheet docstring
```

Conventions: 0-based indices, half-open ranges `[l, r)`, `INF = 1 << 60`, `MOD = 998244353`,
`MOD7 = 10**9 + 7`. Functions take their data as arguments and never read stdin; fast I/O lives
in `rustinpy.io` (`rustinpy show fast_io_template`).

### Modules

| Module | Contents |
|---|---|
| `io` | fast input / output, solution template |
| `interactive` | interactive problem templates (`make_ask`, binary search on answers) |
| `mathx` | modular arithmetic, combinatorics, sieves, Miller-Rabin and Pollard rho, phi and mu, matrices, convolutions (NTT, decimal-based), Gauss, probability |
| `ds` | prefix sums, Fenwick, sparse table, segment trees (lazy, persistent), Mo, treap, SortedList, offline queries, sliding windows |
| `graph` | traversals, shortest paths, DAG, DSU and MST, SCC and 2-SAT, bridges, Euler, functional graphs, flows, matchings |
| `tree` | diameter, LCA, HLD, centroids, Euler tour, isomorphism |
| `dp` | knapsacks, LIS / LCS, bitmask, profile and digit DP, CHT / Li Chao, D&C and Knuth |
| `strings` | Z, prefix function, hashing, trie, Aho-Corasick, suffix array and automaton, Manacher, BWT |
| `roman` | Roman numerals and the ICPC-UZ problems built on them |
| `bits` | bit tricks, xor basis, SOS DP, Walsh-Hadamard transforms |
| `geometry` | exact integer geometry: hull, closest pair, sweeps, 3D |
| `game` | Nim, Sprague-Grundy |
| `introductory` | CSES introductory problems and constructions (Prufer, de Bruijn, Gray) |
| `sorting` | binary search on the answer, two pointers, scheduling, Josephus, sliding median |
| `counting` | CSES counting and construction problems: bishops, tournaments, functional graphs, Koenig, grid flows |
| `misc` | short ICPC-UZ problems |

The full list with complexities, problems and verification status is in
[docs/CATALOG.md](https://github.com/MzMPrO/rustinpy/blob/main/docs/CATALOG.md).

### CLI

```bash
rustinpy list                          # all algorithms by module
rustinpy list --module graph --tag flow
rustinpy list --unverified             # NOT VERIFIED items and stubs
rustinpy search suffix
rustinpy show dijkstra                 # source without @algo, with its dependencies
rustinpy show graph.dijkstra --raw     # as written in the package
rustinpy export --modules graph,tree --out trd.txt
rustinpy export --names dijkstra,LCA,Dinic --out trd.md --docstrings none
rustinpy --version
```

`export` writes one file: a table of contents with line numbers, one shared header of stdlib
imports, then blocks `# ==== module.name ====`. Lines are at most 100 characters, `@algo` and
`rustinpy` imports are removed, constants and helpers are included. `--docstrings
full|short|none` (default `short`: first line and complexity).

### TRD (team reference document)

ICPC allows a printed reference document: **up to 25 A4 pages, printed on one side** (check
the rules of your contest). `rustinpy` helps you prepare it but does not replace it: the team
still has to choose algorithms it understands and check the printout.

```bash
python scripts/export_trd.py --modules graph,tree,strings --out trd.txt --docstrings none
```

The script prints the number of lines and a rough page estimate (two columns of small
monospace). The whole package does not fit into 25 pages, so pick modules and names. Every
block is self-contained and can be pasted into a solution as is.

### Limitations

- This is CPython: some algorithms are slower than a typical contest limit. They carry a
  `Python speed:` line in the docstring; measurements are in [docs/PROGRESS.md](https://github.com/MzMPrO/rustinpy/blob/main/docs/PROGRESS.md).
- Statements of the ICPC Uzbekistan 2023–2025 problems were not found publicly. Solutions for
  them (and a few CSES problems whose statements were reconstructed from memory) are marked
  `NOT VERIFIED`; unclear ones are stubs with a solution idea. See docs/PROGRESS.md and
  `rustinpy list --unverified`.
- No recursion (except O(log n) depth), but large structures still need memory in Python:
  keep an eye on the memory limit for big n.
- Tests run on CPython 3.9–3.13; PyPy is not tested.

### License

MIT, © Mirahmad. See [LICENSE](https://github.com/MzMPrO/rustinpy/blob/main/LICENSE).
