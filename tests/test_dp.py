"""dp: brute-force comparisons on small random inputs (AC-05, AC-06)."""

from __future__ import annotations

import itertools
import random
from functools import cache

from rustinpy.dp import (
    LiChaoTree,
    MonotoneCHT,
    array_description,
    coin_combinations_ordered,
    coin_combinations_unordered,
    count_increasing_subsequences,
    counting_numbers,
    counting_tilings,
    counting_towers,
    dc_optimization,
    dice_combinations,
    edit_distance,
    elevator_rides,
    fence_painting,
    grid_paths,
    hamiltonian_flights,
    houses_and_schools,
    knapsack_01,
    knapsack_bounded,
    knapsack_unbounded,
    knuth_optimization,
    lcs,
    lis,
    lis_length,
    min_coins,
    money_sums,
    rectangle_cutting,
    removal_game,
    removing_digits,
    weighted_interval_scheduling,
)

P = 10**9 + 7


def test_coins_and_dice(rng: random.Random) -> None:
    for n in range(0, 15):
        ways = (
            sum(
                1
                for k in range(n + 1)
                for t in itertools.product(range(1, 7), repeat=k)
                if sum(t) == n
            )
            if n <= 8
            else None
        )
        if ways is not None:
            assert dice_combinations(n) == ways
    for _ in range(100):
        coins = sorted({rng.randint(1, 6) for _ in range(rng.randint(1, 3))})
        x = rng.randint(0, 12)
        ordered = unordered = 0
        best = None
        for k in range(x + 1):
            for t in itertools.product(coins, repeat=k):
                if sum(t) == x:
                    ordered += 1
                    if list(t) == sorted(t):
                        unordered += 1
                    best = k if best is None or k < best else best
        assert coin_combinations_ordered(coins, x) == ordered
        assert coin_combinations_unordered(coins, x) == unordered
        assert min_coins(coins, x) == (best if best is not None else -1)


def test_removing_digits_vs_bfs() -> None:
    dist = {0: 0}
    for v in range(1, 300):
        dist[v] = 1 + min(dist[v - int(d)] for d in str(v) if d != "0")
    for v in range(1, 300):
        assert removing_digits(v) == dist[v]


def test_grid_paths_vs_dfs(rng: random.Random) -> None:
    for _ in range(100):
        R, C = rng.randint(1, 5), rng.randint(1, 5)
        g = ["".join(rng.choice("..*") for _ in range(C)) for _ in range(R)]

        @cache
        def ways(r: int, c: int, g: tuple[str, ...] = tuple(g)) -> int:
            rows, cols = len(g), len(g[0])
            if r >= rows or c >= cols or g[r][c] == "*":
                return 0
            if (r, c) == (rows - 1, cols - 1):
                return 1
            return ways(r + 1, c) + ways(r, c + 1)

        assert grid_paths(g) == ways(0, 0)


