"""AC-15: performance on typical contest limits (run with: pytest -m slow -s).

Ориентир задаётся на CPython 3.11; порог в тесте = 2.5 x ориентир, чтобы ловить регрессии,
а не шум машины. Что заведомо медленнее ориентира контеста (~2 с), помечено в докстринге
строкой «Python speed:». Фактические времена записываются в docs/PROGRESS.md.
"""

from __future__ import annotations

import random
import time
from collections.abc import Callable

import pytest

from rustinpy.ds import (
    Fenwick,
    LazySegAddSum,
    SegTree,
    SortedList,
    distinct_values_queries,
    sliding_window_mode,
)
from rustinpy.mathx import (
    Comb,
    convolution,
    convolution_int,
    convolution_ntt,
    factorize,
    is_prime,
    linear_sieve,
    phi_prefix_sum,
    sieve,
)

N = 2 * 10**5
MARGIN = 2.5


def run_all(cases: list[tuple[str, float, Callable[[], object]]]) -> None:
    slow = []
    for name, expected, fn in cases:
        t0 = time.perf_counter()
        fn()
        dt = time.perf_counter() - t0
        flag = "" if dt <= expected * MARGIN else "  <-- REGRESSION"
        print(f"\n  {name:<48} {dt:6.2f} s (expected ~{expected} s){flag}")
        if flag:
            slow.append(f"{name}: {dt:.2f} s")
    assert slow == []


