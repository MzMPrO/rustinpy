"""Strongly connected components, condensation, 2-SAT, bridges, articulation points.

Компоненты сильной связности и всё, что на них строится. Всё итеративно.
"""

from __future__ import annotations

from rustinpy._registry import algo


@algo(tags=["scc", "tarjan"], cses=["Planets and Kingdoms (1683)"])
def scc_tarjan(n: int, adj: list[list[int]]) -> tuple[int, list[int]]:
    """Strongly connected components by Tarjan (iterative).   # Компоненты сильной связности.

    When to use:  condensation of a directed graph, 2-SAT, "which cities form a kingdom".
    Complexity:   O(n + m)
    Returns:      (k, comp): comp[v] in 0..k-1 numbered in TOPOLOGICAL order of the
                  condensation (every edge goes from a smaller or equal id to a larger one).
    Related:      scc_kosaraju, condensation, two_sat.
    CSES:         Planets and Kingdoms (1683) (print comp + 1).
    Example:
        >>> scc_tarjan(5, [[1], [2], [0, 3], [4], [3]])
        (2, [0, 0, 0, 1, 1])
    """
    index = [-1] * n
    low = [0] * n
    on_stack = [False] * n
    comp = [-1] * n
    it = [0] * n
    st: list[int] = []
    counter = k = 0
    for s in range(n):
        if index[s] != -1:
            continue
        index[s] = low[s] = counter
        counter += 1
        st.append(s)
        on_stack[s] = True
        call = [s]  # явный стек вызовов
        while call:
            u = call[-1]
            if it[u] < len(adj[u]):
                v = adj[u][it[u]]
                it[u] += 1
                if index[v] == -1:
                    index[v] = low[v] = counter
                    counter += 1
                    st.append(v)
                    on_stack[v] = True
                    call.append(v)
                elif on_stack[v] and index[v] < low[u]:
                    low[u] = index[v]
            else:
                call.pop()
                if call and low[u] < low[call[-1]]:
                    low[call[-1]] = low[u]  # «возврат из рекурсии»
                if low[u] == index[u]:  # u - корень компоненты
                    while True:
                        w = st.pop()
                        on_stack[w] = False
                        comp[w] = k
                        if w == u:
                            break
                    k += 1
    # Тарьян выдаёт компоненты в обратном топологическом порядке
    return k, [k - 1 - c for c in comp]


@algo(tags=["scc", "kosaraju"], cses=["Planets and Kingdoms (1683)"])
def scc_kosaraju(n: int, adj: list[list[int]]) -> tuple[int, list[int]]:
    """Strongly connected components by Kosaraju (two iterative passes).   # Алгоритм Косараю.

    When to use:  same as scc_tarjan; easier to remember.
    Complexity:   O(n + m)
    Returns:      (k, comp) in topological order of the condensation.
    Related:      scc_tarjan.
    CSES:         Planets and Kingdoms (1683).
    Example:
        >>> scc_kosaraju(5, [[1], [2], [0, 3], [4], [3]])
        (2, [0, 0, 0, 1, 1])
    """
    seen = [False] * n
    order: list[int] = []  # порядок выхода
    it = [0] * n
    for s in range(n):
        if seen[s]:
            continue
        seen[s] = True
        stack = [s]
        while stack:
            u = stack[-1]
            if it[u] < len(adj[u]):
                v = adj[u][it[u]]
                it[u] += 1
                if not seen[v]:
                    seen[v] = True
                    stack.append(v)
            else:
                order.append(stack.pop())
    radj: list[list[int]] = [[] for _ in range(n)]
    for u in range(n):
        for v in adj[u]:
            radj[v].append(u)
    comp = [-1] * n
    k = 0
    for s in reversed(order):  # по убыванию времени выхода, в обратном графе
        if comp[s] != -1:
            continue
        comp[s] = k
        stack = [s]
        while stack:
            u = stack.pop()
            for v in radj[u]:
                if comp[v] == -1:
                    comp[v] = k
                    stack.append(v)
        k += 1
    return k, comp


