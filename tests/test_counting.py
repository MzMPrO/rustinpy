"""counting: brute-force checks of the counting problems and constructions (AC-05, AC-06)."""

from __future__ import annotations

import itertools
import random
from collections import Counter, deque

import pytest

from rustinpy.counting import (
    binary_subsequences,
    bubble_sort_rounds,
    coding_company,
    coin_arrangement,
    coin_grid,
    counting_bishops,
    counting_permutations,
    counting_reorders,
    counting_sequences,
    cyclic_array,
    empty_string,
    filled_subgrid_count,
    functional_graph_distribution,
    grid_completion,
    grid_puzzle_i,
    grid_puzzle_ii,
    maximum_building,
    maximum_building_counts,
    permutation_inversions,
    programmers_and_artists,
    raab_game_construct,
    raab_game_count,
    school_excursion,
    sorting_methods,
    stick_divisions,
    swap_round_sorting,
    tournament_graph_distribution,
    two_stacks_sorting,
)

MOD7 = 10**9 + 7


def rand_grid(rng: random.Random, n: int, m: int, alphabet: str) -> list[str]:
    return ["".join(rng.choice(alphabet) for _ in range(m)) for _ in range(n)]


def test_filled_subgrid_count(rng: random.Random) -> None:
    for _ in range(150):
        n, m, k = rng.randint(1, 5), rng.randint(1, 5), rng.randint(1, 3)
        g = rand_grid(rng, n, m, "ABC"[:k])
        rect = [0] * k
        sq = [0] * k
        for r1 in range(n):
            for r2 in range(r1, n):
                for c1 in range(m):
                    for c2 in range(c1, m):
                        cells = {g[r][c] for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)}
                        if len(cells) == 1:
                            idx = ord(cells.pop()) - 65
                            rect[idx] += 1
                            if r2 - r1 == c2 - c1:
                                sq[idx] += 1
        assert filled_subgrid_count(g, k) == rect
        assert filled_subgrid_count(g, k, squares=True) == sq


def test_counting_bishops() -> None:
    for n in range(1, 5):
        cells = [(r, c) for r in range(n) for c in range(n)]
        for k in range(0, 2 * n + 2):
            cnt = sum(
                1
                for s in itertools.combinations(cells, k)
                if all(
                    a[0] + a[1] != b[0] + b[1] and a[0] - a[1] != b[0] - b[1]
                    for a, b in itertools.combinations(s, 2)
                )
            )
            assert counting_bishops(n, k) == cnt, (n, k)


def test_counting_permutations() -> None:
    for n in range(0, 10):
        cnt = sum(
            1
            for p in itertools.permutations(range(n))
            if all(abs(p[i] - p[i + 1]) != 1 for i in range(n - 1))
        )
        assert counting_permutations(n) == cnt


def test_permutation_inversions() -> None:
    for n in range(0, 7):
        dist = Counter(
            sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j])
            for p in itertools.permutations(range(n))
        )
        for k in range(0, n * (n - 1) // 2 + 3):
            assert permutation_inversions(n, k) == dist.get(k, 0)


def test_counting_reorders(rng: random.Random) -> None:
    for _ in range(80):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(1, 8)))
        cnt = sum(
            1
            for p in set(itertools.permutations(s))
            if all(p[i] != p[i + 1] for i in range(len(p) - 1))
        )
        assert counting_reorders(s) == cnt, s


def all_completions(grid: list[str]) -> int:
    n = len(grid)
    cnt = 0
    for pa in itertools.permutations(range(n)):
        for pb in itertools.permutations(range(n)):
            ok = True
            for i in range(n):
                if pa[i] == pb[i]:
                    ok = False
                    break
                for j in range(n):
                    want = "A" if pa[i] == j else "B" if pb[i] == j else "."
                    if grid[i][j] != "." and grid[i][j] != want:
                        ok = False
                        break
                if not ok:
                    break
            cnt += ok
    return cnt


def test_grid_completion(rng: random.Random) -> None:
    for _ in range(150):
        n = rng.randint(1, 4)
        g = [list("." * n) for _ in range(n)]
        for _ in range(rng.randint(0, n + 1)):
            g[rng.randrange(n)][rng.randrange(n)] = rng.choice("AB")
        grid = ["".join(r) for r in g]
        assert grid_completion(grid) == all_completions(grid), grid


