"""Dynamic programming: coins, knapsacks, subsequences, intervals, bitmasks, profiles, digits,
convex hull trick, divide & conquer and Knuth optimisations.

Динамическое программирование. Всё итеративно.
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right
from typing import Callable

from rustinpy._registry import algo

MOD = 998244353
MOD7 = 10**9 + 7
INF = 1 << 60


@algo(tags=["dp", "counting", "dice"], cses=["Dice Combinations (1633)"], requires=["MOD7"])
def dice_combinations(n: int, mod: int = MOD7) -> int:
    """Ordered ways to get sum n with dice throws 1..6.   # Комбинации кубика.

    When to use:  the first DP of CSES; n up to 10^6 (for 10^18 use mathx.throwing_dice).
    Complexity:   O(6n)
    Returns:      count mod mod; dice_combinations(0) = 1.
    Related:      mathx.throwing_dice, coin_combinations_ordered.
    CSES:         Dice Combinations (1633).
    Example:
        >>> dice_combinations(3), dice_combinations(7)
        (4, 63)
    """
    dp = [1] + [0] * n
    for s in range(1, n + 1):
        dp[s] = sum(dp[max(0, s - 6) : s]) % mod  # последний бросок 1..6
    return dp[n]


@algo(tags=["dp", "coins", "unbounded"], cses=["Minimizing Coins (1634)"], requires=["INF"])
def min_coins(coins: list[int], x: int) -> int:
    """Fewest coins (unlimited supply) with sum exactly x.   # Минимум монет.

    When to use:  unbounded "make change" minimisation.
    Complexity:   O(n * x)
    Returns:      minimal number of coins, -1 if impossible.
    Related:      coin_combinations_unordered, knapsack_unbounded.
    CSES:         Minimizing Coins (1634).
    Example:
        >>> min_coins([1, 5, 7], 11), min_coins([4, 6], 7)
        (3, -1)
    """
    dp = [0] + [INF] * x
    for s in range(1, x + 1):
        best = INF
        for c in coins:
            if c <= s and dp[s - c] + 1 < best:
                best = dp[s - c] + 1  # последняя монета - c
        dp[s] = best
    return dp[x] if dp[x] < INF else -1


@algo(tags=["dp", "coins", "counting"], cses=["Coin Combinations I (1635)"], requires=["MOD7"])
def coin_combinations_ordered(coins: list[int], x: int, mod: int = MOD7) -> int:
    """Number of ORDERED sequences of coins with sum x.   # Комбинации монет (порядок важен).

    When to use:  compositions: 2 + 3 and 3 + 2 are different.
    Complexity:   O(n * x)
    Returns:      count mod mod.
    Pitfalls:     loop over sums OUTSIDE, coins inside (the opposite counts multisets).
    Related:      coin_combinations_unordered.
    CSES:         Coin Combinations I (1635).
    Example:
        >>> coin_combinations_ordered([2, 3, 5], 9)
        8
    """
    dp = [1] + [0] * x
    for s in range(1, x + 1):
        t = 0
        for c in coins:
            if c <= s:
                t += dp[s - c]  # последняя монета - c
        dp[s] = t % mod
    return dp[x]


@algo(tags=["dp", "coins", "counting"], cses=["Coin Combinations II (1636)"], requires=["MOD7"])
def coin_combinations_unordered(coins: list[int], x: int, mod: int = MOD7) -> int:
    """Number of multisets of coins with sum x.   # Комбинации монет (порядок не важен).

    When to use:  partitions into given parts.
    Complexity:   O(n * x)
    Returns:      count mod mod.
    Pitfalls:     coins OUTSIDE, sums inside: each coin type is considered once.
    Related:      coin_combinations_ordered.
    CSES:         Coin Combinations II (1636).
    Example:
        >>> coin_combinations_unordered([2, 3, 5], 9)
        3
    """
    dp = [1] + [0] * x
    for c in coins:
        for s in range(c, x + 1):  # монеты типа c добавляются по одной
            dp[s] = (dp[s] + dp[s - c]) % mod
    return dp[x]


@algo(tags=["dp", "greedy", "digits"], cses=["Removing Digits (1637)"])
def removing_digits(n: int) -> int:
    """Min steps to reach 0 subtracting one of the current digits.   # Удаление цифр.

    When to use:  DP over numbers with transitions by digits.
    Complexity:   O(n * digits)
    Returns:      minimal number of steps.
    Pitfalls:     greedy "subtract the largest digit" is also optimal here, the DP proves it.
    CSES:         Removing Digits (1637).
    Example:
        >>> removing_digits(27)
        5
    """
    dp = [0] * (n + 1)
    for v in range(1, n + 1):
        dp[v] = 1 + min(dp[v - int(d)] for d in str(v) if d != "0")  # вычитаем цифру
    return dp[n]


@algo(tags=["dp", "grid", "counting"], cses=["Grid Paths (1638)"], requires=["MOD7"])
def grid_paths(grid: list[str], mod: int = MOD7) -> int:
    """Paths from top-left to bottom-right moving right / down, avoiding '*'.   # Пути по сетке.

    When to use:  counting monotone lattice paths with obstacles.
    Complexity:   O(R * C)
    Returns:      count mod mod.
    CSES:         Grid Paths (1638).
    Example:
        >>> grid_paths(["....", ".*..", "...*", "*..."])
        3
    """
    C = len(grid[0])
    dp = [0] * C
    dp[0] = 1
    for row in grid:
        for c in range(C):
            if row[c] == "*":
                dp[c] = 0  # ловушка
            elif c:
                dp[c] = (dp[c] + dp[c - 1]) % mod  # сверху + слева
    return dp[C - 1] % mod


@algo(tags=["dp", "knapsack"], cses=["Book Shop (1158)"])
def knapsack_01(weights: list[int], values: list[int], cap: int) -> int:
    """0/1 knapsack: each item at most once.   # Рюкзак 0/1.

    When to use:  choose items with total weight <= cap maximising value.
    Complexity:   O(n * cap)
    Returns:      maximal total value.
    Pitfalls:     iterate capacity DOWNWARDS, otherwise items are reused.
    Python speed: n = 1000, cap = 10^5 (10^8 updates) is too slow in pure loops; this version
                  updates whole rows with list comprehensions: ~13 s.
    Related:      knapsack_unbounded, knapsack_bounded, money_sums.
    CSES:         Book Shop (1158).
    Example:
        >>> knapsack_01([4, 8, 5, 3], [5, 12, 8, 1], 10)
        13
    """
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        if w > cap:
            continue
        # новая строка целиком: dp[c] = max(dp[c], dp[c - w] + v) для c >= w
        dp[w:] = [max(a, b + v) for a, b in zip(dp[w:], dp[: cap + 1 - w])]
    return dp[cap]


@algo(tags=["dp", "knapsack", "unbounded"], cses=["- (unbounded knapsack)"])
def knapsack_unbounded(weights: list[int], values: list[int], cap: int) -> int:
    """Knapsack with unlimited copies of each item.   # Неограниченный рюкзак.

    When to use:  items can be taken any number of times.
    Complexity:   O(n * cap)
    Returns:      maximal total value.
    Related:      knapsack_01, min_coins.
    CSES:         - (unbounded knapsack)
    Example:
        >>> knapsack_unbounded([3, 4], [4, 6], 10)
        14
    """
    dp = [0] * (cap + 1)
    for c in range(1, cap + 1):
        best = dp[c - 1]  # можно не использовать единицу ёмкости
        for w, v in zip(weights, values):
            if w <= c and dp[c - w] + v > best:
                best = dp[c - w] + v
        dp[c] = best
    return dp[cap]


@algo(
    tags=["dp", "knapsack", "bounded", "binary-splitting"],
    cses=["Book Shop II (1159)"],
    requires=["knapsack_01"],
)
def knapsack_bounded(weights: list[int], values: list[int], counts: list[int], cap: int) -> int:
    """Knapsack where item i has counts[i] copies (binary splitting).   # Ограниченный рюкзак.

    When to use:  "k copies of each book".
    Complexity:   O(cap * sum log counts)
    Returns:      maximal total value.
    Idea:         split k copies into packs 1, 2, 4, ..., rest; then 0/1 knapsack.
    Related:      knapsack_01.
    CSES:         Book Shop II (1159).
    Example:
        >>> knapsack_bounded([2, 3], [3, 5], [3, 1], 8)
        11
    """
    ws: list[int] = []
    vs: list[int] = []
    for w, v, k in zip(weights, values, counts):
        p = 1
        while k > 0:
            take = min(p, k)  # пачки 1, 2, 4, ... и остаток
            ws.append(w * take)
            vs.append(v * take)
            k -= take
            p *= 2
    return knapsack_01(ws, vs, cap)


@algo(tags=["dp", "counting", "arrays"], cses=["Array Description (1746)"], requires=["MOD7"])
def array_description(a: list[int], m: int, mod: int = MOD7) -> int:
    """Fill zeros with 1..m so that neighbours differ by at most 1.   # Описание массива.

    When to use:  count arrays with local constraints and some fixed values.
    Complexity:   O(n * m)
    Input:        a[i] = 0 means unknown, otherwise fixed value in 1..m.
    Returns:      count mod mod.
    CSES:         Array Description (1746).
    Example:
        >>> array_description([2, 0, 2], 5)
        3
    """
    dp = [0] * (m + 2)  # dp[v] - способов, если текущее значение v
    for v in range(1, m + 1):
        if a[0] in (0, v):
            dp[v] = 1
    for x in a[1:]:
        new = [0] * (m + 2)
        for v in range(1, m + 1):
            if x in (0, v):
                new[v] = (dp[v - 1] + dp[v] + dp[v + 1]) % mod  # сосед отличается <= 1
        dp = new
    return sum(dp) % mod


@algo(tags=["dp", "counting", "tilings"], cses=["Counting Towers (2413)"], requires=["MOD7"])
def counting_towers(n: int, mod: int = MOD7) -> int:
    """Number of towers of width 2 and height n built from rectangles.   # Подсчёт башен.

    When to use:  linear DP with two states (top joined / top split).
    Complexity:   O(n)
    Returns:      count mod mod.
    Idea:         joined' = 2 joined + split, split' = joined + 4 split.
    CSES:         Counting Towers (2413).
    Example:
        >>> counting_towers(2), counting_towers(6)
        (8, 2864)
    """
    joined, split = 1, 1  # верхний ряд - один блок ширины 2 / два блока
    for _ in range(n - 1):
        joined, split = (2 * joined + split) % mod, (joined + 4 * split) % mod
    return (joined + split) % mod


@algo(tags=["dp", "strings", "edit-distance"], cses=["Edit Distance (1639)"])
def edit_distance(a: str, b: str) -> int:
    """Levenshtein distance (insert / delete / replace).   # Расстояние редактирования.

    When to use:  minimal edits to turn a into b.
    Complexity:   O(|a| * |b|) time, O(|b|) memory
    Returns:      edit distance.
    CSES:         Edit Distance (1639).
    Example:
        >>> edit_distance("LOVE", "MOVIE")
        2
    """
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))  # 3 операции
        prev = cur
    return prev[-1]


@algo(tags=["dp", "lcs", "subsequence"], cses=["Longest Common Subsequence (3403)"])
def lcs(a: list[int], b: list[int]) -> list[int]:
    """One longest common subsequence (restored).   # Наибольшая общая подпоследовательность.

    When to use:  n, m <= ~3000.
    Complexity:   O(n * m)
    Returns:      the subsequence itself.
    CSES:         Longest Common Subsequence (3403).
    Example:
        >>> r = lcs([2, 3, 1, 2, 5], [3, 2, 2, 5, 1])
        >>> len(r), r[-1]
        (3, 5)
    """
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        ai, row, nxt = a[i], dp[i], dp[i + 1]
        for j in range(m):
            nxt[j + 1] = row[j] + 1 if ai == b[j] else max(row[j + 1], nxt[j])
    res = []
    i, j = n, m
    while i and j:  # восстановление с конца
        if a[i - 1] == b[j - 1]:
            res.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return res[::-1]


@algo(tags=["dp", "lis", "binary-search"], cses=["Increasing Subsequence (1145)"])
def lis(a: list[int], strict: bool = True) -> list[int]:
    """Indices of one longest increasing subsequence.   # Наибольшая возрастающая подпосл-ть.

    When to use:  LIS with reconstruction; strict=False for non-decreasing.
    Complexity:   O(n log n)
    Returns:      list of indices i_1 < i_2 < ... of a longest (non-)decreasing chain.
    Related:      lis_length, count_increasing_subsequences.
    CSES:         Increasing Subsequence (1145).
    Example:
        >>> a = [7, 3, 5, 3, 6, 2, 9, 8]
        >>> [a[i] for i in lis(a)], lis([1, 1, 2], strict=False)
        ([3, 5, 6, 8], [0, 1, 2])
    """
    tails: list[int] = []  # минимальный последний элемент цепочки длины k + 1
    tails_idx: list[int] = []
    prev = [-1] * len(a)
    for i, x in enumerate(a):
        k = bisect_left(tails, x) if strict else bisect_right(tails, x)
        if k == len(tails):
            tails.append(x)
            tails_idx.append(i)
        else:
            tails[k] = x
            tails_idx[k] = i
        prev[i] = tails_idx[k - 1] if k else -1  # предыдущий элемент цепочки
    res = []
    i = tails_idx[-1] if tails_idx else -1
    while i != -1:
        res.append(i)
        i = prev[i]
    return res[::-1]


@algo(tags=["dp", "lis", "binary-search"], cses=["Increasing Subsequence (1145)"])
def lis_length(a: list[int], strict: bool = True) -> int:
    """Length of the longest increasing subsequence.   # Длина LIS.

    When to use:  only the length is needed (shortest code).
    Complexity:   O(n log n)
    Returns:      LIS length.
    Related:      lis.
    CSES:         Increasing Subsequence (1145).
    Example:
        >>> lis_length([7, 3, 5, 3, 6, 2, 9, 8]), lis_length([2, 2, 2], strict=False)
        (4, 3)
    """
    tails: list[int] = []
    for x in a:
        k = bisect_left(tails, x) if strict else bisect_right(tails, x)
        if k == len(tails):
            tails.append(x)
        else:
            tails[k] = x  # улучшили хвост цепочки длины k + 1
    return len(tails)


@algo(
    tags=["dp", "lis", "fenwick", "counting"],
    cses=["Increasing Subsequence II (1748)"],
    requires=["MOD7"],
)
def count_increasing_subsequences(a: list[int], mod: int = MOD7) -> int:
    """Number of strictly increasing subsequences.   # Число возрастающих подпоследовательностей.

    When to use:  count chains, not just the longest.
    Complexity:   O(n log n)
    Returns:      count mod mod.
    Idea:         ways[i] = 1 + sum of ways[j] with j < i, a[j] < a[i]: Fenwick by value.
    Related:      lis.
    CSES:         Increasing Subsequence II (1748).
    Example:
        >>> count_increasing_subsequences([2, 1, 3])
        5
    """
    comp = {v: i for i, v in enumerate(sorted(set(a)))}
    m = len(comp)
    t = [0] * (m + 1)
    total = 0
    for x in a:
        i = comp[x]
        s, j = 0, i  # сумма по значениям < x
        while j > 0:
            s += t[j]
            j -= j & -j
        ways = (s + 1) % mod
        total = (total + ways) % mod
        j = i + 1
        while j <= m:
            t[j] = (t[j] + ways) % mod
            j += j & -j
    return total


@algo(tags=["dp", "subset-sum", "bitset"], cses=["Money Sums (1745)"])
def money_sums(coins: list[int]) -> list[int]:
    """All sums obtainable from a subset of coins (bitset on a Python int).   # Суммы монет.

    When to use:  subset-sum feasibility; the int bitset does the work in C.
    Complexity:   O(n * S / 64), S = total sum
    Returns:      sorted list of positive reachable sums.
    Related:      knapsack_01, bits.
    CSES:         Money Sums (1745).
    Example:
        >>> money_sums([4, 2, 5, 2])
        [2, 4, 5, 6, 7, 8, 9, 11, 13]
    """
    bs = 1  # бит s - сумма s достижима
    for c in coins:
        bs |= bs << c
    s = bin(bs)[:1:-1]  # младшие биты первыми
    return [i for i, ch in enumerate(s) if ch == "1" and i]


@algo(tags=["dp", "intervals", "2d"], cses=["Rectangle Cutting (1744)"])
def rectangle_cutting(a: int, b: int) -> int:
    """Min cuts to split an a x b rectangle into squares.   # Разрезание прямоугольника.

    When to use:  2D DP over sub-rectangles.
    Complexity:   O(a * b * (a + b))
    Returns:      minimal number of cuts.
    Python speed: 200 x 200 ~ 0.2 s; 500 x 500 ~ 6 s in CPython.
    CSES:         Rectangle Cutting (1744).
    Example:
        >>> rectangle_cutting(3, 5)
        3
    """
    dp = [[0] * (b + 1) for _ in range(a + 1)]
    for i in range(1, a + 1):
        for j in range(1, b + 1):
            if i == j:
                continue  # квадрат - разрезов не нужно
            best = 1 << 30  # i != j: хотя бы один разрез возможен
            row = dp[i]
            for k in range(1, j // 2 + 1):  # вертикальный разрез
                v = row[k] + row[j - k]
                if v < best:
                    best = v
            for k in range(1, i // 2 + 1):  # горизонтальный разрез
                v = dp[k][j] + dp[i - k][j]
                if v < best:
                    best = v
            row[j] = best + 1
    return dp[a][b]


@algo(tags=["dp", "intervals", "games"], cses=["Removal Game (1097)"])
def removal_game(a: list[int]) -> int:
    """Optimal score of the first player taking from either end.   # Игра с удалением.

    When to use:  two-player zero-sum games on an array (interval DP).
    Complexity:   O(n^2)
    Returns:      maximal sum the first player can guarantee.
    Idea:         best[l][r] = sum(l..r) - min(best[l+1][r], best[l][r-1]).
    CSES:         Removal Game (1097).
    Example:
        >>> removal_game([4, 5, 1, 3])
        8
    """
    n = len(a)
    pre = [0] * (n + 1)
    for i, x in enumerate(a):
        pre[i + 1] = pre[i] + x
    best = list(a)  # отрезки длины 1
    for length in range(2, n + 1):
        new = []
        for l in range(n - length + 1):
            r = l + length
            s = pre[r] - pre[l]
            new.append(s - min(best[l + 1], best[l]))  # соперник играет оптимально
        best = new
    return best[0] if n else 0


@algo(tags=["dp", "intervals", "scheduling", "binary-search"], cses=["Projects (1140)"])
def weighted_interval_scheduling(jobs: list[tuple[int, int, int]]) -> int:
    """Max total reward of non-overlapping projects [start, end] (inclusive days).   # Проекты.

    When to use:  weighted interval scheduling.
    Complexity:   O(n log n)
    Returns:      maximal total reward.
    Related:      sorting.movie_festival (unweighted).
    CSES:         Projects (1140).
    Example:
        >>> weighted_interval_scheduling([(2, 4, 4), (3, 6, 6), (6, 8, 2), (5, 7, 3)])
        7
    """
    jobs = sorted(jobs, key=lambda j: j[1])
    ends = [e for _, e, _ in jobs]
    dp = [0] * (len(jobs) + 1)  # dp[i] - лучшее среди первых i по концу
    for i, (s, _, p) in enumerate(jobs):
        k = bisect_left(ends, s)  # проекты, закончившиеся строго до s
        dp[i + 1] = max(dp[i], dp[k] + p)
    return dp[-1]


@algo(tags=["dp", "bitmask"], cses=["Elevator Rides (1653)"])
def elevator_rides(weights: list[int], cap: int) -> int:
    """Min rides of an elevator with capacity cap (bitmask DP).   # Поездки на лифте.

    When to use:  bin packing for n <= 20.
    Complexity:   O(2^n * n)
    Returns:      minimal number of rides.
    Python speed: n = 20 ~ 3 s in CPython; n = 16 ~ 0.15 s.
    Idea:         best[mask] = (rides, weight of the last ride), compare lexicographically.
    CSES:         Elevator Rides (1653).
    Example:
        >>> elevator_rides([2, 3, 3, 5, 6], 10)
        2
    """
    n = len(weights)
    best: list[tuple[int, int]] = [(n + 1, 0)] * (1 << n)
    best[0] = (1, 0)
    for mask in range(1, 1 << n):
        b = (n + 1, 0)
        for i in range(n):
            if mask >> i & 1:
                rides, last = best[mask ^ (1 << i)]
                w = weights[i]
                cand = (rides, last + w) if last + w <= cap else (rides + 1, w)  # новая поездка
                if cand < b:
                    b = cand
        best[mask] = b
    return best[-1][0] if n else 0


@algo(
    tags=["dp", "bitmask", "hamiltonian", "counting"],
    cses=["Hamiltonian Flights (1690)"],
    requires=["MOD7"],
)
def hamiltonian_flights(n: int, edges: list[tuple[int, int]], mod: int = MOD7) -> int:
    """Number of routes 0 -> n-1 visiting every city exactly once.   # Гамильтоновы маршруты.

    When to use:  counting Hamiltonian paths, n <= 20.
    Complexity:   O(2^n * m)
    Returns:      count mod mod.
    Python speed: complete graph n = 18 ~ 0.5 s, n = 20 ~ 3 s in CPython.
    Related:      graph.hamiltonian_path.
    CSES:         Hamiltonian Flights (1690).
    Example:
        >>> hamiltonian_flights(4, [(0, 1), (0, 2), (1, 2), (1, 3), (2, 1), (2, 3)])
        2
    """
    radj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        radj[v].append(u)  # входящие рёбра
    full = (1 << n) - 1
    dp = [[0] * n for _ in range(1 << n)]
    dp[1][0] = 1
    last = n - 1
    for mask in range(1, full + 1):
        if not mask & 1:
            continue  # путь всегда начинается в 0
        if mask >> last & 1 and mask != full:
            continue  # n-1 только в самом конце
        row = dp[mask]
        for v in range(1, n):
            if mask >> v & 1:
                prev = dp[mask ^ (1 << v)]
                s = 0
                for u in radj[v]:
                    s += prev[u]
                row[v] = s % mod
    return dp[full][last] % mod


@algo(
    tags=["dp", "profile", "broken-profile", "tilings"],
    cses=["Counting Tilings (2181)"],
    requires=["MOD7"],
)
def counting_tilings(n: int, m: int, mod: int = MOD7) -> int:
    """Domino tilings of an n x m grid (broken profile DP).   # Подсчёт замощений (DP по профилю).

    When to use:  n <= 10, m up to 1000.
    Complexity:   O(n * m * 2^n)
    Returns:      number of tilings mod mod.
    Python speed: n = 10, m = 1000 ~ 0.7 s in CPython (only reachable masks are non-zero).
    Idea:         go cell by cell; bit i of the mask = the cell in row i is already covered
                  by a domino sticking out from the left.
    CSES:         Counting Tilings (2181).
    Example:
        >>> counting_tilings(3, 4), counting_tilings(2, 3)
        (11, 3)
    """
    size = 1 << n
    dp = [0] * size
    dp[0] = 1
    for j in range(m):
        for i in range(n):
            new = [0] * size
            bit = 1 << i
            for mask in range(size):
                v = dp[mask]
                if not v:
                    continue
                if mask & bit:
                    new[mask ^ bit] = (new[mask ^ bit] + v) % mod  # клетка уже занята
                    continue
                if j + 1 < m:
                    new[mask | bit] = (new[mask | bit] + v) % mod  # горизонтальная доминошка
                if i + 1 < n and not mask & (bit << 1):
                    nm = mask | (bit << 1)  # вертикальная: занимаем клетку ниже
                    new[nm] = (new[nm] + v) % mod
            dp = new
    return dp[0] % mod


@algo(tags=["dp", "digit-dp"], cses=["Counting Numbers (2220)"])
def counting_numbers(a: int, b: int) -> int:
    """Numbers in [a, b] without two equal adjacent digits (digit DP).   # Подсчёт чисел (digit DP).

    When to use:  template of digit DP: f(b) - f(a - 1), walk the digits of the bound.
    Complexity:   O(digits * 10)
    Returns:      count of valid numbers in [a, b] (0 counts as valid).
    Related:      mathx.deep_numbers_count (ICPC-UZ 2024 D).
    CSES:         Counting Numbers (2220).
    Example:
        >>> counting_numbers(123, 321)
        171
    """

    def f(x: int) -> int:  # сколько подходящих в [0, x]
        if x < 0:
            return 0
        s = str(x)
        L = len(s)
        total = 1  # число 0
        for length in range(1, L):
            total += 9**length  # все короче: первая 1..9, дальше 9 вариантов
        for i in range(L):
            d = int(s[i])
            prev = int(s[i - 1]) if i else -1
            for c in range(1 if i == 0 else 0, d):  # ставим меньшую цифру на позицию i
                if c != prev:
                    total += 9 ** (L - i - 1)
            if i and d == prev:
                return total  # сам префикс уже некорректен
        return total + 1  # само число x подходит

    return f(b) - f(a - 1)


INF_LINE = 1 << 62  # «нет прямой» в узле Ли Чао


@algo(
    tags=["cht", "li-chao", "lines", "min"],
    cses=["Lines and Queries I (3204)"],
    requires=["INF", "INF_LINE"],
)
class LiChaoTree:
    """Li Chao tree: insert lines y = kx + b, query min at integer x.   # Дерево Ли Чао.

    When to use:  DP of the form dp[i] = min_j (k_j * x_i + b_j) with arbitrary order.
    Complexity:   O(log C) per operation, C = hi - lo; nodes are created lazily
    Methods:      add_line(k, b); query(x) (INF = 1 << 60 if there are no lines)
    Pitfalls:     for maximum insert (-k, -b) and negate the answer.
    Related:      MonotoneCHT, geometry.LiChaoMax.
    CSES:         Lines and Queries I (3204).
    Example:
        >>> t = LiChaoTree(0, 100)
        >>> t.add_line(2, 3); t.add_line(-1, 20)
        >>> t.query(0), t.query(10), t.query(99)
        (3, 10, -79)
    """

    def __init__(self, lo: int, hi: int) -> None:
        self.lo, self.hi = lo, hi
        self.k = [0]
        self.b = [INF_LINE]
        self.left = [-1]
        self.right = [-1]  # узел 0 - корень, дети создаются по требованию

    def _new(self) -> int:
        self.k.append(0)
        self.b.append(INF_LINE)
        self.left.append(-1)
        self.right.append(-1)
        return len(self.k) - 1

    def add_line(self, k: int, b: int) -> None:
        node, lo, hi = 0, self.lo, self.hi
        while True:
            mid = (lo + hi) // 2
            ck, cb = self.k[node], self.b[node]
            if k * mid + b < ck * mid + cb:  # в середине новая прямая лучше - меняем местами
                self.k[node], self.b[node] = k, b
                k, b = ck, cb
            if hi - lo == 1 or b == INF_LINE:
                return
            if k * lo + b < self.k[node] * lo + self.b[node]:
                if self.left[node] == -1:
                    self.left[node] = self._new()
                node, hi = self.left[node], mid
            elif k * (hi - 1) + b < self.k[node] * (hi - 1) + self.b[node]:
                if self.right[node] == -1:
                    self.right[node] = self._new()
                node, lo = self.right[node], mid
            else:
                return  # проигравшая прямая хуже везде на отрезке

    def query(self, x: int) -> int:
        node, lo, hi = 0, self.lo, self.hi
        res = INF
        while node != -1:
            if self.b[node] != INF_LINE:
                res = min(res, self.k[node] * x + self.b[node])
            if hi - lo == 1:
                break
            mid = (lo + hi) // 2
            if x < mid:
                node, hi = self.left[node], mid
            else:
                node, lo = self.right[node], mid
        return res


@algo(tags=["cht", "convex-hull-trick", "lines", "min"], cses=["- (monotone CHT)"])
class MonotoneCHT:
    """Convex hull trick: slopes DECREASE, min queries at any x.   # Монотонный CHT.

    When to use:  dp[i] = min_j (dp[j] + k_j x_i) where k_j decreases with j.
    Complexity:   O(1) amortised add, O(log n) query
    Methods:      add_line(k, b) (k strictly decreasing, equal k: keep the smaller b);
                  query(x) -> min over lines of k * x + b
    Pitfalls:     intersection checks are done with exact integer cross-multiplication.
    Related:      LiChaoTree (any order).
    CSES:         - (monotone CHT)
    Example:
        >>> h = MonotoneCHT()
        >>> for k, b in [(3, 0), (1, 4), (0, 9), (-2, 30)]: h.add_line(k, b)
        >>> [h.query(x) for x in (0, 2, 5, 12)]
        [0, 6, 9, 6]
    """

    def __init__(self) -> None:
        self.ks: list[int] = []
        self.bs: list[int] = []

    def _bad(self, k1: int, b1: int, k2: int, b2: int, k3: int, b3: int) -> bool:
        # средняя прямая не нужна, если пересечение 1 и 3 левее пересечения 1 и 2
        return (b3 - b1) * (k1 - k2) <= (b2 - b1) * (k1 - k3)

    def add_line(self, k: int, b: int) -> None:
        ks, bs = self.ks, self.bs
        if ks and ks[-1] == k:
            if bs[-1] <= b:
                return
            ks.pop()
            bs.pop()
        while len(ks) >= 2 and self._bad(ks[-2], bs[-2], ks[-1], bs[-1], k, b):
            ks.pop()
            bs.pop()
        ks.append(k)
        bs.append(b)

    def query(self, x: int) -> int:
        ks, bs = self.ks, self.bs
        lo, hi = 0, len(ks) - 1
        while lo < hi:  # оптимальная прямая сдвигается вправо с ростом x
            mid = (lo + hi) // 2
            if ks[mid] * x + bs[mid] <= ks[mid + 1] * x + bs[mid + 1]:
                hi = mid
            else:
                lo = mid + 1
        return ks[lo] * x + bs[lo]


@algo(
    tags=["dp", "divide-and-conquer-optimization"],
    cses=["Houses and Schools (3354)"],
    requires=["INF"],
)
def dc_optimization(n: int, k: int, cost: Callable[[int, int], int]) -> int:
    """Split 0..n-1 into k segments minimising sum cost(l, r).   # D&C-оптимизация.

    When to use:  dp[j][i] = min_p dp[j-1][p] + cost(p, i) with monotone optimal p
                  (cost satisfies the quadrangle inequality).
    Complexity:   O(k * n log n) cost evaluations
    Input:        cost(l, r) for the half-open segment [l, r).
    Returns:      minimal total cost (INF if k > n).
    Pitfalls:     iterative (stack of (l, r, optl, optr)) - no recursion depth issues.
    Related:      knuth_optimization, houses_and_schools.
    CSES:         Houses and Schools (3354).
    Example:
        >>> a = [1, 3, 2, 6, 4]
        >>> dc_optimization(5, 2, lambda l, r: (r - l) * sum(a[l:r]))
        38
    """
    prev = [INF] * (n + 1)
    prev[0] = 0
    for _ in range(k):
        cur = [INF] * (n + 1)
        stack = [(1, n, 0, n - 1)]  # считаем cur[i] для i в [lo, hi], оптимум в [optl, optr]
        while stack:
            lo, hi, optl, optr = stack.pop()
            if lo > hi:
                continue
            mid = (lo + hi) // 2
            best, best_p = INF, optl
            for p in range(optl, min(mid - 1, optr) + 1):
                if prev[p] < INF:
                    v = prev[p] + cost(p, mid)
                    if v < best:
                        best, best_p = v, p
            cur[mid] = best
            stack.append((lo, mid - 1, optl, best_p))
            stack.append((mid + 1, hi, best_p, optr))
        prev = cur
    return prev[n]


@algo(
    tags=["dp", "divide-and-conquer-optimization", "median"],
    cses=["Houses and Schools (3354)"],
    requires=["INF", "dc_optimization"],
)
def houses_and_schools(c: list[int], k: int) -> int:
    """Place k schools; minimise sum c_i * distance to the nearest school.   # Дома и школы.

    When to use:  k-median on a line with weights (D&C optimisation).
    Complexity:   O(k n log^2 n)
    Returns:      minimal total walking distance.
    Python speed: n = 3000, k = 3000 is far too slow in CPython; n * k <= ~3 * 10^5.
    Idea:         each school serves a segment; best place = weighted median; segment cost
                  in O(log n) by prefix sums of c_i and i * c_i.
    Related:      dc_optimization.
    CSES:         Houses and Schools (3354).
    Example:
        >>> houses_and_schools([2, 7, 1, 4, 6], 2)  # школы в домах 1 и 4
        7
    """
    n = len(c)
    W = [0] * (n + 1)
    S = [0] * (n + 1)
    for i, x in enumerate(c):
        W[i + 1] = W[i] + x
        S[i + 1] = S[i] + i * x

    def cost(l: int, r: int) -> int:
        total = W[r] - W[l]
        if total == 0:
            return 0
        m = bisect_left(W, W[l] + (total + 1) // 2, l + 1, r + 1) - 1  # взвешенная медиана
        left = m * (W[m] - W[l]) - (S[m] - S[l])
        right = (S[r] - S[m + 1]) - m * (W[r] - W[m + 1])
        return left + right

    return dc_optimization(n, min(k, n), cost)


@algo(
    tags=["dp", "knuth-optimization", "intervals"], cses=["Knuth Division (2088)"], requires=["INF"]
)
def knuth_optimization(w: list[int]) -> int:
    """Min total cost to split an array into single elements.   # Оптимизация Кнута.

    When to use:  a split costs the sum of the part; interval DP
                  dp[i][j] = min_k dp[i][k] + dp[k][j] + sum(i, j) with monotone
                  opt[i][j-1] <= opt[i][j] <= opt[i+1][j] (optimal merge / optimal BST).
    Complexity:   O(n^2)
    Returns:      minimal total cost.
    Python speed: n = 2000 ~ 1.6 s, n = 5000 ~ 10 s in CPython.
    Related:      dc_optimization.
    CSES:         Knuth Division (2088).
    Example:
        >>> knuth_optimization([2, 7, 3, 2, 5])
        43
    """
    n = len(w)
    pre = [0] * (n + 1)
    for i, x in enumerate(w):
        pre[i + 1] = pre[i] + x
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    opt = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n):
        opt[i][i + 1] = i  # отрезок из одного элемента
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length
            best, bk = INF, i + 1
            dpi = dp[i]
            for k in range(max(i + 1, opt[i][j - 1]), min(j - 1, opt[i + 1][j]) + 1):
                v = dpi[k] + dp[k][j]  # кандидаты только между соседними оптимумами
                if v < best:
                    best, bk = v, k
            dp[i][j] = best + pre[j] - pre[i]
            opt[i][j] = bk
    return dp[0][n] if n else 0


@algo(tags=["dp", "coloring", "counting"], icpc=["2023 F"], requires=["MOD"], verified=False)
def fence_painting(colors: list[int], k: int, mod: int = MOD) -> int:
    """Colour the zeros with 1..k so that neighbours always differ.   # Покраска забора.

    When to use:  "some planks are already painted, adjacent planks must differ".
    Complexity:   O(n)
    Input:        colors[i] = 0 (free) or a fixed colour 1..k.
    Returns:      number of colourings mod mod (0 if two fixed neighbours are equal).
    Idea:         split by fixed planks; a gap of L zeros between colours x and y is a walk of
                  L + 1 steps on the complete graph K_k: same(t + 1) = (k - 1) diff(t),
                  diff(t + 1) = same(t) + (k - 2) diff(t); ends of the fence give (k - 1)^L,
                  an all-zero fence k (k - 1)^(n - 1).
    ICPC-UZ:      2023 F "Fence Painting" (exact statement NOT VERIFIED).
    Example:
        >>> fence_painting([1, 0, 0, 2], 3), fence_painting([0, 0, 0], 2)
        (3, 2)
    """
    # NOT VERIFIED: формулы сверены перебором, условие 2023 F не сверено
    n = len(colors)
    fixed = [i for i, c in enumerate(colors) if c]
    if not fixed:
        return k * pow(k - 1, n - 1, mod) % mod if n else 1 % mod
    res = pow(k - 1, fixed[0], mod) * pow(k - 1, n - 1 - fixed[-1], mod) % mod  # края
    for a, b in zip(fixed, fixed[1:]):
        steps = b - a  # шагов по полному графу между цветами
        same, diff = 1, 0  # за 0 шагов: в той же вершине
        for _ in range(steps):
            same, diff = (k - 1) * diff % mod, (same + (k - 2) * diff) % mod
        res = res * (same if colors[a] == colors[b] else diff) % mod
    return res
