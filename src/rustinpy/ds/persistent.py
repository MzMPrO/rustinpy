"""Persistent segment tree, k-th smallest on a range, merge sort tree.

Персистентное дерево отрезков и деревья для k-й статистики. Отрезки [l, r).
"""

from __future__ import annotations

from bisect import bisect_right

from rustinpy._registry import algo


@algo(tags=["segment-tree", "persistent"], cses=["Range Queries and Copies (1737)"])
class PersistentSegTree:
    """Persistent sum segment tree: every set() returns a new version.   # Персистентное дерево.

    When to use:  queries to old versions of an array, "copy array k" operations.
    Complexity:   O(n) build, O(log n) time and memory per set / query
    Methods:      root0 (initial version); set(root, i, v) -> new root; query(root, l, r)
    Pitfalls:     memory grows by ~log n nodes per update: 2 * 10^5 updates -> ~4 * 10^6 ints.
    Related:      range_kth_smallest (same idea over values).
    CSES:         Range Queries and Copies (1737).
    Example:
        >>> pst = PersistentSegTree([2, 3, 1, 2, 4])
        >>> v1 = pst.set(pst.root0, 2, 10)
        >>> pst.query(pst.root0, 0, 5), pst.query(v1, 0, 5), pst.query(v1, 2, 3)
        (12, 21, 10)
    """

    def __init__(self, a: list[int]) -> None:
        self.n = max(1, len(a))
        self.left: list[int] = [0]  # узел 0 - пустой (сумма 0)
        self.right: list[int] = [0]
        self.val: list[int] = [0]
        vals = a if a else [0]
        # построение без рекурсии: (lo, hi, выход?)
        stack: list[tuple[int, int, bool]] = [(0, self.n, False)]
        out: list[int] = []
        while stack:
            lo, hi, exiting = stack.pop()
            if hi - lo == 1:
                out.append(self._new(0, 0, vals[lo]))
            elif not exiting:
                mid = (lo + hi) // 2
                stack.append((lo, hi, True))
                stack.append((mid, hi, False))
                stack.append((lo, mid, False))
            else:
                r = out.pop()
                l = out.pop()
                out.append(self._new(l, r, self.val[l] + self.val[r]))
        self.root0 = out[0]

    def _new(self, l: int, r: int, v: int) -> int:
        self.left.append(l)
        self.right.append(r)
        self.val.append(v)
        return len(self.val) - 1

    def set(self, root: int, i: int, v: int) -> int:
        path: list[tuple[int, bool]] = []  # (узел, ушли ли вправо)
        node, lo, hi = root, 0, self.n
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if i < mid:
                path.append((node, False))
                node, hi = self.left[node], mid
            else:
                path.append((node, True))
                node, lo = self.right[node], mid
        cur = self._new(0, 0, v)
        for node, went_right in reversed(path):  # копируем путь снизу вверх
            if went_right:
                l, r = self.left[node], cur
            else:
                l, r = cur, self.right[node]
            cur = self._new(l, r, self.val[l] + self.val[r])
        return cur

    def query(self, root: int, l: int, r: int) -> int:
        s = 0
        stack = [(root, 0, self.n)]
        while stack:
            node, lo, hi = stack.pop()
            if r <= lo or hi <= l or node == 0:
                continue
            if l <= lo and hi <= r:
                s += self.val[node]  # узел целиком внутри
                continue
            mid = (lo + hi) // 2
            stack.append((self.left[node], lo, mid))
            stack.append((self.right[node], mid, hi))
        return s


@algo(
    tags=["persistent", "kth", "order-statistics", "offline"], cses=["- (k-th smallest on a range)"]
)
def range_kth_smallest(a: list[int], queries: list[tuple[int, int, int]]) -> list[int]:
    """k-th smallest value in a[l:r] for many queries (persistent tree).   # k-я статистика.

    When to use:  static array, "k-th smallest on a subarray" queries.
    Complexity:   O((n + q) log n)
    Input:        queries (l, r, k), half-open [l, r), k is 1-based (1 = minimum).
    Returns:      answers in query order.
    Idea:         version i = counts of a[0:i] over compressed values; descend with the
                  difference of versions r and l.
    Related:      PersistentSegTree, MergeSortTree, SortedList.
    CSES:         - (k-th smallest on a range)
    Example:
        >>> range_kth_smallest([5, 1, 4, 2, 3], [(0, 5, 2), (1, 4, 3), (2, 3, 1)])
        [2, 4, 4]
    """
    vals = sorted(set(a))
    idx = {v: i for i, v in enumerate(vals)}
    m = max(1, len(vals))
    L, R, C = [0], [0], [0]  # узел 0 - пустое дерево
    roots = [0]
    for x in a:
        pos = idx[x]
        # копия пути от корня до листа pos с +1
        prev = roots[-1]
        path: list[tuple[int, bool]] = []
        lo, hi = 0, m
        node = prev
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if pos < mid:
                path.append((node, False))
                node, hi = L[node], mid
            else:
                path.append((node, True))
                node, lo = R[node], mid
        L.append(0)
        R.append(0)
        C.append(C[node] + 1)
        cur = len(C) - 1
        for nd, went_right in reversed(path):
            if went_right:
                L.append(L[nd])
                R.append(cur)
            else:
                L.append(cur)
                R.append(R[nd])
            C.append(C[nd] + 1)
            cur = len(C) - 1
        roots.append(cur)
    res = []
    for l, r, k in queries:
        u, v = roots[r], roots[l]
        lo, hi = 0, m
        while hi - lo > 1:
            mid = (lo + hi) // 2
            cnt = C[L[u]] - C[L[v]]  # сколько значений в левой половине
            if k <= cnt:
                u, v, hi = L[u], L[v], mid
            else:
                k -= cnt
                u, v, lo = R[u], R[v], mid
        res.append(vals[lo])
    return res


@algo(tags=["segment-tree", "merge-sort-tree", "counting"], cses=["- (count <= x on a range)"])
class MergeSortTree:
    """Each node keeps its sorted subarray: count values <= x on a range.   # Дерево сортировок.

    When to use:  static array, "how many a[i] <= x for l <= i < r".
    Complexity:   O(n log n) build and memory, O(log^2 n) per query
    Methods:      count_le(l, r, x)
    Python speed: build of 2 * 10^5 is ~1 s; prefer offline sorting + Fenwick if possible.
    Related:      range_kth_smallest, Fenwick (offline).
    CSES:         - (count <= x on a range)
    Example:
        >>> mst = MergeSortTree([5, 1, 4, 2, 3])
        >>> mst.count_le(0, 5, 3), mst.count_le(2, 5, 2)
        (3, 1)
    """

    def __init__(self, a: list[int]) -> None:
        n = len(a)
        size = 1
        while size < n:
            size <<= 1
        self.size = size
        t: list[list[int]] = [[] for _ in range(2 * size)]
        for i, x in enumerate(a):
            t[size + i] = [x]  # лист - один элемент
        for k in range(size - 1, 0, -1):
            t[k] = sorted(t[2 * k] + t[2 * k + 1])  # Timsort сливает два отсортированных куска
        self.t = t

    def count_le(self, l: int, r: int, x: int) -> int:
        res = 0
        l += self.size
        r += self.size
        t = self.t
        while l < r:
            if l & 1:
                res += bisect_right(t[l], x)  # бинпоиск в отсортированном узле
                l += 1
            if r & 1:
                r -= 1
                res += bisect_right(t[r], x)
            l >>= 1
            r >>= 1
        return res
