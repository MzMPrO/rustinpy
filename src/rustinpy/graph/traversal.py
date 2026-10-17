"""Graph traversals: BFS, iterative DFS, components, bipartiteness, cycles, girth.

Обходы графов. Вершины 0..n-1, adj[u] = список соседей. Всё без рекурсии.
"""

from __future__ import annotations

from collections import deque

from rustinpy._registry import algo


@algo(tags=["bfs", "shortest-path", "unweighted"], cses=["Message Route (1667)"])
def bfs(n: int, adj: list[list[int]], src: int) -> list[int]:
    """Distances in edges from src in an unweighted graph.   # Обход в ширину.

    When to use:  shortest paths when all edges have the same length.
    Complexity:   O(n + m)
    Input:        adj[u] = [v, ...], directed or undirected (store both directions).
    Returns:      dist[v] in edges, -1 if unreachable.
    Related:      bfs_path, multi_source_bfs, zero_one_bfs, dijkstra.
    CSES:         Message Route (1667).
    Example:
        >>> bfs(4, [[1, 2], [3], [3], []], 0)
        [0, 1, 1, 2]
    """
    dist = [-1] * n
    dist[src] = 0
    q = deque([src])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] < 0:  # первый раз - кратчайшее расстояние
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


@algo(tags=["bfs", "path"], cses=["Message Route (1667)"])
def bfs_path(n: int, adj: list[list[int]], src: int, dst: int) -> list[int] | None:
    """One shortest path src -> dst in an unweighted graph.   # Кратчайший путь BFS.

    When to use:  restore the route, not only its length.
    Complexity:   O(n + m)
    Returns:      vertices of the path [src, ..., dst], or None if unreachable.
    Related:      bfs.
    CSES:         Message Route (1667).
    Example:
        >>> bfs_path(5, [[1, 2], [3], [3], [4], []], 0, 4)
        [0, 1, 3, 4]
    """
    par = [-2] * n  # -2 = не посещена
    par[src] = -1
    q = deque([src])
    while q:
        u = q.popleft()
        if u == dst:
            break
        for v in adj[u]:
            if par[v] == -2:
                par[v] = u
                q.append(v)
    if par[dst] == -2:
        return None
    path = [dst]
    while path[-1] != src:  # восстановление по родителям
        path.append(par[path[-1]])
    return path[::-1]


@algo(tags=["bfs", "multi-source"], cses=["Monsters (1194)"])
def multi_source_bfs(n: int, adj: list[list[int]], sources: list[int]) -> list[int]:
    """BFS from many sources at once: distance to the nearest source.   # BFS из многих источников.

    When to use:  "nearest monster / exit / shop" for every vertex.
    Complexity:   O(n + m)
    Returns:      dist[v] to the closest source, -1 if unreachable.
    Related:      bfs, grid_bfs.
    CSES:         Monsters (1194).
    Example:
        >>> multi_source_bfs(5, [[1], [0, 2], [1, 3], [2, 4], [3]], [0, 4])
        [0, 1, 2, 1, 0]
    """
    dist = [-1] * n
    q: deque[int] = deque()
    for s in sources:
        if dist[s] < 0:
            dist[s] = 0  # все источники - на уровне 0
            q.append(s)
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] < 0:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


@algo(tags=["bfs", "grid"], cses=["Labyrinth (1193)", "Counting Rooms (1192)"])
def grid_bfs(grid: list[str], start: tuple[int, int], wall: str = "#") -> list[list[int]]:
    """BFS on a grid with 4-neighbourhood.   # BFS по клетчатому полю.

    When to use:  mazes, labyrinths, flood fill.
    Complexity:   O(R * C)
    Input:        grid rows as strings, start = (row, col), cells equal to wall are blocked.
    Returns:      dist[r][c] in steps, -1 for walls / unreachable cells.
    Pitfalls:     restore the path by walking from the target to a neighbour with dist - 1.
    Related:      multi_source_bfs, bfs.
    CSES:         Labyrinth (1193), Counting Rooms (1192).
    Example:
        >>> grid_bfs(["..#", "...", "#.."], (0, 0))
        [[0, 1, -1], [1, 2, 3], [-1, 3, 4]]
    """
    R, C = len(grid), len(grid[0]) if grid else 0
    dist = [[-1] * C for _ in range(R)]
    sr, sc = start
    if grid[sr][sc] == wall:
        return dist
    dist[sr][sc] = 0
    q = deque([start])
    while q:
        r, c = q.popleft()
        d = dist[r][c] + 1
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):  # 4 соседа
            if 0 <= nr < R and 0 <= nc < C and dist[nr][nc] < 0 and grid[nr][nc] != wall:
                dist[nr][nc] = d  # впервые достигли - кратчайшее
                q.append((nr, nc))
    return dist


