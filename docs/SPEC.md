# ТЗ: rustinpy — шпаргалка алгоритмов для ICPC в виде Python-пакета

> **Статус:** УТВЕРЖДЕНО
> Статус УТВЕРЖДЕНО ставится, когда пользователь пишет «утверждаю».
> Исходное задание: [docs/handoff/000-kickoff.md](handoff/000-kickoff.md). Там, где спека и задание расходятся, спека уточняет задание; все такие места перечислены в разделах 11 «Допущения» и 12 «Открытые вопросы».

## 1. Цель

Пакет `rustinpy` (`pip install rustinpy`) с готовыми, проверенными тестами реализациями алгоритмов для ICPC: темы CSES Problem Set и задачи ICPC Uzbekistan Regional 2023–2025. У каждого алгоритма есть докстринг-конспект и рабочий doctest, его можно скопировать в TRD без самого пакета.

Проект удался, если:
- `from rustinpy.graph import dijkstra` работает сразу после установки;
- любой алгоритм можно выгрузить командой `rustinpy export`, и выгруженный код проходит свой doctest без установленного пакета;
- все проверки зелёные на Python 3.9–3.13, пакет готов к публикации на PyPI (публикует пользователь сам).

## 2. Пользователи и роли

| Роль | Кто это | Что может |
|---|---|---|
| Участник команды | Мирахмад и команда | Тренируется с импортом из пакета, смотрит исходники, собирает TRD |
| Мейнтейнер | Мирахмад | Утверждает спеку, проверяет пункты `NOT VERIFIED`, публикует релизы на PyPI |
| Строитель | Claude Code | Пишет код и тесты по утверждённой спеке, готовит публикацию, но не публикует |

## 3. Основные сценарии

1. **Тренировка.** `pip install rustinpy` → `from rustinpy.graph import dijkstra` → вызов. Результат: функция работает, подсказка в `help(dijkstra)`.
2. **Подготовка TRD.** `rustinpy export --modules graph,tree --out trd.txt` → один моноширинный файл с оглавлением, без декораторов и служебных импортов, с нужными вспомогалками и константами. Результат: файл можно вставить в TRD, каждая функция в нём самодостаточна.
3. **Поиск.** `rustinpy search lca` → список «модуль.имя — первая строка докстринга». `rustinpy show lca` → исходник. Те же функции доступны из Python: `rustinpy.search("lca")`, `rustinpy.show("lca")`.
4. **Контест-шаблон.** `rustinpy show fast_io_template` → 10 строк быстрого ввода-вывода, которые копируются в решение.

## 4. Функциональные требования

### Обязательно (0.1.0)
- [ ] Модули из раздела 4.3 с функциями и сигнатурами из него.
- [ ] Реестр `@algo`, функции `show`, `search`, `list_algos`, `help`.
- [ ] CLI `rustinpy list | show | search | export`.
- [ ] `scripts/gen_catalog.py` → `docs/CATALOG.md`; `scripts/export_trd.py` (обёртка над `export`).
- [ ] Тесты, brute-force сравнения, slow-бенчмарки, CI, publish-workflow, README RU+EN, CHANGELOG.

### Желательно (после 0.1.0)
- Покрытие оставшихся задач CSES, которые не перечислены в разделе 4.3 (Forbidden Cities, Visiting Cities, Network Breakdown, Increasing Array Queries и т.п.).
- Русские формулировки задач ICPC-UZ в CATALOG.
- `rustinpy export --format pdf` (через внешний инструмент).

### Не делаем (вне рамок)
- Зависимости времени выполнения (numpy, sortedcontainers и т.п.).
- Решения целиком «под ввод CSES» (чтение stdin внутри функции). Функции принимают данные аргументами; шаблон ввода отдельно в `io`.
- Самостоятельная публикация на PyPI.

### 4.1 Общие правила для каждого алгоритма

**Реестр и самодостаточность.**
```python
@algo(tags=["shortest-path"], cses=["Shortest Routes I (1671)"], icpc=[], requires=["INF"])
def dijkstra(n: int, adj: list[list[tuple[int, int]]], src: int) -> list[int]: ...
```
- `algo()` регистрирует функцию или класс и **возвращает исходный объект без обёртки**. Поэтому `inspect.getsource`, doctest и скорость не страдают.
- `requires=[...]` перечисляет имена из того же модуля (константы, приватные вспомогалки `_xxx`), без которых код не запустится. `show` и `export` печатают их перед функцией.
- Импортировать другие модули `rustinpy` внутри алгоритмов нельзя. Общие вспомогалки (Fenwick, DSU, mex и т.п.) дублируются в виде приватных `_Fenwick`, `_DSU` рядом с тем, кому они нужны. Разрешены только импорты из стандартной библиотеки: `heapq`, `bisect`, `collections`, `math`, `random`, `itertools`, `sys`, `typing`, `fractions`, `functools`.
- `verified=False` у алгоритма ставится, если решение не подтверждено условием или тестами против эталона. Такой алгоритм в теле и докстринге содержит строку `# NOT VERIFIED: <причина>`, а в `docs/PROGRESS.md` он попадает в список ручной проверки.
- Заглушка `stub=True`: функция бросает `NotImplementedError`, в докстринге есть ссылка на задачу, идея решения и причина, почему не реализовано.

**Докстринг.** Шаблон из задания, раздел 4. Обязательные поля: первая строка (английский + `# русская подсказка`), `When to use:`, `Complexity:`, `Returns:`, `CSES:` и/или `ICPC-UZ:` (значение `—` разрешено для чисто служебных функций), `Example:` с doctest. Необязательные поля: `Input:`, `Pitfalls:`, `Related:`, `Python speed:`, `Idea:` (обязательно для задач ICPC-UZ). Порядок полей фиксированный. Его проверяет тест.

**Код.**
- Индексация 0-based, если в докстринге не сказано иное.
- `INF = 1 << 60` в каждом модуле, где нужен; `MOD = 998244353`; функции принимают `mod: int = MOD`.
- Без рекурсии. Исключения допустимы только там, где глубина O(log n) (D&C closest pair, D&C-оптимизация, FFT), и такие функции явно перечислены в whitelist теста.
- Русские комментарии к ключевым шагам в теле функции.
- Совместимость с 3.9: `from __future__ import annotations` в каждом модуле, никаких `X | Y` и `list[int]` в выражениях, которые выполняются во время работы (алиасы типов пишем через `typing`), никакого `match`, `int.bit_count` (только `bin(x).count("1")`), `math.lcm`, `itertools.pairwise`.
- Графы задаются списком смежности `adj: list[list[int]]` или `list[list[tuple[int, int]]]` (вершина, вес). Если удобнее список рёбер, это `edges: list[tuple[int, int]]` или `list[tuple[int, int, int]]`, и выбор указан в `Input:`.

### 4.2 Служебные модули

```python
# rustinpy/__init__.py
__version__: str = "0.1.0"
def show(name: str, *, raw: bool = False) -> None          # печатает исходник (+ requires), без @algo, если raw=False
def search(query: str, *, module: str | None = None) -> list[AlgoInfo]   # печатает и возвращает совпадения
def list_algos(module: str | None = None) -> list[AlgoInfo]
def help(name: str | None = None) -> None                    # обзор модулей или докстринг алгоритма
# сами алгоритмы на верхний уровень НЕ реэкспортируются (см. Допущения A-3)

# rustinpy/_registry.py
@dataclass(frozen=True)
class AlgoInfo:
    module: str            # "graph"
    name: str              # "dijkstra"
    qualname: str          # "graph.dijkstra"
    obj: object
    tags: tuple[str, ...]
    cses: tuple[str, ...]
    icpc: tuple[str, ...]
    requires: tuple[str, ...]
    complexity: str        # берётся из строки "Complexity:" докстринга
    summary: str           # первая строка докстринга
    verified: bool
    stub: bool
def algo(*, tags: Sequence[str] = (), cses: Sequence[str] = (), icpc: Sequence[str] = (),
         requires: Sequence[str] = (), verified: bool = True, stub: bool = False) -> Callable[[T], T]
def load_all() -> None                                     # импортирует все модули алгоритмов
def resolve(name: str) -> AlgoInfo                          # "dijkstra" или "graph.dijkstra"; неоднозначно -> ValueError со списком
def source_of(info: AlgoInfo, *, with_requires: bool = True, strip_decorator: bool = True) -> str

# rustinpy/cli.py   ([project.scripts] rustinpy = "rustinpy.cli:main")
def main(argv: list[str] | None = None) -> int
#   rustinpy list [--module M] [--tag T] [--unverified]
#   rustinpy show NAME [--raw]
#   rustinpy search QUERY [--module M]
#   rustinpy export --modules graph,tree | --names dijkstra,lca  --out trd.txt|trd.md
#                   [--docstrings full|short|none]  (short = первая строка + Complexity; по умолчанию short)
#   rustinpy --version
```
Формат `export`: оглавление (номер, `модуль.имя`, номер строки), затем блоки `# ==== graph.dijkstra ====`, ширина строки не больше 100 символов, без `@algo`, без `from rustinpy...`. Импорты stdlib собираются в шапку файла один раз.

