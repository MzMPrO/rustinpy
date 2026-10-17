"""CSES Counting Problems and Advanced Techniques: combinatorial counting (bishops, reorders,
derangements, tournaments, functional graphs), histogram counting on grids, greedy orders,
Huffman, Koenig and flows on grids.

Задачи на подсчёт и конструктивы CSES. Всё итеративно, ответы по модулю MOD7.
"""

from __future__ import annotations

import heapq
from collections import deque
from math import gcd

from rustinpy._registry import algo

MOD7 = 10**9 + 7
INF = 1 << 60


@algo(
    tags=["grid", "histogram", "stack", "counting"], cses=["Filled Subgrid Count"], verified=False
)
def filled_subgrid_count(grid: list[str], k: int, squares: bool = False) -> list[int]:
    """Count one-letter subgrids for each of the first k letters.   # Одноцветные подсетки.

    When to use:  grid of letters 'A'..; rectangles (default) or only squares.
    Complexity:   O(n * m)
    Input:        grid - list of equal-length strings over the first k capital letters.
    Returns:      res[c] = number of subgrids made only of letter chr(65 + c).
    Pitfalls:     answers reach ~n^2 m^2 / 4 - fine for Python ints.
    Idea:         rectangles: column heights h of equal letters, monotonic stack per row:
                  cnt[j] = cnt[p] + h[j] * (j - p), p = last column with smaller height (the
                  stack restarts where the letter changes). Squares: classic dp
                  1 + min(up, left, up-left) when all four cells have the same letter.
                  NOT VERIFIED: which CSES version (I = squares or rectangles) is meant.
    CSES:         Filled Subgrid Count I / II (version NOT VERIFIED).
    Example:
        >>> filled_subgrid_count(["AAB", "AAB"], 2)
        [9, 3]
        >>> filled_subgrid_count(["AAB", "AAB"], 2, squares=True)
        [5, 2]
    """
    # NOT VERIFIED: какая версия задачи CSES (квадраты или прямоугольники) не сверено
    n = len(grid)
    m = len(grid[0]) if n else 0
    res = [0] * k
    if squares:
        prev = [0] * m
        for i in range(n):
            row = grid[i]
            cur = [1] * m
            for j in range(m):
                c = row[j]
                if i and j and grid[i - 1][j] == c and row[j - 1] == c and grid[i - 1][j - 1] == c:
                    cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])  # квадрат с углом (i, j)
                res[ord(c) - 65] += cur[j]
            prev = cur
        return res
    h = [0] * m
    for i in range(n):
        row = grid[i]
        for j in range(m):
            h[j] = h[j] + 1 if i and grid[i - 1][j] == row[j] else 1  # высота столбца одной буквы
        cnt = [0] * m
        st: list[int] = []
        start = 0
        for j in range(m):
            if j and row[j] != row[j - 1]:
                st = []  # буква сменилась: новый отрезок
                start = j
            while st and h[st[-1]] >= h[j]:
                st.pop()
            if st:
                p = st[-1]
                cnt[j] = cnt[p] + h[j] * (j - p)
            else:
                cnt[j] = h[j] * (j - start + 1)
            st.append(j)
            res[ord(row[j]) - 65] += cnt[j]  # прямоугольники с правым нижним углом (i, j)
    return res


@algo(tags=["combinatorics", "dp", "chess"], cses=["Counting Bishops"], requires=["MOD7"])
def counting_bishops(n: int, k: int, mod: int = MOD7) -> int:
    """Ways to place k non-attacking bishops on an n x n board.   # Расстановки слонов.

    When to use:  split by colour; inside one colour sort diagonals by length.
    Complexity:   O(n^2)
    Returns:      the number of placements mod mod.
    Idea:         cells of one colour lie on diagonals i + j = s of one parity. Sorted by
                  length, each perpendicular diagonal of a shorter one is also met by a longer
                  one, so dp[j] += dp[j - 1] * (len - (j - 1)). Combine the two colours by
                  convolution of their dp arrays.
    CSES:         Counting Bishops.
    Example:
        >>> counting_bishops(3, 2), counting_bishops(4, 4), counting_bishops(2, 3)
        (26, 260, 0)
    """
    if k > 2 * n:
        return 0
    color = []
    for par in range(2):
        lens = sorted(min(s, 2 * n - 2 - s) + 1 for s in range(par, 2 * n - 1, 2))
        dp = [1] + [0] * len(lens)
        for i, ln in enumerate(lens):
            for j in range(i + 1, 0, -1):  # j-й слон на очередной диагонали
                if ln - j + 1 > 0:
                    dp[j] = (dp[j] + dp[j - 1] * (ln - j + 1)) % mod
        color.append(dp)
    a, b = color
    return sum(a[j] * b[k - j] for j in range(len(a)) if 0 <= k - j < len(b)) % mod


@algo(
    tags=["combinatorics", "recurrence", "permutations"],
    cses=["Counting Permutations"],
    requires=["MOD7"],
)
def counting_permutations(n: int, mod: int = MOD7) -> int:
    """Permutations of 1..n with no two neighbours differing by 1.   # Перестановки без |d| = 1.

    When to use:  OEIS A002464 (Hertzsprung's problem), linear recurrence.
    Complexity:   O(n)
    Returns:      the count mod mod.
    Idea:         a(n) = (n+1) a(n-1) - (n-2) a(n-2) - (n-5) a(n-3) + (n-3) a(n-4),
                  a(0..3) = 1, 1, 0, 0 (checked against brute force for n <= 9).
    CSES:         Counting Permutations.
    Example:
        >>> [counting_permutations(n) for n in range(7)]
        [1, 1, 0, 0, 2, 14, 90]
    """
    a = [1, 1, 0, 0]
    if n < 4:
        return a[n] % mod
    for i in range(4, n + 1):
        v = (i + 1) * a[-1] - (i - 2) * a[-2] - (i - 5) * a[-3] + (i - 3) * a[-4]
        a = [a[1], a[2], a[3], v % mod]  # храним только четыре последних
    return a[-1]


