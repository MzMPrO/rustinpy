"""graph: brute-force comparisons on small random graphs (AC-05, AC-06)."""

from __future__ import annotations

import itertools
import random

import pytest

from rustinpy.graph import (
    DSU,
    INF,
    Dinic,
    MinCostFlow,
    RollbackDSU,
    articulation_points,
    bellman_ford,
    bfs,
    bfs_path,
    bipartite_coloring,
    bridges,
    build_lifting,
    bus_companies,
    coin_collector,
    condensation,
    connected_components,
    count_paths_dag,
    critical_cities,
    cycle_steps,
    dfs_order,
    dijkstra,
    dijkstra_coupon,
    dijkstra_path,
    dijkstra_states,
    dijkstra_stats,
    edge_disjoint_paths,
    edmonds_karp,
    escalators,
    euler_path_directed,
    euler_path_undirected,
    even_outdegree_edges,
    find_cycle_directed,
    find_cycle_undirected,
    find_negative_cycle,
    flight_route_requests,
    floyd_warshall,
    functional_distance,
    girth,
    grid_bfs,
    hamiltonian_path,
    hopcroft_karp,
    hungarian,
    k_shortest_walks,
    knights_tour,
    kruskal,
    kth_successor,
    kuhn_matching,
    longest_path_dag,
    max_score_path,
    min_cut_edges,
    multi_source_bfs,
    network_renovation,
    prim,
    reachability_queries,
    reachable_counts,
    road_construction,
    scc_kosaraju,
    scc_tarjan,
    strongly_connected_edges,
    toposort_kahn,
    toposort_lex_min,
    toposort_smallest_first,
    two_sat,
    zero_one_bfs,
)

# ------------------------------------------------------------------ генераторы


def rand_simple_undirected(rng: random.Random, n: int, p: float) -> list[tuple[int, int]]:
    return [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]


