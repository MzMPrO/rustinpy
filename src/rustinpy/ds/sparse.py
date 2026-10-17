"""Sparse table for idempotent range queries.

Разреженная таблица: min / max / gcd на отрезке за O(1).
"""

from __future__ import annotations

from typing import Callable

from rustinpy._registry import algo


@algo(tags=["sparse-table", "rmq", "range-min"], cses=["Static Range Minimum Queries (1647)"])
class SparseTable:
    """Static range query for idempotent op (min, max, gcd, and, or).   # Разреженная таблица.

    When to use:  no updates, many queries; O(1) per query.
    Complexity:   O(n log n) build, O(1) per query
    Methods:      query(l, r) = op over a[l:r] (l < r)
    Pitfalls:     only idempotent ops (op(x, x) = x); sum needs prefix sums instead.
    Related:      SegTree (with updates), LCAEuler.
    CSES:         Static Range Minimum Queries (1647).
    Example:
        >>> st = SparseTable([5, 2, 8, 1, 9])
        >>> st.query(0, 3), st.query(2, 5)
        (2, 1)
        >>> from math import gcd
        >>> SparseTable([12, 18, 8], gcd).query(0, 2)
        6
    """

    def __init__(self, a: list[int], op: Callable[[int, int], int] = min) -> None:
        self.op = op
        table = [list(a)]
        n = len(a)
        k = 1
        while 2 * k <= n:
            prev = table[-1]
            # блок длины 2k = op двух блоков длины k
            table.append(list(map(op, prev[: n - 2 * k + 1], prev[k : n - k + 1])))
            k *= 2
        self.table = table

    def query(self, l: int, r: int) -> int:
        k = (r - l).bit_length() - 1  # наибольшая степень двойки <= длины
        row = self.table[k]
        return self.op(row[l], row[r - (1 << k)])
