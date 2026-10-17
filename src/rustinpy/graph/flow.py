"""Maximum flow (Dinic, Edmonds-Karp), minimum cut, disjoint paths, min-cost flow.

Потоки. Рёбра хранятся парами: e и e ^ 1 - обратное.
"""

from __future__ import annotations

from collections import deque

from rustinpy._registry import algo

INF = 1 << 60


@algo(
    tags=["flow", "dinic", "max-flow", "min-cut"],
    cses=["Download Speed (1694)", "Police Chase (1695)", "School Dance (1696)"],
    requires=["INF"],
)
class Dinic:
    """Dinic max flow with iterative augmenting (no recursion).   # Максимальный поток (Диниц).

    When to use:  max flow / min cut / bipartite matching with capacities.
    Complexity:   O(V^2 E) worst case, much faster in practice; O(E sqrt V) on unit graphs
    Methods:      add_edge(u, v, cap, rev_cap=0) -> edge id; max_flow(s, t);
                  min_cut_side(s) -> reachable[v] in the residual graph; flow_on(e)
    Python speed: unit bipartite graph 9 * 10^4 vertices, 1.8 * 10^5 edges ~0.3 s.
    Related:      edmonds_karp, min_cut_edges, edge_disjoint_paths, hopcroft_karp.
    CSES:         Download Speed (1694), Police Chase (1695), School Dance (1696).
    Example:
        >>> d = Dinic(4)
        >>> e = d.add_edge(0, 1, 3); _ = d.add_edge(0, 2, 2)
        >>> _ = d.add_edge(1, 3, 2); _ = d.add_edge(2, 3, 3); _ = d.add_edge(1, 2, 1)
        >>> d.max_flow(0, 3), d.flow_on(e), d.min_cut_side(0)
        (5, 3, [True, False, False, False])
    """

    def __init__(self, n: int) -> None:
        self.n = n
        self.g: list[list[int]] = [[] for _ in range(n)]
        self.to: list[int] = []
        self.cap: list[int] = []
        self.orig: list[int] = []

    def add_edge(self, u: int, v: int, cap: int, rev_cap: int = 0) -> int:
        e = len(self.to)
        self.to += [v, u]
        self.cap += [cap, rev_cap]  # прямое и обратное ребро рядом
        self.orig += [cap, rev_cap]
        self.g[u].append(e)
        self.g[v].append(e + 1)
        return e

    def _bfs(self, s: int, t: int) -> list[int] | None:
        level = [-1] * self.n
        level[s] = 0
        q = deque([s])
        to, cap = self.to, self.cap
        while q:
            u = q.popleft()
            for e in self.g[u]:
                v = to[e]
                if cap[e] > 0 and level[v] < 0:
                    level[v] = level[u] + 1  # слоистая сеть
                    q.append(v)
        return level if level[t] >= 0 else None

    def max_flow(self, s: int, t: int) -> int:
        flow = 0
        to, cap, g = self.to, self.cap, self.g
        while True:
            level = self._bfs(s, t)
            if level is None:
                return flow
            it = [0] * self.n
            while True:  # блокирующий поток: ищем пути итеративно
                path: list[int] = []
                v = s
                while v != t:
                    ev = g[v]
                    while it[v] < len(ev):
                        e = ev[it[v]]
                        if cap[e] > 0 and level[to[e]] == level[v] + 1:
                            break
                        it[v] += 1
                    if it[v] < len(ev):
                        e = ev[it[v]]
                        path.append(e)
                        v = to[e]
                    else:
                        if v == s:
                            break
                        level[v] = -1  # тупик - выкидываем вершину из слоёв
                        e = path.pop()
                        v = to[e ^ 1]
                        it[v] += 1
                if v != t:
                    break
                f = min(cap[e] for e in path)
                for e in path:
                    cap[e] -= f
                    cap[e ^ 1] += f
                flow += f

    def min_cut_side(self, s: int) -> list[bool]:
        seen = [False] * self.n
        seen[s] = True
        stack = [s]
        while stack:  # достижимость по остаточной сети
            u = stack.pop()
            for e in self.g[u]:
                v = self.to[e]
                if self.cap[e] > 0 and not seen[v]:
                    seen[v] = True
                    stack.append(v)
        return seen

    def flow_on(self, e: int) -> int:
        return self.cap[e ^ 1] - self.orig[e ^ 1]


