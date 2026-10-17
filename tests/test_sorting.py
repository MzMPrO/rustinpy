"""sorting: brute-force comparisons on small random inputs (AC-05, AC-06)."""

from __future__ import annotations

import itertools
import random
from statistics import median_low

from rustinpy.sorting import (
    apartments,
    array_division,
    bisect_answer,
    bisect_answer_max,
    bisect_real,
    collecting_numbers,
    concert_tickets,
    factory_machines,
    ferris_wheel,
    josephus_order,
    josephus_queries,
    josephus_survivor,
    max_subarray_sum,
    max_subarray_sum_range,
    meet_in_middle_count,
    missing_coin_sum,
    movie_festival,
    movie_festival_k,
    nearest_smaller_values,
    nested_ranges,
    nested_ranges_count,
    playlist,
    reading_books,
    restaurant_customers,
    room_allocation,
    sliding_window_cost,
    sliding_window_median,
    stick_lengths,
    subarray_distinct_values,
    subarray_divisibility,
    subarray_sums_count,
    sum_of_four_values,
    sum_of_three_values,
    sum_of_two_values,
    tasks_and_deadlines,
    towers,
    traffic_lights,
)


def test_binary_searches(rng: random.Random) -> None:
    for _ in range(300):
        lo = rng.randint(-50, 50)
        hi = lo + rng.randint(0, 50)
        t = rng.randint(lo - 2, hi + 2)
        assert bisect_answer(lo, hi, lambda x, t=t: x >= t) == min(max(t, lo), hi + 1)
        assert bisect_answer_max(lo, hi, lambda x, t=t: x <= t) == max(min(t, hi), lo - 1)
    assert abs(bisect_real(0, 10, lambda x: x**3 >= 7) - 7 ** (1 / 3)) < 1e-9


def test_greedy_pairing(rng: random.Random) -> None:
    for _ in range(150):
        w = [rng.randint(1, 10) for _ in range(rng.randint(1, 7))]
        x = rng.randint(10, 15)
        # перебор разбиений на пары/одиночек
        best = len(w)
        idx = list(range(len(w)))
        for perm in itertools.permutations(idx):
            cnt, i = 0, 0
            pairs = 0
            while i < len(perm):
                if i + 1 < len(perm) and w[perm[i]] + w[perm[i + 1]] <= x:
                    pairs += 1
                    i += 2
                else:
                    i += 1
                cnt += 1
            best = min(best, cnt)
        assert ferris_wheel(w, x) == best
        a = [rng.randint(1, 20) for _ in range(rng.randint(1, 5))]
        b = [rng.randint(1, 20) for _ in range(rng.randint(1, 5))]
        k = rng.randint(0, 3)
        best = 0
        for r in range(min(len(a), len(b)) + 1):
            for ia in itertools.combinations(range(len(a)), r):
                for ib in itertools.permutations(range(len(b)), r):
                    if all(abs(a[i] - b[j]) <= k for i, j in zip(ia, ib)):
                        best = max(best, r)
        assert apartments(a, b, k) == best


def test_concert_tickets_vs_list(rng: random.Random) -> None:
    for _ in range(200):
        h = [rng.randint(1, 10) for _ in range(rng.randint(1, 8))]
        t = [rng.randint(1, 12) for _ in range(rng.randint(1, 8))]
        pool = list(h)
        exp = []
        for m in t:
            cand = [p for p in pool if p <= m]
            if cand:
                pool.remove(max(cand))
                exp.append(max(cand))
            else:
                exp.append(-1)
        assert concert_tickets(h, t) == exp


def rand_intervals(rng: random.Random, n: int, span: int = 15) -> list[tuple[int, int]]:
    res = []
    for _ in range(n):
        a = rng.randint(0, span)
        res.append((a, a + rng.randint(1, 5)))
    return res


