"""Segment trees without lazy propagation (iterative, bottom-up).

Деревья отрезков без отложенных операций. Отрезки полуоткрытые [l, r).
"""

from __future__ import annotations

from typing import Callable, Generic, TypeVar

from rustinpy._registry import algo

T = TypeVar("T")


@algo(
    tags=["segment-tree", "range-query", "binary-search"],
    cses=["Dynamic Range Minimum Queries (1649)", "Hotel Queries (1143)"],
    requires=["T"],
)
class SegTree(Generic[T]):
    """Iterative segment tree for any monoid (op associative, e identity).   # Дерево отрезков.

    When to use:  point update + range query: sum, min, max, gcd, xor, matrices...
    Complexity:   O(n) build, O(log n) per operation
    Methods:      set(i, v); get(i); query(l, r) = op over a[l:r]; all();
                  max_right(l, f): largest r with f(op(a[l:r])) True (f(e) must be True);
                  min_left(r, f): smallest l with f(op(a[l:r])) True
    Pitfalls:     op is called in order (left, right): fine for non-commutative ops.
    Python speed: ~7 us per operation (op is a Python call): 4 * 10^5 ops ~ 3 s; for sums
                  Fenwick is 2x faster; inline the op for hot loops.
    Related:      LazySegAddSum (range updates), SparseTable (static), Fenwick (sums).
    CSES:         Dynamic Range Minimum Queries (1649), Hotel Queries (1143).
    Example:
        >>> st = SegTree([5, 3, 7, 1], min, 1 << 60)
        >>> st.query(0, 3), st.query(1, 4)
        (3, 1)
        >>> st.set(3, 10); st.all()
        3
        >>> sums = SegTree([2, 1, 4, 3], lambda a, b: a + b, 0)
        >>> sums.max_right(0, lambda s: s <= 6)  # longest prefix with sum <= 6
        2
    """

    def __init__(self, data: list[T], op: Callable[[T, T], T], e: T) -> None:
        n = len(data)
        size = 1
        while size < n:
            size <<= 1
        self.n, self.size, self.op, self.e = n, size, op, e
        d = [e] * (2 * size)
        d[size : size + n] = data  # листья
        for i in range(size - 1, 0, -1):
            d[i] = op(d[2 * i], d[2 * i + 1])
        self.d = d

    def set(self, i: int, v: T) -> None:
        d, op = self.d, self.op
        i += self.size
        d[i] = v
        i >>= 1
        while i:  # пересчёт предков
            d[i] = op(d[2 * i], d[2 * i + 1])
            i >>= 1

    def get(self, i: int) -> T:
        return self.d[i + self.size]

    def query(self, l: int, r: int) -> T:
        d, op = self.d, self.op
        sl = sr = self.e
        l += self.size
        r += self.size
        while l < r:
            if l & 1:
                sl = op(sl, d[l])
                l += 1
            if r & 1:
                r -= 1
                sr = op(d[r], sr)  # правую часть копим справа: порядок важен
            l >>= 1
            r >>= 1
        return op(sl, sr)

    def all(self) -> T:
        return self.d[1]

    def max_right(self, l: int, f: Callable[[T], bool]) -> int:
        if l == self.n:
            return self.n
        d, op, size = self.d, self.op, self.size
        l += size
        sm = self.e
        while True:
            while l % 2 == 0:
                l >>= 1
            if not f(op(sm, d[l])):
                while l < size:  # спускаемся к первому «плохому» листу
                    l *= 2
                    if f(op(sm, d[l])):
                        sm = op(sm, d[l])
                        l += 1
                return l - size
            sm = op(sm, d[l])
            l += 1
            if (l & -l) == l:
                return self.n

    def min_left(self, r: int, f: Callable[[T], bool]) -> int:
        if r == 0:
            return 0
        d, op, size = self.d, self.op, self.size
        r += size
        sm = self.e
        while True:
            r -= 1
            while r > 1 and r % 2:
                r >>= 1
            if not f(op(d[r], sm)):
                while r < size:
                    r = 2 * r + 1
                    if f(op(d[r], sm)):
                        sm = op(d[r], sm)
                        r -= 1
                return r + 1 - size
            sm = op(d[r], sm)
            if (r & -r) == r:
                return 0


