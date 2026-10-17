"""tree: brute-force comparisons on small random trees (AC-05, AC-06)."""

from __future__ import annotations

import itertools
import random

from rustinpy.tree import (
    HLD,
    LCA,
    LCAEuler,
    PathSumQueries,
    SubtreeQueries,
    centroid_decomposition,
    counting_paths,
    distinct_colors,
    euler_tour,
    find_centroid,
    fix_the_leak,
    fixed_length_paths,
    fixed_length_paths_range,
    subtree_sizes,
    tree_diameter,
    tree_distance_sums,
    tree_farthest,
    tree_isomorphic,
    tree_matching,
    tree_parents_order,
)


def random_tree(rng: random.Random, n: int) -> tuple[list[tuple[int, int]], list[list[int]]]:
    labels = list(range(n))
    rng.shuffle(labels)
    edges = [(labels[rng.randrange(v)], labels[v]) for v in range(1, n)]
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return edges, adj


def all_dist(n: int, adj: list[list[int]]) -> list[list[int]]:
    res = []
    for s in range(n):
        d = [-1] * n
        d[s] = 0
        q = [s]
        for u in q:
            for v in adj[u]:
                if d[v] < 0:
                    d[v] = d[u] + 1
                    q.append(v)
        res.append(d)
    return res


def naive_parents(n: int, adj: list[list[int]], root: int = 0) -> tuple[list[int], list[int]]:
    par = [-1] * n
    depth = [0] * n
    st = [root]
    seen = {root}
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                par[v] = u
                depth[v] = depth[u] + 1
                st.append(v)
    return par, depth


def ancestors(v: int, par: list[int]) -> list[int]:
    res = [v]
    while par[res[-1]] != -1:
        res.append(par[res[-1]])
    return res


def path_vertices(a: int, b: int, par: list[int]) -> list[int]:
    up_a, up_b = ancestors(a, par), ancestors(b, par)
    common = next(x for x in up_a if x in set(up_b))
    return up_a[: up_a.index(common) + 1] + up_b[: up_b.index(common)][::-1]


def test_orders_sizes_diameter_rerooting(rng: random.Random) -> None:
    for _ in range(150):
        n = rng.randint(1, 12)
        _, adj = random_tree(rng, n)
        order, parent = tree_parents_order(n, adj)
        par, depth = naive_parents(n, adj)
        assert parent == par and sorted(order) == list(range(n))
        assert [depth[v] for v in order] == sorted(depth[v] for v in order)
        sizes = subtree_sizes(n, adj)
        assert sizes == [sum(1 for u in range(n) if v in ancestors(u, par)) for v in range(n)]
        D = all_dist(n, adj)
        length, a, b = tree_diameter(n, adj)
        assert length == max(max(row) for row in D) == D[a][b]
        assert tree_farthest(n, adj) == [max(row) for row in D]
        assert tree_distance_sums(n, adj) == [sum(row) for row in D]
        c = find_centroid(n, adj)
        for v in adj[c]:  # каждая часть после удаления c - не больше n / 2
            part = sum(1 for u in range(n) if D[v][u] < D[c][u])
            assert 2 * part <= n


def test_euler_tour_and_lca(rng: random.Random) -> None:
    for _ in range(150):
        n = rng.randint(1, 15)
        _, adj = random_tree(rng, n)
        root = rng.randrange(n)
        par, _ = naive_parents(n, adj, root)
        tin, tout = euler_tour(n, adj, root)
        assert sorted(tin) == list(range(n))
        for u in range(n):
            for v in range(n):
                assert (tin[u] <= tin[v] < tout[u]) == (u in ancestors(v, par))
        t1 = LCA(n, adj, root)
        t2 = LCAEuler(n, adj, root)
        D = all_dist(n, adj)
        for _ in range(30):
            a, b = rng.randrange(n), rng.randrange(n)
            anc = set(ancestors(b, par))
            exp = next(x for x in ancestors(a, par) if x in anc)
            assert t1.lca(a, b) == exp == t2.lca(a, b)
            assert t1.dist(a, b) == D[a][b] == t2.dist(a, b)
            k = rng.randint(0, n)
            chain = ancestors(a, par)
            assert t1.kth_ancestor(a, k) == (chain[k] if k < len(chain) else -1)


def test_matching_and_counting_paths(rng: random.Random) -> None:
    for _ in range(150):
        n = rng.randint(1, 9)
        edges, adj = random_tree(rng, n)
        best = 0
        for mask in range(1 << len(edges)):
            used: set[int] = set()
            ok = True
            cnt = 0
            for i, (u, v) in enumerate(edges):
                if mask >> i & 1:
                    if u in used or v in used:
                        ok = False
                        break
                    used |= {u, v}
                    cnt += 1
            if ok:
                best = max(best, cnt)
        assert tree_matching(n, adj) == best
        par, _ = naive_parents(n, adj)
        paths = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 8))]
        exp = [0] * n
        for a, b in paths:
            for v in path_vertices(a, b, par):
                exp[v] += 1
        assert counting_paths(n, adj, paths) == exp


