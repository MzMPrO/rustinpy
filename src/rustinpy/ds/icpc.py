"""ICPC Uzbekistan problems around range queries.

Задачи ICPC-UZ на структуры данных. Условия сверяются на этапе 5.
"""

from __future__ import annotations

from rustinpy._registry import algo


@algo(tags=["mex", "offline", "segment-tree"], icpc=["2025 E"], cses=["- (mex of a subarray)"])
def subarray_mex_offline(a: list[int], queries: list[tuple[int, int]]) -> list[int]:
    """Mex of a[l:r] for many queries, offline by right end.   # Mex на подотрезке.

    When to use:  static array, mex queries; building block for ICPC-UZ 2025 E.
    Complexity:   O((n + q) log n)
    Returns:      answers in query order.
    Idea:         sweep r; last[v] = last position of value v (or -1); mex of [l, r) is the
                  smallest v with last[v] < l -> descend a min segment tree over values.
    Related:      sliding_window_mex.
    CSES:         - (mex of a subarray)
    ICPC-UZ:      2025 E "Exclusions" (building block).
    Example:
        >>> subarray_mex_offline([0, 2, 1, 0, 3], [(0, 3), (1, 3), (0, 5), (2, 4)])
        [3, 0, 4, 2]
    """
    n = len(a)
    m = n + 1  # mex отрезка не больше его длины <= n
    size = 1
    while size < m:
        size <<= 1
    t = [-1] * (2 * size)  # минимум last[v] по значениям узла
    for i in range(m, size):
        t[size + i] = n + 5  # фиктивные значения никогда не ответ
    for i in range(size - 1, 0, -1):
        t[i] = min(t[2 * i], t[2 * i + 1])
    by_r: list[list[int]] = [[] for _ in range(n + 1)]
    for qi, (_, r) in enumerate(queries):
        by_r[r].append(qi)
    res = [0] * len(queries)

    def answer(l: int) -> int:
        k = 1
        while k < size:  # первый v с last[v] < l
            k = 2 * k if t[2 * k] < l else 2 * k + 1
        return k - size

    for qi in by_r[0]:
        res[qi] = 0
    for i, v in enumerate(a):
        if v < m:
            k = size + v
            t[k] = i
            k >>= 1
            while k:
                t[k] = min(t[2 * k], t[2 * k + 1])
                k >>= 1
        for qi in by_r[i + 1]:
            res[qi] = answer(queries[qi][0])
    return res


_Node = tuple[int, int, int, int, int, int, int]


def _runs_merge(a: _Node | None, b: _Node | None) -> _Node | None:
    """(len, pref1, suf1, ones-subarrays, pref0, suf0, zeros-subarrays) of a + b."""
    if a is None:
        return b
    if b is None:
        return a
    la, p1a, s1a, c1a, p0a, s0a, c0a = a
    lb, p1b, s1b, c1b, p0b, s0b, c0b = b
    return (
        la + lb,
        p1a + p1b if p1a == la else p1a,
        s1b + s1a if s1b == lb else s1b,
        c1a + c1b + s1a * p1b,  # подотрезки из единиц через середину
        p0a + p0b if p0a == la else p0a,
        s0b + s0a if s0b == lb else s0b,
        c0a + c0b + s0a * p0b,
    )