### 4.3 Алгоритмы по модулям

Обозначения: `[NV]` — `verified=False` (`NOT VERIFIED`), `[stub]` — заглушка, `[slow]` — в докстринге будет строка `Python speed:`. Сигнатуры даны для понимания объёма. Мелкие правки имён и параметров при реализации допустимы, если они не меняют смысла. Крупные правки идут через «Открытые вопросы».

#### `rustinpy.io` — быстрый ввод-вывод (этап 1)
```python
class FastReader:                       # обёртка над sys.stdin.buffer.read().split()
    def __init__(self, stream: BinaryIO | None = None) -> None
    def int(self) -> int; def ints(self, k: int) -> list[int]
    def str(self) -> str; def strs(self, k: int) -> list[str]; def bytes(self) -> bytes
    def float(self) -> float
class FastWriter:                       # копит куски в список, один sys.stdout.write в конце
    def __init__(self, stream: TextIO | None = None) -> None
    def write(self, *items: object, sep: str = " ", end: str = "\n") -> None
    def write_lines(self, items: Iterable[object]) -> None
    def flush(self) -> None
def read_int() -> int; def read_ints(k: int) -> list[int]; def read_str() -> str   # глобальный ленивый FastReader
def read_all_ints() -> list[int]
def fast_io_template() -> str           # строка-шаблон из 10 строк для копирования в решение
```

#### `rustinpy.interactive` — интерактивные задачи (этап 1)
```python
def make_ask(inp: TextIO | None = None, out: TextIO | None = None) -> Callable[[str], str]
    # ask(q): print(q) + flush; читает строку; "-1" или EOF -> SystemExit(0) (не ловить WA как TLE)
def answer(out_line: str, out: TextIO | None = None) -> None              # "! x" + flush
def interactive_bisect(lo: int, hi: int, is_ge: Callable[[int], bool]) -> int   # Hidden Integer (CSES)
def find_hidden_rectangle(n: int, inside_count: Callable[[int, int, int, int], int]) -> tuple[int, int, int, int]  # [NV] 2024 F
def hidden_permutation(n: int, less: Callable[[int, int], bool]) -> list[int]     # CSES Hidden Permutation, слиянием ~n log n
def kth_highest_score(...)  [NV]   # CSES K-th Highest Score
def permuted_binary_strings(...) [NV]; def colored_chairs(...) [NV]; def inversion_sorting(...) [NV]
ADAPTIVE_NOTE: str     # конспект: адаптивный интерактор, детерминизм, рандомизация, лимит запросов
```
Интерактивные функции получают `ask`/предикат аргументом, поэтому тестируются симулятором интерактора.

#### `rustinpy.mathx` (этап 1)
Пакет: `modular.py, comb.py, primes.py, numtheory.py, matrix.py, poly.py, linalg.py, prob.py, icpc.py`, всё реэкспортируется из `rustinpy.mathx`.
```python
MOD = 998244353; MOD7 = 10**9 + 7
# modular
def modpow(a: int, e: int, mod: int = MOD) -> int
def ext_gcd(a: int, b: int) -> tuple[int, int, int]                 # (g, x, y), итеративно
def modinv(a: int, mod: int = MOD) -> int                            # ValueError, если gcd != 1
def crt(rems: list[int], mods: list[int]) -> tuple[int, int] | None   # общий, модули не обязательно взаимно просты
def exp_tower(a: int, b: int, c: int, mod: int = MOD7) -> int         # Exponentiation II: a^(b^c), mod простой
# comb
class Comb:                                                           # факториалы до n_max, только ПРОСТОЙ mod
    def __init__(self, n_max: int, mod: int = MOD) -> None
    def nCr(self, n: int, r: int) -> int; def nPr(self, n: int, r: int) -> int
    def multinomial(self, ks: list[int]) -> int
def nCr_pascal(n_max: int, mod: int) -> list[list[int]]              # СОСТАВНОЙ mod (2025 B: 2112025), O(n^2)
def nCr_lucas(n: int, r: int, p: int) -> int
def nCr_composite(n: int, r: int, mod: int) -> int                   # через разложение mod и CRT (n до ~10^6)
def catalan(n: int, mod: int = MOD) -> int                           # Bracket Sequences I
def bracket_sequences_prefix(n: int, prefix: str, mod: int = MOD) -> int  # Bracket Sequences II
def stirling1_table(n: int, mod: int = MOD) -> list[list[int]]
def stirling2_table(n: int, mod: int = MOD) -> list[list[int]]
def bell_numbers(n: int, mod: int = MOD) -> list[int]
def derangements(n: int, mod: int = MOD) -> int                      # Christmas Party
def stars_and_bars(n: int, k: int, mod: int = MOD) -> int            # Distributing Apples
def necklaces_count(n: int, m: int, mod: int = MOD7) -> int          # Burnside, Counting Necklaces
def grid_colorings_count(n: int, mod: int = MOD7) -> int             # Burnside, Counting Grids (повороты)
def prime_multiples_count(n: int, primes: list[int]) -> int          # inclusion-exclusion
def coprime_pairs_count(a: list[int]) -> int                         # μ + счётчик кратных
# primes
def sieve(n: int) -> bytearray; def primes_up_to(n: int) -> list[int]
def linear_sieve(n: int) -> tuple[list[int], list[int]]              # (spf, primes)
def phi_table(n: int) -> list[int]; def mobius_table(n: int) -> list[int]
def segmented_sieve(lo: int, hi: int) -> list[int]
def is_prime(n: int) -> bool                                          # детерминированный Miller-Rabin, n < 2^64
def pollard_rho(n: int) -> int                                        # нетривиальный делитель составного n (Брент)
def factorize(n: int) -> dict[int, int]                               # до 10^18 (2024 E) [slow при 2e5 запросов]
def factorize_spf(x: int, spf: list[int]) -> dict[int, int]
def next_prime(n: int) -> int
# numtheory
def divisors(n: int) -> list[int]; def divisor_count_table(n: int) -> list[int]
def sum_of_divisors_sum(n: int, mod: int = MOD7) -> int              # CSES Sum of Divisors, блоки floor(n/i)
def divisor_analysis(pe: list[tuple[int, int]], mod: int = MOD7) -> tuple[int, int, int]  # (кол-во, сумма, произведение)
def common_divisors_max_gcd(a: list[int]) -> int                      # Common Divisors
def euler_phi(n: int) -> int
def floor_blocks(n: int) -> Iterator[tuple[int, int, int]]            # (l, r, n // l)
def phi_prefix_sum(n: int) -> int                                     # Du's sieve, O(n^{2/3}) — 2023 J [NV условие]
def coprime_pairs_up_to(n: int) -> int                                # пары (i, j) <= n, gcd = 1
def gcd_sum_pairs(n: int, mod: int | None = None) -> int              # Σ_{i,j<=n} gcd(i,j) — 2025 C [NV условие]
def gcd_sum_with_n(n: int) -> int                                     # Pillai: Σ_{i<=n} gcd(i, n)
def sum_of_four_squares(n: int) -> tuple[int, int, int, int]
# matrix
def mat_mul(a: list[list[int]], b: list[list[int]], mod: int = MOD) -> list[list[int]]
def mat_pow(m: list[list[int]], e: int, mod: int = MOD) -> list[list[int]]
def minplus_mat_pow(m: list[list[int]], e: int) -> list[list[int]]   # Graph Paths II
def linear_recurrence_kth(coef: list[int], init: list[int], k: int, mod: int = MOD) -> int   # Kitamasa
def berlekamp_massey(seq: list[int], mod: int = MOD) -> list[int]     # простой mod
def fib(n: int, mod: int = MOD7) -> int                               # fast doubling, итеративно
def throwing_dice(n: int, mod: int = MOD7) -> int                     # CSES Throwing Dice
def zeckendorf(n: int) -> list[int]                                   # 2023 H, 2025 J
def count_fib_representations(n: int) -> int                          # число представлений суммой различных Фибоначчи [NV условие]
# poly
def ntt(a: list[int], invert: bool, mod: int = MOD) -> None           # in-place, итеративно
def convolution(a: list[int], b: list[int], mod: int = MOD) -> list[int]
def convolution_int(a: list[int], b: list[int]) -> list[int]          # точная свёртка неотрицательных int через упаковку в big int (быстро на CPython)
def fft_convolution_float(a: list[float], b: list[float]) -> list[float]
# linalg
def gauss_mod(a: list[list[int]], b: list[int], mod: int = MOD7) -> list[int] | None   # System of Linear Equations
def gauss_float(a: list[list[float]], b: list[float], eps: float = 1e-9) -> list[float] | None
def det_mod(a: list[list[int]], mod: int = MOD) -> int
# prob
def dice_probability(n: int, a: int, b: int) -> float
def moving_robots(k: int) -> float
def candy_lottery(n: int, k: int) -> float
def inversion_probability(r: list[int]) -> float
def min_trials_for_probability(p: float, q: float) -> int             # 2023 D: K = ceil(ln(1-p)/ln(1-q)) с проверкой границы [NV условие]
# icpc (задачи ICPC-UZ)
def min_digit_changes_count(counts: list[int], mod: int = 2112025) -> int   # 2025 B [NV]
def deep_numbers_count(n: int) -> int                                 # 2024 D [NV], идея в докстринге
def infinite_game_count(n: int, mod: int = MOD) -> int                # 2025 I [NV], матрица (сумма mod 3, последняя цифра)
```

