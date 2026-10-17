# Каталог алгоритмов rustinpy

Версия 0.1.0: 449 алгоритмов в 16 модулях, из них NOT VERIFIED - 36, заглушек - 19.
Файл генерируется командой `python scripts/gen_catalog.py`, руками не правится.

Статус: пусто - проверено тестами против эталона; `NV` - код проверен тестами, но условие
задачи не сверено (см. docs/PROGRESS.md); `stub` - заглушка с идеей решения.

| Модуль | Алгоритмов | NV | stub |
|---|---:|---:|---:|
| [`io`](#io) | 8 | 0 | 0 |
| [`interactive`](#interactive) | 9 | 3 | 2 |
| [`mathx`](#mathx) | 68 | 7 | 1 |
| [`ds`](#ds) | 55 | 2 | 2 |
| [`graph`](#graph) | 63 | 0 | 2 |
| [`tree`](#tree) | 20 | 1 | 0 |
| [`dp`](#dp) | 30 | 1 | 0 |
| [`strings`](#strings) | 29 | 2 | 2 |
| [`roman`](#roman) | 7 | 2 | 2 |
| [`bits`](#bits) | 22 | 3 | 0 |
| [`geometry`](#geometry) | 26 | 3 | 1 |
| [`game`](#game) | 9 | 0 | 0 |
| [`introductory`](#introductory) | 28 | 1 | 1 |
| [`sorting`](#sorting) | 37 | 0 | 0 |
| [`counting`](#counting) | 28 | 7 | 0 |
| [`misc`](#misc) | 10 | 4 | 6 |

## io

| Имя | Что делает | Сложность | Задачи | Теги | Статус |
|---|---|---|---|---|---|
| `FastReader` | Token reader over sys.stdin.buffer. (Быстрое чтение токенов из stdin.) | O(input size) once, O(1) per token |  | io, template |  |
| `FastWriter` | Buffered writer: collect pieces, one write at the end. (Буферизованный вывод.) | O(total output) |  | io, template |  |
| `fast_io_template` | Minimal fast I/O skeleton to paste into a solution. (Шаблон решения с быстрым вводом.) | O(1) |  | io, template |  |
| `read_all_ints` | All remaining integers from stdin. (Все оставшиеся числа.) | O(input size) |  | io |  |
| `read_int` | Next integer from stdin. (Следующее целое из stdin.) | O(1) per call after the first one |  | io |  |
| `read_ints` | Next k integers from stdin. (Следующие k целых.) | O(k) |  | io |  |
| `read_str` | Next whitespace-separated token as str. (Следующий токен строкой.) | O(len) |  | io |  |
| `set_input` | Replace the stream behind read_int/read_ints/read_str. (Подменить источник ввода.) | O(1) |  | io |  |

## interactive

| Имя | Что делает | Сложность | Задачи | Теги | Статус |
|---|---|---|---|---|---|
| `answer` | Print the final answer line and flush. (Вывести ответ с flush.) | O(len(line)) |  | interactive |  |
| `colored_chairs` | Find i with color(i) == color((i+1) % n) on an odd circle. (Соседние одинаковые стулья.) | about log2(n) + 2 queries | CSES: Colored Chairs (3273) | interactive, binary-search | NV |
| `find_hidden_rectangle` | Locate a hidden axis-parallel rectangle by 4 binary searches. (Поиск прямоугольника.) | 4 * ceil(log2 n) queries: n = 10^9 -> 120 <= 125 | ICPC-UZ 2024 F | interactive, binary-search, 2d | NV |
| `hidden_permutation` | Recover a permutation from "is p[i] < p[j]?" queries. (Восстановить перестановку.) | O(n log n) queries (Timsort comparisons) | CSES: Hidden Permutation (3139) | interactive, sorting |  |
| `interactive_bisect` | Smallest x in [lo, hi] with pred(x) True, pred monotone. (Бинпоиск по ответу.) | ceil(log2(hi - lo + 1)) calls of pred | CSES: Hidden Integer (3112) | interactive, binary-search |  |
| `inversion_sorting` | CSES Inversion Sorting - not implemented yet. (Заглушка.) | - | CSES: Inversion Sorting | interactive | stub |
| `kth_highest_score` | k-th largest value of two hidden descending arrays. (k-й максимум двух массивов.) | O(log min(n, m)) reads | CSES: K-th Highest Score (3305) | interactive, binary-search | NV |
| `make_ask` | Build ask(query) -> reply with flush and -1/EOF handling. (Запрос к интерактору.) | O(1) per query (plus I/O latency) | ICPC-UZ 2023 I; ICPC-UZ 2024 F; ICPC-UZ 2024 J; ICPC-UZ 2025 J | interactive, template |  |
| `permuted_binary_strings` | CSES Permuted Binary Strings - not implemented yet. (Заглушка.) | - | CSES: Permuted Binary Strings | interactive | stub |

## mathx

| Имя | Что делает | Сложность | Задачи | Теги | Статус |
|---|---|---|---|---|---|
| `Comb` | Factorials and inverse factorials up to n_max. (nCr, nPr, мультиномиальные по модулю.) | O(n_max) build, O(1) per query | CSES: Binomial Coefficients (1079); ICPC-UZ 2025 B | combinatorics, binomial, factorial |  |
| `bell_numbers` | Bell numbers B_0..B_n (set partitions) via the Bell triangle. (Числа Белла.) | O(n^2) |  | combinatorics, bell, partitions |  |
| `berlekamp_massey` | Shortest linear recurrence of a sequence modulo a prime. (Берлекэмп-Месси.) | O(n^2) |  | recurrence, berlekamp-massey |  |
| `bracket_sequences_prefix` | Number of correct bracket sequences of length n starting with prefix. (Скобки с префиксом.) | O(n) | CSES: Bracket Sequences II (2187) | combinatorics, catalan, brackets, reflection |  |
| `candy_lottery` | Expected maximum of n uniform values from 1..k. (Ожидаемый максимум.) | O(k) | CSES: Candy Lottery (1727) | probability, expected-value |  |
| `catalan` | n-th Catalan number C(2n, n) / (n + 1) mod prime. (Числа Каталана.) | O(n) | CSES: Bracket Sequences I (2064) | combinatorics, catalan, brackets |  |
| `common_divisors_max_gcd` | Maximum gcd over all pairs of the array. (Максимальный НОД пары.) | O(M log M), M = max(a) | CSES: Common Divisors (1081) | divisors, gcd |  |
| `convolution` | c[k] = sum a[i] * b[k - i] modulo ANY modulus. (Свёртка по модулю.) | one exact convolution of values < mod, then % mod |  | convolution, decimal, polynomial, modular |  |
| `convolution_int` | Exact convolution of NON-NEGATIVE ints via one decimal product. (Точная свёртка.) | O(N log N) inside libmpdec (it multiplies huge numbers with an NTT in C) |  | convolution, decimal, polynomial |  |
| `convolution_ntt` | c[k] = sum a[i] * b[k - i] modulo an NTT prime, via ntt(). (Свёртка через NTT.) | O((n + m) log(n + m)); naive for short inputs |  | ntt, convolution, polynomial |  |
| `coprime_pairs_count` | Pairs i < j with gcd(a_i, a_j) = 1 (Mobius over divisors). (Взаимно простые пары.) | O(M log M), M = max(a) | CSES: Counting Coprime Pairs (2417) | inclusion-exclusion, mobius, gcd |  |
| `coprime_pairs_up_to` | Ordered pairs (i, j), 1 <= i, j <= n, with gcd(i, j) = 1. (Взаимно простые пары до n.) | O(n^(2/3)) | ICPC-UZ 2023 J | phi, gcd, coprime | NV |
| `count_fib_representations` | Ways to write n as a sum of DISTINCT Fibonacci numbers 1, 2, 3, 5, ... (Число разложений.) | O(log n) | ICPC-UZ 2023 H; ICPC-UZ 2025 J | fibonacci, zeckendorf, dp | NV |
| `crt` | Chinese remainder theorem, moduli not necessarily coprime. (КТО для любых модулей.) | O(k log M) |  | modular, crt |  |
| `deep_numbers_count` | ICPC-UZ 2024 D "Deep Numbers": numbers without a prime digit subsequence. (Заглушка.) | - | ICPC-UZ 2024 D | primes, subsequence, digit-dp | stub |
| `derangements` | Permutations without fixed points D(n). (Беспорядки (никто не получил свой подарок).) | O(n) | CSES: Christmas Party (1717) | combinatorics, derangements |  |
| `det_mod` | Determinant of a square matrix modulo a prime. (Определитель по модулю.) | O(n^3) |  | gauss, determinant, modular |  |
| `dice_probability` | Probability that the sum of n dice lies in [a, b]. (Вероятность суммы кубиков.) | O(n * 6n * 6) | CSES: Dice Probability (1725) | probability, dp, dice |  |
| `divisor_analysis` | Count, sum and product of divisors from the factorization. (Анализ делителей.) | O(k log) | CSES: Divisor Analysis (2182) | divisors |  |
| `divisor_count_table` | Number of divisors d(x) for all x <= n. (Количество делителей для всех чисел.) | O(n log n) | CSES: Counting Divisors (1713) | divisors, sieve |  |
| `divisors` | All divisors of n by trial division up to sqrt(n). (Делители числа.) | O(sqrt n) |  | divisors |  |
| `euler_phi` | Euler's totient of one number by trial division. (Функция Эйлера одного числа.) | O(sqrt n) |  | phi, totient |  |
| `exp_tower` | a^(b^c) mod p for PRIME p via Fermat. (Степень степени по простому модулю.) | O(log b + log c + log p) | CSES: Exponentiation II (1712) | modular, power, fermat |  |
| `ext_gcd` | Extended Euclid: g = gcd(a, b) = a*x + b*y. (Расширенный алгоритм Евклида.) | O(log min(a, b)) |  | modular, gcd |  |
| `factorize` | Prime factorization of n >= 1 (trial division + Pollard rho). (Разложение на простые.) | O(B + n^(1/4)) expected, B = 1000 trial divisions | ICPC-UZ 2024 E | primes, factorization |  |
| `factorize_spf` | Factorize x <= n with a precomputed spf table. (Разложение по таблице spf.) | O(log x) | CSES: Counting Divisors (1713) | primes, factorization, spf |  |
| `fft_convolution_float` | Convolution of real sequences via complex FFT. (Свёртка вещественных чисел.) | O(n log n) |  | fft, convolution, polynomial, float |  |
| `fib` | F(n) mod mod by fast doubling, F(0) = 0, F(1) = 1. (Быстрый Фибоначчи.) | O(log n) | CSES: Fibonacci Numbers (1722) | fibonacci, doubling |  |
| `floor_blocks` | Blocks [l, r] where n // i is constant. (Блоки одинаковых floor(n / i).) | O(sqrt n) blocks (at most 2 * sqrt n) | ICPC-UZ 2023 J; ICPC-UZ 2025 C | floor-blocks, harmonic |  |
| `gauss_float` | Solve A x = b over reals with partial pivoting. (Метод Гаусса с плавающей точкой.) | O(n * m * min(n, m)) |  | gauss, linear-system, float |  |
| `gauss_mod` | Solve A x = b modulo a prime (Gauss-Jordan). (Система уравнений по модулю.) | O(n * m * min(n, m)) | CSES: System of Linear Equations (3154) | gauss, linear-system, modular |  |
| `gcd_sum_pairs` | sum_{i=1}^{n} sum_{j=1}^{n} gcd(i, j). (Сумма НОД всех пар.) | O(n^(2/3)) | ICPC-UZ 2025 C | gcd, phi, floor-blocks | NV |
| `gcd_sum_with_n` | Pillai's function sum_{i=1}^{n} gcd(i, n). (Сумма gcd(i, n).) | O(sqrt n) |  | gcd, pillai |  |
| `grid_colorings_count` | Black/white n x n grids up to rotation (Burnside). (Сетки с точностью до поворота.) | O(log n) | CSES: Counting Grids (2210) | combinatorics, burnside |  |
| `infinite_game_count` | Number of positions after n moves of the digit game. (Бесконечная игра.) | O(9^3 log n) | ICPC-UZ 2025 I | dp, matrix, games | NV |
| `inversion_probability` | Expected inversions when x_i is uniform in [1, r_i]. (Ожидаемое число инверсий.) | O(n^2) | CSES: Inversion Probability (1728) | probability, expected-value, inversions |  |
| `is_prime` | Deterministic Miller-Rabin for n < 3.3 * 10^24. (Проверка простоты Миллера-Рабина.) | O(12 * log^3 n) bit operations | ICPC-UZ 2024 E | primes, miller-rabin |  |
| `linear_recurrence_kth` | k-th term of a_n = sum_{i=1}^{d} coef[i-1] * a_{n-i} (Kitamasa). (k-й член рекуррентности.) | O(d^2 log k) | CSES: Throwing Dice (1096) | recurrence, kitamasa, polynomial |  |
| `linear_sieve` | Linear sieve: smallest prime factor of every x <= n. (Линейное решето (spf).) | O(n) | CSES: Counting Divisors (1713) | primes, sieve, spf |  |
| `mat_mul` | Matrix product modulo mod. (Произведение матриц.) | O(n * m * k) | CSES: Graph Paths I (1723) | matrix |  |
| `mat_pow` | Square matrix to the power e modulo mod. (Матричная экспонента.) | O(n^3 log e) | CSES: Graph Paths I (1723); CSES: Fibonacci Numbers (1722) | matrix, power |  |
| `min_digit_changes_count` | Arrangements of a multiset with the fewest neighbour changes. (Мин. число смен цифр.) | O(len(counts)) | ICPC-UZ 2025 B | combinatorics, blocks, composite-mod | NV |
| `min_trials_for_probability` | Smallest K with 1 - (1 - q)^K >= p. (Минимум попыток, чтобы вероятность успеха была >= p.) | O(1) | ICPC-UZ 2023 D | probability, logarithm, precision | NV |
| `minplus_mat_pow` | Min-plus (tropical) matrix power: cheapest walks with exactly e edges. (Min-plus степень.) | O(n^3 log e) | CSES: Graph Paths II (1724) | matrix, min-plus, shortest-path |  |
| `mobius_table` | Mobius function mu(x) for all x <= n. (Функция Мёбиуса.) | O(n log log n) | CSES: Counting Coprime Pairs (2417) | primes, mobius |  |
| `modinv` | Inverse of a modulo mod (mod need not be prime). (Обратный элемент по модулю.) | O(log m) |  | modular, inverse |  |
| `modpow` | a^e mod m by binary exponentiation. (Быстрое возведение в степень по модулю.) | O(log e) | CSES: Exponentiation (1095) | modular, power |  |
| `moving_robots` | Expected number of empty squares after k random robot moves on 8x8. (Роботы на доске.) | O(64 * k * 64 * 4) | CSES: Moving Robots (1726) | probability, expected-value, grid |  |
| `nCr_composite` | C(n, r) modulo any composite modulus via prime powers + CRT. (nCr по составному модулю.) | O(n * omega(mod) + sqrt(mod)) | ICPC-UZ 2025 B | combinatorics, binomial, composite-mod, crt |  |
| `nCr_lucas` | C(n, r) mod small prime p by Lucas' theorem. (Теорема Люка.) | O(p + log_p n) per call (digit binomials by multiplicative formula) |  | combinatorics, binomial, lucas |  |
| `nCr_pascal` | Pascal triangle C[n][r] mod any modulus. (Треугольник Паскаля по любому модулю.) | O(n_max^2) time and memory | ICPC-UZ 2025 B | combinatorics, binomial, composite-mod |  |
| `necklaces_count` | Necklaces of n beads in m colours up to rotation (Burnside). (Лемма Бернсайда.) | O(n log n) | CSES: Counting Necklaces (2209) | combinatorics, burnside, necklaces |  |
| `next_prime` | Smallest prime strictly greater than n. (Следующее простое.) | O(log^2 n) expected primality tests (prime gaps are small) |  | primes |  |
| `ntt` | In-place number theoretic transform (iterative). (Быстрое преобразование (NTT).) | O(n log n), len(a) must be a power of two |  | ntt, fft, polynomial |  |
| `phi_prefix_sum` | sum_{i=1}^{n} phi(i) for n up to ~10^10 (Du's sieve). (Сумма функции Эйлера.) | O(n^(2/3)) | ICPC-UZ 2023 J | phi, totient, du-sieve, floor-blocks | NV |
| `phi_table` | Euler's totient phi(x) for all x <= n. (Функция Эйлера для всех чисел.) | O(n log log n) | ICPC-UZ 2023 J | primes, phi, totient |  |
| `pollard_rho` | A non-trivial divisor of composite n (Pollard rho, Brent). (Ро-алгоритм Полларда.) | expected O(n^(1/4)) multiplications | ICPC-UZ 2024 E | primes, pollard-rho, factorization |  |
| `prime_multiples_count` | How many of 1..n are divisible by at least one given prime. (Включения-исключения.) | O(number of subsets with product <= n) <= O(2^k) | CSES: Prime Multiples (2185) | inclusion-exclusion |  |
| `primes_up_to` | All primes <= n. (Список простых до n.) | O(n log log n) |  | primes, sieve |  |
| `segmented_sieve` | Primes in [lo, hi] for big hi and moderate hi - lo. (Сегментированное решето.) | O(sqrt(hi) + (hi - lo) log log hi) |  | primes, sieve, segmented |  |
| `sieve` | Sieve of Eratosthenes: is_prime flags for 0..n. (Решето Эратосфена.) | O(n log log n), slice assignment makes it fast in CPython |  | primes, sieve |  |
| `stars_and_bars` | Ways to give m identical apples to n children: C(n + m - 1, m). (Шары и перегородки.) | O(n + m) | CSES: Distributing Apples (1716) | combinatorics, stars-and-bars |  |
| `stirling1_table` | Unsigned Stirling numbers of the first kind c(i, k). (Стирлинг 1-го рода.) | O(n^2) |  | combinatorics, stirling |  |
| `stirling2_table` | Stirling numbers of the second kind S(i, k). (Стирлинг 2-го рода.) | O(n^2) | CSES: Counting Sequences | combinatorics, stirling, partitions |  |
| `sum_of_divisors_sum` | sum_{i=1}^{n} sigma(i) = sum_d d * floor(n / d). (Сумма сумм делителей.) | O(sqrt n) | CSES: Sum of Divisors (1082) | divisors, floor-blocks |  |
| `sum_of_four_squares` | n = a^2 + b^2 + c^2 + d^2 (Lagrange), a >= b >= c >= d >= 0. (Сумма четырёх квадратов.) | fast in practice (a few sqrt checks), worst case O(n^(3/4)) | CSES: Sum of Four Squares (3355) | squares, lagrange |  |
| `throwing_dice` | Ways to get sum n with dice throws 1..6 (ordered). (Броски кубика с суммой n.) | O(36 log n) | CSES: Throwing Dice (1096) | recurrence, dice |  |
| `zeckendorf` | Zeckendorf representation: n as a sum of non-adjacent Fibonacci numbers. (Цекендорф.) | O(log n) | ICPC-UZ 2023 H; ICPC-UZ 2025 J | fibonacci, zeckendorf |  |

## ds

| Имя | Что делает | Сложность | Задачи | Теги | Статус |
|---|---|---|---|---|---|
| `Fenwick` | Fenwick tree: point add, prefix sum, k-th by prefix. (Дерево Фенвика.) | O(n) build, O(log n) per operation | CSES: Dynamic Range Sum Queries (1648); CSES: List Removals (1749) | fenwick, bit, range-sum, kth |  |
| `Fenwick2D` | 2D Fenwick: point add, rectangle sum. (Двумерное дерево Фенвика.) | O(log R * log C) per operation | CSES: Forest Queries II (1739) | fenwick, bit, 2d |  |
| `FenwickRangeAdd` | Fenwick on differences: range add, point query. (Прибавление на отрезке, значение в точке.) | O(log n) per operation | CSES: Range Update Queries (1651) | fenwick, bit, range-update |  |
| `FenwickRangeRange` | Two Fenwicks: range add AND range sum. (Прибавление и сумма на отрезке.) | O(log n) per operation |  | fenwick, bit, range-update, range-sum |  |
| `ImplicitTreap` | Implicit treap (array by position) with reversal and range min. (Неявное декартово дерево.) | O(n) build, O(log n) expected per operation | CSES: Cut and Paste (2072); CSES: Substring Reversals (2073); CSES: Reversal Sorting (2074) | treap, implicit-treap, reverse |  |
| `LazySegAddMin` | Range add + range min. (Прибавление на отрезке, минимум на отрезке.) | O(log n) per operation |  | segment-tree, lazy, range-add, range-min |  |
| `LazySegAddSum` | Range add + range sum. (Прибавление и сумма на отрезке.) | O(log n) per operation |  | segment-tree, lazy, range-add, range-sum |  |
| `LazySegArithmetic` | Add an arithmetic progression on a range + range sum. (Прибавление прогрессии.) | O(log n) per operation | CSES: Polynomial Queries (1736) | segment-tree, lazy, arithmetic-progression, range-sum |  |
| `LazySegAssignAddSum` | Range assign + range add + range sum. (Присвоение и прибавление на отрезке, сумма.) | O(log n) per operation | CSES: Range Updates and Sums (1735) | segment-tree, lazy, range-assign, range-add, range-sum |  |
| `MergeSortTree` | Each node keeps its sorted subarray: count values <= x on a range. (Дерево сортировок.) | O(n log n) build and memory, O(log^2 n) per query |  | segment-tree, merge-sort-tree, counting |  |
| `MinStack` | Stack with O(1) minimum. (Стек минимумов.) | O(1) per operation |  | stack, min-stack |  |
| `MonotonicQueue` | FIFO queue with O(1) amortised min (or max). (Монотонная очередь.) | O(1) amortised per operation | CSES: Sliding Window Minimum (3221) | monotonic-queue, sliding-window, deque |  |
| `PersistentSegTree` | Persistent sum segment tree: every set() returns a new version. (Персистентное дерево.) | O(n) build, O(log n) time and memory per set / query | CSES: Range Queries and Copies (1737) | segment-tree, persistent |  |
| `PrefixSum2D` | 2D prefix sums for rectangle sums. (Двумерные префиксные суммы.) | O(R * C) build, O(1) per query | CSES: Forest Queries (1652) | prefix-sums, 2d, range-sum |  |
| `SegTree` | Iterative segment tree for any monoid (op associative, e identity). (Дерево отрезков.) | O(n) build, O(log n) per operation | CSES: Dynamic Range Minimum Queries (1649); CSES: Hotel Queries (1143) | segment-tree, range-query, binary-search |  |
| `SegTreeFlipRuns` | Range flip of bits + number of all-ones subarrays. (Инверсия отрезка и серии единиц.) | O(log n) per operation | ICPC-UZ 2025 H | segment-tree, lazy, flip, runs, merge-nodes | NV |
| `SegTreeMaxPrefix` | Point set + maximum prefix sum inside a range. (Максимальная префиксная сумма.) | O(log n) per operation | CSES: Prefix Sum Queries (2166) | segment-tree, prefix-sums, merge-nodes |  |
| `SegTreeMaxSubarray` | Point set + maximum subarray sum on a range (node merge). (Максимальная подсумма.) | O(log n) per operation | CSES: Subarray Sum Queries (1190) | segment-tree, max-subarray, merge-nodes |  |
| `SegTreeRuns` | Longest run of equal characters with point changes. (Самая длинная серия одинаковых.) | O(log n) per change | CSES: Bit Inversions (1188) | segment-tree, runs, merge-nodes |  |
| `SortedList` | Sorted multiset: add / remove / k-th / rank, bucket-based. (Мультимножество.) | O(sqrt n) per operation, but buckets are C-level lists -> fast in practice | CSES: Concert Tickets (1091); CSES: Salary Queries (1144); CSES: Sliding Window Median (1076) | sorted-list, ordered-set, order-statistics, multiset |  |
| `SparseTable` | Static range query for idempotent op (min, max, gcd, and, or). (Разреженная таблица.) | O(n log n) build, O(1) per query | CSES: Static Range Minimum Queries (1647) | sparse-table, rmq, range-min |  |
| `SqrtDecomposition` | Blocks of size ~sqrt(n): point set + range sum. (Корневая декомпозиция.) | O(1) set, O(sqrt n) query |  | sqrt, decomposition, range-sum |  |
| `Treap` | Ordered multiset on a treap: insert, erase, k-th, rank. (Декартово дерево по ключу.) | O(log n) expected per operation |  | treap, ordered-set, order-statistics |  |
| `TwoStackQueue` | Queue with O(1) amortised aggregate for any associative op. (Очередь на двух стеках.) | O(1) amortised per operation | CSES: Sliding Window Or (3405) | queue, two-stacks, sliding-window, monoid |  |
| `cut_and_paste` | Repeatedly cut s[l:r] and append it to the end. (Вырезать и вставить в конец.) | O((n + q) log n) expected | CSES: Cut and Paste (2072) | treap, implicit-treap, strings |  |
| `distinct_values_queries` | Number of distinct values in a[l:r], offline by right end. (Различные значения на отрезке.) | O((n + q) log n) | CSES: Distinct Values Queries (1734) | fenwick, offline, distinct |  |
| `dynamic_connectivity_offline` | Components count after each edge addition / removal (offline). (Динамическая связность.) | O(q log q log n) | CSES: Dynamic Connectivity (2133) | dsu, rollback, offline, divide-and-conquer |  |
| `exclusions` | ICPC-UZ 2025 E "Exclusions": f(k) for splitting into k blocks by mex. (Заглушка.) | - | ICPC-UZ 2025 E | mex, partition, dp | stub |
| `generic_strings` | ICPC-UZ 2023 G "Generic Strings": no repeats on windows after deletions. (Заглушка.) | - | ICPC-UZ 2023 G | two-pointers, binary-search, strings | stub |
| `hotel_queries` | Each group takes the first hotel with enough free rooms. (Первый подходящий отель.) | O((n + m) log n) | CSES: Hotel Queries (1143) | segment-tree, descend, first-fit |  |
| `isotonic_sse_mod` | Least squares error of the best non-decreasing fit, mod prime. (Ошибка подгонки по модулю.) | O(n) | ICPC-UZ 2023 L | isotonic-regression, pav, modular | NV |
| `list_removals` | Remove elements by their CURRENT position; report removed values. (Удаление по позиции.) | O(n log n) | CSES: List Removals (1749) | fenwick, kth, order-statistics |  |
| `longest_window_no_repeats` | Length of the longest substring without repeated characters. (Окно без повторов.) | O(n) | CSES: Playlist (1141); ICPC-UZ 2023 G | two-pointers, distinct, window |  |
| `missing_coin_sum_queries` | Smallest sum that coins a[l:r] cannot form. (Наименьшая непредставимая сумма на отрезке.) | O(n log n + q * 30 * log n) | CSES: Missing Coin Sum Queries (2184) | sparse-table, greedy, powers-of-two |  |
| `mo_distinct_count` | Number of distinct values in a[l:r] with Mo's algorithm. (Различные значения (Мо).) | O((n + q) sqrt n) | CSES: Distinct Values Queries (1734) | mo, offline, distinct |  |
| `mo_order` | Order of offline range queries for Mo's algorithm. (Порядок запросов для Мо.) | O(q log q) sorting; total pointer moves O((n + q) sqrt n) | CSES: Distinct Values Queries (1734) | mo, offline, sqrt |  |
| `mo_with_updates` | Mo's algorithm with point updates: distinct values in a[l:r]. (Мо с изменениями.) | O(n^(5/3)) with block = n^(2/3) |  | mo, offline, updates |  |
| `movie_festival_queries` | Max number of non-overlapping movies inside [a, b]. (Сколько фильмов успеть за [a, b].) | O((n + q + T) log T), T = number of distinct time points | CSES: Movie Festival Queries (1664) | binary-lifting, greedy, intervals |  |
| `new_roads_queries` | Earliest day when a and b get connected (edge i on day i + 1). (Когда станут связаны.) | O((m + q) log n) | CSES: New Roads Queries (2101) | dsu, offline, timestamps |  |
| `pav` | Best non-decreasing least-squares fit as blocks of equal values. (Изотоническая регрессия.) | O(n) amortised (stack of blocks) | ICPC-UZ 2023 L | isotonic-regression, pav, stack, least-squares |  |
| `pizzeria_queries` | min_i (p_i + \|i - k\|) with point updates. (Ближайшая дешёвая пиццерия.) | O((n + q) log n) | CSES: Pizzeria Queries (2206) | segment-tree, abs-trick |  |
| `prefix_sums` | Prefix sums p[i] = a[0] + ... + a[i-1]. (Префиксные суммы.) | O(n) build, O(1) per query | CSES: Static Range Sum Queries (1646) | prefix-sums, range-sum |  |
| `range_kth_smallest` | k-th smallest value in a[l:r] for many queries (persistent tree). (k-я статистика.) | O((n + q) log n) |  | persistent, kth, order-statistics, offline |  |
| `reversal_sorting` | Sort an array with at most n reversals; return them. (Сортировка разворотами.) | O(n log n) expected | CSES: Reversal Sorting (2074) | treap, implicit-treap, sorting, construction |  |
| `salary_queries` | Point changes of salaries + count of salaries in [a, b]. (Запросы о зарплатах.) | O((n + q) log(n + q)) | CSES: Salary Queries (1144) | fenwick, offline, compression |  |
| `sliding_window_distinct` | Number of distinct values in every window. (Различные значения в окне.) | O(n) expected | CSES: Sliding Window Distinct Values (3222) | sliding-window, distinct, counting |  |
| `sliding_window_inversions` | Number of inversions inside every window. (Инверсии в окне.) | O(n log n) | CSES: Sliding Window Inversions (3223) | sliding-window, inversions, fenwick |  |
| `sliding_window_mex` | Mex (smallest missing non-negative integer) of every window. (Mex в окне.) | O(n log k) | CSES: Sliding Window Mex (3219) | sliding-window, mex, heap |  |
| `sliding_window_min` | Minimum of every window of length k (monotonic deque). (Минимум в окне.) | O(n) | CSES: Sliding Window Minimum (3221) | sliding-window, deque, range-min |  |
| `sliding_window_mode` | Most frequent value of every window (smallest on ties). (Мода в окне.) | O(n log n) | CSES: Sliding Window Mode (3224) | sliding-window, mode, heap |  |
| `sliding_window_or` | Bitwise or of every window of length k (two-stack queue). (Or в окне.) | O(n) amortised | CSES: Sliding Window Or (3405) | sliding-window, or, two-stacks |  |
| `sliding_window_sum` | Sum of every window of length k. (Сумма в окне.) | O(n) | CSES: Sliding Window Sum (3220) | sliding-window, prefix-sums |  |
| `sliding_window_xor` | Xor of every window of length k. (Xor в окне.) | O(n) | CSES: Sliding Window Xor (3426) | sliding-window, xor, prefix-sums |  |
| `subarray_mex_offline` | Mex of a[l:r] for many queries, offline by right end. (Mex на подотрезке.) | O((n + q) log n) | ICPC-UZ 2025 E | mex, offline, segment-tree |  |
| `substring_reversals` | Repeatedly reverse s[l:r]. (Развороты подстрок.) | O((n + q) log n) expected | CSES: Substring Reversals (2073) | treap, implicit-treap, strings, reverse |  |

## graph

| Имя | Что делает | Сложность | Задачи | Теги | Статус |
|---|---|---|---|---|---|
| `DSU` | Union-find with union by size and path halving. (Система непересекающихся множеств.) | ~O(alpha(n)) amortised per operation | CSES: Road Construction (1676); CSES: Building Roads (1666) | dsu, union-find |  |
| `Dinic` | Dinic max flow with iterative augmenting (no recursion). (Максимальный поток (Диниц).) | O(V^2 E) worst case, much faster in practice; O(E sqrt V) on unit graphs | CSES: Download Speed (1694); CSES: Police Chase (1695); CSES: School Dance (1696) | flow, dinic, max-flow, min-cut |  |
| `MinCostFlow` | Min-cost flow by successive shortest paths (SPFA). (Поток минимальной стоимости.) | O(F * V * E) worst case (SPFA per augmentation) | CSES: Parcel Delivery (2121); CSES: Task Assignment | flow, min-cost-flow, spfa |  |
| `RollbackDSU` | Union-find with undo (no path compression). (СНМ с откатом.) | O(log n) per find / union, O(1) per undone union | CSES: Dynamic Connectivity (2133) | dsu, rollback, offline |  |
| `articulation_points` | Cut vertices of an undirected graph (lowlink, iterative). (Точки сочленения.) | O(n + m) | CSES: Necessary Cities (2076) | articulation-points, lowlink, dfs |  |
| `bellman_ford` | Shortest paths with negative edges; -INF where a negative cycle interferes. (Беллман-Форд.) | O(n * m) | CSES: High Score (1673) | bellman-ford, negative-weights, shortest-path |  |
| `bfs` | Distances in edges from src in an unweighted graph. (Обход в ширину.) | O(n + m) | CSES: Message Route (1667) | bfs, shortest-path, unweighted |  |
| `bfs_path` | One shortest path src -> dst in an unweighted graph. (Кратчайший путь BFS.) | O(n + m) | CSES: Message Route (1667) | bfs, path |  |
| `bipartite_coloring` | 2-colouring of an undirected graph, or None if it has an odd cycle. (Двудольность.) | O(n + m) | CSES: Building Teams (1668) | bipartite, coloring, bfs |  |
| `bridges` | Bridges of an undirected multigraph (lowlink, iterative). (Мосты.) | O(n + m) |  | bridges, lowlink, dfs |  |
| `build_lifting` | Jump table up[j][x] = f applied 2^j times to x. (Двоичные подъёмы по функции.) | O(n log K) time and memory | CSES: Planets Queries I (1750) | functional-graph, binary-lifting |  |
| `bus_companies` | CSES Bus Companies - not implemented yet. (Заглушка.) | - | CSES: Bus Companies | shortest-path, companies | stub |
| `coin_collector` | Max coins collected on a walk (re-visits allowed) in a directed graph. (Сборщик монет.) | O(n + m) | CSES: Coin Collector (1686) | scc, dag, dp |  |
| `condensation` | DAG of strongly connected components (no duplicate edges). (Конденсация графа.) | O(n + m) | CSES: Coin Collector (1686) | scc, condensation, dag |  |
| `connected_components` | Connected components of an undirected graph. (Компоненты связности.) | O(n + m) | CSES: Building Roads (1666); CSES: Counting Rooms (1192) | components, bfs |  |
| `count_paths_dag` | Number of paths src -> dst in a DAG. (Количество путей в DAG.) | O(n + m) | CSES: Game Routes (1681) | dag, counting, dp |  |
| `critical_cities` | Vertices lying on EVERY path 0 -> n-1 of a directed graph. (Критические города.) | O(n + m) | CSES: Critical Cities (1703) | dominators, path, bfs |  |
| `cycle_steps` | Steps from each start until a vertex repeats (tail + cycle). (Длина пути до повтора.) | O(n) | CSES: Planets Cycles (1751) | functional-graph, cycles |  |
| `dfs_order` | Iterative DFS: preorder and DFS-tree parents. (Итеративный обход в глубину.) | O(n + m) | CSES: Building Roads (1666) | dfs, iterative |  |
| `dijkstra` | Shortest paths from src, non-negative weights. (Кратчайшие пути из src.) | O((n + m) log n) | CSES: Shortest Routes I (1671) | dijkstra, shortest-path |  |
| `dijkstra_coupon` | Cheapest route when one edge may be halved (floor). (Дейкстра с купоном.) | O((n + m) log n) | CSES: Flight Discount (1195) | dijkstra, states, coupon |  |
| `dijkstra_path` | Shortest distance and one shortest path src -> dst. (Дейкстра с восстановлением пути.) | O((n + m) log n) |  | dijkstra, shortest-path, path |  |
| `dijkstra_states` | Dijkstra over any hashable states (vertex + terminal / mask). (Дейкстра на состояниях.) | O(S log S) over reachable states S |  | dijkstra, states, generic |  |
| `dijkstra_stats` | Dijkstra + number of shortest paths, min and max edges among them. (Статистика путей.) | O((n + m) log n) | CSES: Investigation (1202) | dijkstra, counting |  |
| `edge_disjoint_paths` | Maximum set of edge-disjoint directed paths s -> t. (Рёберно-непересекающиеся пути.) | unit-capacity max flow + flow decomposition | CSES: Distinct Routes (1711) | flow, disjoint-paths |  |
| `edmonds_karp` | Max flow by shortest augmenting paths (BFS). (Эдмондс-Карп.) | O(V E^2) | CSES: Download Speed (1694) | flow, edmonds-karp, max-flow |  |
| `escalators` | ICPC-UZ 2023 E "Escalators": movement graph with single-vertex changes. (Заглушка.) | - | ICPC-UZ 2023 E | functional-graph, updates | stub |
| `euler_path_directed` | Directed Euler path src -> dst using every edge once. (Эйлеров путь (ориентированный).) | O(n + m) | CSES: Teleporters Path (1693) | euler, hierholzer, directed |  |
| `euler_path_undirected` | Euler path / cycle of an undirected multigraph. (Эйлеров путь (неориентированный).) | O(n + m) | CSES: Mail Delivery (1691) | euler, hierholzer, undirected |  |
| `even_outdegree_edges` | Orient edges so every vertex has even out-degree. (Чётные исходящие степени.) | O(n + m) | CSES: Even Outdegree Edges (2179) | orientation, dfs, parity |  |
| `find_cycle_directed` | Any directed cycle (three-colour DFS). (Цикл в ориентированном графе.) | O(n + m) | CSES: Round Trip II (1678) | cycle, dfs, directed |  |
| `find_cycle_undirected` | Any cycle of a simple undirected graph. (Цикл в неориентированном графе.) | O(n + m) | CSES: Round Trip (1669) | cycle, dfs, undirected |  |
| `find_negative_cycle` | Any negative cycle of a directed graph. (Поиск отрицательного цикла.) | O(n * m) | CSES: Cycle Finding (1197) | bellman-ford, negative-cycle |  |
| `flight_route_requests` | Fewest one-way routes so that every a reaches b. (Запросы на маршруты.) | O(n + m) | CSES: Flight Route Requests (1699) | dsu, dag, construction |  |
| `floyd_warshall` | All-pairs shortest paths. (Флойд-Уоршелл.) | O(n^3) | CSES: Shortest Routes II (1672) | floyd-warshall, all-pairs |  |
| `functional_distance` | Minimal number of steps from a to b, or -1. (Расстояние в функциональном графе.) | O(n + q) | CSES: Planets Queries II (1160) | functional-graph, distance, euler-tour |  |
| `girth` | Length of the shortest cycle of a simple undirected graph. (Обхват графа.) | O(n * (n + m)) | CSES: Graph Girth (1707) | cycle, girth, bfs |  |
| `grid_bfs` | BFS on a grid with 4-neighbourhood. (BFS по клетчатому полю.) | O(R * C) | CSES: Labyrinth (1193); CSES: Counting Rooms (1192) | bfs, grid |  |
| `hamiltonian_path` | Any Hamiltonian path of a directed graph (bitmask DP over end sets). (Гамильтонов путь.) | O(2^n * n) with bitset rows | CSES: Hamiltonian Flights (1690) | hamiltonian, bitmask-dp |  |
| `hopcroft_karp` | Maximum bipartite matching, Hopcroft-Karp with iterative DFS. (Хопкрофт-Карп.) | O(E sqrt V) | CSES: School Dance (1696) | matching, hopcroft-karp, bipartite |  |
| `hungarian` | Minimum-cost assignment of n rows to distinct columns (n <= m). (Венгерский алгоритм.) | O(n^2 m) | CSES: Task Assignment (2129) | assignment, hungarian, matching |  |
| `k_shortest_walks` | Costs of the k cheapest walks src -> dst (vertices may repeat). (k кратчайших маршрутов.) | O(k (n + m) log(k m)) | CSES: Flight Routes (1196) | dijkstra, k-shortest |  |
| `knights_tour` | Knight's tour from (r, c) on an n x n board (Warnsdorff). (Обход доски конём.) | O(n^2 * 8) per attempt, a few attempts in practice | CSES: Knight's Tour (1689) | knights-tour, warnsdorff, heuristic |  |
| `kruskal` | Minimum spanning tree by Kruskal. (Минимальный остов (Краскал).) | O(m log m) | CSES: Road Reparation (1675) | mst, kruskal, dsu |  |
| `kth_successor` | f^k(x) using a table from build_lifting. (k-й преемник.) | O(log k) | CSES: Planets Queries I (1750) | functional-graph, binary-lifting |  |
| `kuhn_matching` | Maximum bipartite matching by Kuhn's augmenting paths (iterative). (Алгоритм Куна.) | O(V * E) | CSES: School Dance (1696) | matching, kuhn, bipartite |  |
| `longest_path_dag` | Path src -> dst with the most vertices in a DAG. (Самый длинный путь в DAG.) | O(n + m) | CSES: Longest Flight Route (1680) | dag, longest-path, dp |  |
| `max_score_path` | Max total weight of a path src -> dst; None if unbounded. (Максимальный путь (High Score).) | O(n * m) | CSES: High Score (1673) | bellman-ford, longest-path, positive-cycle |  |
| `min_cut_edges` | Edges of a minimum s-t cut. (Минимальный разрез.) | one max flow | CSES: Police Chase (1695) | flow, min-cut |  |
| `multi_source_bfs` | BFS from many sources at once: distance to the nearest source. (BFS из многих источников.) | O(n + m) | CSES: Monsters (1194) | bfs, multi-source |  |
| `network_renovation` | New edges making a tree 2-edge-connected (no bridges). (Ремонт сети.) | O(n) | CSES: Network Renovation (1704) | tree, leaves, construction, 2-edge-connected |  |
| `prim` | Minimum spanning tree weight by Prim (lazy heap). (Минимальный остов (Прим).) | O(m log m) | CSES: Road Reparation (1675) | mst, prim, heap |  |
| `reachability_queries` | Can a reach b? for many pairs in a general digraph. (Запросы достижимости.) | O(n + m) + O(k * m_c / 64) for the bitsets | CSES: Reachability Queries (2143) | reachability, scc, bitset |  |
| `reachable_counts` | How many vertices each vertex of a DAG reaches (itself too). (Достижимые вершины.) | O(n * m / 64) word operations | CSES: Reachable Nodes (2138) | dag, reachability, bitset |  |
| `road_construction` | After each added road: number of components and the largest one. (Строительство дорог.) | O(m alpha(n)) | CSES: Road Construction (1676) | dsu, components |  |
| `scc_kosaraju` | Strongly connected components by Kosaraju (two iterative passes). (Алгоритм Косараю.) | O(n + m) | CSES: Planets and Kingdoms (1683) | scc, kosaraju |  |
| `scc_tarjan` | Strongly connected components by Tarjan (iterative). (Компоненты сильной связности.) | O(n + m) | CSES: Planets and Kingdoms (1683) | scc, tarjan |  |
| `strongly_connected_edges` | Orient edges to make the graph strongly connected. (Ориентация до сильной связности.) | O(n + m) | CSES: Strongly Connected Edges (2177) | orientation, dfs, strong-connectivity |  |
| `toposort_kahn` | Topological order by Kahn's algorithm. (Топологическая сортировка (Кан).) | O(n + m) | CSES: Course Schedule (1679) | toposort, kahn, dag |  |
| `toposort_lex_min` | Lexicographically smallest topological order. (Лексикографически первая топосортировка.) | O((n + m) log n) |  | toposort, lexicographic, heap |  |
| `toposort_smallest_first` | Order with vertex 0 as early as possible, then 1, ... (Курс «Course Schedule II».) | O((n + m) log n) | CSES: Course Schedule II (1757) | toposort, reverse-graph, heap |  |
| `two_sat` | 2-SAT: satisfy all clauses (x_a == va) OR (x_b == vb). (Задача 2-SAT.) | O(n_vars + clauses) | CSES: Giant Pizza (1684) | 2-sat, scc, logic |  |
| `zero_one_bfs` | Shortest paths when every weight is 0 or 1 (deque). (Обход 0-1 BFS на деке.) | O(n + m) | ICPC-UZ 2024 I | 0-1-bfs, shortest-path, deque |  |

## tree

| Имя | Что делает | Сложность | Задачи | Теги | Статус |
|---|---|---|---|---|---|
| `HLD` | Heavy-light decomposition with a max segment tree on paths. (Тяжёлые пути (HLD).) | O(n) build, O(log^2 n) per path query | CSES: Path Queries II (2134) | tree, hld, segment-tree, path |  |
| `LCA` | Lowest common ancestor by binary lifting. (LCA двоичными подъёмами.) | O(n log n) build, O(log n) per query | CSES: Company Queries I (1687); CSES: Company Queries II (1688); CSES: Distance Queries (1135) | tree, lca, binary-lifting |  |
| `LCAEuler` | LCA via Euler tour + sparse table: O(1) per query. (LCA через эйлеров обход.) | O(n log n) build, O(1) per query | CSES: Distance Queries (1135) | tree, lca, euler-tour, sparse-table |  |
| `PathSumQueries` | Point update + sum on the root -> v path. (Суммы на пути от корня.) | O(n log n) build, O(log n) per operation | CSES: Path Queries (1138) | tree, euler-tour, fenwick, path |  |
| `SubtreeQueries` | Point update + subtree sum (Euler tour + Fenwick). (Запросы на поддеревьях.) | O(n log n) build, O(log n) per operation | CSES: Subtree Queries (1137) | tree, euler-tour, fenwick, subtree |  |
| `centroid_decomposition` | Centroid tree: parent of every vertex in it. (Центроидная декомпозиция.) | O(n log n) | CSES: Finding a Centroid (2079) | tree, centroid, decomposition |  |
| `counting_paths` | For every vertex: how many of the given paths pass through it. (Разности на дереве.) | O((n + q) log n) | CSES: Counting Paths (1136) | tree, lca, difference-array |  |
| `distinct_colors` | Number of distinct colours in every subtree. (Различные цвета в поддеревьях.) | O(n log n) set insertions | CSES: Distinct Colors (1139) | tree, small-to-large, sets |  |
| `euler_tour` | DFS entry indices: subtree of v is [tin[v], tout[v]). (Эйлеров обход (tin/tout).) | O(n) | CSES: Subtree Queries (1137) | tree, euler-tour, subtree |  |
| `find_centroid` | A centroid: removing it leaves components of size <= n / 2. (Центроид дерева.) | O(n) | CSES: Finding a Centroid (2079) | tree, centroid |  |
| `fix_the_leak` | Prune k vertices (leaf by leaf) to leave the fewest leaves. (Почини утечку.) | O(n log n) | ICPC-UZ 2025 F | tree, greedy, leaves, long-path | NV |
| `fixed_length_paths` | Number of paths with exactly k edges. (Пути длины ровно k.) | O(n log n) | CSES: Fixed-Length Paths I (2080) | tree, centroid, paths, counting |  |
| `fixed_length_paths_range` | Number of paths whose length is in [k1, k2]. (Пути длины от k1 до k2.) | O(n log n) (subtrees merged by increasing depth, prefix sums rebuilt) | CSES: Fixed-Length Paths II (2081) | tree, centroid, paths, counting |  |
| `subtree_sizes` | Size of every subtree. (Размеры поддеревьев.) | O(n) | CSES: Subordinates (1674) | tree, subtree, dp |  |
| `tree_diameter` | Longest path of a tree (in edges) by two BFS. (Диаметр дерева.) | O(n) | CSES: Tree Diameter (1131) | tree, diameter, bfs |  |
| `tree_distance_sums` | Sum of distances from every vertex to all others. (Суммы расстояний (перекорневание).) | O(n) | CSES: Tree Distances II (1133) | tree, rerooting, dp |  |
| `tree_farthest` | Distance from every vertex to the farthest vertex. (Расстояние до самой дальней вершины.) | O(n) | CSES: Tree Distances I (1132) | tree, diameter, eccentricity |  |
| `tree_isomorphic` | Are two trees isomorphic? (AHU canonical forms). (Изоморфизм деревьев.) | O(n log n) | CSES: Tree Isomorphism I (1700); CSES: Tree Isomorphism II (1701) | tree, isomorphism, hashing, ahu |  |
| `tree_matching` | Maximum matching in a tree (greedy from the leaves). (Паросочетание в дереве.) | O(n) | CSES: Tree Matching (1130) | tree, matching, greedy |  |
| `tree_parents_order` | BFS order and parents of a rooted tree (base of tree DP). (Порядок обхода дерева.) | O(n) | CSES: Subordinates (1674) | tree, bfs, order |  |

## dp

| Имя | Что делает | Сложность | Задачи | Теги | Статус |
|---|---|---|---|---|---|
| `LiChaoTree` | Li Chao tree: insert lines y = kx + b, query min at integer x. (Дерево Ли Чао.) | O(log C) per operation, C = hi - lo; nodes are created lazily | CSES: Lines and Queries I (3204) | cht, li-chao, lines, min |  |
| `MonotoneCHT` | Convex hull trick: slopes DECREASE, min queries at any x. (Монотонный CHT.) | O(1) amortised add, O(log n) query |  | cht, convex-hull-trick, lines, min |  |
| `array_description` | Fill zeros with 1..m so that neighbours differ by at most 1. (Описание массива.) | O(n * m) | CSES: Array Description (1746) | dp, counting, arrays |  |
| `coin_combinations_ordered` | Number of ORDERED sequences of coins with sum x. (Комбинации монет (порядок важен).) | O(n * x) | CSES: Coin Combinations I (1635) | dp, coins, counting |  |
| `coin_combinations_unordered` | Number of multisets of coins with sum x. (Комбинации монет (порядок не важен).) | O(n * x) | CSES: Coin Combinations II (1636) | dp, coins, counting |  |
| `count_increasing_subsequences` | Number of strictly increasing subsequences. (Число возрастающих подпоследовательностей.) | O(n log n) | CSES: Increasing Subsequence II (1748) | dp, lis, fenwick, counting |  |
| `counting_numbers` | Numbers in [a, b] without two equal adjacent digits (digit DP). (Подсчёт чисел (digit DP).) | O(digits * 10) | CSES: Counting Numbers (2220) | dp, digit-dp |  |
| `counting_tilings` | Domino tilings of an n x m grid (broken profile DP). (Подсчёт замощений (DP по профилю).) | O(n * m * 2^n) | CSES: Counting Tilings (2181) | dp, profile, broken-profile, tilings |  |
| `counting_towers` | Number of towers of width 2 and height n built from rectangles. (Подсчёт башен.) | O(n) | CSES: Counting Towers (2413) | dp, counting, tilings |  |
| `dc_optimization` | Split 0..n-1 into k segments minimising sum cost(l, r). (D&C-оптимизация.) | O(k * n log n) cost evaluations | CSES: Houses and Schools (3354) | dp, divide-and-conquer-optimization |  |
| `dice_combinations` | Ordered ways to get sum n with dice throws 1..6. (Комбинации кубика.) | O(6n) | CSES: Dice Combinations (1633) | dp, counting, dice |  |
| `edit_distance` | Levenshtein distance (insert / delete / replace). (Расстояние редактирования.) | O(\|a\| * \|b\|) time, O(\|b\|) memory | CSES: Edit Distance (1639) | dp, strings, edit-distance |  |
| `elevator_rides` | Min rides of an elevator with capacity cap (bitmask DP). (Поездки на лифте.) | O(2^n * n) | CSES: Elevator Rides (1653) | dp, bitmask |  |
| `fence_painting` | Colour the zeros with 1..k so that neighbours always differ. (Покраска забора.) | O(n) | ICPC-UZ 2023 F | dp, coloring, counting | NV |
| `grid_paths` | Paths from top-left to bottom-right moving right / down, avoiding '*'. (Пути по сетке.) | O(R * C) | CSES: Grid Paths (1638) | dp, grid, counting |  |
| `hamiltonian_flights` | Number of routes 0 -> n-1 visiting every city exactly once. (Гамильтоновы маршруты.) | O(2^n * m) | CSES: Hamiltonian Flights (1690) | dp, bitmask, hamiltonian, counting |  |
| `houses_and_schools` | Place k schools; minimise sum c_i * distance to the nearest school. (Дома и школы.) | O(k n log^2 n) | CSES: Houses and Schools (3354) | dp, divide-and-conquer-optimization, median |  |
| `knapsack_01` | 0/1 knapsack: each item at most once. (Рюкзак 0/1.) | O(n * cap) | CSES: Book Shop (1158) | dp, knapsack |  |
| `knapsack_bounded` | Knapsack where item i has counts[i] copies (binary splitting). (Ограниченный рюкзак.) | O(cap * sum log counts) | CSES: Book Shop II (1159) | dp, knapsack, bounded, binary-splitting |  |
| `knapsack_unbounded` | Knapsack with unlimited copies of each item. (Неограниченный рюкзак.) | O(n * cap) |  | dp, knapsack, unbounded |  |
| `knuth_optimization` | Min total cost to split an array into single elements. (Оптимизация Кнута.) | O(n^2) | CSES: Knuth Division (2088) | dp, knuth-optimization, intervals |  |
| `lcs` | One longest common subsequence (restored). (Наибольшая общая подпоследовательность.) | O(n * m) | CSES: Longest Common Subsequence (3403) | dp, lcs, subsequence |  |
| `lis` | Indices of one longest increasing subsequence. (Наибольшая возрастающая подпосл-ть.) | O(n log n) | CSES: Increasing Subsequence (1145) | dp, lis, binary-search |  |
| `lis_length` | Length of the longest increasing subsequence. (Длина LIS.) | O(n log n) | CSES: Increasing Subsequence (1145) | dp, lis, binary-search |  |
| `min_coins` | Fewest coins (unlimited supply) with sum exactly x. (Минимум монет.) | O(n * x) | CSES: Minimizing Coins (1634) | dp, coins, unbounded |  |
| `money_sums` | All sums obtainable from a subset of coins (bitset on a Python int). (Суммы монет.) | O(n * S / 64), S = total sum | CSES: Money Sums (1745) | dp, subset-sum, bitset |  |
| `rectangle_cutting` | Min cuts to split an a x b rectangle into squares. (Разрезание прямоугольника.) | O(a * b * (a + b)) | CSES: Rectangle Cutting (1744) | dp, intervals, 2d |  |
| `removal_game` | Optimal score of the first player taking from either end. (Игра с удалением.) | O(n^2) | CSES: Removal Game (1097) | dp, intervals, games |  |
| `removing_digits` | Min steps to reach 0 subtracting one of the current digits. (Удаление цифр.) | O(n * digits) | CSES: Removing Digits (1637) | dp, greedy, digits |  |
| `weighted_interval_scheduling` | Max total reward of non-overlapping projects [start, end] (inclusive days). (Проекты.) | O(n log n) | CSES: Projects (1140) | dp, intervals, scheduling, binary-search |  |

## strings

| Имя | Что делает | Сложность | Задачи | Теги | Статус |
|---|---|---|---|---|---|
| `AhoCorasick` | Aho-Corasick automaton for many patterns at once. (Ахо-Корасик.) | O(sum \|patterns\| + \|text\|) (+ alphabet in dict transitions) | CSES: Finding Patterns (2102); CSES: Counting Patterns (2103); CSES: Pattern Positions (2104) | strings, aho-corasick, matching, automaton |  |
| `PalindromeQueries` | Character updates + "is s[l:r] a palindrome?". (Запросы палиндромов.) | O(n log n) build, O(log n) per operation | CSES: Palindrome Queries (2420) | strings, hashing, fenwick, palindrome |  |
| `StringHash` | Polynomial hash modulo 2^61 - 1 with a random base. (Хеш строки по модулю 2^61-1.) | O(n) build, O(1) per get |  | strings, hashing, polynomial-hash |  |
| `StringHashDouble` | Double polynomial hash (mods 10^9 + 7 and 998244353). (Двойной хеш.) | O(n) build, O(1) per get |  | strings, hashing, double-hash |  |
| `SuffixAutomaton` | Suffix automaton with occurrence counts and k-th substring queries. (Суффиксный автомат.) | O(n * \|alphabet\|) build (dict transitions), queries O(answer length * sigma) | CSES: Distinct Substrings (2105); CSES: Substring Order I (2108); CSES: Substring Order II (2109); CSES: Repeating Substring (2106); CSES: Substring Distribution (2110) | strings, suffix-automaton |  |
| `Trie` | Prefix tree of words. (Бор (префиксное дерево).) | O(\|word\|) per operation | CSES: Word Combinations (1731) | strings, trie, prefix |  |
| `apostrophe_number` | ICPC-UZ 2024 K: apostrophes in numbers. (Заглушка.) | - | ICPC-UZ 2024 K | strings, formatting | stub |
| `borders` | Lengths of all borders (proper prefixes that are also suffixes). (Границы строки.) | O(n) | CSES: Finding Borders (1732) | strings, borders, prefix-function |  |
| `brands` | Fewest insertions so vowels and consonants alternate. (Бренды.) | O(n) | ICPC-UZ 2023 B | strings, greedy, construction | NV |
| `bwt` | Burrows-Wheeler transform of s + ' ('.   # Преобразование Барроуза-Уилера.) | O(n log^2 n) via sorted rotations of the doubled string | CSES: String Transform (1113) | strings, bwt, burrows-wheeler |  |
| `distinct_subsequences` | Number of distinct non-empty subsequences. (Различные подпоследовательности.) | O(n) | CSES: Distinct Subsequences (1149) | strings, subsequence, dp, counting |  |
| `distinct_substrings_count` | Number of distinct non-empty substrings. (Число различных подстрок.) | O(n log^2 n) | CSES: Distinct Substrings (2105) | strings, suffix-array, counting |  |
| `inverse_bwt` | Recover s from the Burrows-Wheeler transform of s + ' ('.   # Обратное преобразование BWT.) | O(n log n) | CSES: String Transform (1113) | strings, bwt, burrows-wheeler |  |
| `inverse_suffix_array` | Smallest string with the given suffix array. (Строка по суффиксному массиву.) | O(n) |  | strings, suffix-array, construction | NV |
| `kmp_find_all` | All start positions of pat in text (overlaps included). (Поиск подстроки (КМП).) | O(\|text\| + \|pat\|) | CSES: String Matching (1753) | strings, kmp, matching |  |
| `lcp_kasai` | LCP array: lcp[i] = lcp(sa[i-1], sa[i]), lcp[0] = 0. (Массив LCP (Касаи).) | O(n) | CSES: Distinct Substrings (2105) | strings, lcp, kasai |  |
| `longest_palindrome` | Longest palindromic substring (the leftmost one). (Самый длинный палиндром.) | O(n) | CSES: Longest Palindrome (1111) | strings, palindrome, manacher |  |
| `longest_palindrome_ending_at` | Longest palindrome ending at every position. (Длиннейший палиндром с концом в i.) | O(n) | CSES: All Palindromes (3138) | strings, palindrome, manacher, two-pointers |  |
| `lyndon_factorization` | Duval: s = w1 w2 ... wk with Lyndon words w1 >= w2 >= ... >= wk. (Разложение Линдона.) | O(n) |  | strings, lyndon, duval |  |
| `manacher` | Manacher: radii of odd and even palindromes at every center. (Алгоритм Манакера.) | O(n) | CSES: Longest Palindrome (1111) | strings, palindrome, manacher |  |
| `min_rotation` | Start index of the lexicographically smallest rotation. (Минимальный циклический сдвиг.) | O(n) | CSES: Minimal Rotation (1110) | strings, rotation, lexicographic |  |
| `periods` | All periods p (s[i] == s[i + p] for all valid i), 1 <= p <= n. (Периоды строки.) | O(n) | CSES: Finding Periods (1733) | strings, periods, z-function |  |
| `prefix_function` | pi[i] = length of the longest proper border of s[:i+1]. (Префикс-функция.) | O(n) | CSES: Finding Borders (1732) | strings, prefix-function, kmp |  |
| `required_substring` | Number of strings of length n over alphabet containing pattern. (Обязательная подстрока.) | O(n * m * \|alphabet\|) | CSES: Required Substring (1112) | strings, kmp-automaton, dp, counting |  |
| `shortest_non_subsequence` | Shortest string that is NOT a subsequence of s. (Кратчайшая не-подпоследовательность.) | O(n) | CSES: Shortest Subsequence (1087) | strings, subsequence, greedy |  |
| `string_functions` | CSES String Functions - not implemented yet. (Заглушка.) | - | CSES: String Functions | strings, prefix-function, z-function, construction | stub |
| `suffix_array` | Suffix array by prefix doubling with C-level sorts. (Суффиксный массив.) | O(n log^2 n) comparisons inside sorted() (fast in practice) |  | strings, suffix-array, doubling |  |
| `word_combinations` | Ways to write s as a concatenation of dictionary words. (Комбинации слов.) | O(\|s\| * max word length) | CSES: Word Combinations (1731) | strings, trie, dp, counting |  |
| `z_function` | Z-array: z[i] = length of the longest common prefix of s and s[i:]. (Z-функция.) | O(n) | CSES: Finding Periods (1733); CSES: String Matching (1753) | strings, z-function |  |

## roman

| Имя | Что делает | Сложность | Задачи | Теги | Статус |
|---|---|---|---|---|---|
| `from_roman` | Value of a CANONICAL Roman numeral; ValueError for anything else. (Римская запись в число.) | O(len) | ICPC-UZ 2023 C; ICPC-UZ 2024 E; ICPC-UZ 2025 G | roman, conversion, validation |  |
| `is_valid_roman` | Is s a canonical Roman numeral of 1..3999? (Корректна ли римская запись.) | O(len) | ICPC-UZ 2023 C; ICPC-UZ 2024 E; ICPC-UZ 2025 G | roman, validation |  |
| `roman_product_unique` | ICPC-UZ 2024 E: is n uniquely a product of Roman numbers > 1? (Заглушка.) | - | ICPC-UZ 2024 E | roman, factorization | stub |
| `roman_split_min_max` | Fewest and most parts when cutting s into numerals. (Разбиение на римские числа.) | O(n * 15) (a numeral has at most 15 letters: MMMDCCCLXXXVIII) | ICPC-UZ 2025 G | roman, dp, partition | NV |
| `roman_symmetry` | ICPC-UZ 2023 C: symmetry of Roman numerals. (Заглушка.) | - | ICPC-UZ 2023 C | roman, symmetry | stub |
| `scroogius_shortest` | Shortest, then smallest string whose split sums differ by n. (Губернатор Скрудж.) | O(n / 2) output length | ICPC-UZ 2025 G | roman, construction, greedy | NV |
| `to_roman` | Canonical Roman numeral of 1 <= n <= 3999. (Число в римскую запись.) | O(1) | ICPC-UZ 2023 C; ICPC-UZ 2024 E; ICPC-UZ 2025 G | roman, conversion |  |

## bits

| Имя | Что делает | Сложность | Задачи | Теги | Статус |
|---|---|---|---|---|---|
| `XorBasis` | Linear basis over GF(2) (Gaussian elimination on bits). (Линейный базис (xor-базис).) | O(B) per insert / query, B = bits | CSES: Maximum Xor Subset (3191); CSES: Number of Subset Xors (3211) | bits, xor-basis, gf2, linear-algebra |  |
| `XorTrie` | Binary trie over fixed-width numbers: max / min xor with a query. (Xor-бор.) | O(B) per operation, B = bits (default 31) | CSES: Maximum Xor Subarray (1655) | bits, xor, trie |  |
| `all_subarray_xors` | All distinct values of xor over non-empty subarrays. (Все xor подмассивов.) | O(V log V + n), V = next power of two above max value | CSES: All Subarray Xors (3233) | bits, xor, fwht, prefix | NV |
| `and_convolution` | c[k] = sum over i & j = k of a[i] * b[j]. (AND-свёртка.) | O(N log N) |  | bits, fwht, and-convolution |  |
| `and_subset_count` | For every x: non-empty subsets whose AND equals x. (Подмножества с данным AND.) | O(n + B 2^B) | CSES: And Subset Count (3141) | bits, sos-dp, inclusion-exclusion, counting |  |
| `counting_bits_total` | Total number of ones in binary representations of 1..n. (Подсчёт битов.) | O(log n) | CSES: Counting Bits (1146) | bits, counting, digits |  |
| `fwht_and` | In-place transform for AND convolution (superset sums). (Преобразование для AND-свёртки.) | O(N log N) |  | bits, fwht, and-convolution |  |
| `fwht_or` | In-place transform for OR convolution (subset sums). (Преобразование для OR-свёртки.) | O(N log N) |  | bits, fwht, or-convolution |  |
| `fwht_xor` | In-place Walsh-Hadamard transform for XOR convolution. (Преобразование Уолша-Адамара.) | O(N log N), N = len(a) (power of two) | ICPC-UZ 2025 K | bits, fwht, xor-convolution |  |
| `k_subset_xors` | The k smallest xors over all 2^n subsets. (k наименьших xor подмножеств.) | O(n * B + k * B) | CSES: K Subset Xors (3192) | bits, xor-basis, kth | NV |
| `kenobi_skywalker` | Is there a sub-multiset of exactly c elements with xor x? (Кеноби и Скайуокер.) | O(D^2 * M + q log D), D = distinct values, M = 2^bits of max(a) | ICPC-UZ 2025 K | bits, xor, dp, subsets | NV |
| `max_xor_subarray` | Maximum xor of a non-empty subarray. (Максимальный xor подмассива.) | O(n * B) | CSES: Maximum Xor Subarray (1655) | bits, xor, trie, prefix |  |
| `max_xor_subset` | Maximum xor of a subset (empty subset gives 0). (Максимальный xor подмножества.) | O(n * B) | CSES: Maximum Xor Subset (3191) | bits, xor-basis |  |
| `min_hamming_distance` | Minimum Hamming distance between two bit strings (as ints). (Расстояние Хэмминга.) | O(n^2) popcounts | CSES: Hamming Distance (2136) | bits, hamming, popcount |  |
| `number_of_subset_xors` | How many DISTINCT subset xors exist (0 included). (Число различных xor подмножеств.) | O(n * B) | CSES: Number of Subset Xors (3211) | bits, xor-basis, counting |  |
| `or_convolution` | c[k] = sum over i \| j = k of a[i] * b[j]. (OR-свёртка.) | O(N log N) |  | bits, fwht, or-convolution |  |
| `popcount` | Number of set bits of x >= 0 (works on Python 3.9). (Число единичных битов.) | O(bits) in C |  | bits, popcount |  |
| `sos_bit_problem` | For each x: (y with x\|y == x, #y with x&y == x, #y with x&y != 0.   # Задача SOS Bit Problem.) | O(n + B 2^B), B = bit length of max(a) | CSES: SOS Bit Problem (1654) | bits, sos-dp |  |
| `sos_subset_sum` | g[mask] = sum of f over all submasks of mask (zeta transform). (SOS DP по подмножествам.) | O(bits * 2^bits) | CSES: SOS Bit Problem (1654) | bits, sos-dp, subsets |  |
| `sos_superset_sum` | g[mask] = sum of f[sup] over all supermasks sup of mask. (SOS DP по надмножествам.) | O(bits * 2^bits) | CSES: SOS Bit Problem (1654) | bits, sos-dp, supersets |  |
| `xor_convolution` | c[k] = sum over i ^ j = k of a[i] * b[j] (lengths padded to a power of two). (Xor-свёртка.) | O(N log N) |  | bits, fwht, xor-convolution |  |
| `xor_pyramid_peak` | Top of the xor pyramid built from the bottom row a. (Вершина xor-пирамиды.) | O(n) | CSES: Xor Pyramid Peak (3194) | bits, lucas, parity, pyramid |  |

## geometry

| Имя | Что делает | Сложность | Задачи | Теги | Статус |
|---|---|---|---|---|---|
| `LiChaoMax` | Li Chao tree for MAXIMUM of lines at integer x (self-contained copy). (Ли Чао на максимум.) | O(log C) per operation | CSES: Lines and Queries I (3204) | geometry, li-chao, lines, max |  |
| `Point` | 2D integer point / vector with the usual operations. (Точка / вектор.) | O(1) per operation |  | geometry, point, vector |  |
| `all_manhattan_distances_sum` | Sum of Manhattan distances over all unordered pairs. (Сумма всех манхэттенских расстояний.) | O(n log n) | CSES: All Manhattan Distances (3411) | geometry, manhattan, prefix-sums |  |
| `area_of_rectangles` | Area of the union of axis-parallel rectangles. (Площадь объединения прямоугольников.) | O(n log n) | CSES: Area of Rectangles (1741) | geometry, sweep-line, segment-tree, union-area |  |
| `biathlon_route` | Shortest closed route through all points (base version). (Маршрут биатлониста.) | O(2^n * n^2) | ICPC-UZ 2023 K | geometry, tsp, bitmask-dp | NV |
| `closest_pair` | Squared distance of the closest pair (bottom-up divide & conquer). (Ближайшая пара точек.) | O(n log n) | CSES: Minimum Euclidean Distance (2194) | geometry, closest-pair, divide-and-conquer |  |
| `closest_pair_sweep` | Closest pair by a sweep over x with a y-ordered window. (Ближайшая пара (сканирование).) | O(n log n) comparisons (+ list insertions, C-fast memmove) | CSES: Minimum Euclidean Distance (2194) | geometry, closest-pair, sweep-line |  |
| `convex_hull` | Convex hull by Andrew's monotone chain, counter-clockwise. (Выпуклая оболочка.) | O(n log n) | CSES: Convex Hull (2195) | geometry, convex-hull, andrew |  |
| `coplanar_with_origin` | Do all points lie in one plane through the origin? (Плоскость через начало координат.) | O(n) after finding two independent vectors | ICPC-UZ 2025 D | geometry, 3d, coplanar, rank |  |
| `cross` | Cross product (a - o) x (b - o). (Векторное произведение.) | O(1) | CSES: Point Location Test (2189) | geometry, cross-product |  |
| `death_star_min_changes` | Fewest coordinates to raise by [0, 1) so that O, A, B, C are coplanar. (Звезда смерти.) | O(2^9) determinants | ICPC-UZ 2025 D | geometry, 3d, determinant, bitmask | NV |
| `det3` | Determinant of the 3 x 3 matrix with rows a, b, c (triple product). (Определитель 3 x 3.) | O(1) | ICPC-UZ 2025 D | geometry, 3d, determinant |  |
| `dot` | Dot product (a - o) . (b - o). (Скалярное произведение.) | O(1) |  | geometry, dot-product |  |
| `intersection_points_count` | Intersections of horizontal and vertical segments. (Точки пересечения.) | O(n log n) | CSES: Intersection Points (1740) | geometry, sweep-line, fenwick |  |
| `line_segments_trace` | CSES Line Segments Trace - not implemented yet. (Заглушка.) | - | CSES: Line Segments Trace I | geometry, li-chao, segments | stub |
| `max_manhattan_distances` | Max Manhattan distance after adding each point. (Максимальное манхэттенское расстояние.) | O(n) | CSES: Maximum Manhattan Distances (3410) | geometry, manhattan, rotation |  |
| `on_segment` | Does p lie on the closed segment [a, b]? (Точка на отрезке.) | O(1) | CSES: Line Segment Intersection (2190) | geometry, segment |  |
| `orientation` | Sign of the turn a -> b -> c: 1 left, -1 right, 0 collinear. (Ориентация тройки точек.) | O(1) | CSES: Point Location Test (2189) | geometry, orientation |  |
| `point_in_polygon` | Point inside / outside / on the boundary of a simple polygon. (Точка в многоугольнике.) | O(n) | CSES: Point in Polygon (2192) | geometry, polygon, point-in-polygon |  |
| `point_location` | Where is p3 relative to the directed line p1 -> p2. (Положение точки относительно прямой.) | O(1) | CSES: Point Location Test (2189) | geometry, orientation |  |
| `polygon_area2` | Twice the signed area of a polygon (shoelace formula). (Удвоенная площадь многоугольника.) | O(n) | CSES: Polygon Area (2191) | geometry, polygon, area, shoelace |  |
| `polygon_lattice_points` | Lattice points inside and on the boundary (Pick). (Целые точки многоугольника.) | O(n log C) | CSES: Polygon Lattice Points (2193) | geometry, polygon, pick |  |
| `robot_path` | Steps until the robot first visits a point twice. (Путь робота.) | O(n^2) | CSES: Robot Path (1742) | geometry, simulation, segments | NV |
| `segment_intersection_point` | The unique common point of two segments (exact fractions). (Точка пересечения отрезков.) | O(1) |  | geometry, segment, intersection |  |
| `segments_intersect` | Do closed segments [p1, p2] and [p3, p4] share at least one point? (Пересечение отрезков.) | O(1) | CSES: Line Segment Intersection (2190) | geometry, segment, intersection |  |
| `tetra_volume6` | Six times the signed volume of tetrahedron abcd. (Удвоенный (x6) объём тетраэдра.) | O(1) |  | geometry, 3d, volume |  |

## game

| Имя | Что делает | Сложность | Задачи | Теги | Статус |
|---|---|---|---|---|---|
| `another_game_first_wins` | Each move removes one coin from every heap of a chosen non-empty subset. (Ещё одна игра.) | O(n) | CSES: Another Game (2208) | games, parity |  |
| `grundy_dag` | Sprague-Grundy values of every vertex of a game DAG (moves = edges). (Гранди на DAG.) | O(n + m) |  | games, grundy, dag |  |
| `grundy_game_first_wins` | Grundy's game: split a heap into two non-empty UNEQUAL heaps. (Игра Гранди.) | O(min(n, 1300)^2) | CSES: Grundy's Game (2207) | games, grundy, split |  |
| `grundy_subtraction` | Grundy values of a subtraction game (remove one of the allowed amounts). (Игра вычитания.) | O(n_max * \|moves\|) | CSES: Stick Game (1729) | games, grundy, subtraction |  |
| `mex` | Minimum excluded non-negative integer. (Mex множества.) | O(k) |  | games, mex, grundy |  |
| `misere_nim_first_wins` | Misere Nim: whoever takes the last stick LOSES. (Ним в поддавки.) | O(n) |  | games, nim, misere |  |
| `nim_first_wins` | Classic Nim: take any positive number from one pile. (Ним.) | O(n) | CSES: Nim Game I (1730) | games, nim |  |
| `nim_k_first_wins` | Nim where a move takes 1..k sticks from one pile. (Ним с ограничением хода.) | O(n) | CSES: Nim Game II (1098) | games, nim, subtraction |  |
| `stair_game_first_wins` | Staircase Nim: move balls from stair k to k - 1 (stair 1 is final). (Ним на лестнице.) | O(n) | CSES: Stair Game (1099) | games, nim, staircase |  |

## introductory

| Имя | Что делает | Сложность | Задачи | Теги | Статус |
|---|---|---|---|---|---|
| `apple_division` | Minimal difference of sums when splitting into two groups. (Деление яблок.) | O(2^n) | CSES: Apple Division (1623) | introductory, subsets, brute-force |  |
| `beautiful_permutation` | Permutation of 1..n with no adjacent values differing by 1. (Красивая перестановка.) | O(n) | CSES: Permutations (1070) | introductory, construction, permutation |  |
| `chess_tournament` | Simple graph with the given degree sequence (Havel-Hakimi). (Шахматный турнир.) | O(m log n) | CSES: Chess Tournament (1697) | construction, graph, degree-sequence, havel-hakimi |  |
| `coin_piles` | Can both piles be emptied removing (1, 2) or (2, 1) coins each move? (Кучи монет.) | O(1) | CSES: Coin Piles (1754) | introductory, math |  |
| `de_bruijn` | Shortest string containing every length-n word. (Последовательность де Брёйна.) | O(k^n) | CSES: De Bruijn Sequence (1692) | construction, de-bruijn, lyndon |  |
| `digit_queries` | k-th digit (1-based) of 123456789101112... (Цифра на позиции k.) | O(log k) | CSES: Digit Queries (2431) | introductory, digits |  |
| `filling_trominos` | CSES Filling Trominos - not implemented yet. (Заглушка.) | - | CSES: Filling Trominos (2423) | construction, tilings, trominoes | stub |
| `gray_code` | All n-bit strings where neighbours differ in exactly one bit. (Код Грея.) | O(2^n * n) | CSES: Gray Code (2205) | introductory, gray-code, bits |  |
| `grid_path_description` | Hamiltonian grid paths matching a pattern. (Описание пути по сетке.) | exponential with strong pruning (dead ends, splitting walls) | CSES: Grid Path Description (1625) | introductory, backtracking, grid |  |
| `hanoi_moves` | Optimal Tower of Hanoi moves from stack 1 to stack 3 (iterative). (Ханойская башня.) | O(2^n) | CSES: Tower of Hanoi (2165) | introductory, hanoi, iterative |  |
| `inverse_inversions` | Permutation of 1..n with exactly k inversions. (Перестановка с k инверсиями.) | O(n) | CSES: Inverse Inversions (2214) | construction, inversions, permutation |  |
| `knight_moves_grid` | Minimal knight moves from the top-left corner to every cell of n x n. (Ходы коня по сетке.) | O(n^2) | CSES: Knight Moves Grid (3217) | introductory, bfs, knight |  |
| `mex_grid_construction` | n x n grid where each cell is the mex of the values above and to the left. (Сетка mex.) | O(n^2) | CSES: Mex Grid Construction (3419) | introductory, construction, mex, xor |  |
| `monotone_subsequences` | Permutation whose longest monotone subsequence is k. (Монотонные подпоследовательности.) | O(n) | CSES: Monotone Subsequences (2215) | construction, monotone, erdos-szekeres | NV |
| `n_queens` | Number of ways to place n non-attacking queens (iterative backtracking). (Ферзи.) | O(n!) worst case, bitmasks make it fast | CSES: Chessboard and Queens (1624) | introductory, backtracking, queens |  |
| `next_permutation` | Transform a into the next lexicographic permutation in place. (Следующая перестановка.) | O(n) | CSES: Creating Strings (1622) | introductory, permutations |  |
| `number_spiral` | Value at row y, column x (1-based) of the CSES number spiral. (Числовая спираль.) | O(1) | CSES: Number Spiral (1071) | introductory, formula |  |
| `palindrome_reorder` | Rearrange letters into the smallest palindrome. (Перестановка в палиндром.) | O(n + sigma log sigma) | CSES: Palindrome Reorder (1755) | introductory, strings, palindrome |  |
| `prufer_decode` | Tree edges from a Prufer code (vertices 0..len(code)+1). (Код Прюфера (декодирование).) | O(n log n) | CSES: Prufer Code (1134) | construction, prufer, tree |  |
| `prufer_encode` | Prufer code of a labelled tree on 0..n-1. (Код Прюфера (кодирование).) | O(n log n) with a heap of leaves | CSES: Prufer Code (1134) | construction, prufer, tree |  |
| `string_permutations` | All distinct permutations of s in lexicographic order. (Все перестановки строки.) | O(n * number of permutations) | CSES: Creating Strings (1622) | introductory, permutations, strings |  |
| `string_reorder` | Smallest rearrangement without equal adjacent letters. (Перестановка строки.) | O(n * sigma) | CSES: String Reorder (1743) | introductory, strings, greedy |  |
| `submasks` | All submasks of mask in decreasing order (including mask and 0). (Перебор подмасок.) | O(2^popcount(mask)) |  | introductory, bitmask, subsets |  |
| `subsets` | All subsets of {0, ..., n-1} as lists, by increasing bitmask. (Перебор подмножеств.) | O(2^n * n) |  | introductory, bitmask, subsets |  |
| `trailing_zeros` | Number of trailing zeros of n! (Legendre for p = 5). (Нули в конце факториала.) | O(log n) | CSES: Trailing Zeros (1618) | introductory, math |  |
| `two_knights` | Ways to place two non-attacking knights on k x k boards, k = 1..n. (Два коня.) | O(n) | CSES: Two Knights (1072) | introductory, combinatorics, chess |  |
| `two_sets` | Split 1..n into two sets with equal sums. (Два множества.) | O(n) | CSES: Two Sets (1092) | introductory, construction, partition |  |
| `weird_algorithm` | Collatz sequence from n down to 1. (Странный алгоритм (Коллатц).) | O(length) | CSES: Weird Algorithm (1068) | introductory, simulation |  |

## sorting

| Имя | Что делает | Сложность | Задачи | Теги | Статус |
|---|---|---|---|---|---|
| `apartments` | Max applicants matched to apartments with \|size - want\| <= k. (Квартиры.) | O(n log n + m log m) | CSES: Apartments (1084) | two-pointers, greedy, matching |  |
| `array_division` | Split into k contiguous parts minimising the maximum part sum. (Деление массива.) | O(n log S) | CSES: Array Division (1085) | binary-search, answer, greedy |  |
| `bisect_answer` | Smallest x in [lo, hi] with ok(x) True (ok monotone). (Бинпоиск по ответу.) | O(log(hi - lo)) calls of ok | CSES: Factory Machines (1620); CSES: Array Division (1085) | binary-search, answer |  |
| `bisect_answer_max` | Largest x in [lo, hi] with ok(x) True (ok monotone). (Бинпоиск: максимум.) | O(log(hi - lo)) calls of ok |  | binary-search, answer |  |
| `bisect_real` | Boundary of a monotone predicate on reals. (Бинпоиск по вещественным числам.) | O(iters) calls of ok |  | binary-search, real |  |
| `collecting_numbers` | Rounds needed to collect 1, 2, ..., n scanning left to right repeatedly. (Сбор чисел.) | O(n) | CSES: Collecting Numbers (2216) | permutation, counting |  |
| `concert_tickets` | Each customer buys the most expensive ticket not above their limit. (Билеты на концерт.) | O((n + m) log n) | CSES: Concert Tickets (1091) | dsu, greedy, binary-search |  |
| `factory_machines` | Minimal time for machines with periods t to produce k products. (Фабрика.) | O(n log(k * min t)) | CSES: Factory Machines (1620) | binary-search, answer |  |
| `ferris_wheel` | Min gondolas, each holds <= 2 children with total weight <= x. (Колесо обозрения.) | O(n log n) | CSES: Ferris Wheel (1090) | two-pointers, greedy, sorting |  |
| `josephus_order` | Removal order when every k-th child is removed. (Порядок удаления (Иосиф).) | O(n log n) | CSES: Josephus Problem II (2163) | josephus, fenwick, kth |  |
| `josephus_queries` | The k-th removed child when every second child is removed (n up to 10^9). (Запросы Иосифа.) | O(log n) | CSES: Josephus Queries (2164) | josephus, recursion-free |  |
| `josephus_survivor` | Last remaining child when every k-th is removed (children 1..n). (Задача Иосифа: выживший.) | O(n) | CSES: Josephus Problem I (2162) | josephus, formula |  |
| `max_subarray_sum` | Maximum sum of a non-empty subarray (Kadane). (Максимальная сумма подмассива.) | O(n) | CSES: Maximum Subarray Sum (1643) | kadane, subarray |  |
| `max_subarray_sum_range` | Maximum sum of a subarray with length in [lo, hi]. (Макс. сумма подмассива длины lo..hi.) | O(n) | CSES: Maximum Subarray Sum II (1644) | monotonic-deque, prefix-sums, subarray |  |
| `meet_in_middle_count` | Number of subsets with sum exactly x, n <= 40. (Встреча посередине.) | O(2^(n/2)) | CSES: Meet in the Middle (1628) | meet-in-the-middle, subset-sum |  |
| `missing_coin_sum` | Smallest sum not formed by a subset of coins. (Наименьшая непредставимая сумма.) | O(n log n) | CSES: Missing Coin Sum (2183) | greedy, sorting |  |
| `movie_festival` | Max number of non-overlapping movies [a, b) (greedy by end). (Кинофестиваль.) | O(n log n) | CSES: Movie Festival (1629) | greedy, intervals, scheduling |  |
| `movie_festival_k` | Max movies watched in total by k club members. (Кинофестиваль II.) | O(n log n) (+ list insertions) | CSES: Movie Festival II (1632) | greedy, intervals, scheduling, multiset |  |
| `nearest_smaller_values` | Index of the nearest strictly smaller element to the left. (Ближайшие меньшие.) | O(n) | CSES: Nearest Smaller Values (1645) | monotonic-stack, nearest-smaller |  |
| `nested_ranges` | For each range: contains another / is contained in another. (Вложенные отрезки.) | O(n log n) | CSES: Nested Ranges Check (2168) | sorting, nested-ranges, fenwick |  |
| `nested_ranges_count` | For each range: how many it contains / how many contain it. (Подсчёт вложенных отрезков.) | O(n log n) | CSES: Nested Ranges Count (2169) | sorting, nested-ranges, fenwick |  |
| `playlist` | Longest contiguous segment with distinct values. (Плейлист.) | O(n) | CSES: Playlist (1141) | two-pointers, distinct, window |  |
| `reading_books` | Minimal time for two readers to read every book. (Чтение книг.) | O(n) | CSES: Reading Books (1631) | greedy, math |  |
| `restaurant_customers` | Maximum number of simultaneous visitors (arrive a, leave b). (Посетители ресторана.) | O(n log n) | CSES: Restaurant Customers (1619) | sweep-line, events |  |
| `room_allocation` | Minimal number of rooms; a room is reused only after its last day. (Распределение комнат.) | O(n log n) | CSES: Room Allocation (1164) | greedy, heap, intervals |  |
| `sliding_window_cost` | Min cost to make each window equal: sum \|x - median\|. (Стоимость окна.) | O(n log n) | CSES: Sliding Window Cost (1077) | sliding-window, median, heap |  |
| `sliding_window_median` | Median of every window of length k (lower median for even k). (Медиана в окне.) | O(n log n) | CSES: Sliding Window Median (1076) | sliding-window, median, heap |  |
| `stick_lengths` | Min total cost to make all sticks equal (cost = \|change\|). (Длины палочек.) | O(n log n) | CSES: Stick Lengths (1074) | median, greedy |  |
| `subarray_distinct_values` | Number of subarrays with at most k distinct values. (Подмассивы с <= k различными.) | O(n) | CSES: Subarray Distinct Values (2428) | two-pointers, distinct, subarray |  |
| `subarray_divisibility` | Number of subarrays whose sum is divisible by n = len(a). (Делимость подмассивов.) | O(n) | CSES: Subarray Divisibility (1662) | prefix-sums, modular, subarray |  |
| `subarray_sums_count` | Number of subarrays with sum exactly x (any signs). (Подмассивы с суммой x.) | O(n) | CSES: Subarray Sums II (1661) | prefix-sums, hashing, subarray |  |
| `sum_of_four_values` | Four distinct indices with sum x (pair sums in a hash map). (Сумма четырёх чисел.) | O(n^2) expected | CSES: Sum of Four Values (1642) | hashing, meet-in-the-middle, four-sum |  |
| `sum_of_three_values` | Three distinct indices with a[i] + a[j] + a[k] = x. (Сумма трёх чисел.) | O(n^2) | CSES: Sum of Three Values (1641) | two-pointers, three-sum |  |
| `sum_of_two_values` | Two distinct indices with a[i] + a[j] = x. (Сумма двух чисел.) | O(n) | CSES: Sum of Two Values (1640) | hashing, two-sum |  |
| `tasks_and_deadlines` | Max total reward sum(d - finish) doing all tasks (duration, deadline). (Задачи и дедлайны.) | O(n log n) | CSES: Tasks and Deadlines (1630) | greedy, scheduling |  |
| `towers` | Min number of towers (each strictly smaller cube on top) placing cubes in order. (Башни.) | O(n log n) | CSES: Towers (1073) | greedy, binary-search, patience |  |
| `traffic_lights` | Longest light-free passage on [0, x] after each traffic light is added. (Светофоры.) | O(n log n) | CSES: Traffic Lights (1163) | offline, linked-list, gaps |  |

## counting

| Имя | Что делает | Сложность | Задачи | Теги | Статус |
|---|---|---|---|---|---|
| `binary_subsequences` | Shortest bit string with exactly n distinct subsequences. (Двоичные подпоследовательности.) | O(n log n) | CSES: Binary Subsequences | strings, subsequences, euclid | NV |
| `bubble_sort_rounds` | Number of bubble sort passes that perform at least one swap. (Раунды пузырька.) | O(n log n) | CSES: Bubble Sort Rounds | sorting, simulation, bubble-sort |  |
| `coding_company` | Ways to split people into teams with total (max - min) penalty <= x. (Компания.) | O(n^2 * x) | CSES: Coding Company | dp, open-groups, counting |  |
| `coin_arrangement` | Fewest unit moves to leave one coin per cell of a 2 x n grid. (Расстановка монет.) | O(n) | CSES: Coin Arrangement | greedy, balance, grid |  |
| `coin_grid` | Fewest row / column clears that collect every coin 'o'. (Монеты на сетке.) | O(n * E) (Kuhn with BFS augmenting paths) | CSES: Coin Grid | bipartite, matching, konig, vertex-cover |  |
| `counting_bishops` | Ways to place k non-attacking bishops on an n x n board. (Расстановки слонов.) | O(n^2) | CSES: Counting Bishops | combinatorics, dp, chess |  |
| `counting_permutations` | Permutations of 1..n with no two neighbours differing by 1. (Перестановки без \|d\| = 1.) | O(n) | CSES: Counting Permutations | combinatorics, recurrence, permutations |  |
| `counting_reorders` | Reorders of s with no two equal adjacent letters. (Перестановки без соседних равных.) | O(n^2) | CSES: Counting Reorders | combinatorics, inclusion-exclusion, strings |  |
| `counting_sequences` | Sequences of length n over 1..k that use every value. (Сюръекции.) | O(k log n) | CSES: Counting Sequences | combinatorics, inclusion-exclusion, surjections |  |
| `cyclic_array` | Fewest parts of a circular array with every part sum <= k. (Циклический массив.) | O(n log n) | CSES: Cyclic Array | binary-lifting, greedy, circular |  |
| `empty_string` | Number of ways to erase s by removing equal adjacent pairs. (Пустая строка.) | O(n^3) | CSES: Empty String | dp, intervals, strings |  |
| `filled_subgrid_count` | Count one-letter subgrids for each of the first k letters. (Одноцветные подсетки.) | O(n * m) | CSES: Filled Subgrid Count | grid, histogram, stack, counting | NV |
| `functional_graph_distribution` | Functional graphs on n vertices with exactly k components. (Функциональные графы.) | O(n^2) | CSES: Functional Graph Distribution | combinatorics, functional-graph, stirling | NV |
| `grid_completion` | Fill the grid so that each row and column has exactly one A and one B. (Дополнение сетки.) | O(n^2) | CSES: Grid Completion | combinatorics, inclusion-exclusion, grid | NV |
| `grid_puzzle_i` | Grid with a_i marked cells in row i and b_j in column j. (Головоломка I.) | O(n * m log m) | CSES: Grid Puzzle I | construction, gale-ryser, greedy |  |
| `grid_puzzle_ii` | Row / column sums as in Grid Puzzle I, maximise the chosen sum. (Головоломка II.) | O(F * V * E), F = sum(a) augmentations of Bellman-Ford (SPFA) | CSES: Grid Puzzle II | min-cost-flow, assignment, grid | NV |
| `maximum_building` | Largest rectangle of free '.' cells. (Максимальное здание I.) | O(n * m) | CSES: Maximum Building I | grid, histogram, stack |  |
| `maximum_building_counts` | For every size h x w, the number of free rectangles of that size. (Здание II.) | O(n * m) | CSES: Maximum Building II | grid, histogram, stack, counting |  |
| `permutation_inversions` | Permutations of n elements with exactly k inversions. (Перестановки с k инверсиями.) | O(n * k) | CSES: Permutation Inversions | dp, prefix-sums, permutations |  |
| `programmers_and_artists` | Pick a programmers and b artists (disjoint), maximise skill. (Программисты и художники.) | O(n log n) | CSES: Programmers and Artists | greedy, heap, exchange-argument |  |
| `raab_game_construct` | Card orders where player 1 wins a rounds and player 2 wins b. (Игра Рааба I.) | O(n) | CSES: Raab Game I | construction, permutations, games |  |
| `raab_game_count` | Number of games where player 1 wins a rounds and player 2 wins b. (Игра Рааба II.) | O(n^2) | CSES: Raab Game II | combinatorics, dp, derangements | NV |
| `school_excursion` | Which group sizes k = 1..n can be formed from whole friend components. (Экскурсия.) | O(n sqrt n / 64) word operations | CSES: School Excursion | dsu, subset-sum, bitset |  |
| `sorting_methods` | Minimal operations to sort p by four kinds of moves. (Способы сортировки.) | O(n log n) | CSES: Sorting Methods | permutations, inversions, lis, cycles |  |
| `stick_divisions` | Minimal cost to cut a stick of length x into the given pieces. (Деление палки.) | O(n log n) | CSES: Stick Divisions | greedy, heap, huffman |  |
| `swap_round_sorting` | Sort with the fewest rounds of disjoint swaps. (Сортировка раундами обменов.) | O(n) | CSES: Swap Round Sorting | permutations, cycles, construction |  |
| `tournament_graph_distribution` | Tournaments on n labelled vertices with exactly k SCCs. (Турниры по числу КСС.) | O(n^3) | CSES: Tournament Graph Distribution | combinatorics, tournaments, scc | NV |
| `two_stacks_sorting` | Assign each element to stack 1 or 2 so that the output is sorted. (Две стопки.) | O(n^2) | CSES: Two Stacks Sorting | stacks, bipartite, permutations |  |

## misc

| Имя | Что делает | Сложность | Задачи | Теги | Статус |
|---|---|---|---|---|---|
| `a_plus_branding` | ICPC-UZ 2024 A "A+Branding": fewest shared tasks. (Заглушка.) | - | ICPC-UZ 2024 A | greedy | stub |
| `a_problems_balloons` | Teams that get a balloon: n teams, k balloons. (Задачи и шарики.) | O(1) | ICPC-UZ 2025 A | math, easy | NV |
| `attacks_number` | Fewest attacks worth 2 or 3 points that sum to exactly n. (Число атак.) | O(1) | ICPC-UZ 2023 A | greedy, math | NV |
| `big_deadline` | ICPC-UZ 2024 B "Big Deadline": count orders of two workers. (Заглушка.) | - | ICPC-UZ 2024 B | combinatorics, counting | stub |
| `certainly_best` | ICPC-UZ 2024 C "Certainly Best": distinct subsets, minimal total size. (Заглушка.) | - | ICPC-UZ 2024 C | combinatorics, subsets, greedy | stub |
| `great_sign` | ICPC-UZ 2024 G "Great Sign": number using all b digits once. (Заглушка.) | - | ICPC-UZ 2024 G | math, bases, construction | stub |
| `hidden_pieces` | ICPC-UZ 2024 H "Hidden Pieces": fog-of-war chess visibility. (Заглушка.) | - | ICPC-UZ 2024 H | simulation, chess | stub |
| `laura_and_arrays` | ICPC-UZ 2024 L "Laura and Arrays": maximal dot product. (Заглушка.) | - | ICPC-UZ 2024 L | greedy, randomized, dot-product | stub |
| `limit_the_arrow` | For each prefix, fewest targets whose thickness sum reaches p. (Ограничь стрелу.) | O(n log n) | ICPC-UZ 2025 L | greedy, heap, prefix | NV |
| `minimum_number_of_tasks` | Fewest problems in a contest given the letters that were submitted. (Число задач.) | O(len) | ICPC-UZ 2025 M | strings, easy | NV |
