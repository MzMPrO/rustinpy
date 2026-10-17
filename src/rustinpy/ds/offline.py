"""Classic CSES range-query problems solved with Fenwick / segment trees / lifting.

Классические задачи на запросы. Позиции 0-based, отрезки [l, r).
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right

from rustinpy._registry import algo

INF = 1 << 60


@algo(tags=["segment-tree", "descend", "first-fit"], cses=["Hotel Queries (1143)"])
def hotel_queries(h: list[int], groups: list[int]) -> list[int]:
    """Each group takes the first hotel with enough free rooms.   # Первый подходящий отель.

    When to use:  "first position with value >= x" + decrease it (segment tree descend).
    Complexity:   O((n + m) log n)
    Returns:      0-based hotel index for each group, or -1 (CSES prints index + 1 or 0).
    Related:      SegTree.max_right.
    CSES:         Hotel Queries (1143).
    Example:
        >>> hotel_queries([3, 2, 4, 1, 5, 5, 2, 6], [4, 4, 7, 1, 1])
        [2, 4, -1, 0, 0]
    """
    n = len(h)
    size = 1
    while size < n:
        size <<= 1
    t = [0] * (2 * size)  # максимум свободных комнат в узле
    t[size : size + n] = h
    for i in range(size - 1, 0, -1):
        t[i] = max(t[2 * i], t[2 * i + 1])
    res = []
    for g in groups:
        if t[1] < g:
            res.append(-1)
            continue
        k = 1
        while k < size:  # спуск: левый сын, если там хватает места
            k = 2 * k if t[2 * k] >= g else 2 * k + 1
        res.append(k - size)
        t[k] -= g
        k >>= 1
        while k:
            t[k] = max(t[2 * k], t[2 * k + 1])
            k >>= 1
    return res


@algo(tags=["fenwick", "kth", "order-statistics"], cses=["List Removals (1749)"])
def list_removals(a: list[int], positions: list[int]) -> list[int]:
    """Remove elements by their CURRENT position; report removed values.   # Удаление по позиции.

    When to use:  "delete the k-th element of the current list" many times.
    Complexity:   O(n log n)
    Input:        positions are 0-based in the current list (CSES: subtract 1).
    Returns:      removed values in order.
    Related:      Fenwick.kth, SortedList.
    CSES:         List Removals (1749).
    Example:
        >>> list_removals([2, 6, 1, 4, 2], [2, 1, 2, 0, 0])
        [1, 6, 2, 2, 4]
    """
    n = len(a)
    t = [0] * (n + 1)
    for i in range(1, n + 1):  # Фенвик из единиц за O(n)
        t[i] += 1
        j = i + (i & -i)
        if j <= n:
            t[j] += t[i]
    LOG = 1 << n.bit_length()
    res = []
    for k in positions:
        pos, step = 0, LOG
        while step:  # k-я живая позиция спуском по Фенвику
            nxt = pos + step
            if nxt <= n and t[nxt] <= k:
                pos = nxt
                k -= t[nxt]
            step >>= 1
        res.append(a[pos])
        i = pos + 1
        while i <= n:
            t[i] -= 1
            i += i & -i
    return res


@algo(tags=["fenwick", "offline", "compression"], cses=["Salary Queries (1144)"])
def salary_queries(p: list[int], ops: list[tuple[str, int, int]]) -> list[int]:
    """Point changes of salaries + count of salaries in [a, b].   # Запросы о зарплатах.

    When to use:  counts in a value range with updates: offline coordinate compression + BIT.
    Complexity:   O((n + q) log(n + q))
    Input:        ops ("!", k, x): p[k] = x (0-based k); ("?", a, b): count with a <= p_i <= b.
    Returns:      answers to "?" in order.
    Related:      Fenwick, SortedList.
    CSES:         Salary Queries (1144).
    Example:
        >>> salary_queries([3, 7, 2, 2, 5], [("?", 2, 3), ("!", 2, 6), ("?", 2, 3)])
        [3, 2]
    """
    vals = set(p)
    for op, _, y in ops:
        if op == "!":
            vals.add(y)  # все значения заранее - для сжатия
    comp = sorted(vals)
    m = len(comp)
    t = [0] * (m + 1)

    def add(i: int, d: int) -> None:
        i += 1
        while i <= m:
            t[i] += d
            i += i & -i

    def pref(i: int) -> int:  # сколько зарплат с индексом значения < i
        s = 0
        while i > 0:
            s += t[i]
            i -= i & -i
        return s

    cur = list(p)
    for x in cur:
        add(bisect_left(comp, x), 1)
    res = []
    for op, x, y in ops:
        if op == "!":
            add(bisect_left(comp, cur[x]), -1)
            cur[x] = y
            add(bisect_left(comp, y), 1)
        else:
            res.append(pref(bisect_right(comp, y)) - pref(bisect_left(comp, x)))
    return res


@algo(tags=["segment-tree", "abs-trick"], cses=["Pizzeria Queries (2206)"], requires=["INF"])
def pizzeria_queries(p: list[int], ops: list[tuple[str, int, int]]) -> list[int]:
    """min_i (p_i + |i - k|) with point updates.   # Ближайшая дешёвая пиццерия.

    When to use:  minimise value + distance: split |i - k| into two linear cases.
    Complexity:   O((n + q) log n)
    Input:        ops ("!", k, x): p[k] = x; ("?", k, 0): query for building k (0-based,
                  the third number is ignored).
    Returns:      answers to "?" in order.
    Idea:         i <= k: (p_i - i) + k; i >= k: (p_i + i) - k -> two min segment trees.
    Related:      SegTree.
    CSES:         Pizzeria Queries (2206).
    Example:
        >>> pizzeria_queries([6, 8, 5, 7, 4], [("?", 1, 0), ("!", 0, 1), ("?", 2, 0)])
        [6, 3]
    """
    n = len(p)
    size = 1
    while size < n:
        size <<= 1
    lo = [INF] * (2 * size)  # p_i - i
    hi = [INF] * (2 * size)  # p_i + i
    for i, x in enumerate(p):
        lo[size + i] = x - i
        hi[size + i] = x + i
    for i in range(size - 1, 0, -1):
        lo[i] = min(lo[2 * i], lo[2 * i + 1])
        hi[i] = min(hi[2 * i], hi[2 * i + 1])

    def query(t: list[int], l: int, r: int) -> int:
        res = INF
        l += size
        r += size
        while l < r:
            if l & 1:
                res = min(res, t[l])
                l += 1
            if r & 1:
                r -= 1
                res = min(res, t[r])
            l >>= 1
            r >>= 1
        return res

    out = []
    for op, k, x in ops:
        if op == "!":
            i = size + k
            lo[i], hi[i] = x - k, x + k  # обновляем оба дерева
            i >>= 1
            while i:
                lo[i] = min(lo[2 * i], lo[2 * i + 1])
                hi[i] = min(hi[2 * i], hi[2 * i + 1])
                i >>= 1
        else:
            # левее k: p_i - i + k; правее k: p_i + i - k
            out.append(min(query(lo, 0, k + 1) + k, query(hi, k, n) - k))
    return out


@algo(tags=["fenwick", "offline", "distinct"], cses=["Distinct Values Queries (1734)"])
def distinct_values_queries(a: list[int], queries: list[tuple[int, int]]) -> list[int]:
    """Number of distinct values in a[l:r], offline by right end.   # Различные значения на отрезке.

    When to use:  static array, many distinct-count queries (faster than Mo in Python).
    Complexity:   O((n + q) log n)
    Returns:      answers in query order.
    Idea:         sweep r; keep 1 only at the LAST occurrence of each value; answer =
                  ones in [l, r).
    Related:      mo_distinct_count, Fenwick.
    CSES:         Distinct Values Queries (1734).
    Example:
        >>> distinct_values_queries([3, 2, 3, 1, 2], [(0, 3), (1, 5), (2, 3)])
        [2, 3, 1]
    """
    n = len(a)
    t = [0] * (n + 1)

    def add(i: int, d: int) -> None:
        i += 1
        while i <= n:
            t[i] += d
            i += i & -i

    def pref(i: int) -> int:
        s = 0
        while i > 0:
            s += t[i]
            i -= i & -i
        return s

    by_r: list[list[int]] = [[] for _ in range(n + 1)]
    for qi, (_, r) in enumerate(queries):
        by_r[r].append(qi)
    last: dict[int, int] = {}
    res = [0] * len(queries)
    for qi in by_r[0]:
        res[qi] = 0
    for i, x in enumerate(a):
        if x in last:
            add(last[x], -1)  # старое вхождение больше не последнее
        last[x] = i
        add(i, 1)
        for qi in by_r[i + 1]:
            res[qi] = pref(i + 1) - pref(queries[qi][0])
    return res


@algo(tags=["binary-lifting", "greedy", "intervals"], cses=["Movie Festival Queries (1664)"])
def movie_festival_queries(
    movies: list[tuple[int, int]], queries: list[tuple[int, int]]
) -> list[int]:
    """Max number of non-overlapping movies inside [a, b].   # Сколько фильмов успеть за [a, b].

    When to use:  greedy "earliest end" applied many times -> binary lifting over time.
    Complexity:   O((n + q + T) log T), T = number of distinct time points
    Input:        movie (s, e) occupies [s, e); query (a, b): movies with a <= s and e <= b.
    Returns:      answers in query order.
    Idea:         nxt[t] = smallest end among movies starting at >= t; jump greedily with
                  up[k][t] = nxt applied 2^k times.
    Related:      sorting.movie_festival (one query).
    CSES:         Movie Festival Queries (1664).
    Example:
        >>> movies = [(2, 5), (6, 10), (4, 7), (9, 10)]
        >>> movie_festival_queries(movies, [(1, 10), (2, 9), (5, 9)])
        [2, 1, 0]
    """
    times = sorted({t for m in movies for t in m} | {t for q in queries for t in q})
    idx = {t: i for i, t in enumerate(times)}
    T = len(times)
    nxt = [T] * (T + 1)  # T = «нельзя»
    for s, e in movies:
        i = idx[s]
        nxt[i] = min(nxt[i], idx[e])
    for i in range(T - 1, -1, -1):  # суффиксный минимум: старт не раньше t
        nxt[i] = min(nxt[i], nxt[i + 1])
    up = [nxt]
    while (1 << len(up)) <= len(movies):
        prev = up[-1]
        up.append([prev[prev[i]] for i in range(T + 1)])
    res = []
    for a, b in queries:
        cur, cnt, lim = idx[a], 0, idx[b]
        for k in range(len(up) - 1, -1, -1):
            if up[k][cur] <= lim:  # прыжок на 2^k фильмов помещается
                cur = up[k][cur]
                cnt += 1 << k
        res.append(cnt)
    return res


@algo(tags=["sparse-table", "greedy", "powers-of-two"], cses=["Missing Coin Sum Queries (2184)"])
def missing_coin_sum_queries(a: list[int], queries: list[tuple[int, int]]) -> list[int]:
    """Smallest sum that coins a[l:r] cannot form.   # Наименьшая непредставимая сумма на отрезке.

    When to use:  missing coin sum on many subarrays.
    Complexity:   O(n log n + q * 30 * log n)
    Returns:      answers in query order.
    Idea:         group coins by bit length k (values in [2^k, 2^(k+1))). With reachable
                  1..s, if s + 1 >= 2^k and the minimum coin of group k is <= s + 1, the
                  whole group can be added; otherwise s + 1 is the answer.
    Related:      sorting.missing_coin_sum (one array).
    CSES:         Missing Coin Sum Queries (2184).
    Example:
        >>> missing_coin_sum_queries([2, 9, 1, 2, 7], [(1, 3), (0, 5), (2, 4)])
        [2, 6, 4]
    """
    groups = max(x.bit_length() for x in a) if a else 0
    pos: list[list[int]] = [[] for _ in range(groups)]  # позиции монет группы
    pre: list[list[int]] = [[0] for _ in range(groups)]  # префиксные суммы группы
    for i, x in enumerate(a):
        g = x.bit_length() - 1
        pos[g].append(i)
        pre[g].append(pre[g][-1] + x)
    # разреженные таблицы минимумов внутри каждой группы
    sparse: list[list[list[int]]] = []
    for g in range(groups):
        vals = [a[i] for i in pos[g]]
        tab = [vals]
        k = 1
        while 2 * k <= len(vals):
            prev = tab[-1]
            tab.append(list(map(min, prev[: len(vals) - 2 * k + 1], prev[k : len(vals) - k + 1])))
            k *= 2
        sparse.append(tab)
    res = []
    for l, r in queries:
        s = 0
        for g in range(groups):
            i = bisect_left(pos[g], l)
            j = bisect_left(pos[g], r)
            if i == j:
                continue  # монет этой группы на отрезке нет
            if s + 1 < (1 << g):
                break
            k = (j - i).bit_length() - 1
            row = sparse[g][k]
            mn = min(row[i], row[j - (1 << k)])  # минимальная монета группы на отрезке
            if mn > s + 1:
                break
            s += pre[g][j] - pre[g][i]
        res.append(s + 1)
    return res