#### `rustinpy.ds` — структуры данных и запросы на отрезках (этап 1)
Пакет: `prefix.py, fenwick.py, sparse.py, segtree.py, lazy.py, persistent.py, offline.py, mo.py, treap.py, sortedlist.py, sliding.py, connectivity.py, pav.py, icpc.py`.
```python
def prefix_sums(a: list[int]) -> list[int]
class PrefixSum2D:   def __init__(self, grid: list[list[int]]) -> None; def query(self, r1, c1, r2, c2) -> int   # Forest Queries
class Fenwick:       add(i, d); prefix(i) -> int; range_sum(l, r) -> int; kth(k) -> int   # lower_bound по префиксу
class FenwickRangeAdd:  range_add(l, r, d); point(i) -> int                               # Range Update Queries
class FenwickRangeRange: range_add(l, r, d); range_sum(l, r) -> int
class Fenwick2D:     add(r, c, d); query(r1, c1, r2, c2) -> int                           # Forest Queries II
class SparseTable:   def __init__(self, a: list[int], op: Callable[[int, int], int] = min) -> None; query(l, r) -> int   # min/max/gcd
class SegTree:       # итеративный, op + identity: sum/min/max/xor
    __init__(a, op, e); set(i, v); get(i); query(l, r); max_right(l, pred) -> int; min_left(r, pred) -> int
class SegTreeMaxSubarray:   set(i, v); query(l, r) -> int        # (sum, pref, suf, best): Subarray Sum Queries
class SegTreeMaxPrefix:     set(i, v); query(l, r) -> int        # Prefix Sum Queries
class SegTreeRuns:          # «слияние узлов»: длиннейшая серия одинаковых: Bit Inversions
class LazySegAddSum:  range_add(l, r, d); range_sum(l, r)
class LazySegAddMin:  range_add(l, r, d); range_min(l, r)
class LazySegAssignAddSum: range_assign(l, r, v); range_add(l, r, d); range_sum(l, r)   # Range Updates and Sums
class LazySegArithmetic:   add_progression(l, r); range_sum(l, r)                        # Polynomial Queries
class SegTreeFlipRuns:   flip(l, r); query(...)                    # 2025 H «Headquarter Reforms» [NV условие]
class PersistentSegTree:  # массивы left/right/val, без объектов на узел: Range Queries and Copies
def range_kth_smallest(a: list[int], queries: list[tuple[int, int, int]]) -> list[int]   # персистентное дерево по значениям
class MergeSortTree:  count_le(l, r, x) -> int    [slow]
def mo_order(queries: list[tuple[int, int]], block: int | None = None) -> list[int]       # порядок Гильберта/змейка
def mo_distinct_count(a: list[int], queries: list[tuple[int, int]]) -> list[int]          # пример Mo
def mo_with_updates(...)   # пример: distinct на отрезке с точечными изменениями [slow]
class SqrtDecomposition: point_set(i, v); range_sum(l, r)
class Treap:          # массивный, по ключам: insert/erase/kth/rank
class ImplicitTreap:  # split/merge, reverse lazy; to_list()
def cut_and_paste(s: str, ops: list[tuple[int, int]]) -> str          # CSES Cut and Paste
def substring_reversals(s: str, ops: list[tuple[int, int]]) -> str    # CSES Substring Reversals
def reversal_sorting(p: list[int]) -> list[tuple[int, int]]           # CSES Reversal Sorting [slow]
class SortedList:     # корзинный (sqrt) список: add/remove/bisect/kth, order-statistics tree для Python
def hotel_queries(h: list[int], groups: list[int]) -> list[int]
def list_removals(a: list[int], pos: list[int]) -> list[int]
def salary_queries(p: list[int], ops: list[tuple]) -> list[int]
def pizzeria_queries(...) -> list[int]
def distinct_values_queries(a: list[int], queries: list[tuple[int, int]]) -> list[int]   # offline + BIT
def movie_festival_queries(movies: list[tuple[int, int]], queries: list[tuple[int, int]]) -> list[int]   # binary lifting
def missing_coin_sum_queries(a: list[int], queries: list[tuple[int, int]]) -> list[int]
def dynamic_connectivity_offline(n: int, ops: list[tuple[int, int, int]]) -> list[int]   # D&C по времени + RollbackDSU
def new_roads_queries(n: int, edges: list[tuple[int, int]], queries: list[tuple[int, int]]) -> list[int]  # параллельный бинпоиск или DSU по времени
class MonotonicQueue: push(x); pop(); min() / max()
class MinStack; class TwoStackQueue:  # моноид: xor/or/gcd в окне
def sliding_window_sum / _min / _xor / _or (a: list[int], k: int) -> list[int]
def sliding_window_distinct(a, k) -> list[int]; def sliding_window_mode(a, k) -> list[int]
def sliding_window_mex(a, k) -> list[int]; def sliding_window_inversions(a, k) -> list[int]
def pav(y: list[int], w: list[int] | None = None) -> list[tuple[int, int, Fraction]]   # блоки (l, r, среднее)
def isotonic_sse_mod(y: list[int], mod: int = MOD) -> int             # 2023 L, сумма квадратов как дробь по модулю [NV запросы]
def subarray_mex_offline(a: list[int], queries: list[tuple[int, int]]) -> list[int]
def exclusions(a: list[int]) -> list[int]                              # 2025 E: f(k) для k = 1..n [NV]
def longest_window_no_repeats(s: str) -> int                           # строительный блок
def generic_strings(...)                                                # 2023 G [NV]
```

