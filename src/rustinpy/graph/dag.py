"""Directed acyclic graphs: topological orders, path counting, longest path, reachability.

Ациклические графы (DAG).
"""

from __future__ import annotations

import heapq
from collections import deque

from rustinpy._registry import algo

MOD7 = 10**9 + 7


@algo(tags=["toposort", "kahn", "dag"], cses=["Course Schedule (1679)"])
def toposort_kahn(n: int, adj: list[list[int]]) -> list[int] | None:
    """Topological order by Kahn's algorithm.   # Топологическая сортировка (Кан).

    When to use:  order tasks with dependencies u -> v ("u before v").
    Complexity:   O(n + m)
    Returns:      order of all vertices, or None if there is a cycle.
    Related:      toposort_lex_min, find_cycle_directed.
    CSES:         Course Schedule (1679).
    Example:
        >>> toposort_kahn(4, [[1, 2], [3], [3], []])
        [0, 1, 2, 3]
        >>> toposort_kahn(2, [[1], [0]]) is None
        True
    """
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1
    q = deque(v for v in range(n) if indeg[v] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:  # все зависимости выполнены
                q.append(v)
    return order if len(order) == n else None


@algo(tags=["toposort", "lexicographic", "heap"], cses=["- (lexicographically smallest order)"])
def toposort_lex_min(n: int, adj: list[list[int]]) -> list[int] | None:
    """Lexicographically smallest topological order.   # Лексикографически первая топосортировка.

    When to use:  "print the smallest order" among all valid ones.
    Complexity:   O((n + m) log n)
    Returns:      order, or None if there is a cycle.
    Pitfalls:     this is NOT "vertex 0 as early as possible" -> toposort_smallest_first.
    Related:      toposort_kahn, toposort_smallest_first.
    CSES:         - (lexicographically smallest order)
    Example:
        >>> toposort_lex_min(4, [[], [0], [], [2]])
        [1, 0, 3, 2]
        >>> toposort_lex_min(3, [[], [], [0]])  # 0 оказался на месте 2
        [1, 2, 0]
    """
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1
    pq = [v for v in range(n) if indeg[v] == 0]
    heapq.heapify(pq)
    order = []
    while pq:
        u = heapq.heappop(pq)  # всегда наименьшая доступная вершина
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(pq, v)
    return order if len(order) == n else None


@algo(tags=["toposort", "reverse-graph", "heap"], cses=["Course Schedule II (1757)"])
def toposort_smallest_first(n: int, adj: list[list[int]]) -> list[int] | None:
    """Order with vertex 0 as early as possible, then 1, ...   # Курс «Course Schedule II».

    When to use:  "course 1 as soon as possible, then course 2, ..." (not lexicographic!).
    Complexity:   O((n + m) log n)
    Returns:      order, or None if there is a cycle.
    Idea:         reverse the edges, repeatedly take the LARGEST available vertex, reverse
                  the result.
    Related:      toposort_lex_min.
    CSES:         Course Schedule II (1757).
    Example:
        >>> toposort_smallest_first(4, [[], [0], [], [2]])
        [1, 0, 3, 2]
        >>> toposort_smallest_first(3, [[], [], [0]])  # 0 на месте 1, раньше, чем у lex_min
        [2, 0, 1]
    """
    radj: list[list[int]] = [[] for _ in range(n)]
    outdeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            radj[v].append(u)  # обратное ребро
            outdeg[u] += 1
    pq = [-v for v in range(n) if outdeg[v] == 0]
    heapq.heapify(pq)
    order = []
    while pq:
        u = -heapq.heappop(pq)  # наибольшая доступная в обратном графе
        order.append(u)
        for v in radj[u]:
            outdeg[v] -= 1
            if outdeg[v] == 0:
                heapq.heappush(pq, -v)
    return order[::-1] if len(order) == n else None


@algo(tags=["dag", "counting", "dp"], cses=["Game Routes (1681)"], requires=["MOD7"])
def count_paths_dag(n: int, adj: list[list[int]], src: int, dst: int, mod: int = MOD7) -> int:
    """Number of paths src -> dst in a DAG.   # Количество путей в DAG.

    When to use:  counting routes in acyclic graphs (DP in topological order).
    Complexity:   O(n + m)
    Returns:      count mod mod (0 if unreachable).
    Related:      toposort_kahn, longest_path_dag.
    CSES:         Game Routes (1681).
    Example:
        >>> count_paths_dag(4, [[1, 2], [3], [3], []], 0, 3)
        2
    """
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1
    ways = [0] * n
    ways[src] = 1 % mod
    q = deque(v for v in range(n) if indeg[v] == 0)
    while q:
        u = q.popleft()
        wu = ways[u]
        for v in adj[u]:
            if wu:
                ways[v] = (ways[v] + wu) % mod  # пути в v через u
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return ways[dst]


@algo(tags=["dag", "longest-path", "dp"], cses=["Longest Flight Route (1680)"])
def longest_path_dag(n: int, adj: list[list[int]], src: int, dst: int) -> list[int] | None:
    """Path src -> dst with the most vertices in a DAG.   # Самый длинный путь в DAG.

    When to use:  maximise the number of visited cities on an acyclic route.
    Complexity:   O(n + m)
    Returns:      vertices of a longest path, or None if dst is unreachable.
    Related:      count_paths_dag, toposort_kahn.
    CSES:         Longest Flight Route (1680).
    Example:
        >>> longest_path_dag(5, [[1, 3], [2], [4], [4], []], 0, 4)
        [0, 1, 2, 4]
    """
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1
    best = [-1] * n  # число вершин на лучшем пути из src
    par = [-1] * n
    best[src] = 1
    q = deque(v for v in range(n) if indeg[v] == 0)
    while q:
        u = q.popleft()
        for v in adj[u]:
            if best[u] > 0 and best[u] + 1 > best[v]:
                best[v] = best[u] + 1
                par[v] = u
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if best[dst] < 0:
        return None
    path = [dst]
    while path[-1] != src:
        path.append(par[path[-1]])
    return path[::-1]


@algo(tags=["dag", "reachability", "bitset"], cses=["Reachable Nodes (2138)"])
def reachable_counts(n: int, adj: list[list[int]]) -> list[int]:
    """How many vertices each vertex of a DAG reaches (itself too).   # Достижимые вершины.

    When to use:  transitive closure sizes; bitsets as Python ints (C speed OR).
    Complexity:   O(n * m / 64) word operations
    Returns:      cnt[v] = |{u : v reaches u}|.
    Python speed: n = 5 * 10^4, m = 10^5 ~ 3 s (ints of 50000 bits).
    Related:      reachability_queries (general digraphs).
    CSES:         Reachable Nodes (2138).
    Example:
        >>> reachable_counts(4, [[1, 2], [3], [3], []])
        [4, 2, 2, 1]
    """
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1
    q = deque(v for v in range(n) if indeg[v] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    reach = [0] * n
    for u in reversed(order):  # дети раньше родителей
        r = 1 << u
        for v in adj[u]:
            r |= reach[v]
        reach[u] = r
    return [bin(r).count("1") for r in reach]
