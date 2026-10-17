"""Mo's algorithm (with and without updates) and sqrt decomposition.

Алгоритм Мо и корневая декомпозиция. Отрезки [l, r).
"""

from __future__ import annotations

from math import isqrt

from rustinpy._registry import algo


@algo(tags=["mo", "offline", "sqrt"], cses=["Distinct Values Queries (1734)"])
def mo_order(queries: list[tuple[int, int]], block: int | None = None) -> list[int]:
    """Order of offline range queries for Mo's algorithm.   # Порядок запросов для Мо.

    When to use:  add/remove of one element is cheap, but no fast merge of ranges.
    Complexity:   O(q log q) sorting; total pointer moves O((n + q) sqrt n)
    Input:        queries (l, r) half-open; block defaults to max(1, n / sqrt(q)).
    Returns:      permutation of query indices to process in.
    Pitfalls:     "odd-even" trick: alternate r direction between blocks (~2x faster).
    Related:      mo_distinct_count (full example), mo_with_updates.
    CSES:         Distinct Values Queries (1734) (offline BIT is faster in Python).
    Example:
        >>> mo_order([(0, 5), (1, 2), (0, 2), (3, 4)], block=2)
        [1, 2, 0, 3]
    """
    if not queries:
        return []
    n = max(r for _, r in queries)
    if block is None:
        block = max(1, int(n / max(1, isqrt(len(queries)))))
    b = block

    def key(i: int) -> tuple[int, int]:
        l, r = queries[i]
        blk = l // b
        return (blk, r if blk % 2 == 0 else -r)  # змейка по r

    return sorted(range(len(queries)), key=key)


@algo(
    tags=["mo", "offline", "distinct"],
    cses=["Distinct Values Queries (1734)"],
    requires=["mo_order"],
)
def mo_distinct_count(a: list[int], queries: list[tuple[int, int]]) -> list[int]:
    """Number of distinct values in a[l:r] with Mo's algorithm.   # Различные значения (Мо).

    When to use:  template of Mo: copy and change add/remove for your statistic.
    Complexity:   O((n + q) sqrt n)
    Returns:      answers in query order.
    Python speed: n = q = 2 * 10^5 is ~10 s in CPython -> use distinct_values_queries.
    Related:      mo_order, distinct_values_queries (offline BIT, O(n log n)).
    CSES:         Distinct Values Queries (1734).
    Example:
        >>> mo_distinct_count([3, 2, 3, 1, 2], [(0, 3), (1, 5), (2, 3)])
        [2, 3, 1]
    """
    comp = {v: i for i, v in enumerate(sorted(set(a)))}
    b = [comp[x] for x in a]
    cnt = [0] * len(comp)
    res = [0] * len(queries)
    cur_l = cur_r = distinct = 0
    for qi in mo_order(queries):
        l, r = queries[qi]
        while cur_r < r:  # расширяем вправо
            v = b[cur_r]
            cnt[v] += 1
            if cnt[v] == 1:
                distinct += 1
            cur_r += 1
        while cur_l > l:  # расширяем влево
            cur_l -= 1
            v = b[cur_l]
            cnt[v] += 1
            if cnt[v] == 1:
                distinct += 1
        while cur_r > r:  # сжимаем справа
            cur_r -= 1
            v = b[cur_r]
            cnt[v] -= 1
            if cnt[v] == 0:
                distinct -= 1
        while cur_l < l:  # сжимаем слева
            v = b[cur_l]
            cnt[v] -= 1
            if cnt[v] == 0:
                distinct -= 1
            cur_l += 1
        res[qi] = distinct
    return res