def undirected_adj(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def rand_digraph(rng: random.Random, n: int, p: float) -> list[list[int]]:
    return [[v for v in range(n) if v != u and rng.random() < p] for u in range(n)]


def rand_dag(rng: random.Random, n: int, p: float) -> list[list[int]]:
    perm = list(range(n))
    rng.shuffle(perm)
    pos = {v: i for i, v in enumerate(perm)}
    return [[v for v in range(n) if pos[v] > pos[u] and rng.random() < p] for u in range(n)]


def reach_matrix(n: int, adj: list[list[int]]) -> list[list[bool]]:
    res = []
    for s in range(n):
        seen = [False] * n
        seen[s] = True
        st = [s]
        while st:
            u = st.pop()
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    st.append(v)
        res.append(seen)
    return res


def floyd_ref(n: int, edges: list[tuple[int, int, int]]) -> list[list[float]]:
    d = [[float("inf")] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


def components_count(n: int, edges: list[tuple[int, int]], skip_v: int = -1) -> int:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            x = parent[x]
        return x

    for u, v in edges:
        if skip_v in (u, v):
            continue
        parent[find(u)] = find(v)
    return len({find(v) for v in range(n) if v != skip_v})


# ------------------------------------------------------------------ обходы


def test_bfs_family(rng: random.Random) -> None:
    for _ in range(150):
        n = rng.randint(1, 9)
        adj = rand_digraph(rng, n, 0.3)
        d = floyd_ref(n, [(u, v, 1) for u in range(n) for v in adj[u]])
        s = rng.randrange(n)
        dist = bfs(n, adj, s)
        assert dist == [int(x) if x < float("inf") else -1 for x in d[s]]
        t = rng.randrange(n)
        p = bfs_path(n, adj, s, t)
        if dist[t] < 0:
            assert p is None
        else:
            assert p is not None and p[0] == s and p[-1] == t and len(p) == dist[t] + 1
            assert all(b in adj[a] for a, b in zip(p, p[1:]))
        srcs = rng.sample(range(n), rng.randint(1, n))
        exp = [
            min((int(d[x][v]) for x in srcs if d[x][v] < float("inf")), default=-1)
            for v in range(n)
        ]
        assert multi_source_bfs(n, adj, srcs) == exp


def test_grid_bfs_vs_graph_bfs(rng: random.Random) -> None:
    for _ in range(80):
        R, C = rng.randint(1, 5), rng.randint(1, 5)
        grid = ["".join(rng.choice("..#") for _ in range(C)) for _ in range(R)]
        sr, sc = rng.randrange(R), rng.randrange(C)
        got = grid_bfs(grid, (sr, sc))
        n = R * C
        adj: list[list[int]] = [[] for _ in range(n)]
        for r in range(R):
            for c in range(C):
                if grid[r][c] == "#":
                    continue
                for nr, nc in ((r + 1, c), (r, c + 1)):
                    if nr < R and nc < C and grid[nr][nc] != "#":
                        adj[r * C + c].append(nr * C + nc)
                        adj[nr * C + nc].append(r * C + c)
        if grid[sr][sc] == "#":
            assert all(x == -1 for row in got for x in row)
            continue
        ref = bfs(n, adj, sr * C + sc)
        assert [x for row in got for x in row] == ref


def test_dfs_order_matches_recursive(rng: random.Random) -> None:
    for _ in range(100):
        n = rng.randint(1, 10)
        adj = undirected_adj(n, rand_simple_undirected(rng, n, 0.3))
        s = rng.randrange(n)
        assert dfs_order(n, adj, s) == recursive_dfs(n, adj, s)


def recursive_dfs(n: int, adj: list[list[int]], s: int) -> tuple[list[int], list[int]]:
    """Эталон: обычная рекурсия на маленьком графе."""
    order: list[int] = []
    par = [-2] * n
    par[s] = -1

    def rec(u: int) -> None:
        order.append(u)
        for v in adj[u]:
            if par[v] == -2:
                par[v] = u
                rec(v)

    rec(s)
    return order, par


def test_components_bipartite_cycles_girth(rng: random.Random) -> None:
    for _ in range(200):
        n = rng.randint(1, 9)
        edges = rand_simple_undirected(rng, n, 0.3)
        adj = undirected_adj(n, edges)
        k, comp = connected_components(n, adj)
        assert k == components_count(n, edges)
        for u, v in edges:
            assert comp[u] == comp[v]
        col = bipartite_coloring(n, adj)
        bip = any(
            all(bits[u] != bits[v] for u, v in edges)
            for bits in itertools.product((0, 1), repeat=n)
        )
        if col is None:
            assert not bip
        else:
            assert all(col[u] != col[v] for u, v in edges)
        cyc = find_cycle_undirected(n, adj)
        forest = len(edges) == n - k
        if cyc is None:
            assert forest
        else:
            assert not forest and cyc[0] == cyc[-1] and len(cyc) >= 4
            assert len(set(cyc[:-1])) == len(cyc) - 1
            assert all(b in adj[a] for a, b in zip(cyc, cyc[1:]))
        best = -1
        for i, (u, v) in enumerate(edges):
            rest = undirected_adj(n, edges[:i] + edges[i + 1 :])
            d = bfs(n, rest, u)[v]
            if d >= 0 and (best < 0 or d + 1 < best):
                best = d + 1
        assert girth(n, adj) == best


def test_find_cycle_directed(rng: random.Random) -> None:
    for _ in range(200):
        n = rng.randint(1, 8)
        adj = rand_digraph(rng, n, 0.2)
        reach = reach_matrix(n, adj)
        has = any(reach[v][u] for u in range(n) for v in adj[u])
        cyc = find_cycle_directed(n, adj)
        if cyc is None:
            assert not has
        else:
            assert has and cyc[0] == cyc[-1]
            assert all(b in adj[a] for a, b in zip(cyc, cyc[1:]))


# ------------------------------------------------------------------ кратчайшие пути


def weighted(rng: random.Random, n: int, p: float, lo: int, hi: int) -> list[tuple[int, int, int]]:
    return [
        (u, v, rng.randint(lo, hi))
        for u in range(n)
        for v in range(n)
        if u != v and rng.random() < p
    ]


def to_adj(n: int, edges: list[tuple[int, int, int]]) -> list[list[tuple[int, int]]]:
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    return adj


def test_dijkstra_family_vs_floyd(rng: random.Random) -> None:
    for _ in range(200):
        n = rng.randint(1, 8)
        edges = weighted(rng, n, 0.35, 1, 9)
        adj = to_adj(n, edges)
        d = floyd_ref(n, edges)
        s, t = rng.randrange(n), rng.randrange(n)
        dist = dijkstra(n, adj, s)
        assert dist == [int(x) if x < float("inf") else INF for x in d[s]]
        assert floyd_warshall(n, edges, directed=True) == [
            [int(x) if x < float("inf") else INF for x in row] for row in d
        ]
        r = dijkstra_path(n, adj, s, t)
        if dist[t] >= INF:
            assert r is None
        else:
            assert r is not None
            cost, path = r
            assert cost == dist[t] and path[0] == s and path[-1] == t
            assert sum(min(w for v, w in adj[a] if v == b) for a, b in zip(path, path[1:])) == cost
        zo = [(u, v, rng.randint(0, 1)) for u, v, _ in edges]
        dz = floyd_ref(n, zo)
        assert zero_one_bfs(n, to_adj(n, zo), s) == [
            int(x) if x < float("inf") else INF for x in dz[s]
        ]
        # купон: перебор ребра, на которое его тратим
        best = d[s][t]
        for u, v, w in edges:
            best = min(best, d[s][u] + w // 2 + d[v][t])
        exp = int(best) if best < float("inf") else INF
        assert dijkstra_coupon(n, adj, s, t) == exp

        def nbrs(st: tuple[int, bool], adj: list[list[tuple[int, int]]] = adj):
            v, used = st
            for u, w in adj[v]:
                yield (u, used), w
                if not used:
                    yield (u, True), w // 2

        assert dijkstra_states((s, False), lambda st, t=t: st[0] == t, nbrs) == exp
    assert floyd_warshall(2, [(0, 1, 5)]) == [[0, 5], [5, 0]]


def all_simple_paths(n: int, adj: list[list[tuple[int, int]]], s: int, t: int):
    stack = [(s, [s], 0)]
    while stack:
        v, path, cost = stack.pop()
        if v == t:
            yield path, cost
            continue
        for u, w in adj[v]:
            if u not in path:
                stack.append((u, [*path, u], cost + w))


def test_dijkstra_stats_vs_enumeration(rng: random.Random) -> None:
    for _ in range(150):
        n = rng.randint(1, 7)
        adj = to_adj(n, weighted(rng, n, 0.4, 1, 3))
        d, cnt, mn, mx = dijkstra_stats(n, adj, 0)
        for t in range(n):
            paths = list(all_simple_paths(n, adj, 0, t))
            if not paths:
                assert d[t] == INF
                continue
            best = min(c for _, c in paths)
            short = [len(p) - 1 for p, c in paths if c == best]
            assert (d[t], cnt[t], mn[t], mx[t]) == (best, len(short), min(short), max(short))


def test_k_shortest_walks_vs_enumeration(rng: random.Random) -> None:
    cap = 10
    for _ in range(100):
        n = rng.randint(1, 5)
        adj = to_adj(n, weighted(rng, n, 0.5, 1, 4))
        s, t = rng.randrange(n), rng.randrange(n)
        costs = []
        stack = [(s, 0)]
        while stack:  # все маршруты стоимостью <= cap
            v, c = stack.pop()
            if v == t:
                costs.append(c)
            for u, w in adj[v]:
                if c + w <= cap:
                    stack.append((u, c + w))
        costs.sort()
        k = rng.randint(1, 6)
        got = k_shortest_walks(n, adj, s, t, k)
        small = [x for x in got if x <= cap]  # всё дешевле cap перебор нашёл полностью
        assert small == costs[: len(small)]
        if len(costs) >= k and costs[k - 1] <= cap:
            assert got == costs[:k]
        assert got == sorted(got) and len(got) <= k


def test_bellman_ford_negative_cycles(rng: random.Random) -> None:
    for _ in range(300):
        n = rng.randint(1, 7)
        edges = weighted(rng, n, 0.3, -4, 6)
        d = floyd_ref(n, edges)
        s = rng.randrange(n)
        got = bellman_ford(n, edges, s)
        for v in range(n):
            neg = any(
                d[s][w] < float("inf") and d[w][w] < 0 and d[w][v] < float("inf") for w in range(n)
            )
            if neg:
                assert got[v] == -INF
            elif d[s][v] == float("inf"):
                assert got[v] == INF
            else:
                assert got[v] == d[s][v]
        cyc = find_negative_cycle(n, edges)
        has_neg = any(d[v][v] < 0 for v in range(n))
        if cyc is None:
            assert not has_neg
        else:
            assert has_neg and cyc[0] == cyc[-1]
            wmap: dict[tuple[int, int], int] = {}
            for u, v, w in edges:
                wmap[(u, v)] = min(w, wmap.get((u, v), w))
            assert sum(wmap[(a, b)] for a, b in zip(cyc, cyc[1:])) < 0
        t = rng.randrange(n)
        neg_edges = [(u, v, -w) for u, v, w in edges]
        dn = floyd_ref(n, neg_edges)
        r = max_score_path(n, edges, s, t)
        inf_score = any(
            dn[s][w] < float("inf") and dn[w][w] < 0 and dn[w][t] < float("inf") for w in range(n)
        )
        if inf_score:
            assert r is None
        elif dn[s][t] == float("inf"):
            assert r == -INF
        else:
            assert r == -dn[s][t]


# ------------------------------------------------------------------ DAG


def valid_topo(n: int, adj: list[list[int]], order: list[int]) -> bool:
    pos = {v: i for i, v in enumerate(order)}
    return sorted(order) == list(range(n)) and all(
        pos[u] < pos[v] for u in range(n) for v in adj[u]
    )


def test_toposorts(rng: random.Random) -> None:
    for _ in range(200):
        n = rng.randint(1, 6)
        adj = rand_dag(rng, n, 0.3) if rng.random() < 0.7 else rand_digraph(rng, n, 0.3)
        valid = [list(p) for p in itertools.permutations(range(n)) if valid_topo(n, adj, list(p))]
        for f in (toposort_kahn, toposort_lex_min, toposort_smallest_first):
            got = f(n, adj)
            if not valid:
                assert got is None
            else:
                assert got is not None and valid_topo(n, adj, got)
        if valid:
            assert toposort_lex_min(n, adj) == min(valid)
            key = min(valid, key=lambda p: [p.index(v) for v in range(n)])
            assert toposort_smallest_first(n, adj) == key


def test_dag_paths_and_reachability(rng: random.Random) -> None:
    for _ in range(200):
        n = rng.randint(1, 8)
        adj = rand_dag(rng, n, 0.35)
        s, t = rng.randrange(n), rng.randrange(n)
        paths = []
        stack = [[s]]
        while stack:
            p = stack.pop()
            if p[-1] == t:
                paths.append(p)
            for v in adj[p[-1]]:
                stack.append([*p, v])
        assert count_paths_dag(n, adj, s, t) == len(paths)
        lp = longest_path_dag(n, adj, s, t)
        if not paths:
            assert lp is None
        else:
            assert lp is not None and lp[0] == s and lp[-1] == t
            assert len(lp) == max(len(p) for p in paths)
            assert all(b in adj[a] for a, b in zip(lp, lp[1:]))
        reach = reach_matrix(n, adj)
        assert reachable_counts(n, adj) == [sum(r) for r in reach]


# ------------------------------------------------------------------ DSU / MST


def test_dsu_and_rollback(rng: random.Random) -> None:
    for _ in range(50):
        n = rng.randint(1, 12)
        d = DSU(n)
        rb = RollbackDSU(n)
        edges: list[tuple[int, int]] = []
        snaps: list[tuple[int, int]] = []
        for _ in range(40):
            op = rng.random()
            if op < 0.6:
                u, v = rng.randrange(n), rng.randrange(n)
                merged = components_count(n, [*edges, (u, v)]) < components_count(n, edges)
                assert d.union(u, v) == merged == rb.union(u, v)
                edges.append((u, v))
            elif op < 0.75:
                snaps.append((rb.snapshot(), len(edges)))
            elif snaps:
                t, m = snaps.pop()
                rb.rollback(t)
                edges = edges[:m]
                d = DSU(n)
                for u, v in edges:
                    d.union(u, v)
            assert d.components == rb.components == components_count(n, edges)
            a, b = rng.randrange(n), rng.randrange(n)
            assert d.same(a, b) == (rb.find(a) == rb.find(b))
            assert d.size(a) == sum(1 for v in range(n) if d.same(a, v))


def test_mst_vs_brute(rng: random.Random) -> None:
    for _ in range(150):
        n = rng.randint(1, 6)
        edges = [(u, v, rng.randint(1, 9)) for u, v in rand_simple_undirected(rng, n, 0.6)]
        best = None
        for combo in itertools.combinations(range(len(edges)), n - 1):
            es = [edges[i] for i in combo]
            if components_count(n, [(u, v) for u, v, _ in es]) == 1:
                w = sum(x[2] for x in es)
                best = w if best is None or w < best else best
        if n == 1:
            best = 0
        k = kruskal(n, edges)
        adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))
        if best is None:
            assert k is None and prim(n, adj) is None
        else:
            assert k is not None and k[0] == best == prim(n, adj)
            assert sum(edges[i][2] for i in k[1]) == best
    for _ in range(50):
        n = rng.randint(1, 8)
        es = [(rng.randrange(n), rng.randrange(n)) for _ in range(10)]
        got = road_construction(n, es)
        for i in range(len(es)):
            part = es[: i + 1]
            comps = components_count(n, part)
            sizes: dict[int, int] = {}
            d = DSU(n)
            for u, v in part:
                d.union(u, v)
            for v in range(n):
                sizes[d.find(v)] = sizes.get(d.find(v), 0) + 1
            assert got[i] == (comps, max(sizes.values()))


# ------------------------------------------------------------------ SCC и компания


def test_scc_both_algorithms(rng: random.Random) -> None:
    for _ in range(200):
        n = rng.randint(1, 9)
        adj = rand_digraph(rng, n, 0.25)
        reach = reach_matrix(n, adj)
        for f in (scc_tarjan, scc_kosaraju):
            k, comp = f(n, adj)
            assert sorted(set(comp)) == list(range(k))
            for u in range(n):
                for v in range(n):
                    assert (comp[u] == comp[v]) == (reach[u][v] and reach[v][u])
                for v in adj[u]:
                    assert comp[u] <= comp[v]
            cadj = condensation(n, adj, comp, k)
            for c in range(k):
                assert c not in cadj[c]
                for d in cadj[c]:
                    assert any(comp[u] == c and comp[v] == d for u in range(n) for v in adj[u])
        qs = [(rng.randrange(n), rng.randrange(n)) for _ in range(10)]
        assert reachability_queries(n, adj, qs) == [reach[a][b] for a, b in qs]


def test_coin_collector_vs_walks(rng: random.Random) -> None:
    for _ in range(150):
        n = rng.randint(1, 6)
        adj = rand_digraph(rng, n, 0.3)
        coins = [rng.randint(1, 9) for _ in range(n)]
        best = 0
        seen = set()
        stack = [(v, 1 << v) for v in range(n)]
        while stack:  # все пары (вершина, множество посещённых)
            v, mask = stack.pop()
            if (v, mask) in seen:
                continue
            seen.add((v, mask))
            best = max(best, sum(coins[i] for i in range(n) if mask >> i & 1))
            for u in adj[v]:
                stack.append((u, mask | 1 << u))
        assert coin_collector(n, adj, coins) == best


def test_two_sat_vs_brute(rng: random.Random) -> None:
    for _ in range(300):
        n = rng.randint(1, 5)
        clauses = [
            (rng.randrange(n), rng.random() < 0.5, rng.randrange(n), rng.random() < 0.5)
            for _ in range(rng.randint(0, 8))
        ]

        def ok(x: list[bool], clauses=clauses) -> bool:
            return all(x[a] == va or x[b] == vb for a, va, b, vb in clauses)

        exists = any(ok(list(bits)) for bits in itertools.product((False, True), repeat=n))
        got = two_sat(n, clauses)
        if got is None:
            assert not exists
        else:
            assert ok(got)


def test_bridges_and_articulation(rng: random.Random) -> None:
    for _ in range(200):
        n = rng.randint(1, 8)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 10))]
        edges = [(u, v) for u, v in edges if u != v]
        base = components_count(n, edges)
        exp = [
            i for i in range(len(edges)) if components_count(n, edges[:i] + edges[i + 1 :]) > base
        ]
        assert bridges(n, edges) == exp
        simple = sorted({(min(u, v), max(u, v)) for u, v in edges})
        adj = undirected_adj(n, simple)
        exp_cut = [
            v for v in range(n) if components_count(n, simple, v) > base - (1 if not adj[v] else 0)
        ]
        assert articulation_points(n, adj) == exp_cut