@algo(tags=["flow", "edmonds-karp", "max-flow"], cses=["Download Speed (1694)"], requires=["INF"])
def edmonds_karp(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int:
    """Max flow by shortest augmenting paths (BFS).   # Эдмондс-Карп.

    When to use:  simple max flow when Dinic is not needed (small graphs).
    Complexity:   O(V E^2)
    Input:        directed edges (u, v, capacity).
    Returns:      maximum flow value.
    Related:      Dinic.
    CSES:         Download Speed (1694).
    Example:
        >>> edmonds_karp(4, [(0, 1, 3), (0, 2, 2), (1, 3, 2), (2, 3, 3), (1, 2, 1)], 0, 3)
        5
    """
    g: list[list[int]] = [[] for _ in range(n)]
    to: list[int] = []
    cap: list[int] = []
    for u, v, c in edges:
        g[u].append(len(to))
        to.append(v)
        cap.append(c)
        g[v].append(len(to))
        to.append(u)
        cap.append(0)
    flow = 0
    while True:
        pe = [-1] * n  # ребро, по которому пришли
        pe[s] = -2
        q = deque([s])
        while q and pe[t] == -1:
            u = q.popleft()
            for e in g[u]:
                if cap[e] > 0 and pe[to[e]] == -1:
                    pe[to[e]] = e
                    q.append(to[e])
        if pe[t] == -1:
            return flow
        f = INF
        v = t
        while v != s:  # узкое место пути
            e = pe[v]
            f = min(f, cap[e])
            v = to[e ^ 1]
        v = t
        while v != s:
            e = pe[v]
            cap[e] -= f
            cap[e ^ 1] += f
            v = to[e ^ 1]
        flow += f


@algo(tags=["flow", "min-cut"], cses=["Police Chase (1695)"], requires=["INF", "Dinic"])
def min_cut_edges(
    n: int, edges: list[tuple[int, int, int]], s: int, t: int, directed: bool = True
) -> list[int]:
    """Edges of a minimum s-t cut.   # Минимальный разрез.

    When to use:  "remove the cheapest set of edges separating s and t".
    Complexity:   one max flow
    Input:        edges (u, v, cap); directed=False treats each edge as two-way.
    Returns:      indices of cut edges (their capacities sum to the max flow).
    Related:      Dinic.min_cut_side.
    CSES:         Police Chase (1695) (undirected, all capacities 1).
    Example:
        >>> min_cut_edges(4, [(0, 1, 1), (0, 2, 1), (1, 3, 1), (2, 3, 1), (1, 2, 1)], 0, 3, False)
        [0, 1]
    """
    d = Dinic(n)
    for u, v, c in edges:
        d.add_edge(u, v, c, 0 if directed else c)
    d.max_flow(s, t)
    side = d.min_cut_side(s)  # вершины на стороне s
    if directed:
        return [i for i, (u, v, _) in enumerate(edges) if side[u] and not side[v]]
    return [i for i, (u, v, _) in enumerate(edges) if side[u] != side[v]]


@algo(tags=["flow", "disjoint-paths"], cses=["Distinct Routes (1711)"], requires=["INF", "Dinic"])
def edge_disjoint_paths(n: int, edges: list[tuple[int, int]], s: int, t: int) -> list[list[int]]:
    """Maximum set of edge-disjoint directed paths s -> t.   # Рёберно-непересекающиеся пути.

    When to use:  "how many routes without sharing a teleporter" + print them.
    Complexity:   unit-capacity max flow + flow decomposition
    Returns:      list of vertex paths (their number is the maximum).
    Related:      Dinic, hopcroft_karp.
    CSES:         Distinct Routes (1711).
    Example:
        >>> paths = edge_disjoint_paths(4, [(0, 1), (1, 3), (0, 2), (2, 3), (1, 2)], 0, 3)
        >>> sorted(paths)
        [[0, 1, 3], [0, 2, 3]]
    """
    d = Dinic(n)
    ids = [d.add_edge(u, v, 1) for u, v in edges]
    d.max_flow(s, t)
    out: list[list[int]] = [[] for _ in range(n)]
    for (u, v), e in zip(edges, ids):
        if d.flow_on(e) > 0:
            out[u].append(v)  # ребро с потоком
    paths = []
    while out[s]:
        path = [s]
        v = s
        while v != t:  # идём по рёбрам с потоком, удаляя их
            v = out[v].pop()
            path.append(v)
        paths.append(path)
    return paths


@algo(
    tags=["flow", "min-cost-flow", "spfa"],
    cses=["Parcel Delivery (2121)", "Task Assignment"],
    requires=["INF"],
)
class MinCostFlow:
    """Min-cost flow by successive shortest paths (SPFA).   # Поток минимальной стоимости.

    When to use:  send k units as cheaply as possible; assignment problems; grid puzzles.
    Complexity:   O(F * V * E) worst case (SPFA per augmentation)
    Methods:      add_edge(u, v, cap, cost) -> edge id; flow(s, t, max_flow=INF) -> (flow, cost)
    Pitfalls:     no negative cycles in the initial graph.
    Related:      Dinic, hungarian.
    CSES:         Parcel Delivery (2121).
    Example:
        >>> mcf = MinCostFlow(4)
        >>> es = [(0, 1, 2, 1), (0, 2, 1, 2), (1, 3, 1, 3), (2, 3, 2, 1), (1, 2, 1, 1)]
        >>> for u, v, c, w in es:
        ...     _ = mcf.add_edge(u, v, c, w)
        >>> mcf.flow(0, 3, 2)
        (2, 6)
    """

    def __init__(self, n: int) -> None:
        self.n = n
        self.g: list[list[int]] = [[] for _ in range(n)]
        self.to: list[int] = []
        self.cap: list[int] = []
        self.cost: list[int] = []

    def add_edge(self, u: int, v: int, cap: int, cost: int) -> int:
        e = len(self.to)
        self.to += [v, u]
        self.cap += [cap, 0]
        self.cost += [cost, -cost]  # обратное ребро возвращает стоимость
        self.g[u].append(e)
        self.g[v].append(e + 1)
        return e

    def flow(self, s: int, t: int, max_flow: int = INF) -> tuple[int, int]:
        n, to, cap, cost, g = self.n, self.to, self.cap, self.cost, self.g
        flow = total = 0
        while flow < max_flow:
            dist = [INF] * n
            in_q = [False] * n
            pe = [-1] * n
            dist[s] = 0
            q = deque([s])
            while q:  # SPFA: кратчайший по стоимости путь в остаточной сети
                u = q.popleft()
                in_q[u] = False
                du = dist[u]
                for e in g[u]:
                    if cap[e] > 0:
                        v = to[e]
                        nd = du + cost[e]
                        if nd < dist[v]:
                            dist[v] = nd
                            pe[v] = e
                            if not in_q[v]:
                                in_q[v] = True
                                q.append(v)
            if dist[t] >= INF:
                break
            f = max_flow - flow
            v = t
            while v != s:
                f = min(f, cap[pe[v]])
                v = to[pe[v] ^ 1]
            v = t
            while v != s:
                e = pe[v]
                cap[e] -= f
                cap[e ^ 1] += f
                v = to[e ^ 1]
            flow += f
            total += f * dist[t]
        return flow, total
