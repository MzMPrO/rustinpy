"""Shortest paths: 0-1 BFS, Dijkstra and its variants, Bellman-Ford, Floyd-Warshall.

Кратчайшие пути. Взвешенный граф: adj[u] = [(v, w), ...]; список рёбер: (u, v, w).
"""

from __future__ import annotations

import heapq
from collections import deque
from collections.abc import Hashable, Iterable
from typing import Callable, TypeVar

from rustinpy._registry import algo

INF = 1 << 60
MOD7 = 10**9 + 7
H = TypeVar("H", bound=Hashable)


@algo(tags=["0-1-bfs", "shortest-path", "deque"], icpc=["2024 I"], requires=["INF"])
def zero_one_bfs(n: int, adj: list[list[tuple[int, int]]], src: int) -> list[int]:
    """Shortest paths when every weight is 0 or 1 (deque).   # Обход 0-1 BFS на деке.

    When to use:  "free moves and paid moves", grids where turning costs 1, ICPC-UZ 2024 I.
    Complexity:   O(n + m)
    Input:        adj[u] = [(v, w), ...] with w in {0, 1}.
    Returns:      dist[v], INF (= 1 << 60) if unreachable.
    Pitfalls:     a vertex may be pushed twice; skip stale entries by comparing distances.
    Related:      bfs, dijkstra.
    ICPC-UZ:      2024 I.
    Example:
        >>> zero_one_bfs(4, [[(1, 1), (2, 0)], [(3, 0)], [(1, 0)], []], 0)
        [0, 0, 0, 0]
    """
    dist = [INF] * n
    dist[src] = 0
    dq = deque([src])
    while dq:
        u = dq.popleft()
        du = dist[u]
        for v, w in adj[u]:
            nd = du + w
            if nd < dist[v]:  # нашли путь короче - обновляем
                dist[v] = nd
                if w == 0:
                    dq.appendleft(v)  # ребро 0 - в начало очереди
                else:
                    dq.append(v)  # ребро 1 - в конец
    return dist


@algo(tags=["dijkstra", "shortest-path"], cses=["Shortest Routes I (1671)"], requires=["INF"])
def dijkstra(n: int, adj: list[list[tuple[int, int]]], src: int) -> list[int]:
    """Shortest paths from src, non-negative weights.   # Кратчайшие пути из src.

    When to use:  single-source shortest path, weights >= 0.
    Complexity:   O((n + m) log n)
    Input:        adj[u] = [(v, w), ...], 0-indexed vertices.
    Returns:      dist[v], or INF (= 1 << 60) if unreachable.
    Pitfalls:     do not use with negative edges -> bellman_ford.   # Подводные камни
    Python speed: n = m = 2 * 10^5 ~ 0.6 s.
    Related:      bellman_ford, zero_one_bfs, floyd_warshall.
    CSES:         Shortest Routes I (1671).
    Example:
        >>> adj = [[(1, 5)], [(2, 1)], []]
        >>> dijkstra(3, adj, 0)
        [0, 5, 6]
    """
    dist = [INF] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue  # устаревшая запись в куче
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


@algo(tags=["dijkstra", "shortest-path", "path"], cses=["- (restore the route)"], requires=["INF"])
def dijkstra_path(
    n: int, adj: list[list[tuple[int, int]]], src: int, dst: int
) -> tuple[int, list[int]] | None:
    """Shortest distance and one shortest path src -> dst.   # Дейкстра с восстановлением пути.

    When to use:  print the route of minimal cost.
    Complexity:   O((n + m) log n)
    Returns:      (distance, [src, ..., dst]) or None if unreachable.
    Related:      dijkstra, bfs_path.
    CSES:         - (restore the route)
    Example:
        >>> dijkstra_path(4, [[(1, 1), (2, 4)], [(2, 1), (3, 7)], [(3, 1)], []], 0, 3)
        (3, [0, 1, 2, 3])
    """
    dist = [INF] * n
    par = [-1] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == dst:
            break  # дальше можно не считать
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                par[v] = u
                heapq.heappush(pq, (nd, v))
    if dist[dst] >= INF:
        return None
    path = [dst]
    while path[-1] != src:
        path.append(par[path[-1]])
    return dist[dst], path[::-1]