@algo(tags=["dfs", "iterative"], cses=["Building Roads (1666)"])
def dfs_order(n: int, adj: list[list[int]], src: int) -> tuple[list[int], list[int]]:
    """Iterative DFS: preorder and DFS-tree parents.   # Итеративный обход в глубину.

    When to use:  any DFS on 10^5+ vertices (recursion would overflow the stack).
    Complexity:   O(n + m)
    Returns:      (order, parent): vertices in visiting order from src, parent[src] = -1,
                  parent[v] = -2 for unreachable v.
    Pitfalls:     the visiting order equals the recursive DFS order (neighbours in adj order).
    Related:      connected_components, scc_tarjan, bridges.
    CSES:         Building Roads (1666).
    Example:
        >>> dfs_order(5, [[1, 2], [0, 3], [0], [1], []], 0)
        ([0, 1, 3, 2], [-1, 0, 0, 1, -2])
    """
    parent = [-2] * n
    parent[src] = -1
    order = [src]
    it = [0] * n  # индекс следующего соседа - заменяет стек вызовов
    stack = [src]
    while stack:
        u = stack[-1]
        if it[u] < len(adj[u]):
            v = adj[u][it[u]]
            it[u] += 1
            if parent[v] == -2:
                parent[v] = u
                order.append(v)
                stack.append(v)
        else:
            stack.pop()
    return order, parent


@algo(tags=["components", "bfs"], cses=["Building Roads (1666)", "Counting Rooms (1192)"])
def connected_components(n: int, adj: list[list[int]]) -> tuple[int, list[int]]:
    """Connected components of an undirected graph.   # Компоненты связности.

    When to use:  count / label components; "how many roads to connect everything".
    Complexity:   O(n + m)
    Returns:      (k, comp) with comp[v] in 0..k-1.
    Related:      DSU, bfs.
    CSES:         Building Roads (1666) (answer k - 1 roads), Counting Rooms (1192).
    Example:
        >>> connected_components(5, [[1], [0], [], [4], [3]])
        (3, [0, 0, 1, 2, 2])
    """
    comp = [-1] * n
    k = 0
    for s in range(n):
        if comp[s] >= 0:
            continue
        comp[s] = k
        stack = [s]
        while stack:  # обход компоненты стеком
            u = stack.pop()
            for v in adj[u]:
                if comp[v] < 0:
                    comp[v] = k
                    stack.append(v)
        k += 1
    return k, comp