@algo(
    tags=["dp", "prefix-sums", "permutations"], cses=["Permutation Inversions"], requires=["MOD7"]
)
def permutation_inversions(n: int, k: int, mod: int = MOD7) -> int:
    """Permutations of n elements with exactly k inversions.   # Перестановки с k инверсиями.

    When to use:  insert the i-th element: it adds 0..i-1 inversions.
    Complexity:   O(n * k)
    Returns:      the count mod mod.
    Idea:         dp_i[j] = sum dp_{i-1}[j - t], t = 0..i-1 - a sliding window of prefix sums.
    CSES:         Permutation Inversions.
    Example:
        >>> permutation_inversions(4, 3), permutation_inversions(3, 0), permutation_inversions(3, 4)
        (6, 1, 0)
    """
    dp = [1] + [0] * k
    for i in range(1, n + 1):
        pre = [0] * (k + 2)
        for j in range(k + 1):
            pre[j + 1] = (pre[j] + dp[j]) % mod
        dp = [(pre[j + 1] - pre[max(0, j - i + 1)]) % mod for j in range(k + 1)]  # окно длины i
    return dp[k]


@algo(
    tags=["combinatorics", "inclusion-exclusion", "strings"],
    cses=["Counting Reorders"],
    requires=["MOD7"],
)
def counting_reorders(s: str, mod: int = MOD7) -> int:
    """Reorders of s with no two equal adjacent letters.   # Перестановки без соседних равных.

    When to use:  multiset arrangements with "no equal neighbours", n up to ~5000.
    Complexity:   O(n^2)
    Returns:      the count mod mod (mod must be prime).
    Idea:         inclusion-exclusion: glue a letter with count c into j blocks (C(c-1, j-1)
                  ways, sign (-1)^(c-j)); blocks of all letters are then arranged in
                  T! / prod(j_i!) ways. Multiply the polynomials sum_j coef * x^j / j! of all
                  letters and take sum coef[T] * T!.
    CSES:         Counting Reorders.
    Example:
        >>> counting_reorders("aab"), counting_reorders("aabb"), counting_reorders("aaab")
        (1, 2, 0)
    """
    n = len(s)
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod
    inv = [1] * (n + 1)
    inv[n] = pow(fact[n], mod - 2, mod)
    for i in range(n, 0, -1):
        inv[i - 1] = inv[i] * i % mod
    cnt: dict[str, int] = {}
    for ch in s:
        cnt[ch] = cnt.get(ch, 0) + 1
    poly = [1]
    for c in cnt.values():
        q = [0] * (c + 1)
        for j in range(1, c + 1):
            ways = fact[c - 1] * inv[j - 1] % mod * inv[c - j] % mod  # C(c-1, j-1)
            q[j] = (ways if (c - j) % 2 == 0 else -ways) * inv[j] % mod  # знак (-1)^(c-j), / j!
        res = [0] * (len(poly) + c)
        for i, x in enumerate(poly):
            if x:
                for j in range(1, c + 1):
                    res[i + j] = (res[i + j] + x * q[j]) % mod
        poly = res  # произведение многочленов всех букв
    return sum(x * fact[t] for t, x in enumerate(poly)) % mod  # блоки переставляем T! способами


@algo(
    tags=["combinatorics", "inclusion-exclusion", "grid"],
    cses=["Grid Completion"],
    requires=["MOD7"],
    verified=False,
)
def grid_completion(grid: list[str], mod: int = MOD7) -> int:
    """Fill the grid so that each row and column has exactly one A and one B.   # Дополнение сетки.

    When to use:  grid of 'A', 'B', '.'; count completions.
    Complexity:   O(n^2)
    Returns:      the number of completions mod mod (0 if the given letters already clash).
    Idea:         missing A form a p x p permutation, missing B a q x q one. Forbidden events:
                  new A = new B in the same cell (only rows/cols missing both), new A on an
                  old B, new B on an old A. Inclusion-exclusion over i common cells,
                  j A-on-B and l B-on-A cells; the j and l sums factor out for fixed i.
                  NOT VERIFIED: statement reconstructed from memory, checked by brute force.
    CSES:         Grid Completion.
    Example:
        >>> grid_completion(["..", ".."]), grid_completion(["A.", ".."])
        (2, 1)
    """
    # NOT VERIFIED: условие CSES восстановлено по памяти, сверено только с перебором
    n = len(grid)
    ra = [True] * n  # строки без A
    ca = [True] * n
    rb = [True] * n
    cb = [True] * n
    for i, row in enumerate(grid):
        for j, ch in enumerate(row):
            if ch == "A":
                if not ra[i] or not ca[j]:
                    return 0
                ra[i] = ca[j] = False
            elif ch == "B":
                if not rb[i] or not cb[j]:
                    return 0
                rb[i] = cb[j] = False
    p = sum(ra)
    q = sum(rb)
    x = sum(1 for i in range(n) if ra[i] and rb[i])
    y = sum(1 for j in range(n) if ca[j] and cb[j])
    e1 = e2 = 0
    for i, row in enumerate(grid):
        for j, ch in enumerate(row):
            if ch == "B" and ra[i] and ca[j]:
                e1 += 1  # старая B мешает новой A
            elif ch == "A" and rb[i] and cb[j]:
                e2 += 1
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod
    inv = [pow(f, mod - 2, mod) for f in fact]

    def comb(a: int, b: int) -> int:
        return fact[a] * inv[b] % mod * inv[a - b] % mod if 0 <= b <= a else 0

    total = 0
    for i in range(min(x, y) + 1):
        if i > p or i > q:
            break
        sa = sum((-1) ** j * comb(e1, j) * fact[p - i - j] for j in range(min(e1, p - i) + 1))
        sb = sum((-1) ** t * comb(e2, t) * fact[q - i - t] for t in range(min(e2, q - i) + 1))
        term = comb(x, i) * comb(y, i) % mod * fact[i] % mod * (sa % mod) % mod * (sb % mod)
        total += -term if i % 2 else term
    return total % mod