@algo(tags=["segment-tree", "max-subarray", "merge-nodes"], cses=["Subarray Sum Queries (1190)"])
class SegTreeMaxSubarray:
    """Point set + maximum subarray sum on a range (node merge).   # Максимальная подсумма.

    When to use:  "change a[i]" + "best subarray sum in [l, r)".
    Complexity:   O(log n) per operation
    Methods:      set(i, v); query(l, r) -> best NON-EMPTY subarray sum of a[l:r]; best()
    Pitfalls:     CSES allows the empty subarray -> print max(0, best()).   # пустой отрезок
    Idea:         node = (sum, best prefix, best suffix, best); merge(L, R):
                  best = max(L.best, R.best, L.suf + R.pref).
    Related:      SegTreeMaxPrefix, SegTree.
    CSES:         Subarray Sum Queries (1190).
    Example:
        >>> st = SegTreeMaxSubarray([-1, 2, -1, 3, -5])
        >>> st.best(), st.query(2, 5)
        (4, 3)
        >>> st.set(4, 6); st.best()
        10
    """

    def __init__(self, a: list[int]) -> None:
        n = len(a)
        size = 1
        while size < n:
            size <<= 1
        self.n, self.size = n, size
        self.d: list[tuple[int, int, int, int] | None] = [None] * (2 * size)
        for i, x in enumerate(a):
            self.d[size + i] = (x, x, x, x)
        for i in range(size - 1, 0, -1):
            self.d[i] = self._merge(self.d[2 * i], self.d[2 * i + 1])

    @staticmethod
    def _merge(
        a: tuple[int, int, int, int] | None, b: tuple[int, int, int, int] | None
    ) -> tuple[int, int, int, int] | None:
        if a is None:
            return b
        if b is None:
            return a
        s1, p1, x1, b1 = a
        s2, p2, x2, b2 = b
        # (сумма, лучший префикс, лучший суффикс, лучший отрезок)
        return (s1 + s2, max(p1, s1 + p2), max(x2, x1 + s2), max(b1, b2, x1 + p2))

    def set(self, i: int, v: int) -> None:
        i += self.size
        self.d[i] = (v, v, v, v)
        i >>= 1
        while i:
            self.d[i] = self._merge(self.d[2 * i], self.d[2 * i + 1])
            i >>= 1

    def query(self, l: int, r: int) -> int:
        left: tuple[int, int, int, int] | None = None
        right: tuple[int, int, int, int] | None = None
        l += self.size
        r += self.size
        while l < r:
            if l & 1:
                left = self._merge(left, self.d[l])
                l += 1
            if r & 1:
                r -= 1
                right = self._merge(self.d[r], right)
            l >>= 1
            r >>= 1
        res = self._merge(left, right)
        if res is None:
            raise ValueError("empty range")
        return res[3]

    def best(self) -> int:
        return self.query(0, self.n)


