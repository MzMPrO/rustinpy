"""Prefix sums in 1D and 2D.

Префиксные суммы. Все отрезки полуоткрытые: [l, r).
"""

from __future__ import annotations

from rustinpy._registry import algo


@algo(tags=["prefix-sums", "range-sum"], cses=["Static Range Sum Queries (1646)"])
def prefix_sums(a: list[int]) -> list[int]:
    """Prefix sums p[i] = a[0] + ... + a[i-1].   # Префиксные суммы.

    When to use:  static range sums: sum(a[l:r]) = p[r] - p[l].
    Complexity:   O(n) build, O(1) per query
    Returns:      list p of length n + 1, p[0] = 0.
    Pitfalls:     with updates use Fenwick; for xor use the same idea with ^.
    Related:      PrefixSum2D, Fenwick.
    CSES:         Static Range Sum Queries (1646).
    Example:
        >>> p = prefix_sums([3, 2, 4, 5, 1])
        >>> p, p[4] - p[1]
        ([0, 3, 5, 9, 14, 15], 11)
    """
    p = [0] * (len(a) + 1)
    for i, x in enumerate(a):
        p[i + 1] = p[i] + x  # сумма первых i + 1 элементов
    return p


@algo(tags=["prefix-sums", "2d", "range-sum"], cses=["Forest Queries (1652)"])
class PrefixSum2D:
    """2D prefix sums for rectangle sums.   # Двумерные префиксные суммы.

    When to use:  many rectangle-sum queries on a static grid.
    Complexity:   O(R * C) build, O(1) per query
    Input:        grid of ints (for a '*' map pass [[ch == '*' for ...]] as ints).
    Methods:      query(r1, c1, r2, c2) = sum of grid[r][c] for r1 <= r < r2, c1 <= c < c2
    Related:      prefix_sums, Fenwick2D (with updates).
    CSES:         Forest Queries (1652).
    Example:
        >>> ps = PrefixSum2D([[1, 2, 3], [4, 5, 6]])
        >>> ps.query(0, 0, 2, 3), ps.query(1, 1, 2, 3)
        (21, 11)
    """

    def __init__(self, grid: list[list[int]]) -> None:
        R = len(grid)
        C = len(grid[0]) if R else 0
        s = [[0] * (C + 1) for _ in range(R + 1)]
        for r in range(R):
            row, prev, cur = grid[r], s[r], s[r + 1]
            acc = 0
            for c in range(C):
                acc += row[c]  # сумма в текущей строке
                cur[c + 1] = prev[c + 1] + acc
        self.s = s

    def query(self, r1: int, c1: int, r2: int, c2: int) -> int:
        s = self.s
        # включения-исключения по четырём углам
        return s[r2][c2] - s[r1][c2] - s[r2][c1] + s[r1][c1]