@algo(tags=["construction", "permutations", "games"], cses=["Raab Game I"])
def raab_game_construct(n: int, a: int, b: int) -> tuple[list[int], list[int]] | None:
    """Card orders where player 1 wins a rounds and player 2 wins b.   # Игра Рааба I.

    When to use:  cards 1..n each; the larger card wins a round, equal cards tie.
    Complexity:   O(n)
    Returns:      (order1, order2) or None if impossible.
    Idea:         possible iff a + b <= n and (a == 0) == (b == 0). Tie on the last n - a - b
                  cards; on the first m = a + b player 1 plays 1..m and player 2 plays the
                  rotation a+1..m, 1..a (b wins, then a losses).
    CSES:         Raab Game I.
    Example:
        >>> raab_game_construct(4, 1, 2)
        ([1, 2, 3, 4], [2, 3, 1, 4])
        >>> raab_game_construct(3, 0, 1) is None
        True
    """
    if a + b > n or (a == 0) != (b == 0):
        return None
    m = a + b
    first = list(range(1, n + 1))
    second = list(range(a + 1, m + 1)) + list(range(1, a + 1)) + list(range(m + 1, n + 1))
    return first, second


@algo(
    tags=["combinatorics", "dp", "derangements"],
    cses=["Raab Game II"],
    requires=["MOD7"],
    verified=False,
)
def raab_game_count(n: int, a: int, b: int, mod: int = MOD7) -> int:
    """Number of games where player 1 wins a rounds and player 2 wins b.   # Игра Рааба II.

    When to use:  count pairs of card orders.
    Complexity:   O(n^2)
    Returns:      the count mod mod.
    Idea:         fix player 1's order as 1..n (multiply by n! at the end). Player 2's order
                  is a permutation with t = n - a - b fixed points, b excedances and a
                  deficiencies; removing fixed points keeps the comparisons, so the count is
                  C(n, t) * d(a + b, b), where d(m, k) = derangements of m with k excedances:
                  d(m,k) = k d(m-1,k) + (m-k) d(m-1,k-1) + (m-1) d(m-2,k-1).
                  NOT VERIFIED: whether CSES counts both orders (n! factor) or only player 2's.
    CSES:         Raab Game II.
    Example:
        >>> raab_game_count(2, 1, 1), raab_game_count(3, 1, 1), raab_game_count(3, 1, 0)
        (2, 18, 0)
    """
    # NOT VERIFIED: множитель n! (считаем обе последовательности карт) не сверен с условием
    if a + b > n:
        return 0
    m = a + b
    pp = [0] * (m + 1)  # d(i-2, .)
    pr = [1] + [0] * m  # d(i-1, .), d(0, 0) = 1
    for i in range(1, m + 1):
        cur = [0] * (m + 1)
        for k in range(1, min(i, b) + 1):
            cur[k] = (k * pr[k] + (i - k) * pr[k - 1] + (i - 1) * pp[k - 1]) % mod
        pp, pr = pr, cur
    t = n - m
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod
    choose = fact[n] * pow(fact[t] * fact[m] % mod, mod - 2, mod) % mod
    return choose * pr[b] % mod * fact[n] % mod


@algo(
    tags=["combinatorics", "functional-graph", "stirling"],
    cses=["Functional Graph Distribution"],
    requires=["MOD7"],
    verified=False,
)
def functional_graph_distribution(n: int, mod: int = MOD7) -> list[int]:
    """Functional graphs on n vertices with exactly k components.   # Функциональные графы.

    When to use:  distribution of components (= cycles) of random maps.
    Complexity:   O(n^2)
    Returns:      res[k - 1] for k = 1..n, mod mod.
    Python speed: n = 5000 ~ 3 s in CPython (n = 2000 ~ 0.5 s).
    Idea:         choose j cyclic vertices (C(n, j)), arrange them into k cycles (unsigned
                  Stirling numbers of the first kind s(j, k)), hang the rest as a forest with
                  j given roots (j * n^(n-j-1) ways, 1 if j = n).
                  NOT VERIFIED: statement reconstructed from memory, checked by brute force.
    CSES:         Functional Graph Distribution.
    Example:
        >>> functional_graph_distribution(3)
        [17, 9, 1]
    """
    # NOT VERIFIED: условие CSES восстановлено по памяти, сверено только с перебором
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod
    inv = [pow(f, mod - 2, mod) for f in fact]
    res = [0] * (n + 1)
    st = [1]  # s(j, .) - числа Стирлинга первого рода
    for j in range(1, n + 1):
        nxt = [0] * (j + 1)
        for k in range(1, j + 1):
            nxt[k] = (st[k - 1] + (j - 1) * (st[k] if k < j else 0)) % mod
        st = nxt
        forest = 1 if j == n else j * pow(n, n - j - 1, mod) % mod
        w = fact[n] * inv[j] % mod * inv[n - j] % mod * forest % mod
        for k in range(1, j + 1):
            res[k] = (res[k] + w * st[k]) % mod
    return res[1:]


@algo(tags=["dp", "intervals", "strings"], cses=["Empty String"], requires=["MOD7"])
def empty_string(s: str, mod: int = MOD7) -> int:
    """Number of ways to erase s by removing equal adjacent pairs.   # Пустая строка.

    When to use:  interval DP with interleaving of independent parts.
    Complexity:   O(n^3)
    Returns:      the number of removal orders mod mod (prime).
    Idea:         f(l, r) for s[l:r]: s[l] is removed together with some s[m] = s[l]; the inside
                  s[l+1:m] is erased first, the rest s[m+1:r] independently; the two streams of
                  operations interleave in C((r - l) / 2, (r - m - 1) / 2) ways.
    CSES:         Empty String.
    Example:
        >>> empty_string("aabccb"), empty_string("abba"), empty_string("ab")
        (3, 1, 0)
    """
    n = len(s)
    if n % 2:
        return 0
    h = n // 2
    fact = [1] * (h + 1)
    for i in range(1, h + 1):
        fact[i] = fact[i - 1] * i % mod
    inv = [pow(f, mod - 2, mod) for f in fact]
    f = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        f[i][i] = 1
    for length in range(2, n + 1, 2):
        half = length // 2
        for l in range(n - length + 1):
            r = l + length
            c = s[l]
            inner = f[l + 1]
            total = 0
            for m in range(l + 1, r, 2):  # s[l] уходит в паре с s[m]
                if s[m] == c:
                    right = (r - m - 1) // 2
                    ways = fact[half] * inv[right] % mod * inv[half - right] % mod  # чередование
                    total += inner[m] * f[m + 1][r] % mod * ways
            f[l][r] = total % mod
    return f[0][n]