@algo(tags=["bipartite", "coloring", "bfs"], cses=["Building Teams (1668)"])
def bipartite_coloring(n: int, adj: list[list[int]]) -> list[int] | None:
    """2-colouring of an undirected graph, or None if it has an odd cycle.   # Двудольность.

    When to use:  split into two groups with every edge between groups.
    Complexity:   O(n + m)
    Returns:      color[v] in {0, 1}, or None if not bipartite.
    Related:      find_cycle_undirected, hopcroft_karp.
    CSES:         Building Teams (1668) (print color + 1).
    Example:
        >>> bipartite_coloring(4, [[1, 3], [0, 2], [1, 3], [0, 2]])
        [0, 1, 0, 1]
        >>> bipartite_coloring(3, [[1, 2], [0, 2], [0, 1]]) is None
        True
    """
    color = [-1] * n
    for s in range(n):
        if color[s] >= 0:
            continue
        color[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if color[v] < 0:
                    color[v] = color[u] ^ 1  # сосед - в другую долю
                    q.append(v)
                elif color[v] == color[u]:
                    return None  # нечётный цикл
    return color


@algo(tags=["cycle", "dfs", "undirected"], cses=["Round Trip (1669)"])
def find_cycle_undirected(n: int, adj: list[list[int]]) -> list[int] | None:
    """Any cycle of a simple undirected graph.   # Цикл в неориентированном графе.

    When to use:  "find a round trip": cycle of length >= 3.
    Complexity:   O(n + m)
    Input:        simple graph (no loops, no multi-edges), both directions stored.
    Returns:      [v0, v1, ..., v0] (first vertex repeated at the end), or None.
    Related:      find_cycle_directed, girth.
    CSES:         Round Trip (1669).
    Example:
        >>> find_cycle_undirected(4, [[1], [0, 2, 3], [1, 3], [1, 2]])
        [1, 2, 3, 1]
    """
    state = [0] * n  # 0 - не были, 1 - на стеке, 2 - обработана
    parent = [-1] * n
    it = [0] * n
    for s in range(n):
        if state[s]:
            continue
        state[s] = 1
        stack = [s]
        while stack:
            u = stack[-1]
            if it[u] < len(adj[u]):
                v = adj[u][it[u]]
                it[u] += 1
                if v == parent[u]:
                    continue
                if state[v] == 1:  # обратное ребро к предку - цикл
                    cyc = [u]
                    while cyc[-1] != v:
                        cyc.append(parent[cyc[-1]])
                    cyc.reverse()
                    return [*cyc, cyc[0]]
                if state[v] == 0:
                    state[v] = 1
                    parent[v] = u
                    stack.append(v)
            else:
                state[u] = 2
                stack.pop()
    return None


@algo(tags=["cycle", "dfs", "directed"], cses=["Round Trip II (1678)"])
def find_cycle_directed(n: int, adj: list[list[int]]) -> list[int] | None:
    """Any directed cycle (three-colour DFS).   # Цикл в ориентированном графе.

    When to use:  check that a dependency graph is acyclic and print a cycle otherwise.
    Complexity:   O(n + m)
    Returns:      [v0, v1, ..., v0], or None if the graph is a DAG.
    Related:      toposort_kahn, find_cycle_undirected.
    CSES:         Round Trip II (1678).
    Example:
        >>> find_cycle_directed(4, [[1], [2], [3], [1]])
        [1, 2, 3, 1]
        >>> find_cycle_directed(3, [[1], [2], []]) is None
        True
    """
    color = [0] * n  # 0 белая, 1 серая (на стеке), 2 чёрная
    parent = [-1] * n
    it = [0] * n
    for s in range(n):
        if color[s]:
            continue
        color[s] = 1
        stack = [s]
        while stack:
            u = stack[-1]
            if it[u] < len(adj[u]):
                v = adj[u][it[u]]
                it[u] += 1
                if color[v] == 1:  # ребро в серую вершину - цикл
                    cyc = [u]
                    while cyc[-1] != v:
                        cyc.append(parent[cyc[-1]])
                    cyc.reverse()
                    return [*cyc, cyc[0]]
                if color[v] == 0:
                    color[v] = 1
                    parent[v] = u
                    stack.append(v)
            else:
                color[u] = 2
                stack.pop()
    return None


@algo(tags=["cycle", "girth", "bfs"], cses=["Graph Girth (1707)"])
def girth(n: int, adj: list[list[int]]) -> int:
    """Length of the shortest cycle of a simple undirected graph.   # Обхват графа.

    When to use:  shortest cycle, n <= ~2500.
    Complexity:   O(n * (n + m))
    Returns:      shortest cycle length, -1 if the graph is a forest.
    Python speed: n = m = 2500 ~ 1.2 s in the worst case (one long cycle).
    Idea:         BFS from every vertex; a non-tree edge (u, w) closes a cycle of length
                  dist[u] + dist[w] + 1 (the minimum over all sources is exact).
    Related:      find_cycle_undirected.
    CSES:         Graph Girth (1707).
    Example:
        >>> girth(5, [[1, 4], [0, 2], [1, 3], [2, 4], [3, 0]])
        5
        >>> girth(3, [[1], [0, 2], [1]])
        -1
    """
    best = n + 1
    for s in range(n):
        dist = [-1] * n
        par = [-1] * n
        dist[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            if 2 * dist[u] >= best:
                break  # дальше циклы не короче найденного
            for w in adj[u]:
                if dist[w] < 0:
                    dist[w] = dist[u] + 1
                    par[w] = u
                    q.append(w)
                elif w != par[u]:
                    best = min(best, dist[u] + dist[w] + 1)  # ребро замыкает цикл
    return best if best <= n else -1
