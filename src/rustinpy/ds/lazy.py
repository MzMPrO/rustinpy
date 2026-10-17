"""Lazy segment trees (iterative, AtCoder Library style).

Деревья отрезков с отложенными операциями. Отрезки полуоткрытые [l, r).
Каждый класс самодостаточен: копируется в TRD целиком.
"""

from __future__ import annotations

from rustinpy._registry import algo

INF = 1 << 60


@algo(tags=["segment-tree", "lazy", "range-add", "range-sum"], cses=["- (range add + range sum)"])
class LazySegAddSum:
    """Range add + range sum.   # Прибавление и сумма на отрезке.

    When to use:  both updates and queries on ranges.
    Complexity:   O(log n) per operation
    Methods:      range_add(l, r, x); range_sum(l, r)
    Python speed: ~30 us per operation: 4 * 10^5 ops ~ 12 s in CPython (fine under PyPy);
                  for add + sum use FenwickRangeRange - about 5x faster.
    Related:      FenwickRangeRange (shorter, same operations), LazySegAddMin.
    CSES:         - (range add + range sum)
    Example:
        >>> st = LazySegAddSum([1, 2, 3, 4])
        >>> st.range_add(1, 3, 10); st.range_sum(0, 4), st.range_sum(2, 3)
        (30, 13)
    """

    def __init__(self, a: list[int] | int) -> None:
        a = [0] * a if isinstance(a, int) else a
        n = len(a)
        size, log = 1, 0
        while size < n:
            size <<= 1
            log += 1
        self.size, self.log = size, log
        self.d = [0] * (2 * size)
        self.ln = [0] * (2 * size)  # длина отрезка узла (0 у фиктивных листьев)
        self.lz = [0] * size
        for i, x in enumerate(a):
            self.d[size + i] = x
            self.ln[size + i] = 1
        for k in range(size - 1, 0, -1):
            self.d[k] = self.d[2 * k] + self.d[2 * k + 1]
            self.ln[k] = self.ln[2 * k] + self.ln[2 * k + 1]

    def _push_path(self, l: int, r: int) -> None:
        # push встроен (без вызовов методов) - заметно быстрее в CPython
        d, lz, ln, size = self.d, self.lz, self.ln, self.size
        for i in range(self.log, 0, -1):  # сверху вниз по границам
            if ((l >> i) << i) != l:
                k = l >> i
                f = lz[k]
                if f:
                    c = 2 * k
                    d[c] += f * ln[c]
                    d[c + 1] += f * ln[c + 1]
                    if c < size:
                        lz[c] += f  # отложенное значение уходит детям
                        lz[c + 1] += f
                    lz[k] = 0
            if ((r >> i) << i) != r:
                k = (r - 1) >> i
                f = lz[k]
                if f:
                    c = 2 * k
                    d[c] += f * ln[c]
                    d[c + 1] += f * ln[c + 1]
                    if c < size:
                        lz[c] += f
                        lz[c + 1] += f
                    lz[k] = 0

    def range_add(self, l: int, r: int, f: int) -> None:
        if l >= r:
            return
        size, d, lz, ln = self.size, self.d, self.lz, self.ln
        l += size
        r += size
        self._push_path(l, r)
        l2, r2 = l, r
        while l < r:
            if l & 1:
                d[l] += f * ln[l]
                if l < size:
                    lz[l] += f  # откладываем для детей
                l += 1
            if r & 1:
                r -= 1
                d[r] += f * ln[r]
                if r < size:
                    lz[r] += f
            l >>= 1
            r >>= 1
        for i in range(1, self.log + 1):  # пересчёт снизу вверх
            if ((l2 >> i) << i) != l2:
                k = l2 >> i
                d[k] = d[2 * k] + d[2 * k + 1]
            if ((r2 >> i) << i) != r2:
                k = (r2 - 1) >> i
                d[k] = d[2 * k] + d[2 * k + 1]

    def range_sum(self, l: int, r: int) -> int:
        if l >= r:
            return 0
        l += self.size
        r += self.size
        self._push_path(l, r)
        s = 0
        d = self.d
        while l < r:
            if l & 1:
                s += d[l]
                l += 1
            if r & 1:
                r -= 1
                s += d[r]
            l >>= 1
            r >>= 1
        return s