@algo(tags=["segment-tree", "prefix-sums", "merge-nodes"], cses=["Prefix Sum Queries (2166)"])
class SegTreeMaxPrefix:
    """Point set + maximum prefix sum inside a range.   # Максимальная префиксная сумма.

    When to use:  "max over k of a[l] + ... + a[l+k]" with updates.
    Complexity:   O(log n) per operation
    Methods:      set(i, v); query(l, r) -> max(0, best prefix sum of a[l:r]) (empty allowed)
    Idea:         node = (sum, best prefix); merge: (s1 + s2, max(p1, s1 + p2)).
    Related:      SegTreeMaxSubarray.
    CSES:         Prefix Sum Queries (2166).
    Example:
        >>> st = SegTreeMaxPrefix([2, -1, 3, -6, 4])
        >>> st.query(0, 5), st.query(3, 5)
        (4, 0)
    """

    def __init__(self, a: list[int]) -> None:
        n = len(a)
        size = 1
        while size < n:
            size <<= 1
        self.size = size
        self.s = [0] * (2 * size)  # сумма узла
        self.p = [0] * (2 * size)  # лучший префикс узла (пустой разрешён)
        for i, x in enumerate(a):
            self.s[size + i] = x
            self.p[size + i] = max(0, x)
        for i in range(size - 1, 0, -1):
            self._pull(i)

    def _pull(self, i: int) -> None:
        s, p = self.s, self.p
        s[i] = s[2 * i] + s[2 * i + 1]
        p[i] = max(p[2 * i], s[2 * i] + p[2 * i + 1])

    def set(self, i: int, v: int) -> None:
        i += self.size
        self.s[i] = v
        self.p[i] = max(0, v)
        i >>= 1
        while i:
            self._pull(i)
            i >>= 1

    def query(self, l: int, r: int) -> int:
        s, p = self.s, self.p
        ls = lp = 0  # левая накопленная часть
        rights: list[int] = []
        l += self.size
        r += self.size
        while l < r:
            if l & 1:
                lp = max(lp, ls + p[l])
                ls += s[l]
                l += 1
            if r & 1:
                r -= 1
                rights.append(r)
            l >>= 1
            r >>= 1
        for node in reversed(rights):  # правые узлы идут справа налево
            lp = max(lp, ls + p[node])
            ls += s[node]
        return lp


@algo(tags=["segment-tree", "runs", "merge-nodes"], cses=["Bit Inversions (1188)"])
class SegTreeRuns:
    """Longest run of equal characters with point changes.   # Самая длинная серия одинаковых.

    When to use:  flip / change one character, ask longest block of equal symbols.
    Complexity:   O(log n) per change
    Methods:      set(i, ch); longest() -> length of the longest run of equal characters
    Idea:         node = (len, first, last, prefix run, suffix run, best); runs glue across the
                  middle when last(L) == first(R).
    Related:      SegTreeMaxSubarray.
    CSES:         Bit Inversions (1188).
    Example:
        >>> st = SegTreeRuns("001011")
        >>> st.longest()
        2
        >>> st.set(3, "1"); st.longest()
        4
    """

    def __init__(self, s: str) -> None:
        n = len(s)
        size = 1
        while size < n:
            size <<= 1
        self.size = size
        self.d: list[tuple[int, str, str, int, int, int] | None] = [None] * (2 * size)
        for i, ch in enumerate(s):
            self.d[size + i] = (1, ch, ch, 1, 1, 1)
        for i in range(size - 1, 0, -1):
            self.d[i] = self._merge(self.d[2 * i], self.d[2 * i + 1])

    @staticmethod
    def _merge(
        a: tuple[int, str, str, int, int, int] | None, b: tuple[int, str, str, int, int, int] | None
    ) -> tuple[int, str, str, int, int, int] | None:
        if a is None:
            return b
        if b is None:
            return a
        la, fa, ea, pa, sa, ba = a
        lb, fb, eb, pb, sb, bb = b
        glue = ea == fb  # серии склеиваются через середину
        pref = la + pb if glue and pa == la else pa
        suf = lb + sa if glue and sb == lb else sb
        best = max(ba, bb, sa + pb if glue else 0)
        return (la + lb, fa, eb, pref, suf, best)

    def set(self, i: int, ch: str) -> None:
        i += self.size
        self.d[i] = (1, ch, ch, 1, 1, 1)
        i >>= 1
        while i:
            self.d[i] = self._merge(self.d[2 * i], self.d[2 * i + 1])
            i >>= 1

    def longest(self) -> int:
        root = self.d[1]
        return root[5] if root is not None else 0