# ------------------------------------------------------------------ Эйлер


def check_euler(edges: list[tuple[int, int]], path: list[int], directed: bool) -> bool:
    if len(path) != len(edges) + 1:
        return False
    left: dict[tuple[int, int], int] = {}
    for u, v in edges:
        key = (u, v) if directed else (min(u, v), max(u, v))
        left[key] = left.get(key, 0) + 1
    for a, b in zip(path, path[1:]):
        key = (a, b) if directed else (min(a, b), max(a, b))
        if left.get(key, 0) == 0:
            return False
        left[key] -= 1
    return True


def test_euler_paths(rng: random.Random) -> None:
    for _ in range(300):
        n = rng.randint(1, 5)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 7))]
        start = rng.randrange(n)
        # перебор: существует ли эйлеров путь из start (поиск по всем порядкам рёбер)
        exists = False
        for perm in itertools.permutations(range(len(edges))):
            v = start
            good = True
            for i in perm:
                a, b = edges[i]
                if a == v:
                    v = b
                elif b == v:
                    v = a
                else:
                    good = False
                    break
            if good:
                exists = True
                break
        got = euler_path_undirected(n, edges, start)
        if exists:
            assert got is not None and got[0] == start and check_euler(edges, got, False)
        else:
            assert got is None
        auto = euler_path_undirected(n, edges)
        if auto is not None:
            assert check_euler(edges, auto, False)
        s, t = rng.randrange(n), rng.randrange(n)
        exists_d = any(
            all(edges[p[i]][1] == edges[p[i + 1]][0] for i in range(len(p) - 1))
            and (not p or (edges[p[0]][0] == s and edges[p[-1]][1] == t))
            for p in itertools.permutations(range(len(edges)))
        ) and (edges or s == t)
        gd = euler_path_directed(n, edges, s, t)
        if exists_d:
            assert gd is not None and gd[0] == s and gd[-1] == t and check_euler(edges, gd, True)
        else:
            assert gd is None