#### `rustinpy.graph` (этап 2)
Пакет: `traversal.py, shortest.py, dag.py, dsu.py, mst.py, scc.py, euler.py, functional.py, flow.py, matching.py, paths.py, advanced.py, icpc.py`.
```python
INF = 1 << 60
# traversal
def bfs(n, adj, src) -> list[int]; def bfs_path(n, adj, src, dst) -> list[int] | None       # Message Route
def multi_source_bfs(n, adj, sources) -> list[int]                                           # Monsters
def grid_bfs(grid: list[str], start: tuple[int, int], wall: str = "#") -> list[list[int]]   # Labyrinth
def dfs_order(n, adj, src) -> tuple[list[int], list[int]]                                    # итеративный: порядок, родители
def connected_components(n, adj) -> tuple[int, list[int]]                                    # Building Roads, Counting Rooms
def bipartite_coloring(n, adj) -> list[int] | None                                           # Building Teams
def find_cycle_undirected(n, adj) -> list[int] | None                                        # Round Trip
def find_cycle_directed(n, adj) -> list[int] | None                                          # Round Trip II
def girth(n, adj) -> int                                                                     # Graph Girth, O(n·m)
# shortest
def zero_one_bfs(n, adj, src) -> list[int]                                                   # 2024 I
def dijkstra(n, adj, src) -> list[int]
def dijkstra_path(n, adj, src, dst) -> tuple[int, list[int]] | None
def dijkstra_stats(n, adj, src, mod=MOD7) -> tuple[list[int], list[int], list[int], list[int]]   # Investigation: dist, count, min/max рёбер
def dijkstra_coupon(n, adj, src, dst) -> int                                                 # Flight Discount, состояния (v, used)
def dijkstra_states(start: H, dst: Callable[[H], bool], nbrs: Callable[[H], Iterable[tuple[H, int]]]) -> int   # «вершина + терминал», любые хешируемые состояния
def k_shortest_walks(n, adj, src, dst, k) -> list[int]                                       # Flight Routes
def bellman_ford(n, edges, src) -> list[int]                                                 # -INF у вершин за отрицательным циклом
def find_negative_cycle(n, edges) -> list[int] | None                                        # Cycle Finding
def max_score_path(n, edges, src, dst) -> int | None                                         # High Score (None = бесконечно)
def floyd_warshall(n, edges) -> list[list[int]]                                              # Shortest Routes II
# dag
def toposort_kahn(n, adj) -> list[int] | None                                                # Course Schedule
def toposort_lex_min(n, adj) -> list[int] | None; def toposort_reverse_trick(...)            # Course Schedule II
def count_paths_dag(n, adj, src, dst, mod=MOD7) -> int                                       # Game Routes
def longest_path_dag(n, adj, src, dst) -> list[int] | None                                   # Longest Flight Route
def reachable_counts(n, adj) -> list[int]                                                    # Reachable Nodes (битсеты на int) [slow]
def reachability_queries(n, adj, queries) -> list[bool]                                      # SCC + битсеты
# dsu / mst
class DSU: find(x); union(a, b) -> bool; size(x); components
class RollbackDSU: union(a, b) -> bool; snapshot() -> int; rollback(t)  # без сжатия путей
def kruskal(n, edges) -> tuple[int, list[int]] | None                                        # Road Reparation
def prim(n, adj) -> int | None
def road_construction(n, edges) -> list[tuple[int, int]]                                     # число компонент и макс. размер после каждого ребра
# scc
def scc_tarjan(n, adj) -> tuple[int, list[int]]        # итеративный; comp в топологическом порядке
def scc_kosaraju(n, adj) -> tuple[int, list[int]]
def condensation(n, adj, comp, k) -> list[list[int]]
def coin_collector(n, adj, coins) -> int                                                     # SCC + DP по DAG
def two_sat(n_vars, clauses: list[tuple[int, bool, int, bool]]) -> list[bool] | None         # Giant Pizza
def bridges(n, edges) -> list[int]                                                           # индексы рёбер
def articulation_points(n, adj) -> list[int]                                                 # Necessary Cities
# euler
def euler_path_undirected(n, edges, start=None) -> list[int] | None                          # Mail Delivery (цикл)
def euler_path_directed(n, edges, src, dst) -> list[int] | None                              # Teleporters Path
# functional
def build_lifting(f: list[int], max_steps: int) -> list[list[int]]
def kth_successor(up, x, k) -> int                                                           # Planets Queries I
def cycle_steps(f) -> list[int]                                                              # Planets Cycles
def functional_distance(f, queries) -> list[int]                                             # Planets Queries II
def escalators(...)                                                                           # 2023 E [NV]
# flow / matching
class Dinic: add_edge(u, v, cap) -> int; max_flow(s, t) -> int; min_cut_side(s) -> list[bool]   # итеративный DFS
def edmonds_karp(n, edges, s, t) -> int
def min_cut_edges(n, edges, s, t) -> list[int]                                               # Police Chase
def edge_disjoint_paths(n, edges, s, t) -> list[list[int]]                                   # Distinct Routes
def hopcroft_karp(n_left, n_right, adj) -> tuple[int, list[int]]                             # School Dance
def kuhn_matching(n_left, n_right, adj) -> tuple[int, list[int]]                             # итеративный
def hungarian(cost: list[list[int]]) -> tuple[int, list[int]]                                # Task Assignment, O(n^3)
class MinCostFlow: add_edge(u, v, cap, cost); flow(s, t, maxf) -> tuple[int, int]            # Parcel Delivery (SPFA/Дейкстра с потенциалами)
# paths
def hamiltonian_path(n, adj) -> list[int] | None                                             # bitmask, n <= 20 [slow]
def knights_tour(n, r, c) -> list[list[int]] | None                                          # Варнсдорф, 8x8
# advanced
def critical_cities(n, adj) -> list[int]                                                     # вершины на всех путях 0 -> n-1
def flight_route_requests(n, pairs) -> int
def network_renovation(n, edges) -> list[tuple[int, int]]
def strongly_connected_edges(n, edges) -> list[tuple[int, int]] | None                       # ориентация рёбер
def even_outdegree_edges(n, edges) -> list[tuple[int, int]] | None
def bus_companies(...)                                                                        # [NV] — нужно точное условие CSES
```

#### `rustinpy.tree` (этап 2)
```python
def tree_parents_order(n, adj, root=0) -> tuple[list[int], list[int]]   # BFS-порядок + родители: база всех итеративных DP
def subtree_sizes(n, adj, root=0) -> list[int]                         # Subordinates
def tree_diameter(n, adj) -> tuple[int, int, int]                       # (длина, a, b)
def tree_farthest(n, adj) -> list[int]                                  # Tree Distances I
def tree_distance_sums(n, adj) -> list[int]                             # Tree Distances II, rerooting
def find_centroid(n, adj) -> int
def euler_tour(n, adj, root=0) -> tuple[list[int], list[int]]           # tin, tout
class LCA:            # binary lifting: lca(a, b); kth_ancestor(v, k); dist(a, b)   (Company Queries I/II, Distance Queries)
class LCAEuler:       # Euler tour + sparse table, O(1) на запрос
def tree_matching(n, adj) -> int
def counting_paths(n, adj, paths) -> list[int]                          # разности на дереве
class SubtreeQueries: # Euler + Fenwick: set_value(v, x); subtree_sum(v)
class PathSumQueries: # Path Queries I: Euler + Fenwick по корневым путям
class HLD:            # Path Queries II: set_value(v, x); path_max(a, b); внутри итеративное SegTree
def centroid_decomposition(n, adj) -> list[int]                         # родитель в дереве центроидов
def fixed_length_paths(n, adj, k) -> int                                # Fixed-Length Paths I
def fixed_length_paths_range(n, adj, k1, k2) -> int                     # Fixed-Length Paths II [slow]
def distinct_colors(n, adj, colors) -> list[int]                        # small-to-large
def tree_isomorphic(n, adj1, adj2, rooted: bool = True) -> bool         # AHU / каноническая форма; без корня — через центры
def fix_the_leak(n, parent, k, ...)                                     # 2025 F [NV]
```