@algo(tags=["dijkstra", "counting"], cses=["Investigation (1202)"], requires=["INF", "MOD7"])
def dijkstra_stats(
    n: int, adj: list[list[tuple[int, int]]], src: int, mod: int = MOD7
) -> tuple[list[int], list[int], list[int], list[int]]:
    """Dijkstra + number of shortest paths, min and max edges among them.   # Статистика путей.

    When to use:  "how many cheapest routes, and their shortest / longest edge counts".
    Complexity:   O((n + m) log n)
    Input:        weights must be POSITIVE (zero edges break the counting order).
    Returns:      (dist, count mod mod, min_edges, max_edges) for every vertex.
    Related:      dijkstra, count_paths_dag.
    CSES:         Investigation (1202).
    Example:
        >>> adj = [[(1, 1), (2, 2)], [(3, 1)], [(3, 1)], []]
        >>> d, c, mn, mx = dijkstra_stats(4, adj, 0)
        >>> d[3], c[3], mn[3], mx[3]
        (2, 1, 2, 2)
    """
    dist = [INF] * n
    cnt = [0] * n
    mn = [0] * n
    mx = [0] * n
    dist[src], cnt[src] = 0, 1 % mod
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:  # новый лучший путь - всё сбрасываем
                dist[v] = nd
                cnt[v] = cnt[u]
                mn[v] = mn[u] + 1
                mx[v] = mx[u] + 1
                heapq.heappush(pq, (nd, v))
            elif nd == dist[v]:  # ещё один кратчайший путь
                cnt[v] = (cnt[v] + cnt[u]) % mod
                mn[v] = min(mn[v], mn[u] + 1)
                mx[v] = max(mx[v], mx[u] + 1)
    return dist, cnt, mn, mx


