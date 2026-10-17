"""Fenwick trees (binary indexed trees).

Деревья Фенвика. Индексы 0-based, отрезки полуоткрытые [l, r).
"""

from __future__ import annotations

from rustinpy._registry import algo


@algo(
    tags=["fenwick", "bit", "range-sum", "kth"],
    cses=["Dynamic Range Sum Queries (1648)", "List Removals (1749)"],
)
class Fenwick:
    """Fenwick tree: point add, prefix sum, k-th by prefix.   # Дерево Фенвика.

    When to use:  point updates + range sums; order statistics over counts (kth).
    Complexity:   O(n) build, O(log n) per operation
    Input:        Fenwick(n) for zeros or Fenwick(list) for initial values.
    Methods:      add(i, d); prefix(i) = sum a[0:i]; range_sum(l, r) = sum a[l:r];
                  kth(k) = smallest i with sum a[0:i+1] > k (values must be >= 0)
    Pitfalls:     kth is 0-based: kth(0) is the first element of the multiset.   # k с нуля
    Related:      FenwickRangeAdd, FenwickRangeRange, Fenwick2D, SegTree.
    CSES:         Dynamic Range Sum Queries (1648), List Removals (1749), Josephus Problem II.
    Example:
        >>> f = Fenwick([1, 0, 1, 1, 0])
        >>> f.range_sum(1, 4), f.kth(0), f.kth(2)
        (2, 0, 3)
        >>> f.add(1, 5); f.prefix(2)
        6
    """

    def __init__(self, n_or_values: int | list[int]) -> None:
        if isinstance(n_or_values, int):
            self.n = n_or_values
            self.t = [0] * (self.n + 1)
        else:
            self.n = len(n_or_values)
            t = [0, *n_or_values]
            for i in range(1, self.n + 1):  # построение за O(n)
                j = i + (i & -i)
                if j <= self.n:
                    t[j] += t[i]
            self.t = t

    def add(self, i: int, d: int) -> None:
        t, n = self.t, self.n
        i += 1
        while i <= n:
            t[i] += d
            i += i & -i  # к следующему отвечающему узлу

    def prefix(self, i: int) -> int:
        t, s = self.t, 0
        while i > 0:
            s += t[i]
            i -= i & -i  # снимаем младший бит
        return s

    def range_sum(self, l: int, r: int) -> int:
        return self.prefix(r) - self.prefix(l)

    def kth(self, k: int) -> int:
        t, pos = self.t, 0
        step = 1 << self.n.bit_length()
        while step:
            nxt = pos + step
            if nxt <= self.n and t[nxt] <= k:  # спуск по степеням двойки
                pos = nxt
                k -= t[nxt]
            step >>= 1
        return pos


@algo(tags=["fenwick", "bit", "range-update"], cses=["Range Update Queries (1651)"])
class FenwickRangeAdd:
    """Fenwick on differences: range add, point query.   # Прибавление на отрезке, значение в точке.

    When to use:  "add x on [l, r)" and "what is a[i]".
    Complexity:   O(log n) per operation
    Methods:      range_add(l, r, d); point(i) -> a[i]
    Related:      Fenwick, FenwickRangeRange.
    CSES:         Range Update Queries (1651).
    Example:
        >>> f = FenwickRangeAdd([3, 2, 4])
        >>> f.range_add(0, 2, 10); [f.point(i) for i in range(3)]
        [13, 12, 4]
    """

    def __init__(self, values: int | list[int]) -> None:
        a = [0] * values if isinstance(values, int) else values
        self.n = len(a)
        self.t = [0] * (self.n + 1)
        prev = 0
        for i, x in enumerate(a):
            self._add(i, x - prev)  # массив разностей
            prev = x

    def _add(self, i: int, d: int) -> None:
        i += 1
        while i <= self.n:
            self.t[i] += d
            i += i & -i

    def range_add(self, l: int, r: int, d: int) -> None:
        self._add(l, d)
        if r < self.n:
            self._add(r, -d)

    def point(self, i: int) -> int:
        s = 0
        i += 1
        while i > 0:  # a[i] = сумма разностей до i
            s += self.t[i]
            i -= i & -i
        return s


@algo(tags=["fenwick", "bit", "range-update", "range-sum"], cses=["- (range add + range sum)"])
class FenwickRangeRange:
    """Two Fenwicks: range add AND range sum.   # Прибавление и сумма на отрезке.

    When to use:  lazy segment tree is too slow / too long to write; add + sum only.
    Complexity:   O(log n) per operation
    Methods:      range_add(l, r, d); range_sum(l, r)
    Idea:         prefix(i) = B1(i) * i - B2(i) with B1 on d, B2 on d * position.
    Related:      FenwickRangeAdd, LazySegAddSum.
    CSES:         - (range add + range sum)
    Example:
        >>> f = FenwickRangeRange(5)
        >>> f.range_add(1, 4, 2); f.range_add(0, 2, 1)
        >>> f.range_sum(0, 5), f.range_sum(1, 2)
        (8, 3)
    """

    def __init__(self, n: int) -> None:
        self.n = n
        self.b1 = [0] * (n + 1)
        self.b2 = [0] * (n + 1)

    def _add(self, i: int, d: int) -> None:
        di = d * i
        b1, b2 = self.b1, self.b2
        i += 1
        while i <= self.n:
            b1[i] += d
            b2[i] += di
            i += i & -i

    def range_add(self, l: int, r: int, d: int) -> None:
        self._add(l, d)
        if r < self.n:
            self._add(r, -d)

    def _prefix(self, i: int) -> int:  # сумма a[0:i]
        s1 = s2 = 0
        j = i
        while j > 0:
            s1 += self.b1[j]
            s2 += self.b2[j]
            j -= j & -j
        return s1 * i - s2

    def range_sum(self, l: int, r: int) -> int:
        return self._prefix(r) - self._prefix(l)


@algo(tags=["fenwick", "bit", "2d"], cses=["Forest Queries II (1739)"])
class Fenwick2D:
    """2D Fenwick: point add, rectangle sum.   # Двумерное дерево Фенвика.

    When to use:  grid with point updates and rectangle sums, R * C <= ~10^6.
    Complexity:   O(log R * log C) per operation
    Methods:      add(r, c, d); query(r1, c1, r2, c2) = sum over r1 <= r < r2, c1 <= c < c2
    Related:      PrefixSum2D (static), Fenwick.
    CSES:         Forest Queries II (1739).
    Example:
        >>> f = Fenwick2D(3, 3)
        >>> f.add(0, 0, 1); f.add(2, 2, 5); f.add(1, 2, 2)
        >>> f.query(0, 0, 3, 3), f.query(1, 1, 3, 3)
        (8, 7)
    """

    def __init__(self, R: int, C: int) -> None:
        self.R, self.C = R, C
        self.t = [[0] * (C + 1) for _ in range(R + 1)]

    def add(self, r: int, c: int, d: int) -> None:
        i = r + 1
        while i <= self.R:
            row = self.t[i]
            j = c + 1
            while j <= self.C:
                row[j] += d
                j += j & -j
            i += i & -i

    def _prefix(self, r: int, c: int) -> int:  # сумма прямоугольника [0, r) x [0, c)
        s = 0
        i = r
        while i > 0:
            row = self.t[i]
            j = c
            while j > 0:
                s += row[j]
                j -= j & -j
            i -= i & -i
        return s

    def query(self, r1: int, c1: int, r2: int, c2: int) -> int:
        p = self._prefix
        return p(r2, c2) - p(r1, c2) - p(r2, c1) + p(r1, c1)