@algo(tags=["mo", "offline", "updates"], cses=["- (distinct values with point updates)"])
def mo_with_updates(a: list[int], ops: list[tuple[str, int, int]]) -> list[int]:
    """Mo's algorithm with point updates: distinct values in a[l:r].   # Мо с изменениями.

    When to use:  offline range queries mixed with point assignments.
    Complexity:   O(n^(5/3)) with block = n^(2/3)
    Input:        ops in time order: ("?", l, r) query on [l, r) or ("!", i, x) set a[i] = x.
    Returns:      answers to "?" in order.
    Python speed: only for n, q <= ~3 * 10^4 in CPython.
    Related:      mo_distinct_count.
    CSES:         - (distinct values with point updates)
    Example:
        >>> mo_with_updates([1, 2, 1], [("?", 0, 3), ("!", 2, 3), ("?", 0, 3), ("?", 2, 3)])
        [2, 3, 1]
    """
    arr = list(a)
    updates: list[tuple[int, int, int]] = []  # (позиция, старое, новое)
    queries: list[tuple[int, int, int, int]] = []  # (l, r, время, номер)
    for op, x, y in ops:
        if op == "!":
            updates.append((x, arr[x], y))
            arr[x] = y
        else:
            queries.append((x, y, len(updates), len(queries)))
    n = max(1, len(a))
    block = max(1, round(n ** (2 / 3)))
    queries.sort(key=lambda q: (q[0] // block, q[1] // block, q[2]))
    cur = list(a)
    cnt: dict[int, int] = {}
    distinct = 0
    cl = cr = t = 0
    res = [0] * len(queries)

    def add(v: int) -> int:
        c = cnt.get(v, 0)
        cnt[v] = c + 1
        return 1 if c == 0 else 0

    def remove(v: int) -> int:
        c = cnt[v] - 1
        cnt[v] = c
        return -1 if c == 0 else 0

    for l, r, tq, qi in queries:
        while t < tq:  # применяем изменения
            pos, _, new = updates[t]
            if cl <= pos < cr:
                distinct += remove(cur[pos]) + add(new)
            cur[pos] = new
            t += 1
        while t > tq:  # откатываем изменения
            t -= 1
            pos, old, _ = updates[t]
            if cl <= pos < cr:
                distinct += remove(cur[pos]) + add(old)
            cur[pos] = old
        while cr < r:
            distinct += add(cur[cr])
            cr += 1
        while cl > l:
            cl -= 1
            distinct += add(cur[cl])
        while cr > r:
            cr -= 1
            distinct += remove(cur[cr])
        while cl < l:
            distinct += remove(cur[cl])
            cl += 1
        res[qi] = distinct
    return res


@algo(tags=["sqrt", "decomposition", "range-sum"], cses=["- (sqrt decomposition template)"])
class SqrtDecomposition:
    """Blocks of size ~sqrt(n): point set + range sum.   # Корневая декомпозиция.

    When to use:  template when a segment tree is awkward (e.g. custom block statistics).
    Complexity:   O(1) set, O(sqrt n) query
    Methods:      set(i, v); range_sum(l, r)
    Related:      Fenwick, SegTree.
    CSES:         - (sqrt decomposition template)
    Example:
        >>> sd = SqrtDecomposition([1, 2, 3, 4, 5, 6, 7])
        >>> sd.range_sum(1, 6)
        20
        >>> sd.set(3, 0); sd.range_sum(0, 7)
        24
    """

    def __init__(self, a: list[int]) -> None:
        self.a = list(a)
        self.b = max(1, isqrt(len(a)))
        self.sums = [0] * (len(a) // self.b + 1)
        for i, x in enumerate(a):
            self.sums[i // self.b] += x  # сумма блока

    def set(self, i: int, v: int) -> None:
        self.sums[i // self.b] += v - self.a[i]
        self.a[i] = v

    def range_sum(self, l: int, r: int) -> int:
        a, b, s = self.a, self.b, 0
        while l < r and l % b:  # хвост слева
            s += a[l]
            l += 1
        while l + b <= r:  # целые блоки
            s += self.sums[l // b]
            l += b
        while l < r:  # хвост справа
            s += a[l]
            l += 1
        return s
