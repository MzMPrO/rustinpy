"""Bipartite matching (Hopcroft-Karp, Kuhn) and the assignment problem (Hungarian).

Паросочетания в двудольных графах и задача о назначениях.
"""

from __future__ import annotations

from collections import deque

from rustinpy._registry import algo

INF = 1 << 60


@algo(tags=["matching", "hopcroft-karp", "bipartite"], cses=["School Dance (1696)"])
def hopcroft_karp(n_left: int, n_right: int, adj: list[list[int]]) -> tuple[int, list[int]]:
    """Maximum bipartite matching, Hopcroft-Karp with iterative DFS.   # Хопкрофт-Карп.

    When to use:  large bipartite matching (10^5 edges and more).
    Complexity:   O(E sqrt V)
    Input:        adj[u] = right vertices 0..n_right-1 adjacent to left vertex u.
    Returns:      (size, match_left) with match_left[u] = right partner or -1.
    Related:      kuhn_matching, Dinic, coin_grid (Konig).
    CSES:         School Dance (1696).
    Example:
        >>> hopcroft_karp(3, 3, [[0, 1], [0], [1, 2]])
        (3, [1, 0, 2])
    """
    match_l = [-1] * n_left
    match_r = [-1] * n_right
    while True:
        dist = [-1] * n_left
        q: deque[int] = deque()
        for u in range(n_left):
            if match_l[u] == -1:
                dist[u] = 0
                q.append(u)
        found = False
        while q:  # BFS: слои от свободных левых вершин
            u = q.popleft()
            for v in adj[u]:
                w = match_r[v]
                if w == -1:
                    found = True
                elif dist[w] == -1:
                    dist[w] = dist[u] + 1
                    q.append(w)
        if not found:
            break
        it = [0] * n_left
        for root in range(n_left):
            if match_l[root] != -1:
                continue
            stack = [root]
            via: list[int] = []  # правые вершины на текущем пути
            while stack:
                x = stack[-1]
                if it[x] < len(adj[x]):
                    v = adj[x][it[x]]
                    it[x] += 1
                    w = match_r[v]
                    if w == -1:  # увеличивающий путь найден - переворачиваем
                        via.append(v)
                        for xx, vv in zip(stack, via):
                            match_l[xx] = vv
                            match_r[vv] = xx
                        break
                    if dist[w] == dist[x] + 1:
                        via.append(v)
                        stack.append(w)
                else:
                    dist[x] = -1  # тупик: вершина больше не используется в фазе
                    stack.pop()
                    if via:
                        via.pop()
    return sum(1 for x in match_l if x != -1), match_l


@algo(tags=["matching", "kuhn", "bipartite"], cses=["School Dance (1696)"])
def kuhn_matching(n_left: int, n_right: int, adj: list[list[int]]) -> tuple[int, list[int]]:
    """Maximum bipartite matching by Kuhn's augmenting paths (iterative).   # Алгоритм Куна.

    When to use:  small graphs (V <= ~1000); the shortest code to remember.
    Complexity:   O(V * E)
    Returns:      (size, match_left), match_left[u] = right partner or -1.
    Related:      hopcroft_karp.
    CSES:         School Dance (1696).
    Example:
        >>> kuhn_matching(3, 2, [[0], [0, 1], [1]])
        (2, [0, 1, -1])
    """
    match_l = [-1] * n_left
    match_r = [-1] * n_right
    for root in range(n_left):
        seen = [False] * n_right
        it = {root: 0}
        stack = [root]
        via: list[int] = []
        while stack:
            x = stack[-1]
            i = it[x]
            if i < len(adj[x]):
                it[x] = i + 1
                v = adj[x][i]
                if seen[v]:
                    continue
                seen[v] = True
                w = match_r[v]
                via.append(v)
                if w == -1:  # свободная правая вершина - чередуем путь
                    for xx, vv in zip(stack, via):
                        match_l[xx] = vv
                        match_r[vv] = xx
                    break
                it[w] = 0
                stack.append(w)
            else:
                stack.pop()
                if via:
                    via.pop()
    return sum(1 for x in match_l if x != -1), match_l


@algo(
    tags=["assignment", "hungarian", "matching"], cses=["Task Assignment (2129)"], requires=["INF"]
)
def hungarian(cost: list[list[int]]) -> tuple[int, list[int]]:
    """Minimum-cost assignment of n rows to distinct columns (n <= m).   # Венгерский алгоритм.

    When to use:  assign workers to tasks minimising total cost (maximise: negate costs).
    Complexity:   O(n^2 m)
    Returns:      (minimal total cost, col[i] chosen for row i).
    Python speed: n = m = 500 ~ 0.7 s.
    Related:      MinCostFlow.
    CSES:         Task Assignment (2129).
    Example:
        >>> hungarian([[17, 8, 16], [3, 11, 8], [9, 13, 6]])
        (17, [1, 0, 2])
    """
    n, m = len(cost), len(cost[0]) if cost else 0
    u = [0] * (n + 1)  # потенциалы строк
    v = [0] * (m + 1)  # потенциалы столбцов
    p = [0] * (m + 1)  # p[j] - строка, назначенная столбцу j (1-based)
    way = [0] * (m + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [INF] * (m + 1)
        used = [False] * (m + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            row = cost[i0 - 1]
            delta, j1 = INF, 0
            for j in range(1, m + 1):
                if not used[j]:
                    cur = row[j - 1] - u[i0] - v[j]  # приведённая стоимость
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta, j1 = minv[j], j
            for j in range(m + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while j0:  # разворачиваем чередующуюся цепочку
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
    col = [-1] * n
    for j in range(1, m + 1):
        if p[j]:
            col[p[j] - 1] = j - 1
    return sum(cost[i][col[i]] for i in range(n)), col