def test_raab_game() -> None:
    for n in range(0, 6):
        dist: Counter[tuple[int, int]] = Counter()
        for q in itertools.permutations(range(1, n + 1)):
            a = sum(1 for i in range(n) if q[i] < i + 1)  # побед первого (он играет 1..n)
            b = sum(1 for i in range(n) if q[i] > i + 1)
            dist[a, b] += 1
        fact = 1
        for i in range(2, n + 1):
            fact *= i
        for a in range(n + 2):
            for b in range(n + 2):
                assert raab_game_count(n, a, b) == dist.get((a, b), 0) * fact % MOD7, (n, a, b)
                res = raab_game_construct(n, a, b)
                assert (res is not None) == ((a, b) in dist), (n, a, b)
                if res is not None:
                    x, y = res
                    assert sorted(x) == sorted(y) == list(range(1, n + 1))
                    assert sum(u > v for u, v in zip(x, y)) == a
                    assert sum(u < v for u, v in zip(x, y)) == b


def components(f: tuple[int, ...]) -> int:
    n = len(f)
    par = list(range(n))

    def find(x: int) -> int:
        while par[x] != x:
            x = par[x]
        return x

    for i, j in enumerate(f):
        par[find(i)] = find(j)
    return len({find(i) for i in range(n)})


def test_functional_graph_distribution() -> None:
    for n in range(1, 6):
        dist = Counter(components(f) for f in itertools.product(range(n), repeat=n))
        assert functional_graph_distribution(n) == [dist.get(k, 0) for k in range(1, n + 1)]


def erase_ways(s: str) -> int:
    memo: dict[str, int] = {"": 1}
    # перебор в ширину по всем достижимым строкам, затем снизу вверх
    seen = {s}
    q = deque([s])
    while q:
        t = q.popleft()
        for i in range(len(t) - 1):
            if t[i] == t[i + 1]:
                u = t[:i] + t[i + 2 :]
                if u not in seen:
                    seen.add(u)
                    q.append(u)
    stack = sorted(seen, key=len)
    for t in stack:
        if t:
            memo[t] = sum(memo[t[:i] + t[i + 2 :]] for i in range(len(t) - 1) if t[i] == t[i + 1])
    return memo[s]


def test_empty_string(rng: random.Random) -> None:
    for _ in range(150):
        s = "".join(rng.choice("ab") for _ in range(2 * rng.randint(0, 5)))
        assert empty_string(s) == erase_ways(s), s
    assert empty_string("abc") == 0


def test_counting_sequences() -> None:
    for n in range(0, 7):
        for k in range(0, 5):
            cnt = sum(1 for t in itertools.product(range(k), repeat=n) if len(set(t)) == k)
            assert counting_sequences(n, k) == cnt


def scc_count(n: int, adj: list[list[bool]]) -> int:
    reach = [row[:] for row in adj]
    for i in range(n):
        reach[i][i] = True
    for k in range(n):
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True
    return len({tuple(reach[i][j] and reach[j][i] for j in range(n)) for i in range(n)})


def test_tournament_graph_distribution() -> None:
    for n in range(1, 6):
        pairs = list(itertools.combinations(range(n), 2))
        dist: Counter[int] = Counter()
        for mask in range(1 << len(pairs)):
            adj = [[False] * n for _ in range(n)]
            for t, (i, j) in enumerate(pairs):
                if mask >> t & 1:
                    adj[i][j] = True
                else:
                    adj[j][i] = True
            dist[scc_count(n, adj)] += 1
        assert tournament_graph_distribution(n) == [dist.get(k, 0) for k in range(1, n + 1)]


def test_maximum_building(rng: random.Random) -> None:
    for _ in range(150):
        n, m = rng.randint(1, 5), rng.randint(1, 5)
        g = rand_grid(rng, n, m, "..*")
        cnt = [[0] * m for _ in range(n)]
        best = 0
        for r1 in range(n):
            for r2 in range(r1, n):
                for c1 in range(m):
                    for c2 in range(c1, m):
                        if all(
                            g[r][c] == "." for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)
                        ):
                            cnt[r2 - r1][c2 - c1] += 1
                            best = max(best, (r2 - r1 + 1) * (c2 - c1 + 1))
        assert maximum_building(g) == best
        assert maximum_building_counts(g) == cnt


def test_cyclic_array(rng: random.Random) -> None:
    for _ in range(300):
        n = rng.randint(1, 9)
        k = rng.randint(1, 12)
        a = [rng.randint(1, k) for _ in range(n)]
        best = n
        for s in range(n):  # жадность от каждой точки разреза
            b = a[s:] + a[:s]
            parts, cur = 1, 0
            for x in b:
                if cur + x > k:
                    parts += 1
                    cur = 0
                cur += x
            best = min(best, parts)
        assert cyclic_array(a, k) == best, (a, k)