@algo(
    tags=["segment-tree", "lazy", "flip", "runs", "merge-nodes"],
    icpc=["2025 H"],
    requires=["_Node", "_runs_merge"],
    verified=False,
)
class SegTreeFlipRuns:
    """Range flip of bits + number of all-ones subarrays.   # Инверсия отрезка и серии единиц.

    When to use:  0/1 array, "invert [l, r)", "sum over runs of ones of L(L+1)/2 in [l, r)".
    Complexity:   O(log n) per operation
    Methods:      flip(l, r); query(l, r) -> sum over maximal runs of ones (inside [l, r)) of
                  L * (L + 1) / 2, i.e. the number of subarrays consisting only of ones
    Idea:         keep the statistics for ones AND zeros in every node; a flip swaps them.
                  For another run function f(L) change the merge (pref / suf / total).
    ICPC-UZ:      2025 H "Headquarter Reforms" (exact run function NOT VERIFIED).
    Example:
        >>> st = SegTreeFlipRuns([1, 1, 0, 1])
        >>> st.query(0, 4)
        4
        >>> st.flip(2, 3); st.query(0, 4), st.query(1, 3)
        (10, 3)
    """

    def __init__(self, bits: list[int]) -> None:
        # NOT VERIFIED: какая функция от длины серии нужна в 2025 H - не сверено
        n = len(bits)
        size, log = 1, 0
        while size < n:
            size <<= 1
            log += 1
        self.size, self.log = size, log
        self.d: list[_Node | None] = [None] * (2 * size)
        self.lz = [False] * size
        for i, b in enumerate(bits):
            self.d[size + i] = (1, 1, 1, 1, 0, 0, 0) if b else (1, 0, 0, 0, 1, 1, 1)
        for k in range(size - 1, 0, -1):
            self.d[k] = _runs_merge(self.d[2 * k], self.d[2 * k + 1])

    def _apply(self, k: int) -> None:
        x = self.d[k]
        if x is not None:
            ln, p1, s1, c1, p0, s0, c0 = x
            self.d[k] = (ln, p0, s0, c0, p1, s1, c1)  # единицы <-> нули
        if k < self.size:
            self.lz[k] = not self.lz[k]

    def _push(self, k: int) -> None:
        if self.lz[k]:
            self._apply(2 * k)
            self._apply(2 * k + 1)
            self.lz[k] = False

    def _push_path(self, l: int, r: int) -> None:
        for i in range(self.log, 0, -1):
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push((r - 1) >> i)

    def flip(self, l: int, r: int) -> None:
        if l >= r:
            return
        l += self.size
        r += self.size
        self._push_path(l, r)
        l2, r2 = l, r
        while l < r:
            if l & 1:
                self._apply(l)
                l += 1
            if r & 1:
                r -= 1
                self._apply(r)
            l >>= 1
            r >>= 1
        d = self.d
        for i in range(1, self.log + 1):
            if ((l2 >> i) << i) != l2:
                k = l2 >> i
                d[k] = _runs_merge(d[2 * k], d[2 * k + 1])
            if ((r2 >> i) << i) != r2:
                k = (r2 - 1) >> i
                d[k] = _runs_merge(d[2 * k], d[2 * k + 1])

    def query(self, l: int, r: int) -> int:
        if l >= r:
            return 0
        l += self.size
        r += self.size
        self._push_path(l, r)
        left: _Node | None = None
        right: _Node | None = None
        while l < r:
            if l & 1:
                left = _runs_merge(left, self.d[l])
                l += 1
            if r & 1:
                r -= 1
                right = _runs_merge(self.d[r], right)
            l >>= 1
            r >>= 1
        res = _runs_merge(left, right)
        return res[3] if res is not None else 0


@algo(tags=["mex", "partition", "dp"], icpc=["2025 E"], verified=False, stub=True)
def exclusions(a: list[int]) -> list[int]:
    """ICPC-UZ 2025 E "Exclusions": f(k) for splitting into k blocks by mex.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return f(1), ..., f(n).
    Idea:         mex of a block is non-increasing when the block shrinks; with
                  subarray_mex_offline / sliding mex compute the optimum per k.
                  NOT VERIFIED: the definition of f(k) is not known yet.
    ICPC-UZ:      2025 E.
    Example:
        >>> exclusions([0, 1])
        Traceback (most recent call last):
        NotImplementedError: ICPC-UZ 2025 E: statement not verified yet
    """
    # NOT VERIFIED: заглушка до сверки условия (этап 5)
    raise NotImplementedError("ICPC-UZ 2025 E: statement not verified yet")


@algo(tags=["two-pointers", "binary-search", "strings"], icpc=["2023 G"], verified=False, stub=True)
def generic_strings(s: str, k: int) -> int:
    """ICPC-UZ 2023 G "Generic Strings": no repeats on windows after deletions.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return the answer of the problem.
    Idea:         binary search on the answer with a two-pointer check of "no repeated letter
                  in a window" (longest_window_no_repeats). NOT VERIFIED: statement unknown.
    ICPC-UZ:      2023 G.
    Example:
        >>> generic_strings("ab", 1)
        Traceback (most recent call last):
        NotImplementedError: ICPC-UZ 2023 G: statement not verified yet
    """
    # NOT VERIFIED: заглушка до сверки условия (этап 5)
    raise NotImplementedError("ICPC-UZ 2023 G: statement not verified yet")