def test_subtree_path_hld_queries(rng: random.Random) -> None:
    for _ in range(80):
        n = rng.randint(1, 15)
        _, adj = random_tree(rng, n)
        vals = [rng.randint(-9, 9) for _ in range(n)]
        par, _ = naive_parents(n, adj)
        sq = SubtreeQueries(n, adj, vals)
        pq = PathSumQueries(n, adj, vals)
        h = HLD(n, adj, vals)
        for _ in range(60):
            v, x = rng.randrange(n), rng.randint(-9, 9)
            vals[v] = x
            sq.set_value(v, x)
            pq.set_value(v, x)
            h.set_value(v, x)
            u = rng.randrange(n)
            assert sq.subtree_sum(u) == sum(vals[w] for w in range(n) if u in ancestors(w, par))
            assert pq.path_sum(u) == sum(vals[w] for w in ancestors(u, par))
            a, b = rng.randrange(n), rng.randrange(n)
            pv = path_vertices(a, b, par)
            assert h.path_max(a, b) == max(vals[w] for w in pv)
            anc = set(ancestors(b, par))
            assert h.lca(a, b) == next(w for w in ancestors(a, par) if w in anc)


def test_centroid_decomposition_properties(rng: random.Random) -> None:
    for _ in range(100):
        n = rng.randint(1, 30)
        _, adj = random_tree(rng, n)
        cpar = centroid_decomposition(n, adj)
        assert cpar.count(-1) == 1
        depth = []
        for v in range(n):
            d, u = 0, v
            while cpar[u] != -1:
                u = cpar[u]
                d += 1
            depth.append(d)
        assert max(depth) <= n.bit_length()
        for c in range(n):
            comp = {v for v in range(n) if c in ancestors(v, cpar)}
            # компонента связна, а после удаления c куски не больше половины
            rest = comp - {c}
            seen: set[int] = set()
            for s in rest:
                if s in seen:
                    continue
                piece = {s}
                st = [s]
                while st:
                    x = st.pop()
                    for y in adj[x]:
                        if y in rest and y not in piece:
                            piece.add(y)
                            st.append(y)
                seen |= piece
                assert 2 * len(piece) <= len(comp)


def test_fixed_length_paths_vs_pairs(rng: random.Random) -> None:
    for _ in range(150):
        n = rng.randint(1, 14)
        _, adj = random_tree(rng, n)
        D = all_dist(n, adj)
        pairs = [D[u][v] for u in range(n) for v in range(u + 1, n)]
        k = rng.randint(1, 6)
        assert fixed_length_paths(n, adj, k) == pairs.count(k)
        k1 = rng.randint(1, 5)
        k2 = rng.randint(k1, 7)
        assert fixed_length_paths_range(n, adj, k1, k2) == sum(1 for d in pairs if k1 <= d <= k2)


def test_distinct_colors(rng: random.Random) -> None:
    for _ in range(150):
        n = rng.randint(1, 15)
        _, adj = random_tree(rng, n)
        colors = [rng.randint(1, 4) for _ in range(n)]
        par, _ = naive_parents(n, adj)
        exp = [len({colors[w] for w in range(n) if v in ancestors(w, par)}) for v in range(n)]
        assert distinct_colors(n, adj, colors) == exp


def brute_iso(n: int, e1: list[tuple[int, int]], e2: list[tuple[int, int]], rooted: bool) -> bool:
    s2 = {frozenset(e) for e in e2}
    for p in itertools.permutations(range(n)):
        if rooted and p[0] != 0:
            continue
        if all(frozenset((p[u], p[v])) in s2 for u, v in e1):
            return True
    return False


def test_tree_isomorphism_vs_permutations(rng: random.Random) -> None:
    for _ in range(200):
        n = rng.randint(1, 7)
        e1, a1 = random_tree(rng, n)
        if rng.random() < 0.5:
            perm = list(range(n))
            rng.shuffle(perm)
            e2 = [(perm[u], perm[v]) for u, v in e1]
        else:
            e2, _ = random_tree(rng, n)
        a2: list[list[int]] = [[] for _ in range(n)]
        for u, v in e2:
            a2[u].append(v)
            a2[v].append(u)
        for rooted in (True, False):
            assert tree_isomorphic(n, a1, a2, rooted) == brute_iso(n, e1, e2, rooted)


def test_fix_the_leak(rng: random.Random) -> None:
    for _ in range(300):
        n = rng.randint(1, 9)
        parent = [-1] + [rng.randrange(i) for i in range(1, n)]
        k = rng.randrange(n)
        best = n
        for removed in itertools.combinations(range(1, n), k):
            rem = set(removed)
            if any(parent[v] in rem for v in range(1, n) if v not in rem):
                continue  # остаток должен быть поддеревом с корнем 0
            has_child = {parent[v] for v in range(1, n) if v not in rem}
            best = min(best, sum(1 for v in range(n) if v not in rem and v not in has_child))
        assert fix_the_leak(n, parent, k) == best, (parent, k)