def test_interval_scheduling(rng: random.Random) -> None:
    for _ in range(200):
        iv = rand_intervals(rng, rng.randint(1, 7))
        exp = max(sum(1 for a, b in iv if a <= t < b) for t in range(0, 30))
        assert restaurant_customers(iv) == exp
        best = 0
        for r in range(len(iv) + 1):
            for sub in itertools.combinations(sorted(iv), r):
                if all(sub[i][1] <= sub[i + 1][0] for i in range(len(sub) - 1)):
                    best = max(best, r)
        assert movie_festival(iv) == best
        k = rng.randint(1, 3)
        best_k = 0
        for assign in itertools.product(range(k + 1), repeat=len(iv)):  # 0 - не смотрим
            ok = True
            for m in range(1, k + 1):
                mine = sorted(iv[i] for i in range(len(iv)) if assign[i] == m)
                if any(mine[i][1] > mine[i + 1][0] for i in range(len(mine) - 1)):
                    ok = False
                    break
            if ok:
                best_k = max(best_k, sum(1 for x in assign if x))
        assert movie_festival_k(iv, k) == best_k
        days = [(a, b - 1 if b - 1 >= a else a) for a, b in iv]
        rooms, room = room_allocation(days)
        assert rooms == max(sum(1 for a, b in days if a <= t <= b) for t in range(0, 30))
        for i in range(len(days)):
            for j in range(i):
                if room[i] == room[j]:
                    assert days[i][1] < days[j][0] or days[j][1] < days[i][0]


def test_k_sums(rng: random.Random) -> None:
    for _ in range(200):
        a = [rng.randint(1, 10) for _ in range(rng.randint(1, 8))]
        x = rng.randint(2, 30)
        for f, r in ((sum_of_two_values, 2), (sum_of_three_values, 3), (sum_of_four_values, 4)):
            exists = any(
                sum(a[i] for i in c) == x for c in itertools.combinations(range(len(a)), r)
            )
            got = f(a, x)
            if exists:
                assert got is not None and len(set(got)) == r and sum(a[i] for i in got) == x
            else:
                assert got is None


def test_subarray_problems(rng: random.Random) -> None:
    for _ in range(200):
        a = [rng.randint(-5, 5) for _ in range(rng.randint(1, 10))]
        n = len(a)
        subs = [(l, r) for l in range(n) for r in range(l + 1, n + 1)]
        assert max_subarray_sum(a) == max(sum(a[l:r]) for l, r in subs)
        lo = rng.randint(1, n)
        hi = rng.randint(lo, n)
        assert max_subarray_sum_range(a, lo, hi) == max(
            sum(a[l:r]) for l, r in subs if lo <= r - l <= hi
        )
        x = rng.randint(-5, 5)
        assert subarray_sums_count(a, x) == sum(1 for l, r in subs if sum(a[l:r]) == x)
        assert subarray_divisibility(a) == sum(1 for l, r in subs if sum(a[l:r]) % n == 0)
        k = rng.randint(1, 4)
        b = [abs(v) % 4 for v in a]
        assert subarray_distinct_values(b, k) == sum(1 for l, r in subs if len(set(b[l:r])) <= k)
        assert playlist(b) == max(r - l for l, r in subs if len(set(b[l:r])) == r - l)
        assert nearest_smaller_values(a) == [
            max((j for j in range(i) if a[j] < a[i]), default=-1) for i in range(n)
        ]