def bfs_dist(p: tuple[int, ...], moves: str) -> int:
    n = len(p)
    target = tuple(range(1, n + 1))
    dist = {p: 0}
    q = deque([p])
    while q:
        cur = q.popleft()
        if cur == target:
            return dist[cur]
        nxt = []
        if moves == "adj":
            for i in range(n - 1):
                t = list(cur)
                t[i], t[i + 1] = t[i + 1], t[i]
                nxt.append(tuple(t))
        elif moves == "swap":
            for i, j in itertools.combinations(range(n), 2):
                t = list(cur)
                t[i], t[j] = t[j], t[i]
                nxt.append(tuple(t))
        else:
            for i in range(n):
                rest = list(cur[:i] + cur[i + 1 :])
                places = range(n) if moves == "move" else [0]
                for j in places:
                    t = rest[:]
                    t.insert(j, cur[i])
                    nxt.append(tuple(t))
        for t in nxt:
            if t not in dist:
                dist[t] = dist[cur] + 1
                q.append(t)
    raise AssertionError


def test_sorting_methods() -> None:
    for n in range(1, 6):
        for p in itertools.permutations(range(1, n + 1)):
            want = tuple(bfs_dist(p, mv) for mv in ("adj", "swap", "move", "front"))
            assert sorting_methods(list(p)) == want, p
    assert sorting_methods([]) == (0, 0, 0, 0)


def test_bubble_sort_rounds(rng: random.Random) -> None:
    for _ in range(300):
        a = [rng.randint(1, 4) for _ in range(rng.randint(0, 8))]
        b = a[:]
        rounds = 0
        while True:
            swapped = False
            for i in range(len(b) - 1):
                if b[i] > b[i + 1]:
                    b[i], b[i + 1] = b[i + 1], b[i]
                    swapped = True
            if not swapped:
                break
            rounds += 1
        assert bubble_sort_rounds(a) == rounds, a


def test_programmers_and_artists(rng: random.Random) -> None:
    for _ in range(200):
        n = rng.randint(1, 7)
        pairs = [(rng.randint(1, 10), rng.randint(1, 10)) for _ in range(n)]
        a = rng.randint(0, n)
        b = rng.randint(0, n - a)
        best = max(
            sum(pairs[i][0] for i in range(n) if role[i] == 1)
            + sum(pairs[i][1] for i in range(n) if role[i] == 2)
            for role in itertools.product(range(3), repeat=n)
            if role.count(1) == a and role.count(2) == b
        )
        assert programmers_and_artists(pairs, a, b) == best


def set_partitions(items: list[int]) -> list[list[list[int]]]:
    res: list[list[list[int]]] = [[]]
    for x in items:
        nxt = []
        for part in res:
            for i in range(len(part)):
                nxt.append([*part[:i], [*part[i], x], *part[i + 1 :]])
            nxt.append([*part, [x]])
        res = nxt
    return res


def test_coding_company(rng: random.Random) -> None:
    for _ in range(80):
        n = rng.randint(1, 6)
        s = [rng.randint(1, 10) for _ in range(n)]
        x = rng.randint(0, 12)
        cnt = sum(
            1
            for part in set_partitions(list(range(n)))
            if sum(max(s[i] for i in g) - min(s[i] for i in g) for g in part) <= x
        )
        assert coding_company(s, x) == cnt, (s, x)


def stacks_ok(a: list[int], labels: list[int]) -> bool:
    st: list[list[int]] = [[], []]
    need = 1
    for v, lab in zip(a, labels):
        st[lab - 1].append(v)
        moved = True
        while moved:
            moved = False
            for s in st:
                if s and s[-1] == need:
                    s.pop()
                    need += 1
                    moved = True
    return need == len(a) + 1


def test_two_stacks_sorting() -> None:
    for n in range(1, 8):
        for p in itertools.permutations(range(1, n + 1)):
            a = list(p)
            possible = any(stacks_ok(a, list(lab)) for lab in itertools.product((1, 2), repeat=n))
            res = two_stacks_sorting(a)
            assert (res is not None) == possible, a
            if res is not None:
                assert stacks_ok(a, res), (a, res)


def merge_cost(t: tuple[int, ...]) -> int:
    """Перебор: минимум суммы слияний по всем порядкам (обратная задача к разрезам)."""
    best: dict[tuple[int, ...], int] = {}
    stack = [t]
    order = []
    while stack:
        u = stack.pop()
        if u in best or len(u) == 1:
            continue
        best[u] = -1
        order.append(u)
        for i, j in itertools.combinations(range(len(u)), 2):
            rest = [u[k] for k in range(len(u)) if k not in (i, j)]
            stack.append(tuple(sorted([*rest, u[i] + u[j]])))
    for u in sorted(order, key=len):
        vals = []
        for i, j in itertools.combinations(range(len(u)), 2):
            rest = [u[k] for k in range(len(u)) if k not in (i, j)]
            w = tuple(sorted([*rest, u[i] + u[j]]))
            vals.append(u[i] + u[j] + (0 if len(w) == 1 else best[w]))
        best[u] = min(vals)
    return 0 if len(t) == 1 else best[t]