@algo(
    tags=["combinatorics", "inclusion-exclusion", "surjections"],
    cses=["Counting Sequences"],
    requires=["MOD7"],
)
def counting_sequences(n: int, k: int, mod: int = MOD7) -> int:
    """Sequences of length n over 1..k that use every value.   # Сюръекции.

    When to use:  surjections = k! * S(n, k).
    Complexity:   O(k log n)
    Returns:      sum (-1)^i C(k, i) (k - i)^n mod mod.
    CSES:         Counting Sequences.
    Example:
        >>> counting_sequences(3, 2), counting_sequences(4, 4), counting_sequences(2, 3)
        (6, 24, 0)
    """
    res = 0
    c = 1  # C(k, i)
    for i in range(k + 1):
        term = c * pow(k - i, n, mod) % mod
        res += -term if i % 2 else term
        c = c * (k - i) % mod * pow(i + 1, mod - 2, mod) % mod
    return res % mod


@algo(
    tags=["combinatorics", "tournaments", "scc"],
    cses=["Tournament Graph Distribution"],
    requires=["MOD7"],
    verified=False,
)
def tournament_graph_distribution(n: int, mod: int = MOD7) -> list[int]:
    """Tournaments on n labelled vertices with exactly k SCCs.   # Турниры по числу КСС.

    When to use:  the condensation of a tournament is a transitive order (a path).
    Complexity:   O(n^3)
    Returns:      res[k - 1] for k = 1..n, mod mod.
    Python speed: n = 500 ~ 3 s in CPython (n = 200 ~ 0.2 s).
    Idea:         strong tournaments t(m) = 2^C(m,2) - sum_{i<m} C(m, i) t(i) 2^C(m-i,2)
                  (i = size of the top component); then g[m][k] = sum_i C(m, i) t(i) g[m-i][k-1].
                  NOT VERIFIED: statement reconstructed from memory, checked by brute force.
    CSES:         Tournament Graph Distribution.
    Example:
        >>> tournament_graph_distribution(3)
        [2, 0, 6]
    """
    # NOT VERIFIED: условие CSES восстановлено по памяти, сверено только с перебором
    c = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        c[i][0] = 1
        for j in range(1, i + 1):
            c[i][j] = (c[i - 1][j - 1] + c[i - 1][j]) % mod
    p2 = [pow(2, m * (m - 1) // 2, mod) for m in range(n + 1)]
    t = [0] * (n + 1)
    for m in range(1, n + 1):
        t[m] = (p2[m] - sum(c[m][i] * t[i] % mod * p2[m - i] for i in range(1, m))) % mod
    g = [[0] * (n + 1) for _ in range(n + 1)]
    g[0][0] = 1
    for m in range(1, n + 1):
        row = g[m]
        for i in range(1, m + 1):
            w = c[m][i] * t[i] % mod  # верхняя компонента из i вершин
            prev = g[m - i]
            for k in range(1, m - i + 2):
                if prev[k - 1]:
                    row[k] = (row[k] + w * prev[k - 1]) % mod
    return g[n][1:]


@algo(tags=["grid", "histogram", "stack"], cses=["Maximum Building I"])
def maximum_building(grid: list[str]) -> int:
    """Largest rectangle of free '.' cells.   # Максимальное здание I.

    When to use:  max empty rectangle; '*' cells are blocked.
    Complexity:   O(n * m)
    Returns:      the maximal area (0 if no free cell).
    Idea:         heights of free columns per row + largest rectangle in a histogram (stack).
    CSES:         Maximum Building I.
    Example:
        >>> maximum_building(["..*.", "....", "*..."])
        6
    """
    m = len(grid[0]) if grid else 0
    h = [0] * (m + 1)  # h[m] = 0 - стоп-элемент
    best = 0
    for row in grid:
        for j in range(m):
            h[j] = h[j] + 1 if row[j] == "." else 0
        st: list[int] = []
        for i in range(m + 1):
            while st and h[st[-1]] >= h[i]:
                top = h[st.pop()]
                left = st[-1] if st else -1
                best = max(best, top * (i - left - 1))
            st.append(i)
    return best


@algo(tags=["grid", "histogram", "stack", "counting"], cses=["Maximum Building II"])
def maximum_building_counts(grid: list[str]) -> list[list[int]]:
    """For every size h x w, the number of free rectangles of that size.   # Здание II.

    When to use:  all rectangle sizes at once; '*' cells are blocked.
    Complexity:   O(n * m)
    Returns:      res[h - 1][w - 1] for 1 <= h <= n, 1 <= w <= m.
    Idea:         per bottom row, each stack block (width W, height h_j, parent height hp)
                  gives W - w + 1 windows of width w for every height in (hp, h_j]. Collect
                  blocks with a difference array over heights, then
                  cnt[h][w] = sum_{W >= w} c[h][W] * (W - w + 1) via two suffix sums.
    CSES:         Maximum Building II.
    Example:
        >>> maximum_building_counts(["..", ".*"])
        [[3, 1], [1, 0]]
    """
    n = len(grid)
    m = len(grid[0]) if n else 0
    diff = [[0] * (m + 1) for _ in range(n + 2)]
    h = [0] * (m + 1)
    for row in grid:
        for j in range(m):
            h[j] = h[j] + 1 if row[j] == "." else 0
        st: list[int] = []
        for i in range(m + 1):
            cur = h[i]
            while st and h[st[-1]] >= cur:
                hj = h[st.pop()]
                if hj == cur:
                    continue  # равная высота: блок продолжится в i
                left = st[-1] if st else -1
                parent = max(cur, h[left] if left >= 0 else 0)
                width = i - left - 1
                diff[parent + 1][width] += 1  # высоты parent+1..hj
                diff[hj + 1][width] -= 1
            st.append(i)
    res = []
    run = [0] * (m + 1)
    for hh in range(1, n + 1):
        d = diff[hh]
        for w in range(m + 1):
            run[w] += d[w]  # run[W] = число блоков ширины W для высоты hh
        out = [0] * m
        s1 = s2 = 0
        for w in range(m, 0, -1):
            s1 += run[w]
            s2 += run[w] * w
            out[w - 1] = s2 - (w - 1) * s1
        res.append(out)
    return res


@algo(tags=["binary-lifting", "greedy", "circular"], cses=["Cyclic Array"])
def cyclic_array(a: list[int], k: int) -> int:
    """Fewest parts of a circular array with every part sum <= k.   # Циклический массив.

    When to use:  circular greedy partition; all a_i <= k.
    Complexity:   O(n log n)
    Returns:      the minimal number of contiguous circular parts.
    Idea:         on the doubled array nxt[i] = end of the greedy part starting at i (two
                  pointers). Binary lifting answers "how many jumps from i reach i + n" for
                  every start i; the optimum starts some part at some i.
    CSES:         Cyclic Array.
    Example:
        >>> cyclic_array([2, 2, 2, 1, 4, 3], 5), cyclic_array([1, 1, 1], 5)
        (3, 1)
    """
    n = len(a)
    if n == 0:
        return 0
    if sum(a) <= k:
        return 1
    b = a + a
    size = 2 * n
    nxt = [size] * (size + 1)
    r = 0
    s = 0
    for i in range(size):
        while r < size and s + b[r] <= k:
            s += b[r]
            r += 1
        nxt[i] = r  # жадный отрезок [i, r)
        s -= b[i]
    up = [nxt]
    for _ in range(n.bit_length()):
        prev = up[-1]
        up.append([prev[prev[i]] for i in range(size + 1)])
    best = n
    for i in range(n):
        pos = i
        cnt = 0
        for j in range(len(up) - 1, -1, -1):
            if up[j][pos] < i + n:
                pos = up[j][pos]
                cnt += 1 << j
        best = min(best, cnt + 1)
    return best


@algo(tags=["permutations", "inversions", "lis", "cycles"], cses=["Sorting Methods"])
def sorting_methods(p: list[int]) -> tuple[int, int, int, int]:
    """Minimal operations to sort p by four kinds of moves.   # Способы сортировки.

    When to use:  p is a permutation of 1..n.
    Complexity:   O(n log n)
    Returns:      (adjacent swaps, any swaps, moves anywhere, moves to the front) =
                  (inversions, n - cycles, n - LIS, n - k) where k is the longest run
                  n-k+1..n appearing in increasing positions.
    CSES:         Sorting Methods.
    Example:
        >>> sorting_methods([2, 1, 4, 5, 3])
        (3, 3, 2, 3)
    """
    n = len(p)
    tree = [0] * (n + 1)
    inv = 0
    for i, v in enumerate(p):
        x = v
        seen = 0
        while x > 0:
            seen += tree[x]  # сколько уже встретилось значений <= v
            x -= x & -x
        inv += i - seen
        x = v
        while x <= n:
            tree[x] += 1
            x += x & -x
    vis = [False] * n
    cycles = 0
    for i in range(n):
        if not vis[i]:
            cycles += 1
            j = i
            while not vis[j]:
                vis[j] = True
                j = p[j] - 1
    tails: list[int] = []
    for v in p:
        lo, hi = 0, len(tails)
        while lo < hi:
            mid = (lo + hi) // 2
            if tails[mid] < v:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(tails):
            tails.append(v)
        else:
            tails[lo] = v
    pos = [0] * (n + 1)
    for i, v in enumerate(p):
        pos[v] = i
    k = 1 if n else 0
    while k < n and pos[n - k] < pos[n - k + 1]:
        k += 1  # хвост n-k+1..n уже стоит по возрастанию
    return inv, n - cycles, n - len(tails), n - k


@algo(tags=["sorting", "simulation", "bubble-sort"], cses=["Bubble Sort Rounds"])
def bubble_sort_rounds(a: list[int]) -> int:
    """Number of bubble sort passes that perform at least one swap.   # Раунды пузырька.

    When to use:  each pass moves every element left by at most one position.
    Complexity:   O(n log n)
    Returns:      max over elements of (original index - index after stable sort).
    CSES:         Bubble Sort Rounds.
    Example:
        >>> bubble_sort_rounds([3, 1, 2]), bubble_sort_rounds([1, 2]), bubble_sort_rounds([2, 2, 1])
        (1, 0, 2)
    """
    order = sorted(range(len(a)), key=lambda i: a[i])  # стабильная сортировка
    return max((i - j for j, i in enumerate(order)), default=0)


@algo(
    tags=["greedy", "heap", "exchange-argument"], cses=["Programmers and Artists"], requires=["INF"]
)
def programmers_and_artists(pairs: list[tuple[int, int]], a: int, b: int) -> int:
    """Pick a programmers and b artists (disjoint), maximise skill.   # Программисты и художники.

    When to use:  two disjoint groups by two different scores.
    Complexity:   O(n log n)
    Input:        pairs[i] = (programming skill, art skill); a + b <= n.
    Returns:      the maximal sum.
    Idea:         sort by x - y descending: some optimum takes all programmers before all
                  artists. Prefix: best a values of x (min-heap); suffix: best b values of y.
    CSES:         Programmers and Artists.
    Example:
        >>> programmers_and_artists([(2, 8), (3, 1), (6, 6), (4, 5)], 2, 1)
        18
    """
    ps = sorted(pairs, key=lambda t: t[1] - t[0])
    n = len(ps)
    pre = [-INF] * (n + 1)
    heap: list[int] = []
    s = 0
    for i in range(n + 1):
        if len(heap) == a:
            pre[i] = s
        if i == n:
            break
        heapq.heappush(heap, ps[i][0])
        s += ps[i][0]
        if len(heap) > a:
            s -= heapq.heappop(heap)  # выкидываем худшего программиста
    suf = [-INF] * (n + 1)
    heap = []
    s = 0
    for i in range(n, -1, -1):
        if len(heap) == b:
            suf[i] = s
        if i == 0:
            break
        heapq.heappush(heap, ps[i - 1][1])
        s += ps[i - 1][1]
        if len(heap) > b:
            s -= heapq.heappop(heap)
    return max(pre[i] + suf[i] for i in range(n + 1))


@algo(tags=["dp", "open-groups", "counting"], cses=["Coding Company"], requires=["MOD7"])
def coding_company(skills: list[int], x: int, mod: int = MOD7) -> int:
    """Ways to split people into teams with total (max - min) penalty <= x.   # Компания.

    When to use:  "open groups" DP: sort, pay gaps for every open team.
    Complexity:   O(n^2 * x)
    Returns:      the number of partitions mod mod.
    Python speed: n = 100, x = 5000 ~ 4 s in CPython.
    Idea:         after sorting, the penalty of a team = sum of gaps it spans; going from s_{i-1}
                  to s_i adds j * gap for j open teams. Element i: own team, open a team,
                  join an open team (j ways) and keep it open or close it.
    CSES:         Coding Company.
    Example:
        >>> coding_company([2, 5, 3], 2), coding_company([1, 2, 3], 0)
        (3, 1)
    """
    s = sorted(skills)
    n = len(s)
    dp = [[0] * (x + 1) for _ in range(n + 2)]
    dp[0][0] = 1
    for i in range(n):
        gap = s[i] - s[i - 1] if i else 0
        new = [[0] * (x + 1) for _ in range(n + 2)]
        for j in range(n + 1):
            row = dp[j]
            shift = j * gap
            if shift > x:
                continue
            for p in range(x + 1 - shift):
                v = row[p]
                if not v:
                    continue
                q = p + shift  # открытые команды растянулись на gap
                new[j][q] = (new[j][q] + v * (j + 1)) % mod  # своя команда или в открытую
                new[j + 1][q] = (new[j + 1][q] + v) % mod  # открыть новую
                if j:
                    new[j - 1][q] = (new[j - 1][q] + v * j) % mod  # закрыть открытую
        dp = new
    return sum(dp[0]) % mod


@algo(tags=["stacks", "bipartite", "permutations"], cses=["Two Stacks Sorting"], requires=["INF"])
def two_stacks_sorting(a: list[int]) -> list[int] | None:
    """Assign each element to stack 1 or 2 so that the output is sorted.   # Две стопки.

    When to use:  a is a permutation of 1..n; push in order, pop greedily 1, 2, ..., n.
    Complexity:   O(n^2)
    Returns:      stack labels (1 / 2) per element or None if impossible.
    Python speed: O(n^2) conflicts: n = 3000 ~ 0.3 s; CSES n = 2 * 10^5 needs the
                  segment-tree version of the conflict graph.
    Idea:         i < j conflict (cannot share a stack) iff a_i < a_j and some k > j has
                  a_k < a_i. Sortable iff the conflict graph is bipartite (Even-Itai); any
                  2-colouring is an answer.
    CSES:         Two Stacks Sorting.
    Example:
        >>> two_stacks_sorting([2, 3, 1]), two_stacks_sorting([2, 3, 4, 1])
        ([1, 2, 1], None)
    """
    n = len(a)
    sufmin = [INF] * (n + 1)
    for i in range(n - 1, -1, -1):
        sufmin[i] = min(a[i], sufmin[i + 1])
    adj: list[list[int]] = [[] for _ in range(n)]
    for i in range(n):
        ai = a[i]
        for j in range(i + 1, n):
            if ai < a[j] and sufmin[j + 1] < ai:  # i не успеет выйти, а j ляжет сверху
                adj[i].append(j)
                adj[j].append(i)
    color = [0] * n
    for s in range(n):
        if color[s]:
            continue
        color[s] = 1
        q = deque([s])
        while q:
            v = q.popleft()
            for u in adj[v]:
                if not color[u]:
                    color[u] = 3 - color[v]
                    q.append(u)
                elif color[u] == color[v]:
                    return None
    return color


@algo(tags=["greedy", "heap", "huffman"], cses=["Stick Divisions"])
def stick_divisions(x: int, lengths: list[int]) -> int:
    """Minimal cost to cut a stick of length x into the given pieces.   # Деление палки.

    When to use:  cost of a cut = current stick length; reversed this is Huffman merging.
    Complexity:   O(n log n)
    Returns:      the minimal total cost (sum(lengths) must equal x).
    CSES:         Stick Divisions.
    Example:
        >>> stick_divisions(8, [2, 3, 3]), stick_divisions(5, [5])
        (13, 0)
    """
    if sum(lengths) != x:
        raise ValueError("pieces must sum to x")
    h = list(lengths)
    heapq.heapify(h)
    cost = 0
    while len(h) > 1:
        s = heapq.heappop(h) + heapq.heappop(h)  # склеиваем два самых коротких
        cost += s
        heapq.heappush(h, s)
    return cost


@algo(tags=["permutations", "cycles", "construction"], cses=["Swap Round Sorting"])
def swap_round_sorting(p: list[int]) -> list[list[tuple[int, int]]]:
    """Sort with the fewest rounds of disjoint swaps.   # Сортировка раундами обменов.

    When to use:  p is a permutation of 1..n; each round swaps disjoint pairs of positions.
    Complexity:   O(n)
    Returns:      list of rounds (0, 1 or 2), each a list of 0-based position pairs.
    Idea:         a cycle is a product of two reflections: with c[i+1] = p[c[i]] - 1, swap
                  c[i] <-> c[-i] in round 1 and c[i] <-> c[1-i] in round 2. 2-cycles only
                  need one swap, so all cycles of length <= 2 give a single round.
    CSES:         Swap Round Sorting.
    Example:
        >>> swap_round_sorting([2, 1, 4, 3]), swap_round_sorting([2, 3, 1])
        ([[(0, 1), (2, 3)]], [[(1, 2)], [(0, 1)]])
    """
    n = len(p)
    seen = [False] * n
    r1: list[tuple[int, int]] = []
    r2: list[tuple[int, int]] = []
    for s in range(n):
        if seen[s]:
            continue
        c = []
        x = s
        while not seen[x]:
            seen[x] = True
            c.append(x)
            x = p[x] - 1  # элемент с позиции x должен уехать на p[x] - 1
        k = len(c)
        for i in range(k):
            j = -i % k
            if i < j:
                r1.append((c[i], c[j]))  # отражение i <-> -i
            j = (1 - i) % k
            if i < j:
                r2.append((c[i], c[j]))  # отражение i <-> 1 - i
    return [r for r in (r1, r2) if r]


@algo(
    tags=["strings", "subsequences", "euclid"],
    cses=["Binary Subsequences"],
    requires=["INF"],
    verified=False,
)
def binary_subsequences(n: int) -> str:
    """Shortest bit string with exactly n distinct subsequences.   # Двоичные подпоследовательности.

    When to use:  Euclid / Stern-Brocot walk; n >= 1.
    Complexity:   O(n log n)
    Returns:      one shortest string.
    Idea:         with X = 1 + #subsequences ending in 0 and Y = 1 + #ending in 1, appending 0
                  maps (X, Y) -> (X + Y, Y), appending 1 maps (X, Y) -> (X, X + Y); start (1, 1),
                  total = X + Y - 2. Try every coprime X + Y = n + 2, length = sum of Euclid
                  quotients - 1; rebuild the string by reverse subtraction.
                  NOT VERIFIED: whether the empty subsequence is counted in the statement.
    CSES:         Binary Subsequences.
    Example:
        >>> binary_subsequences(4), binary_subsequences(5)
        ('1111', '011')
    """
    # NOT VERIFIED: учитывается ли пустая подпоследовательность - не сверено
    total = n + 2
    best = INF
    best_x = 1
    for x in range(1, total):
        y = total - x
        if gcd(x, y) != 1:
            continue
        steps = 0
        u, v = x, y
        while u != 1 or v != 1:
            if steps >= best:
                break
            if u == 1 or v == 1:
                steps += max(u, v) - 1
                break
            if u > v:
                steps += u // v
                u %= v
            else:
                steps += v // u
                v %= u
        if steps < best:
            best = steps
            best_x = x
    u, v = best_x, total - best_x
    out = []
    while u != 1 or v != 1:
        if u > v:
            out.append("0")  # последним дописали 0
            u -= v
        else:
            out.append("1")
            v -= u
    return "".join(reversed(out))


@algo(tags=["dsu", "subset-sum", "bitset"], cses=["School Excursion"])
def school_excursion(n: int, edges: list[tuple[int, int]]) -> str:
    """Which group sizes k = 1..n can be formed from whole friend components.   # Экскурсия.

    When to use:  subset sum over component sizes; Python int as a bitset.
    Complexity:   O(n sqrt n / 64) word operations
    Returns:      string of length n, char k-1 is '1' if exactly k children can go.
    Idea:         DSU for component sizes; equal sizes are grouped and split into powers of
                  two (bounded knapsack), so there are O(sqrt n) shifts.
    CSES:         School Excursion.
    Example:
        >>> school_excursion(5, [(0, 1), (1, 2), (3, 4)])
        '01101'
    """
    parent = list(range(n))
    for u, v in edges:
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        if u != v:
            parent[u] = v
    size: dict[int, int] = {}
    for v in range(n):
        r = v
        while parent[r] != r:
            r = parent[r]
        size[r] = size.get(r, 0) + 1
    cnt: dict[int, int] = {}
    for s in size.values():
        cnt[s] = cnt.get(s, 0) + 1
    bits = 1
    mask = (1 << (n + 1)) - 1
    for s, c in cnt.items():
        part = 1
        while c > 0:
            take = min(part, c)  # двоичное разбиение повторов
            bits = (bits | bits << (s * take)) & mask
            c -= take
            part <<= 1
    return "".join("1" if bits >> k & 1 else "0" for k in range(1, n + 1))


@algo(tags=["bipartite", "matching", "konig", "vertex-cover"], cses=["Coin Grid"])
def coin_grid(grid: list[str]) -> tuple[int, list[tuple[int, int]]]:
    """Fewest row / column clears that collect every coin 'o'.   # Монеты на сетке.

    When to use:  minimum vertex cover in the rows-columns bipartite graph (Koenig).
    Complexity:   O(n * E) (Kuhn with BFS augmenting paths)
    Returns:      (count, moves) with moves (1, r) = clear row r, (2, c) = clear column c.
    Idea:         max matching = min cover; cover = rows not reached + columns reached by
                  alternating BFS from unmatched rows.
    CSES:         Coin Grid.
    Example:
        >>> coin_grid(["o.o", "...", ".o."])
        (2, [(1, 0), (1, 2)])
    """
    n = len(grid)
    m = len(grid[0]) if n else 0
    adj = [[j for j in range(m) if grid[i][j] == "o"] for i in range(n)]
    ml = [-1] * n
    mr = [-1] * m
    for s in range(n):
        par = [-1] * m
        seen = [False] * m
        q = deque([s])
        end = -1
        while q and end < 0:
            v = q.popleft()
            for c in adj[v]:
                if not seen[c]:
                    seen[c] = True
                    par[c] = v
                    if mr[c] < 0:
                        end = c
                        break
                    q.append(mr[c])
        c = end
        while c >= 0:  # разворачиваем увеличивающий путь
            v = par[c]
            nc = ml[v]
            ml[v] = c
            mr[c] = v
            c = nc
    vis_l = [False] * n
    vis_r = [False] * m
    q = deque(i for i in range(n) if ml[i] < 0)
    for i in q:
        vis_l[i] = True
    while q:
        v = q.popleft()
        for c in adj[v]:
            if not vis_r[c]:
                vis_r[c] = True
                u = mr[c]
                if u >= 0 and not vis_l[u]:
                    vis_l[u] = True
                    q.append(u)
    moves = [(1, i) for i in range(n) if not vis_l[i]] + [(2, j) for j in range(m) if vis_r[j]]
    return len(moves), moves


@algo(tags=["greedy", "balance", "grid"], cses=["Coin Arrangement"])
def coin_arrangement(top: list[int], bottom: list[int]) -> int:
    """Fewest unit moves to leave one coin per cell of a 2 x n grid.   # Расстановка монет.

    When to use:  total coins = 2n; a move shifts one coin to a neighbouring cell.
    Complexity:   O(n)
    Returns:      the minimal number of moves.
    Idea:         sweep columns keeping surpluses b1, b2 of the two rows; if they have opposite
                  signs, settle min(|b1|, |b2|) vertically first, then carry |b1| + |b2| coins
                  to the next column.
    CSES:         Coin Arrangement.
    Example:
        >>> coin_arrangement([0, 1, 3], [1, 0, 1])
        4
    """
    b1 = b2 = 0
    cost = 0
    for x, y in zip(top, bottom):
        b1 += x - 1
        b2 += y - 1
        if b1 > 0 > b2:
            t = min(b1, -b2)  # вертикальный перенос сверху вниз
            b1 -= t
            b2 += t
            cost += t
        elif b2 > 0 > b1:
            t = min(b2, -b1)
            b1 += t
            b2 -= t
            cost += t
        cost += abs(b1) + abs(b2)  # перенос остатков в следующий столбец
    return cost


@algo(tags=["construction", "gale-ryser", "greedy"], cses=["Grid Puzzle I"])
def grid_puzzle_i(a: list[int], b: list[int]) -> list[str] | None:
    """Grid with a_i marked cells in row i and b_j in column j.   # Головоломка I.

    When to use:  0/1 matrix with given row and column sums.
    Complexity:   O(n * m log m)
    Returns:      rows of 'X' / '.' or None if impossible.
    Idea:         Gale-Ryser: fill each row with the columns of largest remaining demand
                  (equivalent to the flow source -> rows -> columns -> sink).
    CSES:         Grid Puzzle I.
    Example:
        >>> grid_puzzle_i([1, 2], [2, 1])
        ['X.', 'XX']
        >>> grid_puzzle_i([2, 0], [0, 2]) is None
        True
    """
    m = len(b)
    rem = list(b)
    res = []
    for need in a:
        cols = sorted(range(m), key=lambda j: -rem[j])[:need]
        if need > m or any(rem[j] == 0 for j in cols):
            return None
        row = ["."] * m
        for j in cols:
            rem[j] -= 1  # столбец с наибольшей оставшейся потребностью
            row[j] = "X"
        res.append("".join(row))
    return res if not any(rem) else None


@algo(
    tags=["min-cost-flow", "assignment", "grid"],
    cses=["Grid Puzzle II"],
    requires=["INF"],
    verified=False,
)
def grid_puzzle_ii(
    a: list[int], b: list[int], value: list[list[int]]
) -> tuple[int, list[str]] | None:
    """Row / column sums as in Grid Puzzle I, maximise the chosen sum.   # Головоломка II.

    When to use:  max-weight b-matching on a dense bipartite graph (n <= ~50).
    Complexity:   O(F * V * E), F = sum(a) augmentations of Bellman-Ford (SPFA)
    Returns:      (best total, rows of 'X' / '.') or None if the sums cannot be met.
    Idea:         min-cost flow source -> row i (cap a_i) -> column j (cap 1, cost -value)
                  -> sink (cap b_j); successive shortest paths with SPFA.
                  NOT VERIFIED: statement reconstructed from memory, checked by brute force.
    CSES:         Grid Puzzle II.
    Example:
        >>> grid_puzzle_ii([1, 1], [1, 1], [[5, 1], [1, 2]])
        (7, ['X.', '.X'])
    """
    # NOT VERIFIED: условие CSES восстановлено по памяти, сверено только с перебором
    n = len(a)
    m = len(b)
    if sum(a) != sum(b):
        return None
    src = n + m
    snk = src + 1
    g: list[list[int]] = [[] for _ in range(snk + 1)]
    to: list[int] = []
    cap: list[int] = []
    cost: list[int] = []

    def add(u: int, v: int, c: int, w: int) -> None:
        g[u].append(len(to))
        to.append(v)
        cap.append(c)
        cost.append(w)
        g[v].append(len(to))
        to.append(u)
        cap.append(0)
        cost.append(-w)

    for i in range(n):
        add(src, i, a[i], 0)
        for j in range(m):
            add(i, n + j, 1, -value[i][j])
    for j in range(m):
        add(n + j, snk, b[j], 0)
    flow = 0
    total = 0
    while True:
        dist = [INF] * (snk + 1)
        pe = [-1] * (snk + 1)
        inq = [False] * (snk + 1)
        dist[src] = 0
        q = deque([src])
        while q:
            v = q.popleft()
            inq[v] = False
            for e in g[v]:
                if cap[e] > 0 and dist[v] + cost[e] < dist[to[e]]:
                    u = to[e]
                    dist[u] = dist[v] + cost[e]
                    pe[u] = e
                    if not inq[u]:
                        inq[u] = True
                        q.append(u)
        if dist[snk] == INF:
            break
        f = INF
        v = snk
        while v != src:
            e = pe[v]
            f = min(f, cap[e])
            v = to[e ^ 1]
        v = snk
        while v != src:
            e = pe[v]
            cap[e] -= f  # проталкиваем поток по кратчайшему пути
            cap[e ^ 1] += f
            v = to[e ^ 1]
        flow += f
        total += f * dist[snk]
    if flow != sum(a):
        return None
    rows = []
    for i in range(n):
        row = ["."] * m
        for e in g[i]:
            if n <= to[e] < n + m and cap[e] == 0 and e % 2 == 0:
                row[to[e] - n] = "X"
        rows.append("".join(row))
    return -total, rows
