"""Disjoint set union (with and without rollback) and minimum spanning trees.

Система непересекающихся множеств и минимальные остовы.
"""

from __future__ import annotations

import heapq

from rustinpy._registry import algo


@algo(tags=["dsu", "union-find"], cses=["Road Construction (1676)", "Building Roads (1666)"])
class DSU:
    """Union-find with union by size and path halving.   # Система непересекающихся множеств.

    When to use:  dynamic connectivity with only additions, Kruskal, grouping.
    Complexity:   ~O(alpha(n)) amortised per operation
    Methods:      find(x); union(a, b) -> bool (False if already together); same(a, b);
                  size(x); components (number of sets)
    Related:      RollbackDSU, kruskal.
    CSES:         Road Construction (1676), Building Roads (1666).
    Example:
        >>> d = DSU(5)
        >>> d.union(0, 1), d.union(1, 0), d.union(3, 4)
        (True, False, True)
        >>> d.same(0, 1), d.size(3), d.components
        (True, 2, 3)
    """

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.sz = [1] * n
        self.components = n

    def find(self, x: int) -> int:
        parent = self.parent
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # сжатие путей делением пополам
            x = parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.sz[a] < self.sz[b]:
            a, b = b, a  # меньшее подвешиваем к большему
        self.parent[b] = a
        self.sz[a] += self.sz[b]
        self.components -= 1
        return True

    def same(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)

    def size(self, x: int) -> int:
        return self.sz[self.find(x)]


@algo(tags=["dsu", "rollback", "offline"], cses=["Dynamic Connectivity (2133)"])
class RollbackDSU:
    """Union-find with undo (no path compression).   # СНМ с откатом.

    When to use:  divide and conquer over time / offline dynamic connectivity, DFS with undo.
    Complexity:   O(log n) per find / union, O(1) per undone union
    Methods:      find(x); union(a, b) -> bool; snapshot() -> t; rollback(t); components
    Pitfalls:     never compress paths - rollback relies on the exact parent links.
    Related:      DSU, ds.dynamic_connectivity_offline.
    CSES:         Dynamic Connectivity (2133).
    Example:
        >>> d = RollbackDSU(4)
        >>> t = d.snapshot(); d.union(0, 1); d.union(2, 3); d.components
        True
        True
        2
        >>> d.rollback(t); d.components, d.find(1) == d.find(0)
        (4, False)
    """

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.sz = [1] * n
        self.history: list[int] = []  # корни, которые подвесили
        self.components = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.sz[a] < self.sz[b]:
            a, b = b, a
        self.parent[b] = a
        self.sz[a] += self.sz[b]
        self.history.append(b)
        self.components -= 1
        return True

    def snapshot(self) -> int:
        return len(self.history)

    def rollback(self, t: int) -> None:
        while len(self.history) > t:  # отменяем объединения в обратном порядке
            b = self.history.pop()
            a = self.parent[b]
            self.sz[a] -= self.sz[b]
            self.parent[b] = b
            self.components += 1


@algo(tags=["mst", "kruskal", "dsu"], cses=["Road Reparation (1675)"], requires=["DSU"])
def kruskal(n: int, edges: list[tuple[int, int, int]]) -> tuple[int, list[int]] | None:
    """Minimum spanning tree by Kruskal.   # Минимальный остов (Краскал).

    When to use:  MST of a sparse graph given as an edge list.
    Complexity:   O(m log m)
    Input:        undirected edges (u, v, w).
    Returns:      (total weight, indices of used edges), or None if the graph is disconnected.
    Related:      prim, DSU.
    CSES:         Road Reparation (1675).
    Example:
        >>> kruskal(4, [(0, 1, 5), (1, 2, 3), (0, 2, 1), (2, 3, 4)])
        (8, [2, 1, 3])
        >>> kruskal(3, [(0, 1, 1)]) is None
        True
    """
    d = DSU(n)
    total = 0
    used = []
    for i in sorted(range(len(edges)), key=lambda i: edges[i][2]):  # рёбра по весу
        u, v, w = edges[i]
        if d.union(u, v):
            total += w
            used.append(i)
    return (total, used) if d.components == 1 or n == 0 else None


@algo(tags=["mst", "prim", "heap"], cses=["Road Reparation (1675)"])
def prim(n: int, adj: list[list[tuple[int, int]]]) -> int | None:
    """Minimum spanning tree weight by Prim (lazy heap).   # Минимальный остов (Прим).

    When to use:  MST from adjacency lists; dense graphs.
    Complexity:   O(m log m)
    Input:        adj[u] = [(v, w), ...] with both directions stored.
    Returns:      MST weight, or None if disconnected.
    Related:      kruskal.
    CSES:         Road Reparation (1675).
    Example:
        >>> adj = [[(1, 5), (2, 1)], [(0, 5), (2, 3)], [(0, 1), (1, 3), (3, 4)], [(2, 4)]]
        >>> prim(4, adj)
        8
    """
    if n == 0:
        return 0
    seen = [False] * n
    pq = [(0, 0)]
    total = taken = 0
    while pq and taken < n:
        w, u = heapq.heappop(pq)
        if seen[u]:
            continue
        seen[u] = True  # самое дешёвое ребро наружу
        total += w
        taken += 1
        for v, wv in adj[u]:
            if not seen[v]:
                heapq.heappush(pq, (wv, v))
    return total if taken == n else None


@algo(tags=["dsu", "components"], cses=["Road Construction (1676)"], requires=["DSU"])
def road_construction(n: int, edges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """After each added road: number of components and the largest one.   # Строительство дорог.

    When to use:  online statistics while uniting sets.
    Complexity:   O(m alpha(n))
    Returns:      list of (components, largest component size) after each edge.
    Related:      DSU.
    CSES:         Road Construction (1676).
    Example:
        >>> road_construction(5, [(0, 1), (1, 2), (3, 4), (0, 2)])
        [(4, 2), (3, 3), (2, 3), (2, 3)]
    """
    d = DSU(n)
    best = 1 if n else 0
    res = []
    for u, v in edges:
        if d.union(u, v):
            best = max(best, d.size(u))  # размер может только расти
        res.append((d.components, best))
    return res
