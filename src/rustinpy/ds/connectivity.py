"""Offline connectivity: dynamic connectivity (segment tree over time + rollback DSU),
earliest connection time.

Связность офлайн.
"""

from __future__ import annotations

from rustinpy._registry import algo


@algo(
    tags=["dsu", "rollback", "offline", "divide-and-conquer"], cses=["Dynamic Connectivity (2133)"]
)
def dynamic_connectivity_offline(n: int, events: list[tuple[str, int, int]]) -> list[int]:
    """Components count after each edge addition / removal (offline).   # Динамическая связность.

    When to use:  edges appear and disappear, queries about connectivity; all known in advance.
    Complexity:   O(q log q log n)
    Input:        events ("+", u, v) add edge, ("-", u, v) remove an existing edge.
    Returns:      components count after each event (CSES also wants the initial count:
                  pass the initial edges as "+" events and take the tail).
    Idea:         each edge lives on a time interval -> put it into O(log q) nodes of a
                  segment tree over time; DFS the tree with a rollback DSU (no path
                  compression), undo when leaving a node.
    Related:      graph.RollbackDSU, new_roads_queries.
    CSES:         Dynamic Connectivity (2133).
    Example:
        >>> dynamic_connectivity_offline(3, [("+", 0, 1), ("+", 1, 2), ("-", 0, 1)])
        [2, 1, 2]
    """
    q = len(events)
    if q == 0:
        return []
    size = 1
    while size < q:
        size <<= 1
    seg: list[list[tuple[int, int]]] = [[] for _ in range(2 * size)]

    def add_interval(l: int, r: int, e: tuple[int, int]) -> None:
        l += size
        r += size
        while l < r:  # ребро живёт на [l, r) по времени
            if l & 1:
                seg[l].append(e)
                l += 1
            if r & 1:
                r -= 1
                seg[r].append(e)
            l >>= 1
            r >>= 1

    start: dict[tuple[int, int], int] = {}
    for t, (op, u, v) in enumerate(events):
        key = (min(u, v), max(u, v))
        if op == "+":
            start[key] = t
        else:
            add_interval(start.pop(key), t, key)
    for key, t in start.items():
        add_interval(t, q, key)

    parent = list(range(n))
    sz = [1] * n
    history: list[int] = []  # кого подвесили (для отката)
    comps = n
    res = [0] * q

    def find(x: int) -> int:
        while parent[x] != x:  # без сжатия путей - иначе откат невозможен
            x = parent[x]
        return x

    # обход дерева отрезков без рекурсии: (узел, выход?, сколько объединений сделали)
    stack: list[tuple[int, bool, int]] = [(1, False, 0)]
    while stack:
        node, leaving, cnt = stack.pop()
        if leaving:
            for _ in range(cnt):  # откат объединений этого узла
                b = history.pop()
                a = parent[b]
                sz[a] -= sz[b]
                parent[b] = b
                comps += 1
            continue
        done = 0
        for u, v in seg[node]:
            a, b = find(u), find(v)
            if a != b:
                if sz[a] < sz[b]:
                    a, b = b, a
                parent[b] = a
                sz[a] += sz[b]
                history.append(b)
                comps -= 1
                done += 1
        stack.append((node, True, done))
        if node >= size:
            if node - size < q:
                res[node - size] = comps
        else:
            stack.append((2 * node + 1, False, 0))
            stack.append((2 * node, False, 0))
    return res


@algo(tags=["dsu", "offline", "timestamps"], cses=["New Roads Queries (2101)"])
def new_roads_queries(
    n: int, edges: list[tuple[int, int]], queries: list[tuple[int, int]]
) -> list[int]:
    """Earliest day when a and b get connected (edge i on day i + 1).   # Когда станут связаны.

    When to use:  edges only added, many "since when connected" queries.
    Complexity:   O((m + q) log n)
    Returns:      day (1-based) for each query, 0 if a == b, -1 if never.
    Idea:         DSU with union by size and NO path compression; store the day each node
                  got its parent. Link days increase towards the root, so climb from the
                  endpoint with the smaller link day until both meet.
    Related:      dynamic_connectivity_offline, graph.DSU.
    CSES:         New Roads Queries (2101).
    Example:
        >>> new_roads_queries(5, [(0, 1), (2, 3), (1, 2)], [(0, 3), (0, 4), (2, 3), (1, 1)])
        [3, -1, 2, 0]
    """
    never = 1 << 60
    parent = list(range(n))
    sz = [1] * n
    day = [never] * n  # день, когда узел получил родителя

    def find(x: int) -> int:
        while parent[x] != x:
            x = parent[x]
        return x

    for i, (u, v) in enumerate(edges):
        a, b = find(u), find(v)
        if a != b:
            if sz[a] < sz[b]:
                a, b = b, a
            parent[b] = a
            sz[a] += sz[b]
            day[b] = i + 1
    res = []
    for a, b in queries:
        ans = 0
        while a != b:
            if day[a] > day[b]:
                a, b = b, a  # поднимаем тот, у кого связь с родителем раньше
            if day[a] == never:
                ans = -1
                break
            ans = day[a]
            a = parent[a]
        res.append(ans)
    return res
