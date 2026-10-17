"""Advanced graph problems from CSES: critical cities, flight requests, renovations, orientations.

Продвинутые задачи на графы.
"""

from __future__ import annotations

from collections import deque

from rustinpy._registry import algo


@algo(tags=["dominators", "path", "bfs"], cses=["Critical Cities (1703)"])
def critical_cities(n: int, adj: list[list[int]]) -> list[int]:
    """Vertices lying on EVERY path 0 -> n-1 of a directed graph.   # Критические города.

    When to use:  dominators of the target restricted to one source-target pair.
    Complexity:   O(n + m)
    Returns:      sorted list (contains 0 and n - 1), [] if n - 1 is unreachable.
    Idea:         take any path p_0..p_k; walk along it, expanding everything reachable without
                  stepping onto path vertices (stop there, remember the farthest index);
                  p_i is critical iff the farthest index reached before passing p_i is i.
    Related:      articulation_points, bfs_path.
    CSES:         Critical Cities (1703).
    Example:
        >>> critical_cities(5, [[1, 2], [3], [3], [4], []])
        [0, 3, 4]
    """
    par = [-2] * n
    par[0] = -1
    q = deque([0])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if par[v] == -2:
                par[v] = u
                q.append(v)
    if par[n - 1] == -2:
        return []
    path = [n - 1]
    while path[-1] != 0:
        path.append(par[path[-1]])
    path.reverse()
    idx = [-1] * n  # номер вершины на пути
    for i, v in enumerate(path):
        idx[v] = i
    seen = [False] * n
    far = 0
    res = [path[0]]

    def expand(s: int) -> int:
        best = 0
        stack = [s]
        while stack:  # обходим, не наступая на вершины пути
            u = stack.pop()
            for v in adj[u]:
                if idx[v] >= 0:
                    best = max(best, idx[v])
                elif not seen[v]:
                    seen[v] = True
                    stack.append(v)
        return best

    far = expand(path[0])
    for i in range(1, len(path)):
        if far == i:
            res.append(path[i])  # дальше i не перепрыгнуть - город критический
        far = max(far, expand(path[i]))
    return sorted(res)


@algo(tags=["dsu", "dag", "construction"], cses=["Flight Route Requests (1699)"])
def flight_route_requests(n: int, pairs: list[tuple[int, int]]) -> int:
    """Fewest one-way routes so that every a reaches b.   # Запросы на маршруты.

    When to use:  reachability requirements per weakly connected component.
    Complexity:   O(n + m)
    Returns:      minimal number of directed edges.
    Idea:         in a weak component of size s the requests need s - 1 edges (a path in
                  topological order) if they form a DAG, otherwise s edges (one big cycle).
    Related:      toposort_kahn, DSU.
    CSES:         Flight Route Requests (1699).
    Example:
        >>> flight_route_requests(4, [(0, 1), (1, 2), (0, 3)])
        3
        >>> flight_route_requests(3, [(0, 1), (1, 2), (2, 0)])
        3
    """
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    adj: list[list[int]] = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in pairs:
        adj[a].append(b)
        indeg[b] += 1
        parent[find(a)] = find(b)  # слабая связность
    size: dict[int, int] = {}
    for v in range(n):
        r = find(v)
        size[r] = size.get(r, 0) + 1
    q = deque(v for v in range(n) if indeg[v] == 0)
    done = [False] * n
    while q:  # Кан: оставшиеся вершины лежат на циклах или за ними
        u = q.popleft()
        done[u] = True
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    cyclic = {find(v) for v in range(n) if not done[v]}
    return sum(s if r in cyclic else s - 1 for r, s in size.items())