# ------------------------------------------------------------------ функциональные графы


def test_functional_graphs(rng: random.Random) -> None:
    for _ in range(200):
        n = rng.randint(1, 10)
        f = [rng.randrange(n) for _ in range(n)]
        up = build_lifting(f, 50)
        for _ in range(10):
            x, k = rng.randrange(n), rng.randint(0, 50)
            y = x
            for _ in range(k):
                y = f[y]
            assert kth_successor(up, x, k) == y
        exp = []
        for s in range(n):
            seen = set()
            v = s
            while v not in seen:
                seen.add(v)
                v = f[v]
            exp.append(len(seen))
        assert cycle_steps(f) == exp
        qs = [(rng.randrange(n), rng.randrange(n)) for _ in range(15)]
        want = []
        for a, b in qs:
            v, d = a, 0
            while v != b and d <= n:
                v = f[v]
                d += 1
            want.append(d if v == b else -1)
        assert functional_distance(f, qs) == want


# ------------------------------------------------------------------ потоки и паросочетания


def brute_min_cut(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int:
    best = None
    for mask in range(1 << n):
        if not mask >> s & 1 or mask >> t & 1:
            continue
        c = sum(w for u, v, w in edges if mask >> u & 1 and not mask >> v & 1)
        best = c if best is None or c < best else best
    assert best is not None
    return best


def test_max_flow_min_cut(rng: random.Random) -> None:
    for _ in range(200):
        n = rng.randint(2, 7)
        edges = weighted(rng, n, 0.4, 1, 6)
        s, t = rng.sample(range(n), 2)
        exp = brute_min_cut(n, edges, s, t)
        d = Dinic(n)
        ids = [d.add_edge(u, v, w) for u, v, w in edges]
        assert d.max_flow(s, t) == exp == edmonds_karp(n, edges, s, t)
        for (_, _, w), e in zip(edges, ids):
            assert 0 <= d.flow_on(e) <= w
        cut = min_cut_edges(n, edges, s, t)
        assert sum(edges[i][2] for i in cut) == exp
        rest = [(u, v) for i, (u, v, _) in enumerate(edges) if i not in set(cut)]
        radj: list[list[int]] = [[] for _ in range(n)]
        for u, v in rest:
            radj[u].append(v)
        assert bfs(n, radj, s)[t] == -1
        und = [(u, v, 1) for u, v in rand_simple_undirected(rng, n, 0.5)]
        both = [(u, v, c) for u, v, c in und] + [(v, u, c) for u, v, c in und]
        ucut = min_cut_edges(n, und, s, t, directed=False)
        assert len(ucut) == brute_min_cut(n, both, s, t)
        plain = [(u, v) for u, v, _ in edges]
        paths = edge_disjoint_paths(n, plain, s, t)
        assert len(paths) == brute_min_cut(n, [(u, v, 1) for u, v in plain], s, t)
        used: dict[tuple[int, int], int] = {}
        for p in paths:
            assert p[0] == s and p[-1] == t
            for a, b in zip(p, p[1:]):
                used[(a, b)] = used.get((a, b), 0) + 1
        avail: dict[tuple[int, int], int] = {}
        for e in plain:
            avail[e] = avail.get(e, 0) + 1
        assert all(c <= avail.get(e, 0) for e, c in used.items())


def brute_matching(nl: int, nr: int, adj: list[list[int]]) -> int:
    best = 0
    dp = {0: 0}  # маска занятых правых -> лучшее
    for u in range(nl):
        nxt = dict(dp)
        for mask, val in dp.items():
            for v in adj[u]:
                if not mask >> v & 1:
                    m2 = mask | 1 << v
                    nxt[m2] = max(nxt.get(m2, 0), val + 1)
        dp = nxt
    best = max(dp.values())
    return best


def test_matchings_and_assignment(rng: random.Random) -> None:
    for _ in range(200):
        nl, nr = rng.randint(1, 7), rng.randint(1, 7)
        adj = [[v for v in range(nr) if rng.random() < 0.35] for _ in range(nl)]
        exp = brute_matching(nl, nr, adj)
        for f in (hopcroft_karp, kuhn_matching):
            size, ml = f(nl, nr, adj)
            assert size == exp
            used = [v for v in ml if v != -1]
            assert len(used) == len(set(used)) == size
            assert all(v == -1 or v in adj[u] for u, v in enumerate(ml))
    for _ in range(100):
        n = rng.randint(1, 5)
        m = rng.randint(n, 6)
        cost = [[rng.randint(-5, 20) for _ in range(m)] for _ in range(n)]
        best = min(
            sum(cost[i][p[i]] for i in range(n)) for p in itertools.permutations(range(m), n)
        )
        val, col = hungarian(cost)
        assert val == best and len(set(col)) == n
        mcf = MinCostFlow(n + m + 2)
        S, T = n + m, n + m + 1
        for i in range(n):
            mcf.add_edge(S, i, 1, 0)
            for j in range(m):
                mcf.add_edge(i, n + j, 1, cost[i][j])
        for j in range(m):
            mcf.add_edge(n + j, T, 1, 0)
        assert mcf.flow(S, T, n) == (n, best)


# ------------------------------------------------------------------ гамильтонов путь, конь


def test_hamiltonian_and_knight(rng: random.Random) -> None:
    for _ in range(150):
        n = rng.randint(1, 7)
        adj = rand_digraph(rng, n, 0.4)
        exists = any(
            all(p[i + 1] in adj[p[i]] for i in range(n - 1))
            for p in itertools.permutations(range(n))
        )
        got = hamiltonian_path(n, adj)
        if exists:
            assert got is not None and sorted(got) == list(range(n))
            assert all(b in adj[a] for a, b in zip(got, got[1:]))
        else:
            assert got is None
    moves = {(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)}
    for r in range(8):
        for c in range(8):
            b = knights_tour(8, r, c)
            assert b is not None and b[r][c] == 1
            pos = {b[x][y]: (x, y) for x in range(8) for y in range(8)}
            assert sorted(pos) == list(range(1, 65))
            for k in range(1, 64):
                (x1, y1), (x2, y2) = pos[k], pos[k + 1]
                assert (x2 - x1, y2 - y1) in moves
    assert knights_tour(3, 0, 0) is None


# ------------------------------------------------------------------ advanced


def test_critical_cities_vs_removal(rng: random.Random) -> None:
    for _ in range(200):
        n = rng.randint(2, 8)
        adj = rand_digraph(rng, n, 0.3)
        if bfs(n, adj, 0)[n - 1] < 0:
            assert critical_cities(n, adj) == []
            continue
        exp = []
        for v in range(n):
            if v in (0, n - 1):
                exp.append(v)
                continue
            cut = [[u for u in adj[x] if u != v] if x != v else [] for x in range(n)]
            if bfs(n, cut, 0)[n - 1] < 0:
                exp.append(v)
        assert critical_cities(n, adj) == exp


def test_flight_route_requests_vs_brute(rng: random.Random) -> None:
    for _ in range(60):
        n = rng.randint(1, 4)
        pairs = [tuple(rng.sample(range(n), 2)) for _ in range(rng.randint(0, 4))] if n > 1 else []
        all_edges = [(u, v) for u in range(n) for v in range(n) if u != v]
        best = None
        for size in range(len(all_edges) + 1):
            for combo in itertools.combinations(all_edges, size):
                adj: list[list[int]] = [[] for _ in range(n)]
                for u, v in combo:
                    adj[u].append(v)
                reach = reach_matrix(n, adj)
                if all(reach[a][b] for a, b in pairs):
                    best = size
                    break
            if best is not None:
                break
        assert flight_route_requests(n, pairs) == best


def random_tree(rng: random.Random, n: int) -> list[tuple[int, int]]:
    return [(rng.randrange(v), v) for v in range(1, n)]


def test_network_renovation(rng: random.Random) -> None:
    for _ in range(150):
        n = rng.randint(2, 12)
        edges = random_tree(rng, n)
        add = network_renovation(n, edges)
        leaves = sum(1 for v in range(n) if len(undirected_adj(n, edges)[v]) == 1)
        assert len(add) == (leaves + 1) // 2
        assert bridges(n, edges + add) == []


def test_orientations(rng: random.Random) -> None:
    for _ in range(200):
        n = rng.randint(1, 7)
        edges = rand_simple_undirected(rng, n, 0.5)
        res = strongly_connected_edges(n, edges)
        possible = components_count(n, edges) == 1 and bridges(n, edges) == []
        if not possible:
            assert res is None
        else:
            assert res is not None
            assert sorted((min(a, b), max(a, b)) for a, b in res) == sorted(edges)
            adj: list[list[int]] = [[] for _ in range(n)]
            for a, b in res:
                adj[a].append(b)
            assert all(all(r) for r in reach_matrix(n, adj))
        res2 = even_outdegree_edges(n, edges)
        adj_u = undirected_adj(n, edges)
        k, comp = connected_components(n, adj_u)
        per = [0] * k
        for u, _ in edges:
            per[comp[u]] += 1
        if any(c % 2 for c in per):
            assert res2 is None
        else:
            assert res2 is not None
            out = [0] * n
            for (a, b), (u, v) in zip(res2, edges):
                assert {a, b} == {u, v}
                out[a] += 1
            assert all(x % 2 == 0 for x in out)


def test_graph_stubs_raise() -> None:
    with pytest.raises(NotImplementedError):
        bus_companies(1, [])
    with pytest.raises(NotImplementedError):
        escalators([0], [])