def test_misc_greedy(rng: random.Random) -> None:
    for _ in range(200):
        p = [rng.randint(1, 20) for _ in range(rng.randint(1, 8))]
        assert stick_lengths(p) == min(sum(abs(v - c) for v in p) for c in range(0, 21))
        sums = {sum(c) for r in range(len(p) + 1) for c in itertools.combinations(p, r)}
        s = 1
        while s in sums:
            s += 1
        assert missing_coin_sum(p) == s
        perm = list(range(1, len(p) + 1))
        rng.shuffle(perm)
        rounds, need = 0, 1
        while need <= len(perm):
            rounds += 1
            for v in perm:
                if v == need:
                    need += 1
        assert collecting_numbers(perm) == rounds
        cubes = [rng.randint(1, 9) for _ in range(rng.randint(1, 8))]
        tops: list[int] = []
        for c in cubes:  # тот же жадный алгоритм, но перебором
            cand = [i for i, t in enumerate(tops) if t > c]
            if cand:
                best = min(cand, key=lambda i: tops[i])
                tops[best] = c
            else:
                tops.append(c)
        assert towers(cubes) == len(tops)
        tasks = [(rng.randint(1, 5), rng.randint(1, 20)) for _ in range(rng.randint(1, 6))]
        best = max(
            sum(
                d - sum(tasks[j][0] for j in perm[: i + 1])
                for i, (_, d) in enumerate(tasks[j] for j in perm)
            )
            for perm in itertools.permutations(range(len(tasks)))
        )
        assert tasks_and_deadlines(tasks) == best
        assert reading_books(p) == max(sum(p), 2 * max(p))
        k = rng.randint(1, len(p))
        best_div = min(
            max(sum(p[a:b]) for a, b in zip((0, *cuts), (*cuts, len(p))))
            for cuts in itertools.combinations(range(1, len(p)), k - 1)
        )
        assert array_division(p, k) == best_div
        t = [rng.randint(1, 5) for _ in range(rng.randint(1, 4))]
        need_k = rng.randint(1, 15)
        T = 0
        while sum(T // x for x in t) < need_k:
            T += 1
        assert factory_machines(need_k, t) == T


def test_traffic_lights_vs_brute(rng: random.Random) -> None:
    for _ in range(150):
        x = rng.randint(2, 30)
        pos = rng.sample(range(1, x), rng.randint(1, min(8, x - 1)))
        exp = []
        for i in range(len(pos)):
            pts = sorted({0, x, *pos[: i + 1]})
            exp.append(max(b - a for a, b in zip(pts, pts[1:])))
        assert traffic_lights(x, pos) == exp


def test_josephus_family() -> None:
    for n in range(1, 40):
        for k in range(1, 6):
            circle = list(range(1, n + 1))
            order = []
            i = 0
            while circle:
                i = (i + k - 1) % len(circle)
                order.append(circle.pop(i))
            assert josephus_order(n, k) == order
            assert josephus_survivor(n, k) == order[-1]
            if k == 2:
                assert [josephus_queries(n, q) for q in range(1, n + 1)] == order
    order = josephus_order(2000, 2)
    for q in (1, 2, 999, 1000, 1001, 1999, 2000):
        assert josephus_queries(2000, q) == order[q - 1]
    assert 1 <= josephus_queries(10**9, 10**9) <= 10**9


def test_nested_ranges_vs_brute(rng: random.Random) -> None:
    for _ in range(200):
        rs = []
        for _ in range(rng.randint(1, 8)):
            a = rng.randint(1, 8)
            rs.append((a, a + rng.randint(0, 5)))
        contains = [
            sum(
                1
                for j in range(len(rs))
                if j != i and rs[i][0] <= rs[j][0] and rs[j][1] <= rs[i][1]
            )
            for i in range(len(rs))
        ]
        contained = [
            sum(
                1
                for j in range(len(rs))
                if j != i and rs[j][0] <= rs[i][0] and rs[i][1] <= rs[j][1]
            )
            for i in range(len(rs))
        ]
        assert nested_ranges_count(rs) == (contains, contained)
        assert nested_ranges(rs) == ([c > 0 for c in contains], [c > 0 for c in contained])


def test_meet_in_middle_vs_brute(rng: random.Random) -> None:
    for _ in range(100):
        a = [rng.randint(1, 10) for _ in range(rng.randint(0, 12))]
        x = rng.randint(0, 30)
        exp = sum(1 for r in range(len(a) + 1) for c in itertools.combinations(a, r) if sum(c) == x)
        assert meet_in_middle_count(a, x) == exp


def test_sliding_median_and_cost(rng: random.Random) -> None:
    for _ in range(200):
        a = [rng.randint(1, 9) for _ in range(rng.randint(1, 15))]
        k = rng.randint(1, len(a))
        wins = [a[i : i + k] for i in range(len(a) - k + 1)]
        meds = [median_low(w) for w in wins]
        assert sliding_window_median(a, k) == meds
        assert sliding_window_cost(a, k) == [sum(abs(v - m) for v in w) for w, m in zip(wins, meds)]