def test_stick_divisions(rng: random.Random) -> None:
    for _ in range(100):
        d = [rng.randint(1, 9) for _ in range(rng.randint(1, 6))]
        assert stick_divisions(sum(d), d) == merge_cost(tuple(sorted(d)))
    with pytest.raises(ValueError):
        stick_divisions(3, [1, 1])


def test_swap_round_sorting() -> None:
    for n in range(0, 8):
        for p in itertools.permutations(range(1, n + 1)):
            rounds = swap_round_sorting(list(p))
            cur = list(p)
            for r in rounds:
                used = [i for pair in r for i in pair]
                assert len(used) == len(set(used))
                for i, j in r:
                    cur[i], cur[j] = cur[j], cur[i]
            assert cur == sorted(p)
            if list(p) == sorted(p):
                want = 0
            elif all(p[p[i] - 1] == i + 1 for i in range(n)):
                want = 1
            else:
                want = 2
            assert len(rounds) == want


def distinct_subseq(s: str) -> int:
    return len(
        {"".join(s[i] for i in range(len(s)) if mask >> i & 1) for mask in range(1, 1 << len(s))}
    )


def test_binary_subsequences() -> None:
    shortest: dict[int, int] = {}
    for length in range(1, 11):
        for t in itertools.product("01", repeat=length):
            c = distinct_subseq("".join(t))
            shortest.setdefault(c, length)
    for n in range(1, 40):
        s = binary_subsequences(n)
        assert distinct_subseq(s) == n
        assert len(s) == shortest[n], n


def root(par: list[int], x: int) -> int:
    while par[x] != x:
        x = par[x]
    return x


def test_school_excursion(rng: random.Random) -> None:
    for _ in range(150):
        n = rng.randint(1, 9)
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, n))]
        par = list(range(n))
        for u, v in edges:
            par[root(par, u)] = root(par, v)
        sizes = list(Counter(root(par, v) for v in range(n)).values())
        sums = {sum(c) for r in range(len(sizes) + 1) for c in itertools.combinations(sizes, r)}
        want = "".join("1" if k in sums else "0" for k in range(1, n + 1))
        assert school_excursion(n, edges) == want


def test_coin_grid(rng: random.Random) -> None:
    for _ in range(150):
        n, m = rng.randint(1, 4), rng.randint(1, 4)
        g = rand_grid(rng, n, m, "o..")
        coins = [(i, j) for i in range(n) for j in range(m) if g[i][j] == "o"]
        best = n + m
        for rmask in range(1 << n):
            for cmask in range(1 << m):
                if all(rmask >> i & 1 or cmask >> j & 1 for i, j in coins):
                    best = min(best, bin(rmask).count("1") + bin(cmask).count("1"))
        cnt, moves = coin_grid(g)
        assert cnt == best == len(moves)
        rows = {i for t, i in moves if t == 1}
        cols = {j for t, j in moves if t == 2}
        assert all(i in rows or j in cols for i, j in coins)


def test_coin_arrangement(rng: random.Random) -> None:
    for _ in range(80):
        n = rng.randint(1, 4)
        cells = [(r, c) for r in range(2) for c in range(n)]
        coins = [rng.choice(cells) for _ in range(2 * n)]
        top = [sum(1 for x in coins if x == (0, c)) for c in range(n)]
        bot = [sum(1 for x in coins if x == (1, c)) for c in range(n)]
        best = min(
            sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in zip(coins, perm))
            for perm in itertools.permutations(cells)
        )
        assert coin_arrangement(top, bot) == best, (top, bot)


def test_grid_puzzles(rng: random.Random) -> None:
    for _ in range(120):
        n, m = rng.randint(1, 3), rng.randint(1, 3)
        a = [rng.randint(0, m) for _ in range(n)]
        b = [rng.randint(0, n) for _ in range(m)]
        val = [[rng.randint(0, 9) for _ in range(m)] for _ in range(n)]
        best = None
        for mask in range(1 << (n * m)):
            cell = [[mask >> (i * m + j) & 1 for j in range(m)] for i in range(n)]
            if all(sum(cell[i]) == a[i] for i in range(n)) and all(
                sum(cell[i][j] for i in range(n)) == b[j] for j in range(m)
            ):
                s = sum(val[i][j] for i in range(n) for j in range(m) if cell[i][j])
                best = s if best is None else max(best, s)
        g1 = grid_puzzle_i(a, b)
        g2 = grid_puzzle_ii(a, b, val)
        assert (g1 is None) == (best is None) == (g2 is None), (a, b)
        for res in (g1, None if g2 is None else g2[1]):
            if res is not None:
                assert [r.count("X") for r in res] == a
                assert [sum(r[j] == "X" for r in res) for j in range(m)] == b
        if g2 is not None:
            total, rows = g2
            assert total == best
            assert total == sum(val[i][j] for i in range(n) for j in range(m) if rows[i][j] == "X")