@algo(tags=["scc", "condensation", "dag"], cses=["Coin Collector (1686)"])
def condensation(n: int, adj: list[list[int]], comp: list[int], k: int) -> list[list[int]]:
    """DAG of strongly connected components (no duplicate edges).   # Конденсация графа.

    When to use:  DP on the component DAG after scc_tarjan / scc_kosaraju.
    Complexity:   O(n + m)
    Returns:      cadj[c] = sorted list of components reachable by one edge from c.
    Related:      scc_tarjan, coin_collector.
    CSES:         Coin Collector (1686).
    Example:
        >>> condensation(5, [[1], [2], [0, 3], [4], [3]], [0, 0, 0, 1, 1], 2)
        [[1], []]
    """
    sets: list[set[int]] = [set() for _ in range(k)]
    for u in range(n):
        cu = comp[u]
        for v in adj[u]:
            if comp[v] != cu:
                sets[cu].add(comp[v])  # рёбра между разными компонентами
    return [sorted(s) for s in sets]


@algo(
    tags=["scc", "dag", "dp"],
    cses=["Coin Collector (1686)"],
    requires=["scc_tarjan", "condensation"],
)
def coin_collector(n: int, adj: list[list[int]], coins: list[int]) -> int:
    """Max coins collected on a walk (re-visits allowed) in a directed graph.   # Сборщик монет.

    When to use:  inside an SCC you take everything; then longest path on the DAG.
    Complexity:   O(n + m)
    Returns:      maximum total coins over all walks.
    Related:      scc_tarjan, condensation.
    CSES:         Coin Collector (1686).
    Example:
        >>> coin_collector(4, [[1], [0, 2], [], [2]], [4, 5, 2, 7])
        11
    """
    k, comp = scc_tarjan(n, adj)
    cadj = condensation(n, adj, comp, k)
    total = [0] * k
    for v in range(n):
        total[comp[v]] += coins[v]
    best = [0] * k
    for c in range(k - 1, -1, -1):  # с конца топологического порядка
        best[c] = total[c] + max((best[d] for d in cadj[c]), default=0)
    return max(best, default=0)


@algo(tags=["2-sat", "scc", "logic"], cses=["Giant Pizza (1684)"], requires=["scc_tarjan"])
def two_sat(n_vars: int, clauses: list[tuple[int, bool, int, bool]]) -> list[bool] | None:
    """2-SAT: satisfy all clauses (x_a == va) OR (x_b == vb).   # Задача 2-SAT.

    When to use:  boolean choices with pairwise "at least one of" constraints.
    Complexity:   O(n_vars + clauses)
    Input:        clause (a, va, b, vb) means "x_a is va or x_b is vb" (CSES: "+1 -2" ->
                  (0, True, 1, False)).
    Returns:      assignment list, or None if impossible.
    Idea:         clause A or B = edges not A -> B and not B -> A; unsatisfiable iff x and
                  not x share an SCC; x = True iff comp[x] comes later topologically.
    Related:      scc_tarjan.
    CSES:         Giant Pizza (1684).
    Example:
        >>> two_sat(2, [(0, True, 1, True), (0, False, 1, False), (0, True, 1, False)])
        [True, False]
        >>> two_sat(1, [(0, True, 0, True), (0, False, 0, False)]) is None
        True
    """
    N = 2 * n_vars
    adj: list[list[int]] = [[] for _ in range(N)]
    for a, va, b, vb in clauses:
        la = 2 * a + (0 if va else 1)  # вершина 2i - x_i истинно, 2i+1 - ложно
        lb = 2 * b + (0 if vb else 1)
        adj[la ^ 1].append(lb)  # не A -> B
        adj[lb ^ 1].append(la)  # не B -> A
    _, comp = scc_tarjan(N, adj)
    res = []
    for i in range(n_vars):
        if comp[2 * i] == comp[2 * i + 1]:
            return None
        res.append(comp[2 * i] > comp[2 * i + 1])
    return res