@algo(
    tags=["segment-tree", "lazy", "range-add", "range-min"],
    cses=["- (range add + range min)"],
    requires=["INF"],
)
class LazySegAddMin:
    """Range add + range min.   # Прибавление на отрезке, минимум на отрезке.

    When to use:  scheduling / sweep problems: "add to a range, ask the minimum".
    Complexity:   O(log n) per operation
    Methods:      range_add(l, r, x); range_min(l, r) (INF = 1 << 60 for an empty range)
    Pitfalls:     for max use negated values or swap min -> max in the code.
    Python speed: ~30 us per operation: 4 * 10^5 ops ~ 12 s in CPython (fine under PyPy).
    Related:      LazySegAddSum, SegTree.
    CSES:         - (range add + range min)
    Example:
        >>> st = LazySegAddMin([5, 1, 4, 3])
        >>> st.range_add(1, 2, 10); st.range_min(0, 4), st.range_min(1, 3)
        (3, 4)
    """

    def __init__(self, a: list[int] | int) -> None:
        a = [0] * a if isinstance(a, int) else a
        n = len(a)
        size, log = 1, 0
        while size < n:
            size <<= 1
            log += 1
        self.size, self.log = size, log
        self.d = [INF] * (2 * size)
        self.lz = [0] * size
        self.d[size : size + n] = a
        for k in range(size - 1, 0, -1):
            self.d[k] = min(self.d[2 * k], self.d[2 * k + 1])

    def _apply(self, k: int, f: int) -> None:
        self.d[k] += f  # минимум сдвигается на f
        if k < self.size:
            self.lz[k] += f

    def _push(self, k: int) -> None:
        f = self.lz[k]
        if f:
            self._apply(2 * k, f)
            self._apply(2 * k + 1, f)
            self.lz[k] = 0

    def _push_path(self, l: int, r: int) -> None:
        for i in range(self.log, 0, -1):
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push((r - 1) >> i)

    def range_add(self, l: int, r: int, f: int) -> None:
        if l >= r:
            return
        l += self.size
        r += self.size
        self._push_path(l, r)
        l2, r2 = l, r
        while l < r:
            if l & 1:
                self._apply(l, f)
                l += 1
            if r & 1:
                r -= 1
                self._apply(r, f)
            l >>= 1
            r >>= 1
        d = self.d
        for i in range(1, self.log + 1):
            if ((l2 >> i) << i) != l2:
                k = l2 >> i
                d[k] = min(d[2 * k], d[2 * k + 1])
            if ((r2 >> i) << i) != r2:
                k = (r2 - 1) >> i
                d[k] = min(d[2 * k], d[2 * k + 1])

    def range_min(self, l: int, r: int) -> int:
        if l >= r:
            return INF
        l += self.size
        r += self.size
        self._push_path(l, r)
        res = INF
        d = self.d
        while l < r:
            if l & 1:
                res = min(res, d[l])
                l += 1
            if r & 1:
                r -= 1
                res = min(res, d[r])
            l >>= 1
            r >>= 1
        return res


@algo(
    tags=["segment-tree", "lazy", "range-assign", "range-add", "range-sum"],
    cses=["Range Updates and Sums (1735)"],
)
class LazySegAssignAddSum:
    """Range assign + range add + range sum.   # Присвоение и прибавление на отрезке, сумма.

    When to use:  two kinds of range updates at once.
    Complexity:   O(log n) per operation
    Methods:      range_add(l, r, x); range_assign(l, r, x); range_sum(l, r)
    Python speed: ~30 us per operation: 4 * 10^5 ops ~ 12 s in CPython (fine under PyPy).
    Idea:         lazy tag = (assign or None, add) meaning "assign, then add";
                  new assign resets the add part.   # композиция меток
    Related:      LazySegAddSum.
    CSES:         Range Updates and Sums (1735).
    Example:
        >>> st = LazySegAssignAddSum([2, 3, 1, 1, 5, 3])
        >>> st.range_add(2, 4, 1); st.range_sum(0, 6)
        17
        >>> st.range_assign(1, 5, 2); st.range_sum(0, 6)
        13
    """

    def __init__(self, a: list[int] | int) -> None:
        a = [0] * a if isinstance(a, int) else a
        n = len(a)
        size, log = 1, 0
        while size < n:
            size <<= 1
            log += 1
        self.size, self.log = size, log
        self.d = [0] * (2 * size)
        self.ln = [0] * (2 * size)
        self.asg: list[int | None] = [None] * size
        self.add = [0] * size
        for i, x in enumerate(a):
            self.d[size + i] = x
            self.ln[size + i] = 1
        for k in range(size - 1, 0, -1):
            self.d[k] = self.d[2 * k] + self.d[2 * k + 1]
            self.ln[k] = self.ln[2 * k] + self.ln[2 * k + 1]

    def _apply(self, k: int, asg: int | None, add: int) -> None:
        if asg is not None:
            self.d[k] = asg * self.ln[k]  # присвоение затирает всё
            if k < self.size:
                self.asg[k] = asg
                self.add[k] = 0
        if add:
            self.d[k] += add * self.ln[k]
            if k < self.size:
                self.add[k] += add

    def _push(self, k: int) -> None:
        a, b = self.asg[k], self.add[k]
        if a is not None or b:
            self._apply(2 * k, a, b)
            self._apply(2 * k + 1, a, b)
            self.asg[k] = None
            self.add[k] = 0

    def _push_path(self, l: int, r: int) -> None:
        for i in range(self.log, 0, -1):
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push((r - 1) >> i)

    def _update(self, l: int, r: int, asg: int | None, add: int) -> None:
        if l >= r:
            return
        l += self.size
        r += self.size
        self._push_path(l, r)
        l2, r2 = l, r
        while l < r:
            if l & 1:
                self._apply(l, asg, add)
                l += 1
            if r & 1:
                r -= 1
                self._apply(r, asg, add)
            l >>= 1
            r >>= 1
        d = self.d
        for i in range(1, self.log + 1):
            if ((l2 >> i) << i) != l2:
                k = l2 >> i
                d[k] = d[2 * k] + d[2 * k + 1]
            if ((r2 >> i) << i) != r2:
                k = (r2 - 1) >> i
                d[k] = d[2 * k] + d[2 * k + 1]

    def range_add(self, l: int, r: int, x: int) -> None:
        self._update(l, r, None, x)

    def range_assign(self, l: int, r: int, x: int) -> None:
        self._update(l, r, x, 0)

    def range_sum(self, l: int, r: int) -> int:
        if l >= r:
            return 0
        l += self.size
        r += self.size
        self._push_path(l, r)
        s = 0
        d = self.d
        while l < r:
            if l & 1:
                s += d[l]
                l += 1
            if r & 1:
                r -= 1
                s += d[r]
            l >>= 1
            r >>= 1
        return s