#### `rustinpy.dp` (этап 3)
```python
def dice_combinations(n, mod=MOD7) -> int
def min_coins(coins, x) -> int                                       # Minimizing Coins (-1 если нельзя)
def coin_combinations_ordered(coins, x, mod=MOD7) -> int             # Coin Combinations I
def coin_combinations_unordered(coins, x, mod=MOD7) -> int           # Coin Combinations II
def removing_digits(n) -> int
def grid_paths(grid: list[str], mod=MOD7) -> int
def knapsack_01(weights, values, cap) -> int                         # Book Shop
def knapsack_unbounded(weights, values, cap) -> int
def knapsack_bounded(weights, values, counts, cap) -> int            # Book Shop II, двоичное разбиение
def array_description(a, m, mod=MOD7) -> int
def counting_towers(n, mod=MOD7) -> int
def edit_distance(a: str, b: str) -> int
def lcs(a: list[int], b: list[int]) -> list[int]                     # с восстановлением
def lis(a: list[int], strict: bool = True) -> list[int]              # индексы, n log n, с восстановлением
def lis_length(a: list[int], strict: bool = True) -> int
def count_increasing_subsequences(a, mod=MOD7) -> int                # Increasing Subsequence II
def money_sums(coins) -> list[int]                                    # битсет на int
def rectangle_cutting(a, b) -> int
def removal_game(a) -> int
def weighted_interval_scheduling(jobs: list[tuple[int, int, int]]) -> int   # Projects
def elevator_rides(weights, cap) -> int                               # bitmask (поездки, вес последней)
def hamiltonian_flights(n, edges, mod=MOD7) -> int                    # [slow] n=20 в CPython ~10 c
def counting_tilings(n, m, mod=MOD7) -> int                           # DP по профилю
def counting_numbers(a, b) -> int                                     # digit DP: нет соседних равных цифр
class LiChaoTree: add_line(k, b); query(x) -> int                     # минимум, целочисленный x-домен
class MonotoneCHT: add_line(k, b) (k убывают); query(x)               # монотонный, бинпоиск по запросу
def dc_optimization(n, k, cost: Callable[[int, int], int]) -> int     # D&C opt (глубина log n — whitelist)
def houses_and_schools(c: list[int], k: int) -> int
def knuth_optimization(w: list[int]) -> int                          # Knuth Division / слияние отрезков
def fence_painting(colors: list[int], k: int, mod=MOD) -> int        # 2023 F [NV условие]: 0 = не покрашено, соседи различны
```

#### `rustinpy.strings` (этап 3)
```python
def z_function(s) -> list[int]; def prefix_function(s) -> list[int]
def kmp_find_all(text, pat) -> list[int]                              # String Matching
def borders(s) -> list[int]; def periods(s) -> list[int]
def min_rotation(s) -> int                                            # Booth: Minimal Rotation
def lyndon_factorization(s) -> list[str]                              # Duval
def manacher(s) -> tuple[list[int], list[int]]                        # d1, d2
def longest_palindrome(s) -> str
def longest_palindrome_ending_at(s) -> list[int]                      # All Palindromes
class StringHash:         # mod 2^61-1, случайная база: get(l, r) -> int
class StringHashDouble:   # два mod: (1e9+7, 998244353)
class Trie: insert(word); count_prefix(p) -> int
def word_combinations(s, words, mod=MOD7) -> int
class AhoCorasick: __init__(patterns); count(text) -> list[int]; first_pos(text) -> list[int]   # Finding/Counting Patterns, Pattern Positions
def suffix_array(s) -> list[int]                                      # префиксное удвоение + сортировка подсчётом, O(n log n) [slow 10^6]
def lcp_kasai(s, sa) -> list[int]
def distinct_substrings_count(s) -> int
class SuffixAutomaton: extend(c); distinct_count(); kth_distinct(k) -> str; kth_with_repeats(k) -> str; longest_repeat() -> str; length_distribution() -> list[int]
class PalindromeQueries:  set_char(i, c); is_palindrome(l, r) -> bool   # хеши + BIT
def string_functions(...) [NV]                                        # CSES String Functions — уточнить условие
def inverse_suffix_array(sa: list[int]) -> str | None
def bwt(s) -> str; def inverse_bwt(t) -> str                          # String Transform
def distinct_subsequences(s, mod=MOD7) -> int
def shortest_non_subsequence(s, alphabet="ACGT") -> str               # Shortest Subsequence
def required_substring(n, pattern, mod=MOD7) -> int                   # DP + автомат KMP
def brands(s: str) -> str                                             # 2023 B [NV: набор гласных]
def apostrophe_number(...)                                            # 2024 K [NV]
```

#### `rustinpy.roman` (этап 3)
```python
def to_roman(n: int) -> str            # 1..3999
def from_roman(s: str) -> int          # ValueError на некорректной
def is_valid_roman(s: str) -> bool     # каноническая запись
def roman_symmetry(...)                # 2023 C [NV]
def roman_product_unique(n: int) -> bool   # 2024 E [NV]: единственность n как произведения римских чисел > 1
def roman_split_min_max(s: str) -> tuple[int, int] | None   # 2025 G [NV]
def scroogius_shortest(n: int) -> str  # 2025 G [NV]
```

#### `rustinpy.bits` (этап 3)
```python
def popcount(x: int) -> int                                       # 3.9: bin(x).count("1")
def counting_bits_total(n: int) -> int                            # единицы в 1..n
class XorTrie: insert(x); max_xor(x) -> int; min_xor(x) -> int
def max_xor_subarray(a) -> int
class XorBasis: insert(x) -> bool; can_make(x); max_xor(); kth_smallest(k); rank
def max_xor_subset(a) -> int; def number_of_subset_xors(a) -> int
def k_subset_xors(a: list[int], k: int) -> list[int]              # k наименьших с кратностями
def all_subarray_xors(a) -> list[int]                             # [slow]
def xor_pyramid_peak(a) -> int                                    # Лукас по модулю 2
def sos_subset_sum(f, bits) -> list[int]; def sos_superset_sum(f, bits) -> list[int]
def sos_bit_problem(a) -> list[tuple[int, int, int]]
def and_subset_count(a, mod=MOD7) -> list[int]
def min_hamming_distance(words: list[int], k: int) -> int         # [slow]
def fwht_xor(a, invert, mod=None); def fwht_and(...); def fwht_or(...)
def xor_convolution(a, b, mod=None) -> list[int]; and_convolution; or_convolution
def kenobi_skywalker(a: list[int], queries) -> list[bool]         # 2025 K [NV]
```

#### `rustinpy.geometry` (этап 4)
Точки — `tuple[int, int]` (быстрее объектов и проще копировать). Плюс маленький `class Point(NamedTuple)` с операторами для читаемости.
```python
def cross(o, a, b) -> int; def dot(o, a, b) -> int; def orientation(a, b, c) -> int
def point_location(p1, p2, p3) -> str                              # "LEFT" | "RIGHT" | "TOUCH"
def on_segment(p, a, b) -> bool
def segments_intersect(p1, p2, p3, p4) -> bool
def segment_intersection_point(p1, p2, p3, p4) -> tuple[Fraction, Fraction] | None
def polygon_area2(poly) -> int                                     # удвоенная знаковая площадь
def point_in_polygon(poly, p) -> str                               # "INSIDE" | "OUTSIDE" | "BOUNDARY"
def polygon_lattice_points(poly) -> tuple[int, int]                # Пик: (внутри, на границе)
def convex_hull(points, keep_collinear: bool = False) -> list[tuple[int, int]]
def closest_pair(points) -> int                                    # квадрат расстояния, D&C (глубина log n)
def closest_pair_sweep(points) -> int
def max_manhattan_distances(points) -> list[int]                   # после добавления каждой точки
def all_manhattan_distances_sum(points) -> int
def intersection_points_count(segments) -> int                     # горизонтальные × вертикальные, sweep + BIT
def area_of_rectangles(rects) -> int                               # sweep + дерево покрытия
def robot_path(moves: list[tuple[str, int]]) -> int                # [NV/slow] CSES Robot Path
class LiChaoMax                                                     # Lines and Queries I/II (дубль, самодостаточно)
def line_segments_trace(segments, x_max) -> list[int]              # Li Chao на отрезках
def det3(a, b, c) -> int; def tetra_volume6(a, b, c, d) -> int
def coplanar_with_origin(points: list[tuple[int, int, int]]) -> bool
def death_star_min_changes(...)                                    # 2025 D [NV]
def biathlon_route(...)                                            # 2023 K [NV], базовая версия: DP по подмножествам, N <= ~12
```

#### `rustinpy.game` (этап 4)
```python
def mex(values: Iterable[int]) -> int
def nim_first_wins(piles) -> bool                                  # Nim Game I
def nim_k_first_wins(piles, k=3) -> bool                           # Nim Game II (взять 1..k): кучи mod (k+1)
def misere_nim_first_wins(piles) -> bool
def grundy_subtraction(n_max, moves) -> list[int]                  # Stick Game
def grundy_dag(n, adj) -> list[int]                                # общий Шпраг-Гранди, итеративно
def stair_game_first_wins(piles) -> bool
def grundy_game_first_wins(n) -> bool                              # таблица до 1222 + известный факт о n > 1222
def another_game_first_wins(piles) -> bool
```