@algo(tags=["bridges", "lowlink", "dfs"], cses=["- (bridges)"])
def bridges(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """Bridges of an undirected multigraph (lowlink, iterative).   # Мосты.

    When to use:  edges whose removal disconnects the graph; 2-edge-connectivity.
    Complexity:   O(n + m)
    Returns:      sorted indices of bridge edges (parallel edges are never bridges).
    Related:      articulation_points, strongly_connected_edges.
    CSES:         - (bridges; used by Strongly Connected Edges)
    Example:
        >>> bridges(5, [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4)])
        [3, 4]
    """
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))
        adj[v].append((u, i))
    tin = [-1] * n
    low = [0] * n
    it = [0] * n
    pedge = [-1] * n  # номер ребра в родителя
    timer = 0
    res = []
    for s in range(n):
        if tin[s] != -1:
            continue
        tin[s] = low[s] = timer
        timer += 1
        stack = [s]
        while stack:
            u = stack[-1]
            if it[u] < len(adj[u]):
                v, eid = adj[u][it[u]]
                it[u] += 1
                if eid == pedge[u]:
                    continue  # не идём назад по тому же ребру
                if tin[v] == -1:
                    tin[v] = low[v] = timer
                    timer += 1
                    pedge[v] = eid
                    stack.append(v)
                elif tin[v] < low[u]:
                    low[u] = tin[v]
            else:
                stack.pop()
                if stack:
                    p = stack[-1]
                    if low[u] < low[p]:
                        low[p] = low[u]
                    if low[u] > tin[p]:  # из поддерева u не подняться выше u
                        res.append(pedge[u])
    return sorted(res)


@algo(tags=["articulation-points", "lowlink", "dfs"], cses=["Necessary Cities (2076)"])
def articulation_points(n: int, adj: list[list[int]]) -> list[int]:
    """Cut vertices of an undirected graph (lowlink, iterative).   # Точки сочленения.

    When to use:  vertices whose removal disconnects the graph.
    Complexity:   O(n + m)
    Returns:      sorted list of articulation points.
    Related:      bridges, critical_cities.
    CSES:         Necessary Cities (2076).
    Example:
        >>> articulation_points(5, [[1, 2], [0, 2, 3], [0, 1], [1, 4], [3]])
        [1, 3]
    """
    tin = [-1] * n
    low = [0] * n
    it = [0] * n
    parent = [-1] * n
    is_cut = [False] * n
    timer = 0
    for s in range(n):
        if tin[s] != -1:
            continue
        tin[s] = low[s] = timer
        timer += 1
        children = 0
        stack = [s]
        while stack:
            u = stack[-1]
            if it[u] < len(adj[u]):
                v = adj[u][it[u]]
                it[u] += 1
                if tin[v] == -1:
                    tin[v] = low[v] = timer
                    timer += 1
                    parent[v] = u
                    if u == s:
                        children += 1
                    stack.append(v)
                elif v != parent[u] and tin[v] < low[u]:
                    low[u] = tin[v]
            else:
                stack.pop()
                p = parent[u]
                if p != -1:
                    if low[u] < low[p]:
                        low[p] = low[u]
                    if p != s and low[u] >= tin[p]:  # поддерево u держится только на p
                        is_cut[p] = True
        if children >= 2:  # корень - точка сочленения, если детей хотя бы два
            is_cut[s] = True
    return [v for v in range(n) if is_cut[v]]


@algo(
    tags=["reachability", "scc", "bitset"],
    cses=["Reachability Queries (2143)"],
    requires=["scc_tarjan", "condensation"],
)
def reachability_queries(
    n: int, adj: list[list[int]], queries: list[tuple[int, int]]
) -> list[bool]:
    """Can a reach b? for many pairs in a general digraph.   # Запросы достижимости.

    When to use:  n up to 5 * 10^4, many queries: SCC + bitsets on the condensation.
    Complexity:   O(n + m) + O(k * m_c / 64) for the bitsets
    Returns:      answers in query order.
    Related:      reachable_counts, scc_tarjan.
    CSES:         Reachability Queries (2143).
    Example:
        >>> reachability_queries(4, [[1], [0, 2], [], [2]], [(0, 2), (2, 0), (3, 2), (1, 0)])
        [True, False, True, True]
    """
    k, comp = scc_tarjan(n, adj)
    cadj = condensation(n, adj, comp, k)
    reach = [0] * k
    for c in range(k - 1, -1, -1):  # потомки по топологическому порядку уже готовы
        r = 1 << c
        for d in cadj[c]:
            r |= reach[d]
        reach[c] = r
    return [bool(reach[comp[a]] >> comp[b] & 1) for a, b in queries]