@algo(
    tags=["segment-tree", "lazy", "arithmetic-progression", "range-sum"],
    cses=["Polynomial Queries (1736)"],
)
class LazySegArithmetic:
    """Add an arithmetic progression on a range + range sum.   # Прибавление прогрессии.

    When to use:  a[l] += b, a[l+1] += b + c, a[l+2] += b + 2c, ... and range sums.
    Complexity:   O(log n) per operation
    Methods:      add_progression(l, r, first=1, step=1); range_sum(l, r)
    Python speed: ~35 us per operation: 4 * 10^5 ops ~ 14 s in CPython (fine under PyPy).
    Idea:         lazy tag = (first term at the node's left end, step); the right child gets
                  first + step * len(left child).
    Related:      LazySegAddSum.
    CSES:         Polynomial Queries (1736).
    Example:
        >>> st = LazySegArithmetic([4, 2, 3, 1, 7])
        >>> st.add_progression(1, 4); st.range_sum(0, 5)
        23
        >>> st.range_sum(2, 4)
        9
    """

    def __init__(self, a: list[int] | int) -> None:
        a = [0] * a if isinstance(a, int) else a
        n = len(a)
        size, log = 1, 0
        while size < n:
            size <<= 1
            log += 1
        self.size, self.log = size, log
        self.d = [0] * (2 * size)
        self.ln = [0] * (2 * size)
        self.lf = [0] * (2 * size)  # индекс левого конца узла
        self.b = [0] * size
        self.c = [0] * size
        for i in range(size):
            self.lf[size + i] = i
        for i, x in enumerate(a):
            self.d[size + i] = x
            self.ln[size + i] = 1
        for k in range(size - 1, 0, -1):
            self.d[k] = self.d[2 * k] + self.d[2 * k + 1]
            self.ln[k] = self.ln[2 * k] + self.ln[2 * k + 1]
            self.lf[k] = self.lf[2 * k]

    def _apply(self, k: int, b: int, c: int) -> None:
        L = self.ln[k]
        self.d[k] += b * L + c * (L * (L - 1) // 2)  # сумма прогрессии длины L
        if k < self.size:
            self.b[k] += b
            self.c[k] += c

    def _push(self, k: int) -> None:
        b, c = self.b[k], self.c[k]
        if b or c:
            self._apply(2 * k, b, c)
            self._apply(2 * k + 1, b + c * self.ln[2 * k], c)  # сдвиг на длину левого
            self.b[k] = self.c[k] = 0

    def _push_path(self, l: int, r: int) -> None:
        for i in range(self.log, 0, -1):
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push((r - 1) >> i)

    def add_progression(self, l: int, r: int, first: int = 1, step: int = 1) -> None:
        if l >= r:
            return
        l0 = l
        l += self.size
        r += self.size
        self._push_path(l, r)
        l2, r2 = l, r
        lf = self.lf
        while l < r:
            if l & 1:
                self._apply(l, first + step * (lf[l] - l0), step)
                l += 1
            if r & 1:
                r -= 1
                self._apply(r, first + step * (lf[r] - l0), step)
            l >>= 1
            r >>= 1
        d = self.d
        for i in range(1, self.log + 1):
            if ((l2 >> i) << i) != l2:
                k = l2 >> i
                d[k] = d[2 * k] + d[2 * k + 1]
            if ((r2 >> i) << i) != r2:
                k = (r2 - 1) >> i
                d[k] = d[2 * k] + d[2 * k + 1]

    def range_sum(self, l: int, r: int) -> int:
        if l >= r:
            return 0
        l += self.size
        r += self.size
        self._push_path(l, r)
        s = 0
        d = self.d
        while l < r:
            if l & 1:
                s += d[l]
                l += 1
            if r & 1:
                r -= 1
                s += d[r]
            l >>= 1
            r >>= 1
        return s