#### `rustinpy.introductory` (этап 4)
```python
def gray_code(n) -> list[str]; def hanoi_moves(n) -> list[tuple[int, int]]
def string_permutations(s) -> list[str]; def next_permutation(a: list[int]) -> bool
def submasks(mask) -> Iterator[int]; def subsets(n) -> Iterator[int]
def n_queens(n=8, blocked: list[str] | None = None) -> int          # Chessboard and Queens
def grid_path_description(pattern: str) -> int                      # 7x7, бэктрекинг с отсечениями [slow]
def weird_algorithm(n) -> list[int]; def number_spiral(y, x) -> int; def two_knights(n) -> list[int]
def two_sets(n) -> tuple[list[int], list[int]] | None; def trailing_zeros(n) -> int
def coin_piles(a, b) -> bool; def palindrome_reorder(s) -> str | None; def apple_division(p) -> int
def digit_queries(k) -> int; def beautiful_permutation(n) -> list[int] | None
def string_reorder(s) -> str | None; def mex_grid_construction(n) -> list[list[int]]; def knight_moves_grid(n) -> list[list[int]]
def prufer_encode(n, edges) -> list[int]; def prufer_decode(code) -> list[tuple[int, int]]
def de_bruijn(n: int, k: int = 2) -> str
def inverse_inversions(n, k) -> list[int]; def monotone_subsequences(n, k) -> list[int] | None
def chess_tournament(degrees) -> list[tuple[int, int]] | None       # Havel–Hakimi
def filling_trominos(n, m) -> list[str] | None                      # [NV] построение по блокам 2x3
```

#### `rustinpy.sorting` (этап 4)
```python
def bisect_answer(lo: int, hi: int, ok: Callable[[int], bool]) -> int     # минимальный x с ok(x) (ok монотонен)
def bisect_answer_max(lo, hi, ok) -> int; def bisect_real(lo, hi, ok, iters=100) -> float
def ferris_wheel(w, x) -> int; def apartments(a, b, k) -> int; def concert_tickets(h, t) -> list[int]
def restaurant_customers(intervals) -> int                          # sweep событий
def movie_festival(intervals) -> int; def movie_festival_k(intervals, k) -> int
def room_allocation(intervals) -> tuple[int, list[int]]
def sum_of_two_values(a, x) -> tuple[int, int] | None; sum_of_three_values; sum_of_four_values
def max_subarray_sum(a) -> int; def max_subarray_sum_range(a, lo, hi) -> int   # монотонная дека
def stick_lengths(p) -> int; def missing_coin_sum(a) -> int; def collecting_numbers(a) -> int
def playlist(a) -> int; def towers(a) -> int; def traffic_lights(x, p) -> list[int]
def josephus_survivor(n, k) -> int                                  # формула O(n)
def josephus_order(n, k) -> list[int]                               # Josephus I/II, Fenwick kth
def josephus_queries(n, k) -> int                                   # k-й удалённый при шаге 2, O(log n)
def nested_ranges(ranges) -> tuple[list[bool], list[bool]]; def nested_ranges_count(ranges) -> tuple[list[int], list[int]]
def factory_machines(k, t) -> int; def tasks_and_deadlines(tasks) -> int; def reading_books(t) -> int
def array_division(a, k) -> int
def subarray_sums_count(a, x) -> int; def subarray_divisibility(a) -> int; def subarray_distinct_values(a, k) -> int
def nearest_smaller_values(a) -> list[int]                          # индекс или -1
def meet_in_middle_count(a, x) -> int                               # Meet in the Middle
def sliding_window_median(a, k) -> list[int]; def sliding_window_cost(a, k) -> list[int]   # две кучи с ленивым удалением
```

#### `rustinpy.counting` (этап 5)
```python
def filled_subgrid_count(grid: list[str]) -> list[int]               # [NV: какая версия CSES] стек по гистограмме
def counting_bishops(n, k, mod=MOD7) -> int
def counting_permutations(n, mod=MOD7) -> int                        # |p_i - p_{i+1}| != 1, рекуррентность + brute
def permutation_inversions(n, k, mod=MOD7) -> int
def counting_reorders(s, mod=MOD7) -> int
def grid_completion(grid: list[str], mod=MOD7) -> int                # [NV]
def raab_game_construct(n, a, b) -> tuple[list[int], list[int]] | None; def raab_game_count(n, a, b, mod=MOD7) -> int
def functional_graph_distribution(n, mod=MOD7) -> list[int]          # [NV]
def empty_string(s, mod=MOD7) -> int                                 # интервальная DP, O(n^3) [slow]
def counting_sequences(n, k, mod=MOD7) -> int                        # сюръекции
def tournament_graph_distribution(n, mod=MOD7) -> list[int]          # [stub или NV]
def maximum_building(grid) -> int; def maximum_building_counts(grid) -> list[list[int]]   # I / II
def cyclic_array(a, k) -> int                                        # binary lifting
def sorting_methods(p) -> tuple[int, int, int, int]
def bubble_sort_rounds(a) -> int
def programmers_and_artists(pairs, a, b) -> int
def coding_company(skills, x, mod=MOD7) -> int
def two_stacks_sorting(a) -> list[int] | None                        # [slow]
def stick_divisions(x, lengths) -> int                               # Хаффман
def swap_round_sorting(p) -> list[list[tuple[int, int]]]
def binary_subsequences(n) -> str                                    # [NV]
def school_excursion(n, edges) -> str                                # битсет по размерам компонент
def coin_grid(grid) -> tuple[int, list[tuple[int, int]]]             # Кёниг
def coin_arrangement(grid) -> int
def grid_puzzle_i(a, b) -> list[str] | None                          # поток
def grid_puzzle_ii(...) -> ...                                       # min-cost flow [NV]
```

#### `rustinpy.misc` — короткие задачи ICPC-UZ (этап 5)
Все `[NV]`, пока пользователь не даст условия (см. вопрос Q-2):
```python
def attacks_number(...)          # 2023 A
def a_plus_branding(...)         # 2024 A
def big_deadline(..., mod=MOD)   # 2024 B
def certainly_best(...)          # 2024 C
def great_sign(...)              # 2024 G
def hidden_pieces(...)           # 2024 H
def laura_and_arrays(...)        # 2024 L
def a_problems_balloons(...)     # 2025 A
def limit_the_arrow(...)         # 2025 L
def minimum_number_of_tasks(...) # 2025 M
```

### 4.4 Задачи ICPC-UZ: что понятно из задания и чего не хватает