@algo(tags=["dijkstra", "states", "coupon"], cses=["Flight Discount (1195)"], requires=["INF"])
def dijkstra_coupon(n: int, adj: list[list[tuple[int, int]]], src: int, dst: int) -> int:
    """Cheapest route when one edge may be halved (floor).   # Дейкстра с купоном.

    When to use:  state graph (vertex, coupon used?); generalises to k coupons.
    Complexity:   O((n + m) log n)
    Returns:      minimal cost, INF if unreachable.
    Related:      dijkstra_states.
    CSES:         Flight Discount (1195).
    Example:
        >>> dijkstra_coupon(3, [[(1, 3), (2, 7)], [(2, 5)], []], 0, 2)
        3
    """
    dist = [[INF] * n, [INF] * n]  # dist[использован ли купон][вершина]
    dist[0][src] = 0
    pq = [(0, src, 0)]
    while pq:
        d, u, used = heapq.heappop(pq)
        if d > dist[used][u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[used][v]:
                dist[used][v] = d + w
                heapq.heappush(pq, (d + w, v, used))
            if not used and d + w // 2 < dist[1][v]:  # тратим купон на это ребро
                dist[1][v] = d + w // 2
                heapq.heappush(pq, (d + w // 2, v, 1))
    return min(dist[0][dst], dist[1][dst])


@algo(
    tags=["dijkstra", "states", "generic"], cses=["- (state-space search)"], requires=["INF", "H"]
)
def dijkstra_states(
    start: H, is_target: Callable[[H], bool], nbrs: Callable[[H], Iterable[tuple[H, int]]]
) -> int:
    """Dijkstra over any hashable states (vertex + terminal / mask).   # Дейкстра на состояниях.

    When to use:  the state is more than a vertex: (v, keys), (v, used coupons), (v, time % k).
    Complexity:   O(S log S) over reachable states S
    Input:        nbrs(state) yields (next_state, weight >= 0); states need not be comparable.
    Returns:      distance to the first target popped, INF if none is reachable.
    Related:      dijkstra_coupon, dijkstra.
    CSES:         - (state-space search)
    Example:
        >>> # (вершина, собран ли ключ в вершине 2); цель - вершина 3 с ключом
        >>> g = {0: [(1, 1), (2, 5)], 1: [(3, 1)], 2: [(3, 1)], 3: [(2, 1)]}
        >>> def nbrs(s):
        ...     v, key = s
        ...     for u, w in g[v]:
        ...         yield (u, key or u == 2), w
        >>> dijkstra_states((0, False), lambda s: s == (3, True), nbrs)
        4
    """
    dist: dict[H, int] = {start: 0}
    tie = 0  # счётчик: состояния не сравниваются в куче
    pq: list[tuple[int, int, H]] = [(0, tie, start)]
    while pq:
        d, _, s = heapq.heappop(pq)
        if d > dist[s]:
            continue
        if is_target(s):
            return d
        for t, w in nbrs(s):
            nd = d + w
            if nd < dist.get(t, INF):
                dist[t] = nd
                tie += 1
                heapq.heappush(pq, (nd, tie, t))
    return INF


@algo(tags=["dijkstra", "k-shortest"], cses=["Flight Routes (1196)"])
def k_shortest_walks(
    n: int, adj: list[list[tuple[int, int]]], src: int, dst: int, k: int
) -> list[int]:
    """Costs of the k cheapest walks src -> dst (vertices may repeat).   # k кратчайших маршрутов.

    When to use:  k small (<= 10): pop every vertex at most k times.
    Complexity:   O(k (n + m) log(k m))
    Returns:      up to k costs in non-decreasing order.
    Related:      dijkstra.
    CSES:         Flight Routes (1196).
    Example:
        >>> adj = [[(1, 1), (2, 3)], [(2, 1), (3, 5)], [(3, 1)], [(0, 1)]]
        >>> k_shortest_walks(4, adj, 0, 3, 3)
        [3, 4, 6]
    """
    cnt = [0] * n  # сколько раз вершина уже извлекалась
    res: list[int] = []
    pq = [(0, src)]
    while pq and len(res) < k:
        d, u = heapq.heappop(pq)
        if cnt[u] >= k:
            continue
        cnt[u] += 1
        if u == dst:
            res.append(d)
        for v, w in adj[u]:
            if cnt[v] < k:
                heapq.heappush(pq, (d + w, v))
    return res


@algo(
    tags=["bellman-ford", "negative-weights", "shortest-path"],
    cses=["High Score (1673)"],
    requires=["INF"],
)
def bellman_ford(n: int, edges: list[tuple[int, int, int]], src: int) -> list[int]:
    """Shortest paths with negative edges; -INF where a negative cycle interferes.   # Беллман-Форд.

    When to use:  negative weights, detection of arbitrarily small distances.
    Complexity:   O(n * m)
    Input:        directed edges (u, v, w).
    Returns:      dist[v]: INF unreachable, -INF if a negative cycle reachable from src
                  reaches v, otherwise the exact distance.
    Python speed: ~10^7 edge checks per second (n = 2500, m = 5000 worst case ~0.3 s).
    Related:      find_negative_cycle, max_score_path, dijkstra.
    CSES:         High Score (1673).
    Example:
        >>> d = bellman_ford(4, [(0, 1, 2), (1, 2, -5), (2, 1, 1), (2, 3, 1), (0, 3, 9)], 0)
        >>> [x == -INF for x in d]
        [False, True, True, True]
        >>> bellman_ford(3, [(0, 1, 4), (1, 2, -2)], 0)
        [0, 4, 2]
    """
    dist = [INF] * n
    dist[src] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            du = dist[u]
            if du < INF and du + w < dist[v]:
                dist[v] = du + w
                changed = True
        if not changed:
            return dist  # раннее завершение: цикла нет
    for _ in range(n):  # распространяем -INF от вершин, которые ещё улучшаются
        changed = False
        for u, v, w in edges:
            du = dist[u]
            if du < INF and dist[v] != -INF and (du == -INF or du + w < dist[v]):
                dist[v] = -INF
                changed = True
        if not changed:
            break
    return dist


@algo(tags=["bellman-ford", "negative-cycle"], cses=["Cycle Finding (1197)"])
def find_negative_cycle(n: int, edges: list[tuple[int, int, int]]) -> list[int] | None:
    """Any negative cycle of a directed graph.   # Поиск отрицательного цикла.

    When to use:  arbitrage, "is there a negative cycle and print it".
    Complexity:   O(n * m)
    Returns:      [v0, v1, ..., v0] following the edges, or None.
    Idea:         Bellman-Ford from a virtual source (all dist = 0); a vertex relaxed in the
                  n-th round is reachable from a cycle; walk parents n times to land on it.
    Related:      bellman_ford.
    CSES:         Cycle Finding (1197).
    Example:
        >>> c = find_negative_cycle(4, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 1, -3)])
        >>> c[0] == c[-1], sorted(c[:-1])
        (True, [1, 2, 3])
        >>> find_negative_cycle(2, [(0, 1, 1), (1, 0, 0)]) is None
        True
    """
    dist = [0] * n
    par = [-1] * n
    x = -1
    for _ in range(n):
        x = -1
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                par[v] = u
                x = v
        if x == -1:
            return None
    for _ in range(n):  # гарантированно встаём на цикл
        x = par[x]
    cyc = [x]
    v = par[x]
    while v != x:
        cyc.append(v)
        v = par[v]
    cyc.append(x)
    return cyc[::-1]


@algo(
    tags=["bellman-ford", "longest-path", "positive-cycle"],
    cses=["High Score (1673)"],
    requires=["INF", "bellman_ford"],
)
def max_score_path(n: int, edges: list[tuple[int, int, int]], src: int, dst: int) -> int | None:
    """Max total weight of a path src -> dst; None if unbounded.   # Максимальный путь (High Score).

    When to use:  longest path with possible positive cycles.
    Complexity:   O(n * m)
    Returns:      maximal score, None if arbitrarily large (CSES prints -1),
                  -INF if dst is unreachable.
    Idea:         negate the weights and run bellman_ford: -INF at dst means a positive
                  cycle that is reachable from src and reaches dst.
    Related:      bellman_ford.
    CSES:         High Score (1673).
    Example:
        >>> max_score_path(4, [(0, 1, 3), (1, 2, -2), (2, 3, 4), (0, 3, 1)], 0, 3)
        5
        >>> max_score_path(3, [(0, 1, 1), (1, 0, 1), (1, 2, 1)], 0, 2) is None
        True
    """
    dist = bellman_ford(n, [(u, v, -w) for u, v, w in edges], src)  # максимум = -минимум
    if dist[dst] == -INF:
        return None
    if dist[dst] == INF:
        return -INF
    return -dist[dst]


@algo(tags=["floyd-warshall", "all-pairs"], cses=["Shortest Routes II (1672)"], requires=["INF"])
def floyd_warshall(
    n: int, edges: list[tuple[int, int, int]], directed: bool = False
) -> list[list[int]]:
    """All-pairs shortest paths.   # Флойд-Уоршелл.

    When to use:  n <= ~500 and many distance queries.
    Complexity:   O(n^3)
    Input:        edges (u, v, w); directed=False adds both directions (CSES default).
    Returns:      d[i][j], INF if unreachable.
    Pitfalls:     keep the minimum over parallel edges; negative cycles give d[i][i] < 0.
    Python speed: n = 500 ~ 10 s even with row-wise list comprehensions (n = 300 ~ 2 s).
    Related:      dijkstra (from every vertex if the graph is sparse).
    CSES:         Shortest Routes II (1672).
    Example:
        >>> d = floyd_warshall(3, [(0, 1, 5), (1, 2, 1), (0, 2, 9)])
        >>> d[0][2], d[2][0]
        (6, 6)
    """
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        if w < d[u][v]:
            d[u][v] = w
        if not directed and w < d[v][u]:
            d[v][u] = w
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik < INF:
                row = d[i]
                # строка целиком через list comprehension - быстрее тройного цикла
                d[i] = [x if x <= dik + y else dik + y for x, y in zip(row, dk)]
    return [[x if x < INF // 2 else INF for x in row] for row in d]