def test_knapsacks_vs_brute(rng: random.Random) -> None:
    for _ in range(200):
        n = rng.randint(0, 6)
        w = [rng.randint(1, 8) for _ in range(n)]
        v = [rng.randint(0, 9) for _ in range(n)]
        cap = rng.randint(0, 20)
        best = max(
            sum(v[i] for i in range(n) if m >> i & 1)
            for m in range(1 << n)
            if sum(w[i] for i in range(n) if m >> i & 1) <= cap
        )
        assert knapsack_01(w, v, cap) == best
        cnt = [rng.randint(0, 3) for _ in range(n)]
        bestb = 0
        for take in itertools.product(*[range(c + 1) for c in cnt]):
            if sum(t * x for t, x in zip(take, w)) <= cap:
                bestb = max(bestb, sum(t * x for t, x in zip(take, v)))
        assert knapsack_bounded(w, v, cnt, cap) == bestb
        if n:
            bestu = 0
            for take in itertools.product(*[range(cap // x + 1) for x in w]):
                if sum(t * x for t, x in zip(take, w)) <= cap:
                    bestu = max(bestu, sum(t * x for t, x in zip(take, v)))
            assert knapsack_unbounded(w, v, cap) == bestu


def test_array_description_vs_brute(rng: random.Random) -> None:
    for _ in range(150):
        n, m = rng.randint(1, 5), rng.randint(1, 4)
        a = [rng.choice([0, *list(range(1, m + 1))]) for _ in range(n)]
        cnt = sum(
            1
            for t in itertools.product(range(1, m + 1), repeat=n)
            if all(x == 0 or x == y for x, y in zip(a, t))
            and all(abs(t[i] - t[i + 1]) <= 1 for i in range(n - 1))
        )
        assert array_description(a, m) == cnt


def brute_towers(n: int) -> int:
    """Перебор разбиений сетки 2 x n на прямоугольники."""
    cells = [(r, c) for c in range(n) for r in range(2)]

    def count(filled: frozenset[tuple[int, int]]) -> int:
        free = [x for x in cells if x not in filled]
        if not free:
            return 1
        r0, c0 = min(free, key=lambda x: (x[1], x[0]))
        total = 0
        for h in (1, 2):
            for w in range(1, n - c0 + 1):
                rect = {(r, c) for r in range(r0, r0 + h) for c in range(c0, c0 + w)}
                if r0 + h <= 2 and not rect & filled:
                    total += count(filled | rect)
        return total

    return count(frozenset())


def test_counting_towers() -> None:
    for n in range(1, 5):
        assert counting_towers(n) == brute_towers(n)
    assert counting_towers(6) == 2864 and counting_towers(1337) == 640403945


def test_strings_dp_vs_brute(rng: random.Random) -> None:
    for _ in range(200):
        a = "".join(rng.choice("ab") for _ in range(rng.randint(0, 6)))
        b = "".join(rng.choice("ab") for _ in range(rng.randint(0, 6)))

        @cache
        def ed(i: int, j: int, a: str = a, b: str = b) -> int:
            if i == len(a):
                return len(b) - j
            if j == len(b):
                return len(a) - i
            return min(ed(i + 1, j) + 1, ed(i, j + 1) + 1, ed(i + 1, j + 1) + (a[i] != b[j]))

        assert edit_distance(a, b) == ed(0, 0)
        x = [rng.randint(0, 3) for _ in range(rng.randint(0, 7))]
        y = [rng.randint(0, 3) for _ in range(rng.randint(0, 7))]
        common = lcs(x, y)

        def is_sub(s: list[int], t: list[int]) -> bool:
            it = iter(t)
            return all(c in it for c in s)

        best = max(
            (
                len(c)
                for k in range(len(x) + 1)
                for c in itertools.combinations(x, k)
                if is_sub(list(c), y)
            ),
            default=0,
        )
        assert len(common) == best and is_sub(common, x) and is_sub(common, y)


def test_lis_family_vs_brute(rng: random.Random) -> None:
    for _ in range(200):
        a = [rng.randint(0, 5) for _ in range(rng.randint(0, 9))]
        for strict in (True, False):
            best = 0
            for k in range(len(a) + 1):
                for idx in itertools.combinations(range(len(a)), k):
                    vals = [a[i] for i in idx]
                    ok = all((p < q) if strict else (p <= q) for p, q in zip(vals, vals[1:]))
                    if ok:
                        best = max(best, k)
            got = lis(a, strict)
            assert len(got) == best == lis_length(a, strict)
            vals = [a[i] for i in got]
            assert got == sorted(got) and all(
                (p < q) if strict else (p <= q) for p, q in zip(vals, vals[1:])
            )
        cnt = sum(
            1
            for k in range(1, len(a) + 1)
            for idx in itertools.combinations(range(len(a)), k)
            if all(a[i] < a[j] for i, j in zip(idx, idx[1:]))
        )
        assert count_increasing_subsequences(a) == cnt % P


def test_money_sums_rectangles_removal(rng: random.Random) -> None:
    for _ in range(100):
        coins = [rng.randint(1, 10) for _ in range(rng.randint(1, 7))]
        sums = {sum(c for i, c in enumerate(coins) if m >> i & 1) for m in range(1 << len(coins))}
        assert money_sums(coins) == sorted(s for s in sums if s)

    @cache
    def cut(a: int, b: int) -> int:
        if a == b:
            return 0
        opts = [cut(k, b) + cut(a - k, b) for k in range(1, a)]
        opts += [cut(a, k) + cut(a, b - k) for k in range(1, b)]
        return 1 + min(opts)

    for a in range(1, 13):
        for b in range(1, 13):
            assert rectangle_cutting(a, b) == cut(a, b)
    for _ in range(100):
        arr = [rng.randint(-5, 9) for _ in range(rng.randint(1, 8))]

        @cache
        def game(l: int, r: int, arr: tuple[int, ...] = tuple(arr)) -> int:  # разность счетов
            if l == r:
                return 0
            return max(arr[l] - game(l + 1, r), arr[r - 1] - game(l, r - 1))

        diff = game(0, len(arr))
        assert removal_game(arr) == (sum(arr) + diff) // 2


def test_scheduling_elevator_hamiltonian(rng: random.Random) -> None:
    for _ in range(150):
        jobs = []
        for _ in range(rng.randint(0, 6)):
            a = rng.randint(1, 10)
            jobs.append((a, a + rng.randint(0, 4), rng.randint(1, 9)))
        best = 0
        for m in range(1 << len(jobs)):
            chosen = sorted(jobs[i] for i in range(len(jobs)) if m >> i & 1)
            if all(chosen[i][1] < chosen[i + 1][0] for i in range(len(chosen) - 1)):
                best = max(best, sum(p for _, _, p in chosen))
        assert weighted_interval_scheduling(jobs) == best
    for _ in range(100):
        n = rng.randint(1, 6)
        cap = rng.randint(6, 12)
        w = [rng.randint(1, cap) for _ in range(n)]
        best = n
        for assign in itertools.product(range(n), repeat=n):
            loads = [0] * n
            for i, b in enumerate(assign):
                loads[b] += w[i]
            if max(loads) <= cap:
                best = min(best, len(set(assign)))
        assert elevator_rides(w, cap) == best
    for _ in range(100):
        n = rng.randint(2, 6)
        edges = [(u, v) for u in range(n) for v in range(n) if u != v and rng.random() < 0.5]
        es = set(edges)
        cnt = sum(
            1
            for mid in itertools.permutations(range(1, n - 1))
            if all((a, b) in es for a, b in zip((0, *mid, n - 1), (*mid, n - 1)))
        )
        assert hamiltonian_flights(n, edges) == cnt


def brute_tilings(n: int, m: int) -> int:
    def count(filled: frozenset[tuple[int, int]]) -> int:
        free = [(r, c) for c in range(m) for r in range(n) if (r, c) not in filled]
        if not free:
            return 1
        r, c = free[0]
        total = 0
        for dr, dc in ((1, 0), (0, 1)):
            r2, c2 = r + dr, c + dc
            if r2 < n and c2 < m and (r2, c2) not in filled:
                total += count(filled | {(r, c), (r2, c2)})
        return total

    return count(frozenset())


def test_tilings_and_digits(rng: random.Random) -> None:
    for n in range(1, 5):
        for m in range(1, 6):
            assert counting_tilings(n, m) == brute_tilings(n, m)
    assert counting_tilings(4, 7) == 781

    def good(x: int) -> bool:
        s = str(x)
        return all(a != b for a, b in zip(s, s[1:]))

    pref = [0]
    for x in range(0, 3000):
        pref.append(pref[-1] + good(x))
    for _ in range(300):
        a = rng.randint(0, 2999)
        b = rng.randint(a, 2999)
        assert counting_numbers(a, b) == pref[b + 1] - pref[a]


def test_lichao_and_cht(rng: random.Random) -> None:
    for _ in range(100):
        lo, hi = -50, 50
        t = LiChaoTree(lo, hi)
        lines: list[tuple[int, int]] = []
        for _ in range(30):
            if rng.random() < 0.5:
                k, b = rng.randint(-10, 10), rng.randint(-100, 100)
                t.add_line(k, b)
                lines.append((k, b))
            else:
                x = rng.randint(lo, hi - 1)
                exp = min((k * x + b for k, b in lines), default=1 << 60)
                assert t.query(x) == exp
        h = MonotoneCHT()
        ks = sorted({rng.randint(-20, 20) for _ in range(8)}, reverse=True)
        added = []
        for k in ks:
            b = rng.randint(-50, 50)
            h.add_line(k, b)
            added.append((k, b))
            for x in range(-30, 31, 7):
                assert h.query(x) == min(kk * x + bb for kk, bb in added)


def test_dp_optimisations_vs_quadratic(rng: random.Random) -> None:
    for _ in range(100):
        n = rng.randint(1, 9)
        a = [rng.randint(0, 9) for _ in range(n)]
        k = rng.randint(1, n)

        def cost(l: int, r: int, a: list[int] = a) -> int:
            return (r - l) * sum(a[l:r])  # квадратичная, удовлетворяет условию монотонности

        dp = [[1 << 60] * (n + 1) for _ in range(k + 1)]
        dp[0][0] = 0
        for j in range(1, k + 1):
            for i in range(1, n + 1):
                dp[j][i] = min(dp[j - 1][p] + cost(p, i) for p in range(i))
        assert dc_optimization(n, k, cost) == dp[k][n]
        c = [rng.randint(0, 9) for _ in range(n)]
        best = min(
            sum(min(w * abs(i - s) for s in sch) * 1 for i, w in enumerate(c))
            for sch in itertools.combinations(range(n), k)
        )
        assert houses_and_schools(c, k) == best
        w = [rng.randint(1, 9) for _ in range(n)]

        @cache
        def split(i: int, j: int, w: tuple[int, ...] = tuple(w)) -> int:
            if j - i <= 1:
                return 0
            return sum(w[i:j]) + min(split(i, m) + split(m, j) for m in range(i + 1, j))

        assert knuth_optimization(w) == split(0, n)


def test_fence_painting_vs_brute(rng: random.Random) -> None:
    for _ in range(200):
        n, k = rng.randint(1, 6), rng.randint(1, 4)
        colors = [rng.choice([0, 0, *list(range(1, k + 1))]) for _ in range(n)]
        cnt = sum(
            1
            for t in itertools.product(range(1, k + 1), repeat=n)
            if all(c in (0, x) for c, x in zip(colors, t)) and all(p != q for p, q in zip(t, t[1:]))
        )
        assert fence_painting(colors, k) == cnt % 998244353