@pytest.mark.slow
def test_ac_15_ds_speed() -> None:
    rng = random.Random(1)
    a = [rng.randint(1, 10**9) for _ in range(N)]
    ops = [(rng.randrange(N), rng.randrange(N)) for _ in range(N)]
    small = [rng.randint(1, 1000) for _ in range(N)]

    def fenwick() -> None:
        f = Fenwick(a)
        for i, j in ops:
            f.add(i, 1)
            f.range_sum(min(i, j), max(i, j))

    def segtree() -> None:
        st = SegTree(list(a), min, 1 << 60)
        for i, j in ops:
            st.set(i, j)
            st.query(min(i, j), max(i, j) + 1)

    def lazy() -> None:
        st = LazySegAddSum(list(a))
        for i, j in ops:
            lo, hi = min(i, j), max(i, j) + 1
            st.range_add(lo, hi, 1)
            st.range_sum(lo, hi)

    def sorted_list() -> None:
        s = SortedList()
        for x in a:
            s.add(x)
        for x in a[: N // 2]:
            s.discard(x)
            s.bisect_left(x)

    run_all(
        [
            ("Fenwick: 2e5 add + 2e5 range_sum", 1.3, fenwick),
            ("SegTree(min): 2e5 set + 2e5 query", 3.0, segtree),
            ("LazySegAddSum: 2e5 range_add + 2e5 range_sum", 12.0, lazy),
            ("SortedList: 2e5 add + 1e5 discard/bisect", 2.5, sorted_list),
            (
                "distinct_values_queries n = q = 2e5",
                1.5,
                lambda: distinct_values_queries(small, [(min(i, j), max(i, j)) for i, j in ops]),
            ),
            ("sliding_window_mode n = 2e5", 0.5, lambda: sliding_window_mode(small, 1000)),
        ]
    )


@pytest.mark.slow
def test_ac_15_graph_tree_speed() -> None:
    from rustinpy.graph import Dinic, bfs, dijkstra, hopcroft_karp, scc_tarjan
    from rustinpy.tree import HLD, LCA, fixed_length_paths, tree_distance_sums

    rng = random.Random(3)
    n = m = N
    wadj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    dadj: list[list[int]] = [[] for _ in range(n)]
    for _ in range(m):
        u, v = rng.randrange(n), rng.randrange(n)
        wadj[u].append((v, rng.randint(1, 10**9)))
        dadj[u].append(v)
    for i in range(n - 1):  # цепочка i -> i + 1: из 0 достижим весь граф
        wadj[i].append((i + 1, rng.randint(1, 10**9)))
        dadj[i].append(i + 1)
    tadj: list[list[int]] = [[] for _ in range(n)]
    for v in range(1, n):
        p = rng.randrange(max(0, v - 10), v)  # глубокое дерево: проверка отсутствия рекурсии
        tadj[p].append(v)
        tadj[v].append(p)
    qs = [(rng.randrange(n), rng.randrange(n)) for _ in range(N)]

    def lca_all() -> None:
        t = LCA(n, tadj)
        for a, b in qs:
            t.lca(a, b)

    def hld_all() -> None:
        h = HLD(n, tadj, [rng.randint(1, 10**9) for _ in range(n)])
        for a, b in qs[: N // 4]:
            h.path_max(a, b)

    def dinic_grid() -> None:
        side = 150  # двудольный граф 2 * 150^2 вершин -> поток по сетке
        d = Dinic(2 * side * side + 2)
        s, t = 2 * side * side, 2 * side * side + 1
        for i in range(side * side):
            d.add_edge(s, i, 1)
            d.add_edge(side * side + i, t, 1)
            for j in (i, (i + 1) % (side * side), (i + side) % (side * side)):
                d.add_edge(i, side * side + j, 1)
        d.max_flow(s, t)

    def matching() -> None:
        k = 10**5
        adj = [[rng.randrange(k) for _ in range(3)] for _ in range(k)]
        hopcroft_karp(k, k, adj)

    run_all(
        [
            ("bfs n = 2e5, m = 4e5", 0.3, lambda: bfs(n, dadj, 0)),
            ("dijkstra n = 2e5, m = 4e5", 0.8, lambda: dijkstra(n, wadj, 0)),
            ("scc_tarjan n = 2e5, m = 4e5", 0.8, lambda: scc_tarjan(n, dadj)),
            ("LCA build + 2e5 queries (deep tree)", 2.5, lca_all),
            ("HLD build + 5e4 path_max", 2.0, hld_all),
            ("tree_distance_sums n = 2e5", 0.5, lambda: tree_distance_sums(n, tadj)),
            ("fixed_length_paths n = 2e5, k = 7", 8.0, lambda: fixed_length_paths(n, tadj, 7)),
            ("Dinic unit grid 45000 + 45000 vertices", 4.0, dinic_grid),
            ("hopcroft_karp 1e5 + 1e5, 3e5 edges", 3.0, matching),
        ]
    )


@pytest.mark.slow
def test_ac_15_mathx_speed() -> None:
    rng = random.Random(2)
    a = [rng.randrange(998244353) for _ in range(N)]
    b = [rng.randrange(998244353) for _ in range(N)]
    big = [rng.randrange(1, 10**18) for _ in range(2000)]
    semi = [1000000007 * 998244353, 999999937 * 999999929, (2**31 - 1) * 1000000009]
    run_all(
        [
            ("sieve(10^7)", 0.1, lambda: sieve(10**7)),
            ("linear_sieve(2 * 10^6)", 0.9, lambda: linear_sieve(2 * 10**6)),
            ("Comb(10^6) build", 0.4, lambda: Comb(10**6)),
            ("convolution_int 2e5 x 2e5 (decimal)", 2.0, lambda: convolution_int(a, b)),
            ("convolution mod 2e5 x 2e5 (decimal)", 2.0, lambda: convolution(a, b)),
            (
                "convolution_ntt 5e4 x 5e4 (pure NTT)",
                3.5,
                lambda: convolution_ntt(a[: N // 4], b[: N // 4]),
            ),
            ("is_prime x 2000 (up to 1e18)", 0.2, lambda: [is_prime(x) for x in big]),
            ("factorize 3 semiprimes ~1e18", 0.5, lambda: [factorize(x) for x in semi]),
            ("phi_prefix_sum(10^9)", 3.0, lambda: phi_prefix_sum(10**9)),
        ]
    )