@algo(
    tags=["tree", "leaves", "construction", "2-edge-connected"], cses=["Network Renovation (1704)"]
)
def network_renovation(n: int, edges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """New edges making a tree 2-edge-connected (no bridges).   # Ремонт сети.

    When to use:  a tree must survive the failure of any single edge.
    Complexity:   O(n)
    Input:        tree on n >= 2 vertices.
    Returns:      ceil(L / 2) new edges, L = number of leaves.
    Idea:         list leaves in DFS order, join leaf i with leaf i + L // 2.
    Related:      bridges.
    CSES:         Network Renovation (1704).
    Example:
        >>> network_renovation(5, [(0, 1), (0, 2), (0, 3), (3, 4)])
        [(1, 2), (2, 4)]
    """
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    root = next((v for v in range(n) if len(adj[v]) > 1), 0)
    leaves = []
    seen = [False] * n
    seen[root] = True
    stack = [root]
    while stack:  # DFS-порядок листьев
        u = stack.pop()
        if len(adj[u]) == 1:
            leaves.append(u)
        for v in reversed(adj[u]):
            if not seen[v]:
                seen[v] = True
                stack.append(v)
    L = len(leaves)
    half = L // 2
    return [(leaves[i], leaves[i + half]) for i in range((L + 1) // 2)]


@algo(tags=["orientation", "dfs", "strong-connectivity"], cses=["Strongly Connected Edges (2177)"])
def strongly_connected_edges(n: int, edges: list[tuple[int, int]]) -> list[tuple[int, int]] | None:
    """Orient edges to make the graph strongly connected.   # Ориентация до сильной связности.

    When to use:  possible iff the graph is connected and bridgeless (Robbins' theorem).
    Complexity:   O(n + m)
    Returns:      oriented edges in input order, or None.
    Idea:         DFS tree edges point down, back edges point up; then verify.
    Related:      bridges, scc_tarjan.
    CSES:         Strongly Connected Edges (2177).
    Example:
        >>> strongly_connected_edges(3, [(0, 1), (1, 2), (2, 0)])
        [(0, 1), (1, 2), (2, 0)]
        >>> strongly_connected_edges(3, [(0, 1), (1, 2)]) is None
        True
    """
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))
        adj[v].append((u, i))
    res: list[tuple[int, int] | None] = [None] * len(edges)
    seen = [False] * n
    it = [0] * n
    seen[0] = True
    stack = [0]
    while stack:
        u = stack[-1]
        if it[u] < len(adj[u]):
            v, e = adj[u][it[u]]
            it[u] += 1
            if res[e] is None:
                res[e] = (u, v)  # первое прохождение задаёт направление
                if not seen[v]:
                    seen[v] = True
                    stack.append(v)
        else:
            stack.pop()
    oriented = [x for x in res if x is not None]
    if len(oriented) != len(edges) or not all(seen):
        return None
    for direction in (0, 1):  # проверка: из 0 достижимо всё в графе и в обратном графе
        g: list[list[int]] = [[] for _ in range(n)]
        for a, b in oriented:
            if direction:
                g[b].append(a)
            else:
                g[a].append(b)
        vis = [False] * n
        vis[0] = True
        st = [0]
        while st:
            x = st.pop()
            for y in g[x]:
                if not vis[y]:
                    vis[y] = True
                    st.append(y)
        if not all(vis):
            return None
    return oriented


@algo(tags=["orientation", "dfs", "parity"], cses=["Even Outdegree Edges (2179)"])
def even_outdegree_edges(n: int, edges: list[tuple[int, int]]) -> list[tuple[int, int]] | None:
    """Orient edges so every vertex has even out-degree.   # Чётные исходящие степени.

    When to use:  possible iff every connected component has an even number of edges.
    Complexity:   O(n + m)
    Returns:      oriented edges in input order, or None.
    Idea:         orient non-tree edges arbitrarily; then from the leaves of a DFS tree up,
                  orient each tree edge to fix the parity of the lower endpoint.
    Related:      strongly_connected_edges.
    CSES:         Even Outdegree Edges (2179).
    Example:
        >>> res = even_outdegree_edges(4, [(0, 1), (1, 2), (2, 3), (3, 0)])
        >>> out = [0] * 4
        >>> for a, b in res: out[a] += 1
        >>> all(x % 2 == 0 for x in out)
        True
        >>> even_outdegree_edges(3, [(0, 1), (1, 2), (2, 0)]) is None
        True
    """
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))
        adj[v].append((u, i))
    parent = [-1] * n
    pedge = [-1] * n
    order: list[int] = []
    seen = [False] * n
    roots = []
    for s in range(n):
        if seen[s]:
            continue
        seen[s] = True
        roots.append(s)
        stack = [s]
        while stack:  # остовный лес
            u = stack.pop()
            order.append(u)
            for v, e in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    parent[v] = u
                    pedge[v] = e
                    stack.append(v)
    tree = set(pedge)
    res: list[tuple[int, int]] = [(u, v) for u, v in edges]
    out = [0] * n
    for i, (u, _) in enumerate(edges):
        if i not in tree:
            out[u] += 1  # нерёберные дерева - как есть
    for v in reversed(order):  # дети раньше родителей
        p = parent[v]
        if p == -1:
            continue
        if out[v] % 2:
            res[pedge[v]] = (v, p)
            out[v] += 1
        else:
            res[pedge[v]] = (p, v)
            out[p] += 1
    if any(out[r] % 2 for r in roots):
        return None
    return res


@algo(tags=["shortest-path", "companies"], cses=["Bus Companies"], verified=False, stub=True)
def bus_companies(n: int, companies: list[tuple[int, list[int]]]) -> list[int]:
    """CSES Bus Companies - not implemented yet.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return the cheapest prices from city 0.
    Idea:         Dijkstra on an auxiliary graph with one extra vertex per company (enter
                  = pay the company price, leave for free). NOT VERIFIED: statement unknown.
    CSES:         Bus Companies.
    Example:
        >>> bus_companies(1, [])
        Traceback (most recent call last):
        NotImplementedError: CSES Bus Companies: statement not verified yet
    """
    # NOT VERIFIED: заглушка, условие задачи не сверено
    raise NotImplementedError("CSES Bus Companies: statement not verified yet")
