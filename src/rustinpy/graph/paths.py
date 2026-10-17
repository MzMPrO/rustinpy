"""Hamiltonian paths (bitmask DP) and knight's tour (Warnsdorff).

Гамильтоновы пути и обход конём.
"""

from __future__ import annotations

import random

from rustinpy._registry import algo


@algo(tags=["hamiltonian", "bitmask-dp"], cses=["Hamiltonian Flights (1690)"])
def hamiltonian_path(n: int, adj: list[list[int]]) -> list[int] | None:
    """Any Hamiltonian path of a directed graph (bitmask DP over end sets).   # Гамильтонов путь.

    When to use:  n <= ~18; visit every vertex exactly once.
    Complexity:   O(2^n * n) with bitset rows
    Returns:      vertex order of a Hamiltonian path, or None.
    Python speed: complete graph n = 16 ~ 0.5 s, n = 18 ~ 3 s, n = 20 ~ 15 s.
    Idea:         ends[mask] = bitset of vertices where a path covering exactly mask can
                  end; extend by neighbours outside mask; restore backwards.
    Related:      dp.hamiltonian_flights (counting), knights_tour.
    CSES:         Hamiltonian Flights (1690) (counting version in dp).
    Example:
        >>> hamiltonian_path(4, [[1], [2], [3], []])
        [0, 1, 2, 3]
        >>> hamiltonian_path(3, [[1], [], [1]]) is None
        True
    """
    if n == 0:
        return []
    nb = [0] * n
    for u in range(n):
        for v in adj[u]:
            nb[u] |= 1 << v  # соседи битовой маской
    full = (1 << n) - 1
    ends = [0] * (1 << n)
    for v in range(n):
        ends[1 << v] = 1 << v
    for mask in range(1, full + 1):
        e = ends[mask]
        while e:
            low = e & -e
            v = low.bit_length() - 1
            e ^= low
            free = nb[v] & ~mask  # куда можно продолжить
            while free:
                lw = free & -free
                free ^= lw
                ends[mask | lw] |= lw
    if not ends[full]:
        return None
    last = (ends[full] & -ends[full]).bit_length() - 1
    path = [last]
    mask = full
    while mask != 1 << path[-1]:  # восстановление с конца
        cur = path[-1]
        mask ^= 1 << cur
        e = ends[mask]
        while e:
            low = e & -e
            u = low.bit_length() - 1
            if nb[u] >> cur & 1:
                break
            e ^= low
        path.append(u)
    return path[::-1]


_KNIGHT = ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2))


@algo(
    tags=["knights-tour", "warnsdorff", "heuristic"],
    cses=["Knight's Tour (1689)"],
    requires=["_KNIGHT"],
)
def knights_tour(n: int, r: int, c: int) -> list[list[int]] | None:
    """Knight's tour from (r, c) on an n x n board (Warnsdorff).   # Обход доски конём.

    When to use:  constructive tours on boards 5..~100; CSES uses 8 x 8.
    Complexity:   O(n^2 * 8) per attempt, a few attempts in practice
    Returns:      board[row][col] = move number 1..n^2, or None if all attempts failed.
    Pitfalls:     a heuristic: may fail on some boards (no tour exists for n = 2, 3, 4).
    Idea:         always jump to the square with the fewest onward moves; break ties by the
                  smaller second-level degree, then randomly; restart on failure.
    Related:      hamiltonian_path.
    CSES:         Knight's Tour (1689) (input is 1-based column, row).
    Example:
        >>> b = knights_tour(8, 0, 0)
        >>> sorted(x for row in b for x in row) == list(range(1, 65)), b[0][0]
        (True, 1)
    """
    rng = random.Random(n * 1000 + r * 37 + c)

    def deg(board: list[list[int]], x: int, y: int) -> int:
        return sum(
            1
            for dx, dy in _KNIGHT
            if 0 <= x + dx < n and 0 <= y + dy < n and board[x + dx][y + dy] == 0
        )

    for _ in range(50):  # несколько попыток со случайной разбивкой равенств
        board = [[0] * n for _ in range(n)]
        x, y = r, c
        board[x][y] = 1
        ok = True
        for step in range(2, n * n + 1):
            best = None
            for dx, dy in _KNIGHT:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == 0:
                    board[nx][ny] = -1  # временно занимаем, чтобы считать степени
                    d1 = deg(board, nx, ny)
                    d2 = min(
                        (
                            deg(board, nx + ex, ny + ey)
                            for ex, ey in _KNIGHT
                            if 0 <= nx + ex < n
                            and 0 <= ny + ey < n
                            and board[nx + ex][ny + ey] == 0
                        ),
                        default=0,
                    )
                    board[nx][ny] = 0
                    key = (d1, d2, rng.random())  # правило Варнсдорфа + разбивка равенств
                    if best is None or key < best[0]:
                        best = (key, nx, ny)
            if best is None:
                ok = False
                break
            _, x, y = best
            board[x][y] = step
        if ok:
            return board
    return None