| Задача | Где | Что понятно из задания | Чего не хватает |
|---|---|---|---|
| 2023 A Attacks Number | misc | ходы на 2 и 3 очка, минимум атак | условие целиком |
| 2023 B Brands | strings | вставки для чередования гласных/согласных, лексикографический минимум | набор гласных (y?), алфавит |
| 2023 C (симметрии) | roman | что-то о симметрии римских записей | условие целиком |
| 2023 D | mathx | формула K | что дано и что выводится, точность |
| 2023 E Escalators | graph | функциональный граф, цикл или выход, точечные изменения | формат запросов, ограничения |
| 2023 F Fence Painting | dp | отрезки нулей между покрашенными | точное правило соседей |
| 2023 G Generic Strings | ds | «нет повторов на отрезках», удаление букв | условие целиком |
| 2023 H, 2025 J | mathx | Цекендорф / число представлений | что именно считать; 2025 J ещё и интерактив |
| 2023 I | interactive | интерактив | условие |
| 2023 J | mathx | сумма φ / взаимно простые пары | ограничение n (нужен ли Du's sieve) |
| 2023 K биатлонист | geometry | пары стрельбищ, без самопересечений | условие целиком |
| 2023 L | ds | PAV, сумма квадратов как дробь по модулю | какие запросы |
| 2024 A–C, G, H, L | misc | по одной фразе | условия целиком |
| 2024 D Deep Numbers | mathx/dp | не простое и нет простой подпоследовательности цифр | что значит «до 10^6» (n — граница или длина) |
| 2024 E | mathx + roman | Pollard rho; произведение римских чисел > 1 | одна это задача или две разные |
| 2024 F | interactive | поиск прямоугольника, 10^9×10^9, 125 запросов | тип запроса |
| 2024 I | graph | 0-1 BFS | условие (для теста) |
| 2024 J | interactive | интерактив | условие |
| 2024 K | strings | апострофы в числах | правило |
| 2025 B | mathx | перестановки цифр, мин. число смен, mod 2112025 | условие |
| 2025 C | mathx | сумма gcd | что суммируется, ограничения |
| 2025 D Death Star N | geometry | минимум искажаемых координат, det = 0 | условие целиком |
| 2025 E Exclusions | ds | f(k) для разбиения на k блоков, mex | что такое f(k) |
| 2025 F Fix the Leak | tree | p_i < i, удалить ровно k «агентов» с цепочками, минимум листьев | что такое «агент» и «цепочка» |
| 2025 G Scroogius | roman | макс./мин. разбиение, разность n, кратчайшая строка | условие |
| 2025 H HQ Reforms | ds | инверсия отрезка, сумма по сериям единиц | какая функция от серии |
| 2025 I Infinite Game | mathx | DP (сумма mod 3, последняя цифра) | правила игры |
| 2025 K Kenobi | bits | значения ≤ 511, есть ли подмножество из c элементов с xor x | ограничения n, c, q |
| 2025 A, L, M | misc | по одной фразе | условия |

Без условий каждая функция из таблицы получает сигнатуру по лучшему пониманию, реализацию «как понял», `verified=False` и строку в `docs/PROGRESS.md`.

## 5. Данные

Постоянных данных нет. Реестр живёт в памяти: `dict[str, AlgoInfo]` с ключом `"module.name"`, заполняется при импорте модулей алгоритмов; `load_all()` импортирует их все. `docs/CATALOG.md` — производный артефакт.

## 6. Интеграции и внешние сервисы

| Сервис | Зачем | Заметки |
|---|---|---|
| GitHub Actions | CI (3.9–3.13, ruff, mypy, pytest), publish | `publish.yml`: `workflow_dispatch` → TestPyPI, тег `v*` → PyPI |
| PyPI / TestPyPI | публикация | Trusted Publishing (OIDC, environment `pypi` / `testpypi`); запасной вариант — секрет `PYPI_API_TOKEN` в настройках репозитория, никогда не в файлах |

## 7. Нефункциональные требования

- **Язык:** код, имена и докстринги на английском; русские подсказки в комментариях; README на RU и EN; общение на русском.
- **Python:** 3.9–3.13 (`requires-python = ">=3.9"`), только CPython в CI.
- **Зависимости:** runtime — ни одной. Dev (`[project.optional-dependencies] dev`): pytest, ruff, mypy, build, twine.
- **Производительность** (маркер `slow`, локально на CPython 3.11, ориентир «≤ 2 c на одном ядре»): Dijkstra n = m = 2·10^5; Fenwick и SegTree 2·10^5 операций; Dinic на 500 вершинах и 1000 рёбрах; suffix_array n = 10^5; NTT 2·10^5; линейное решето 10^7. Фактические времена фиксируются в `docs/PROGRESS.md`. Что не укладывается, получает `Python speed:` в докстринге.
- **Безопасность:** токенов нет ни в файлах, ни в логах; `.gitignore` закрывает `dist/`, `build/`, `.venv/`, `*.egg-info`, `.env`.
- **Git:** ветка `main`, Conventional Commits (`feat(graph): add dinic`), коммит после каждого этапа, добавление файлов только по явному списку (без `git add -A`).
- **Версионирование:** `0.1.0`, далее SemVer; `CHANGELOG.md` в формате Keep a Changelog.

## 8. Технологии

- Сборка: **hatchling** (`pyproject.toml`, src-layout, без `setup.py`). Версия хранится в `src/rustinpy/__init__.py` и читается через `[tool.hatch.version]`.
- Тесты: **pytest** (`--doctest-modules` по `src/`, маркер `slow` отключён по умолчанию, `-m slow` включает его).
- Линтер и форматтер: **ruff** (line-length 100; правила RUF001–RUF003 выключены, иначе ruff ругается на кириллицу как на «похожие символы»).
- Типы: **mypy --strict** по `src/rustinpy` с `python_version = 3.9`.
- CI: GitHub Actions, матрица 3.9–3.13 × ubuntu, плюс одна джоба windows-latest на 3.13 (проект разрабатывается на Windows).

## 9. Структура проекта

```
rustin/                         # корень репозитория (папка на диске; на GitHub — rustinpy)
├── pyproject.toml              # hatchling, metadata, [project.scripts], настройки ruff/mypy/pytest
├── README.md                   # RU + EN
├── LICENSE                     # MIT, Mirahmad
├── CHANGELOG.md
├── .gitignore
├── docs/
│   ├── SPEC.md                 # это ТЗ
│   ├── PROGRESS.md             # журнал этапов + список NOT VERIFIED
│   ├── CATALOG.md              # генерируется scripts/gen_catalog.py
│   └── handoff/000-kickoff.md  # исходное задание дословно
├── src/rustinpy/
│   ├── __init__.py             # __version__, show, search, list_algos, help
│   ├── _registry.py            # @algo, AlgoInfo, load_all, resolve, source_of
│   ├── cli.py
│   ├── py.typed
│   ├── io.py, interactive.py
│   ├── mathx/   (__init__ + modular, comb, primes, numtheory, matrix, poly, linalg, prob, icpc)
│   ├── ds/      (__init__ + prefix, fenwick, sparse, segtree, lazy, persistent, offline, mo, treap, sortedlist, sliding, connectivity, pav, icpc)
│   ├── graph/   (__init__ + traversal, shortest, dag, dsu, mst, scc, euler, functional, flow, matching, paths, advanced, icpc)
│   ├── tree.py
│   ├── dp.py
│   ├── strings/ (__init__ + prefix, hashing, trie, suffix, palindromes, misc)
│   ├── roman.py, bits.py, geometry.py, game.py
│   ├── introductory.py, sorting.py, counting.py, misc.py
├── tests/
│   ├── conftest.py             # маркер slow, фикстура seed, общие brute-force
│   ├── test_meta.py            # докстринги, реестр, самодостаточность, отсутствие рекурсии, NOT VERIFIED ↔ PROGRESS
│   ├── test_cli.py, test_io.py, test_interactive.py
│   ├── test_mathx_*.py, test_ds_*.py, test_graph_*.py, test_tree.py, test_dp.py, ...
│   └── test_perf.py            # @pytest.mark.slow
├── scripts/
│   ├── gen_catalog.py
│   └── export_trd.py
└── .github/workflows/
    ├── ci.yml
    └── publish.yml
```
Модуль становится пакетом, если в нём больше ~1500 строк (так уже сделано для mathx, ds, graph, strings). Публичный путь импорта от этого не меняется: `from rustinpy.graph import dijkstra`.

## 10. Граничные случаи и ошибки

- Пустой ввод (n = 0, пустая строка, пустой список) — ответ по смыслу без исключения, если в докстринге не сказано иное.
- Недостижимые вершины — `INF`; отрицательный цикл — `-INF` в `bellman_ford`, `None` в функциях «найди путь».
- Некорректные аргументы (обратный элемент для необратимого, `from_roman("IIII")`) — `ValueError` с понятным сообщением.
- `Comb` с составным модулем — `ValueError` при создании (проверка `is_prime(mod)`), в докстринге отсылка к `nCr_pascal` и `nCr_composite` (2025 B).
- Интерактив: ответ `-1` или EOF — немедленный `SystemExit(0)`.
- `rustinpy show` с неоднозначным именем — список вариантов `module.name` и код возврата 2; неизвестное имя — до 5 похожих (difflib) и код возврата 1.
- Рекурсия: тест на AST падает, если функция вызывает саму себя и не внесена в whitelist.

## 11. Допущения

- **A-1.** Корень репозитория — текущая папка `rustin/`, а не вложенная `rustinpy/`. Имя репозитория на GitHub `rustinpy`.
- **A-2.** Большие модули сделаны пакетами с подмодулями, пути импорта при этом те же.
- **A-3.** Алгоритмы **не** реэкспортируются на верхний уровень `rustinpy`, только `show/search/list_algos/help/__version__`. Причины: конфликты имён (`LiChaoTree` в `dp` и `geometry`, `mex` в `game` и `ds`), и `import rustinpy` остаётся быстрым. «Реэкспорт» из задания понимаем как реэкспорт подмодулей внутри пакетов (`rustinpy.graph` реэкспортирует `graph.shortest` и т.д.).
- **A-4.** Самодостаточность проверяется автоматически: каждый алгоритм выгружается через `source_of`, исполняется в чистом пространстве имён без `rustinpy`, и его doctest запускается там же.
- **A-5.** Функции CSES принимают данные аргументами и не читают stdin.
- **A-6.** `mypy --strict` применяется ко всему `src/rustinpy` (не только к публичному API).
- **A-7.** Для задач CSES из раздела 4.3 тесты строятся на brute-force и примерах, а не на тестах CSES (их нельзя скачивать и класть в репозиторий).
- **A-8.** Задачи с одинаковым номером в двух местах задания (2024 E — Pollard rho и римские числа; 2025 J — интерактив и Цекендорф) считаются одной задачей, которая использует обе техники.
- **A-9.** Чек-лист публикации кладётся в `docs/PUBLISHING.md` и выдаётся в чат.
- **A-10.** В метаданных пакета автор указан как `Mirahmad`, без email.
- **A-11.** Версии Python в CI — 3.9–3.13, как в задании. 3.9 уже вышел из поддержки (EOL октябрь 2025), поэтому dev-инструменты на 3.9 могут быть старее (pytest 8.x вместо 9.x). Это нормально.

## 12. Открытые вопросы

Все вопросы закрыты 2026-10-17: пользователь выбрал варианты по умолчанию.
- **Q-1 → решено:** условия ICPC-UZ ищу сам в открытом доступе на этапе 5; что не найду — `NOT VERIFIED` по таблице 4.4.
- **Q-2 → решено:** приоритет в 5.13 — порядок из задания.
- **Q-3 → решено:** spec-first хуки ставятся; `ci.yml` и `.gitignore` свои, по этой спеке.
- **Q-4 → решено:** публичный репозиторий `rustinpy` на GitHub. Ник владельца пока неизвестен (`gh` не установлен); `project.urls` добавлю, когда он появится — отложено до этапа 5.
- **Q-5 → решено:** в 0.1.0 входит только перечисленное в 4.3.

## 13. Стратегия тестирования

- **Юнит:** у каждого зарегистрированного алгоритма есть хотя бы один тест в `tests/` (проверяется через реестр: имя алгоритма встречается в тестах модуля).
- **Brute-force сравнения** (random, фиксированный seed, 100–500 итераций на малых n): Dijkstra ↔ Floyd/Bellman-Ford; 0-1 BFS ↔ Dijkstra; SegTree/Lazy/Fenwick/SparseTable ↔ наивный массив; LCA ↔ подъём по родителям; Dinic/EK ↔ перебор разрезов; Hopcroft-Karp/Kuhn ↔ перебор; Hungarian ↔ перестановки; SCC ↔ транзитивное замыкание; мосты/точки ↔ удаление и проверка связности; Pollard/factorize ↔ пробное деление; is_prime ↔ решето; NTT/convolution_int/FWHT ↔ наивная свёртка; suffix_array ↔ `sorted`; Aho-Corasick ↔ `str.find`; SuffixAutomaton ↔ множество подстрок; хеши ↔ сравнение срезов; convex_hull/closest_pair/point_in_polygon ↔ перебор; Treap/SortedList ↔ `list` + `bisect`; Mo/offline ↔ наивные запросы; LIS/LCS/edit_distance/knapsack ↔ перебор; D&C/Knuth/CHT ↔ O(n^2)/O(n^3) DP; Grundy ↔ полный перебор позиций; counting-функции ↔ перебор перестановок/строк при n ≤ 8.
- **Мета-тесты (`test_meta.py`):** формат докстрингов; наличие doctest; самодостаточность (A-4); AST-проверка отсутствия рекурсии; `NOT VERIFIED` в коде ↔ список в PROGRESS.md; `CATALOG.md` совпадает с регенерированным; отсутствие runtime-зависимостей в метаданных.
- **CLI:** вызовы `main([...])` и один subprocess-тест установленной команды.
- **Производительность:** `tests/test_perf.py` с маркером `slow`, вне CI по умолчанию (в CI отдельной необязательной джобой на 3.13).
- **Ручная проверка:** CI на GitHub, установка из TestPyPI, реальная вставка экспорта в TRD.
- **Покрытие:** цель ≥ 90% строк по `src/` (pytest-cov в dev-зависимостях).

## 14. Критерии готовности

- [x] AC-01: `pip install .` в чистом venv проходит, `import rustinpy` работает, у пакета нет runtime-зависимостей
- [ ] AC-02: каждый алгоритм из раздела 4.3 зарегистрирован через `@algo` либо помечен `verified=False` / `stub=True` с причиной
- [ ] AC-03: докстринг каждого алгоритма соответствует шаблону 4.1 (обязательные поля, порядок)
- [ ] AC-04: `pytest --doctest-modules src` проходит, doctest есть у каждого алгоритма
- [ ] AC-05: у каждого алгоритма есть хотя бы один тест в `tests/`
- [ ] AC-06: нетривиальные алгоритмы из списка раздела 13 проверены brute-force на случайных данных
- [ ] AC-07: выгруженный исходник каждого алгоритма (с requires) проходит свой doctest без пакета `rustinpy`
- [ ] AC-08: в коде алгоритмов нет рекурсии, кроме whitelist с глубиной O(log n)
- [ ] AC-09: `rustinpy list/show/search/export` и `rustinpy.show/search/list_algos/help` работают по разделу 4.2, включая неоднозначные и неизвестные имена
- [ ] AC-10: `export` создаёт файл с оглавлением, без `@algo` и импортов `rustinpy`, строки ≤ 100 символов
- [ ] AC-11: `docs/CATALOG.md` сгенерирован и совпадает с выводом `scripts/gen_catalog.py`
- [x] AC-12: `FastReader`/`FastWriter` и `make_ask` корректно работают на подменённых потоках (включая `-1` и EOF)
- [ ] AC-13: каждый `NOT VERIFIED` в коде перечислен в `docs/PROGRESS.md`
- [ ] AC-14: `ruff check`, `ruff format --check` и `mypy --strict` чистые
- [ ] AC-15: slow-бенчмарки из раздела 7 укладываются в ориентир или у алгоритма есть `Python speed:`
- [ ] AC-16: README содержит RU и EN разделы: установка, быстрый старт, модули, CLI, TRD, ограничения, лицензия
- [ ] AC-17: `python -m build` и `twine check dist/*` проходят
- [ ] AC-18 (ручная): CI на GitHub зелёный на 3.9–3.13
- [ ] AC-19 (ручная): пакет установлен из TestPyPI в чистое окружение, тесты проходят
- [ ] AC-20 (ручная): чек-лист публикации выдан, на PyPI ничего не опубликовано без команды пользователя

## 15. План реализации

- [x] **Этап 1 — каркас + mathx + ds:** git, `pyproject.toml`, `.gitignore`, LICENSE, CHANGELOG, `_registry`, `__init__`, `cli`, `io`, `interactive`, CI, publish.yml, мета-тесты, `mathx`, `ds` → результат: `pip install -e .[dev]`, ruff/mypy/pytest зелёные, CLI показывает алгоритмы mathx/ds · AC: AC-01, AC-09, AC-12, AC-14 (частично AC-03…AC-08)
- [ ] **Этап 2 — graph, tree** → результат: модули с brute-force тестами · AC: AC-03…AC-08 для этих модулей
- [ ] **Этап 3 — dp, strings, roman, bits** → результат: то же · AC: то же
- [ ] **Этап 4 — geometry, game, introductory, sorting** → результат: то же
- [ ] **Этап 5 — counting, misc, README, CATALOG, export_trd, PUBLISHING** → результат: все AC автоматизированы и зелёные, сборка и `twine check` проходят, чек-лист публикации готов · AC: AC-02, AC-10, AC-11, AC-13, AC-15, AC-16, AC-17, AC-20
- [ ] **Этап 6 — TestPyPI (с пользователем):** пользователь настраивает Trusted Publisher, запускает `workflow_dispatch`, я ставлю пакет из TestPyPI и гоняю тесты · AC: AC-18, AC-19

## История изменений
- 2026-10-17 — создан черновик; имя `rustinpy` свободно на PyPI и TestPyPI (проверено: HTTP 404 на `/pypi/rustinpy/json`, `pip index versions` ничего не находит)
- 2026-10-17 — утверждено пользователем («утверждаю»), Q-1…Q-5 закрыты вариантами по умолчанию
