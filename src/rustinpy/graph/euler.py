"""Euler paths and cycles (Hierholzer, iterative).

Эйлеровы пути и циклы.
"""

from __future__ import annotations

from rustinpy._registry import algo


@algo(tags=["euler", "hierholzer", "undirected"], cses=["Mail Delivery (1691)"])
def euler_path_undirected(
    n: int, edges: list[tuple[int, int]], start: int | None = None
) -> list[int] | None:
    """Euler path / cycle of an undirected multigraph.   # Эйлеров путь (неориентированный).

    When to use:  "walk every street exactly once"; cycle when all degrees are even.
    Complexity:   O(n + m)
    Input:        edges (u, v); start = required first vertex (None: choose automatically).
    Returns:      vertex sequence of length m + 1, or None if impossible.
    Pitfalls:     besides degree parity the edges must be connected - checked by length.
    Related:      euler_path_directed, introductory.de_bruijn.
    CSES:         Mail Delivery (1691) (start=0, must return to 0: all degrees even).
    Example:
        >>> euler_path_undirected(4, [(0, 1), (1, 2), (2, 0), (0, 3), (3, 0)], 0)
        [0, 1, 2, 0, 3, 0]
        >>> euler_path_undirected(4, [(0, 1), (2, 3)]) is None
        True
    """
    m = len(edges)
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))
        adj[v].append((u, i))
    odd = [v for v in range(n) if len(adj[v]) % 2]
    if len(odd) not in (0, 2):
        return None  # больше двух нечётных степеней - пути нет
    if start is None:
        start = odd[0] if odd else next((v for v in range(n) if adj[v]), 0)
    elif odd and start not in odd:
        return None
    used = [False] * m
    ptr = [0] * n
    stack = [start]
    path = []
    while stack:
        u = stack[-1]
        while ptr[u] < len(adj[u]) and used[adj[u][ptr[u]][1]]:
            ptr[u] += 1  # пропускаем использованные рёбра
        if ptr[u] < len(adj[u]):
            v, e = adj[u][ptr[u]]
            used[e] = True
            stack.append(v)
        else:
            path.append(stack.pop())  # тупик - вершина уходит в ответ
    if len(path) != m + 1:
        return None  # рёбра не связны
    return path[::-1]


@algo(tags=["euler", "hierholzer", "directed"], cses=["Teleporters Path (1693)"])
def euler_path_directed(
    n: int, edges: list[tuple[int, int]], src: int, dst: int
) -> list[int] | None:
    """Directed Euler path src -> dst using every edge once.   # Эйлеров путь (ориентированный).

    When to use:  every directed edge exactly once with fixed endpoints (src == dst: cycle).
    Complexity:   O(n + m)
    Returns:      vertex sequence of length m + 1, or None.
    Idea:         out - in = 1 at src, in - out = 1 at dst, balanced elsewhere; Hierholzer.
    Related:      euler_path_undirected, introductory.de_bruijn.
    CSES:         Teleporters Path (1693) (src = 0, dst = n - 1).
    Example:
        >>> euler_path_directed(4, [(0, 1), (1, 2), (2, 0), (0, 3)], 0, 3)
        [0, 1, 2, 0, 3]
    """
    m = len(edges)
    adj: list[list[int]] = [[] for _ in range(n)]
    diff = [0] * n  # out - in
    for u, v in edges:
        adj[u].append(v)
        diff[u] += 1
        diff[v] -= 1
    for v in range(n):
        need = (1 if v == src else 0) - (1 if v == dst else 0)
        if diff[v] != need:
            return None  # нарушен баланс степеней
    ptr = [0] * n
    stack = [src]
    path = []
    while stack:
        u = stack[-1]
        if ptr[u] < len(adj[u]):
            stack.append(adj[u][ptr[u]])
            ptr[u] += 1
        else:
            path.append(stack.pop())
    if len(path) != m + 1:
        return None  # не все рёбра достижимы
    path.reverse()
    return path if path[-1] == dst else None
