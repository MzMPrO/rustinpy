"""ds: every structure against a naive array on random operations (AC-05, AC-06)."""

from __future__ import annotations

import random
from fractions import Fraction
from math import gcd

import pytest

from rustinpy.ds import (
    Fenwick,
    Fenwick2D,
    FenwickRangeAdd,
    FenwickRangeRange,
    ImplicitTreap,
    LazySegAddMin,
    LazySegAddSum,
    LazySegArithmetic,
    LazySegAssignAddSum,
    MergeSortTree,
    MinStack,
    MonotonicQueue,
    PersistentSegTree,
    PrefixSum2D,
    SegTree,
    SegTreeFlipRuns,
    SegTreeMaxPrefix,
    SegTreeMaxSubarray,
    SegTreeRuns,
    SortedList,
    SparseTable,
    SqrtDecomposition,
    Treap,
    TwoStackQueue,
    cut_and_paste,
    distinct_values_queries,
    dynamic_connectivity_offline,
    exclusions,
    generic_strings,
    hotel_queries,
    isotonic_sse_mod,
    list_removals,
    longest_window_no_repeats,
    missing_coin_sum_queries,
    mo_distinct_count,
    mo_order,
    mo_with_updates,
    movie_festival_queries,
    new_roads_queries,
    pav,
    pizzeria_queries,
    prefix_sums,
    range_kth_smallest,
    reversal_sorting,
    salary_queries,
    sliding_window_distinct,
    sliding_window_inversions,
    sliding_window_mex,
    sliding_window_min,
    sliding_window_mode,
    sliding_window_or,
    sliding_window_sum,
    sliding_window_xor,
    subarray_mex_offline,
    substring_reversals,
)

ITER = 300


def rand_range(rng: random.Random, n: int) -> tuple[int, int]:
    l = rng.randint(0, n)
    r = rng.randint(0, n)
    return min(l, r), max(l, r)


def test_prefix_sums_1d_2d(rng: random.Random) -> None:
    for _ in range(100):
        a = [rng.randint(-9, 9) for _ in range(rng.randint(0, 20))]
        p = prefix_sums(a)
        l, r = rand_range(rng, len(a))
        assert p[r] - p[l] == sum(a[l:r])
        R, C = rng.randint(1, 6), rng.randint(1, 6)
        g = [[rng.randint(-5, 5) for _ in range(C)] for _ in range(R)]
        ps = PrefixSum2D(g)
        r1, r2 = rand_range(rng, R)
        c1, c2 = rand_range(rng, C)
        exp = sum(g[r][c] for r in range(r1, r2) for c in range(c1, c2))
        assert ps.query(r1, c1, r2, c2) == exp


def test_fenwick_family(rng: random.Random) -> None:
    for _ in range(60):
        n = rng.randint(1, 30)
        a = [rng.randint(0, 3) for _ in range(n)]
        f = Fenwick(list(a))
        g = FenwickRangeAdd(list(a))
        h = FenwickRangeRange(n)
        b = [0] * n
        for _ in range(ITER):
            t = rng.randrange(5)
            if t == 0:
                i, d = rng.randrange(n), rng.randint(0, 3)
                f.add(i, d)
                a[i] += d
            elif t == 1:
                l, r = rand_range(rng, n)
                assert f.range_sum(l, r) == sum(a[l:r])
            elif t == 2:
                total = sum(a)
                if total:
                    k = rng.randrange(total)
                    acc = 0
                    for i, x in enumerate(a):
                        acc += x
                        if acc > k:
                            assert f.kth(k) == i
                            break
            elif t == 3:
                l, r = rand_range(rng, n)
                d = rng.randint(-5, 5)
                g.range_add(l, r, d)
                h.range_add(l, r, d)
                for i in range(l, r):
                    b[i] += d
            else:
                l, r = rand_range(rng, n)
                assert h.range_sum(l, r) == sum(b[l:r])
    assert Fenwick(5).prefix(5) == 0


def test_fenwick_range_add_point(rng: random.Random) -> None:
    for _ in range(50):
        n = rng.randint(1, 25)
        a = [rng.randint(-5, 5) for _ in range(n)]
        g = FenwickRangeAdd(list(a))
        for _ in range(100):
            l, r = rand_range(rng, n)
            d = rng.randint(-5, 5)
            g.range_add(l, r, d)
            for i in range(l, r):
                a[i] += d
            assert [g.point(i) for i in range(n)] == a


def test_fenwick_2d(rng: random.Random) -> None:
    for _ in range(30):
        R, C = rng.randint(1, 6), rng.randint(1, 6)
        g = [[0] * C for _ in range(R)]
        f = Fenwick2D(R, C)
        for _ in range(100):
            r, c, d = rng.randrange(R), rng.randrange(C), rng.randint(-3, 3)
            f.add(r, c, d)
            g[r][c] += d
            r1, r2 = rand_range(rng, R)
            c1, c2 = rand_range(rng, C)
            exp = sum(g[x][y] for x in range(r1, r2) for y in range(c1, c2))
            assert f.query(r1, c1, r2, c2) == exp


def test_sparse_table(rng: random.Random) -> None:
    for _ in range(100):
        a = [rng.randint(1, 50) for _ in range(rng.randint(1, 40))]
        for op in (min, max, gcd):
            st = SparseTable(a, op)
            for _ in range(20):
                l = rng.randrange(len(a))
                r = rng.randint(l + 1, len(a))
                acc = a[l]
                for x in a[l + 1 : r]:
                    acc = op(acc, x)
                assert st.query(l, r) == acc


def test_segtree_generic_and_binary_search(rng: random.Random) -> None:
    for _ in range(40):
        n = rng.randint(1, 30)
        a = [rng.randint(0, 9) for _ in range(n)]
        st = SegTree(list(a), lambda x, y: x + y, 0)
        mn = SegTree(list(a), min, 1 << 60)
        # некоммутативная операция: конкатенация строк
        cat = SegTree([str(x) for x in a], lambda x, y: x + y, "")
        for _ in range(ITER):
            t = rng.randrange(4)
            if t == 0:
                i, v = rng.randrange(n), rng.randint(0, 9)
                a[i] = v
                st.set(i, v)
                mn.set(i, v)
                cat.set(i, str(v))
                assert st.get(i) == v
            elif t == 1:
                l, r = rand_range(rng, n)
                assert st.query(l, r) == sum(a[l:r])
                assert mn.query(l, r) == min(a[l:r], default=1 << 60)
                assert cat.query(l, r) == "".join(map(str, a[l:r]))
            elif t == 2:
                l = rng.randint(0, n)
                lim = rng.randint(0, 40)
                r = l
                while r < n and sum(a[l : r + 1]) <= lim:
                    r += 1
                assert st.max_right(l, lambda s, lim=lim: s <= lim) == r
            else:
                r = rng.randint(0, n)
                lim = rng.randint(0, 40)
                l = r
                while l > 0 and sum(a[l - 1 : r]) <= lim:
                    l -= 1
                assert st.min_left(r, lambda s, lim=lim: s <= lim) == l
        assert st.all() == sum(a)


def best_subarray(a: list[int]) -> int:
    return max(sum(a[i:j]) for i in range(len(a)) for j in range(i + 1, len(a) + 1))


def test_segtree_merge_variants(rng: random.Random) -> None:
    for _ in range(40):
        n = rng.randint(1, 20)
        a = [rng.randint(-6, 6) for _ in range(n)]
        ms = SegTreeMaxSubarray(list(a))
        mp = SegTreeMaxPrefix(list(a))
        bits = "".join(rng.choice("01") for _ in range(n))
        runs = SegTreeRuns(bits)
        for _ in range(100):
            i, v = rng.randrange(n), rng.randint(-6, 6)
            a[i] = v
            ms.set(i, v)
            mp.set(i, v)
            l = rng.randrange(n)
            r = rng.randint(l + 1, n)
            assert ms.query(l, r) == best_subarray(a[l:r])
            assert mp.query(l, r) == max(0, max(sum(a[l:k]) for k in range(l + 1, r + 1)))
            j = rng.randrange(n)
            bits = bits[:j] + rng.choice("01") + bits[j + 1 :]
            runs.set(j, bits[j])
            longest = max(len(x) for x in bits.replace("01", "0 1").replace("10", "1 0").split())
            assert runs.longest() == longest
        assert ms.best() == best_subarray(a)
    with pytest.raises(ValueError):
        SegTreeMaxSubarray([1]).query(0, 0)


def test_lazy_trees(rng: random.Random) -> None:
    for _ in range(40):
        n = rng.randint(1, 25)
        a = [rng.randint(-5, 5) for _ in range(n)]
        s1, s2, s3 = LazySegAddSum(list(a)), LazySegAddMin(list(a)), LazySegAssignAddSum(list(a))
        s4 = LazySegArithmetic(list(a))
        b = list(a)  # для AssignAdd
        c = list(a)  # для арифметики
        for _ in range(ITER):
            t = rng.randrange(6)
            l, r = rand_range(rng, n)
            x = rng.randint(-5, 5)
            if t == 0:
                s1.range_add(l, r, x)
                s2.range_add(l, r, x)
                for i in range(l, r):
                    a[i] += x
            elif t == 1:
                assert s1.range_sum(l, r) == sum(a[l:r])
                assert s2.range_min(l, r) == min(a[l:r], default=1 << 60)
            elif t == 2:
                s3.range_add(l, r, x)
                for i in range(l, r):
                    b[i] += x
            elif t == 3:
                s3.range_assign(l, r, x)
                for i in range(l, r):
                    b[i] = x
                assert s3.range_sum(0, n) == sum(b)
            elif t == 4:
                first, step = rng.randint(-3, 3), rng.randint(-3, 3)
                s4.add_progression(l, r, first, step)
                for i in range(l, r):
                    c[i] += first + step * (i - l)
            else:
                assert s3.range_sum(l, r) == sum(b[l:r])
                assert s4.range_sum(l, r) == sum(c[l:r])
    assert LazySegAddSum(3).range_sum(0, 3) == 0


def test_persistent_and_kth_and_merge_sort_tree(rng: random.Random) -> None:
    for _ in range(40):
        n = rng.randint(1, 20)
        a = [rng.randint(-5, 5) for _ in range(n)]
        pst = PersistentSegTree(a)
        versions = [(pst.root0, list(a))]
        for _ in range(60):
            root, arr = rng.choice(versions)
            i, v = rng.randrange(n), rng.randint(-5, 5)
            new = list(arr)
            new[i] = v
            versions.append((pst.set(root, i, v), new))
            root, arr = rng.choice(versions)
            l, r = rand_range(rng, n)
            assert pst.query(root, l, r) == sum(arr[l:r])
        qs = []
        for _ in range(50):
            l = rng.randrange(n)
            r = rng.randint(l + 1, n)
            qs.append((l, r, rng.randint(1, r - l)))
        assert range_kth_smallest(a, qs) == [sorted(a[l:r])[k - 1] for l, r, k in qs]
        mst = MergeSortTree(a)
        for _ in range(30):
            l, r = rand_range(rng, n)
            x = rng.randint(-6, 6)
            assert mst.count_le(l, r, x) == sum(1 for v in a[l:r] if v <= x)


def test_mo_and_sqrt(rng: random.Random) -> None:
    for _ in range(50):
        n = rng.randint(1, 30)
        a = [rng.randint(0, 6) for _ in range(n)]
        qs = [rand_range(rng, n) for _ in range(rng.randint(0, 30))]
        exp = [len(set(a[l:r])) for l, r in qs]
        assert mo_distinct_count(a, qs) == exp
        assert distinct_values_queries(a, qs) == exp
        assert sorted(mo_order(qs)) == list(range(len(qs)))
        ops: list[tuple[str, int, int]] = []
        arr = list(a)
        exp2 = []
        for _ in range(30):
            if rng.random() < 0.4:
                i, v = rng.randrange(n), rng.randint(0, 6)
                ops.append(("!", i, v))
                arr[i] = v
            else:
                l, r = rand_range(rng, n)
                ops.append(("?", l, r))
                exp2.append(len(set(arr[l:r])))
        assert mo_with_updates(a, ops) == exp2
        sd = SqrtDecomposition(list(a))
        for _ in range(30):
            i, v = rng.randrange(n), rng.randint(-5, 5)
            sd.set(i, v)
            a[i] = v
            l, r = rand_range(rng, n)
            assert sd.range_sum(l, r) == sum(a[l:r])
    assert mo_order([]) == []


def test_treap_vs_sorted_list(rng: random.Random) -> None:
    t = Treap()
    sl = SortedList()
    ref: list[int] = []
    for _ in range(3000):
        op = rng.randrange(6)
        x = rng.randint(0, 30)
        if op <= 1:
            t.insert(x)
            sl.add(x)
            ref.append(x)
            ref.sort()
        elif op == 2:
            exp = x in ref
            assert t.erase(x) == exp
            assert sl.discard(x) == exp
            if exp:
                ref.remove(x)
        elif op == 3 and ref:
            k = rng.randrange(len(ref))
            assert t.kth(k) == ref[k] == sl[k]
            assert sl[-1 - k] == ref[-1 - k]
        elif op == 4:
            cnt = sum(1 for v in ref if v < x)
            assert t.rank(x) == cnt == sl.bisect_left(x)
            assert sl.bisect_right(x) == sum(1 for v in ref if v <= x)
            assert sl.count(x) == ref.count(x)
            assert (x in t) == (x in sl) == (x in ref)
            assert sl.lt(x) == max((v for v in ref if v < x), default=None)
            assert sl.le(x) == max((v for v in ref if v <= x), default=None)
            assert sl.gt(x) == min((v for v in ref if v > x), default=None)
            assert sl.ge(x) == min((v for v in ref if v >= x), default=None)
        elif ref and rng.random() < 0.3:
            i = rng.randrange(-len(ref), len(ref))
            assert sl.pop(i) == ref.pop(i)
            t = Treap()
            for v in ref:
                t.insert(v)
        assert len(t) == len(ref) == len(sl)
    assert t.to_list() == ref == list(sl)
    with pytest.raises(IndexError):
        Treap().kth(0)
    with pytest.raises(ValueError):
        SortedList().remove(1)
    big = SortedList(rng.randint(0, 10**6) for _ in range(5000))
    assert list(big) == sorted(big)


def test_implicit_treap_ops(rng: random.Random) -> None:
    for _ in range(50):
        n = rng.randint(1, 30)
        a = [rng.randint(0, 50) for _ in range(n)]
        it = ImplicitTreap(list(a))
        for _ in range(60):
            l, r = rand_range(rng, n)
            if rng.random() < 0.5:
                it.reverse(l, r)
                a[l:r] = a[l:r][::-1]
            else:
                it.move_to_end(l, r)
                a = a[:l] + a[r:] + a[l:r]
            assert it.to_list() == a and len(it) == n
        assert it.argmin(it.root) == a.index(min(a))
        s = "".join(rng.choice("abc") for _ in range(n))
        ops = [rand_range(rng, n) for _ in range(20)]
        cur = s
        for l, r in ops:
            cur = cur[:l] + cur[r:] + cur[l:r]
        assert cut_and_paste(s, ops) == cur
        cur = s
        for l, r in ops:
            cur = cur[:l] + cur[l:r][::-1] + cur[r:]
        assert substring_reversals(s, ops) == cur
        p = list(range(n))
        rng.shuffle(p)
        rev = reversal_sorting(p)
        q = list(p)
        for l, r in rev:
            q[l:r] = q[l:r][::-1]
        assert q == sorted(p) and len(rev) <= n


def test_offline_problems(rng: random.Random) -> None:
    for _ in range(80):
        n = rng.randint(1, 15)
        h = [rng.randint(0, 9) for _ in range(n)]
        groups = [rng.randint(1, 9) for _ in range(10)]
        hh = list(h)
        exp = []
        for g in groups:
            i = next((i for i, x in enumerate(hh) if x >= g), -1)
            if i >= 0:
                hh[i] -= g
            exp.append(i)
        assert hotel_queries(h, groups) == exp
        a = [rng.randint(0, 9) for _ in range(n)]
        cur = list(a)
        positions, removed = [], []
        while cur:
            p = rng.randrange(len(cur))
            positions.append(p)
            removed.append(cur.pop(p))
        assert list_removals(a, positions) == removed
        sal = [rng.randint(1, 20) for _ in range(n)]
        ops: list[tuple[str, int, int]] = []
        cur = list(sal)
        exp = []
        for _ in range(20):
            if rng.random() < 0.5:
                k, x = rng.randrange(n), rng.randint(1, 20)
                ops.append(("!", k, x))
                cur[k] = x
            else:
                lo = rng.randint(1, 20)
                hi = rng.randint(lo, 20)
                ops.append(("?", lo, hi))
                exp.append(sum(1 for v in cur if lo <= v <= hi))
        assert salary_queries(sal, ops) == exp
        price = [rng.randint(1, 30) for _ in range(n)]
        pops: list[tuple[str, int, int]] = []
        cur = list(price)
        exp = []
        for _ in range(20):
            if rng.random() < 0.4:
                k, x = rng.randrange(n), rng.randint(1, 30)
                pops.append(("!", k, x))
                cur[k] = x
            else:
                k = rng.randrange(n)
                pops.append(("?", k, 0))
                exp.append(min(cur[i] + abs(i - k) for i in range(n)))
        assert pizzeria_queries(price, pops) == exp


def brute_movies(movies: list[tuple[int, int]], a: int, b: int) -> int:
    inside = sorted((e, s) for s, e in movies if a <= s and e <= b)
    cnt, t = 0, a
    for e, s in inside:
        if s >= t:
            cnt += 1
            t = e
    return cnt


def test_movie_festival_and_missing_coin(rng: random.Random) -> None:
    for _ in range(100):
        movies = []
        for _ in range(rng.randint(1, 10)):
            s = rng.randint(1, 20)
            movies.append((s, s + rng.randint(1, 6)))
        qs = []
        for _ in range(10):
            a = rng.randint(1, 25)
            qs.append((a, a + rng.randint(0, 15)))
        assert movie_festival_queries(movies, qs) == [brute_movies(movies, a, b) for a, b in qs]
        coins = [rng.randint(1, 20) for _ in range(rng.randint(1, 10))]
        cq = [rand_range(rng, len(coins)) for _ in range(10)]
        exp = []
        for l, r in cq:
            sums = {0}
            for c in coins[l:r]:
                sums |= {s + c for s in sums}
            x = 1
            while x in sums:
                x += 1
            exp.append(x)
        assert missing_coin_sum_queries(coins, cq) == exp


def components(n: int, edges: set[tuple[int, int]]) -> int:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            x = parent[x]
        return x

    c = n
    for u, v in edges:
        a, b = find(u), find(v)
        if a != b:
            parent[a] = b
            c -= 1
    return c


def test_connectivity(rng: random.Random) -> None:
    for _ in range(80):
        n = rng.randint(1, 8)
        cur: set[tuple[int, int]] = set()
        events: list[tuple[str, int, int]] = []
        exp = []
        for _ in range(rng.randint(0, 25)):
            if cur and rng.random() < 0.4:
                u, v = rng.choice(sorted(cur))
                cur.remove((u, v))
                events.append(("-", v, u))
            else:
                u, v = rng.randrange(n), rng.randrange(n)
                key = (min(u, v), max(u, v))
                if key in cur:
                    continue
                cur.add(key)
                events.append(("+", u, v))
            exp.append(components(n, cur))
        assert dynamic_connectivity_offline(n, events) == exp
        edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 12))]
        qs = [(rng.randrange(n), rng.randrange(n)) for _ in range(10)]
        exp2 = []
        for a, b in qs:
            ans = -1
            for d in range(len(edges) + 1):
                comp = set(edges[:d])
                parent = list(range(n))

                def find(x: int, parent: list[int] = parent) -> int:
                    while parent[x] != x:
                        x = parent[x]
                    return x

                for u, v in comp:
                    parent[find(u)] = find(v)
                if find(a) == find(b):
                    ans = d
                    break
            exp2.append(ans)
        assert new_roads_queries(n, edges, qs) == exp2


def test_monotonic_structures(rng: random.Random) -> None:
    q = MonotonicQueue()
    qmax = MonotonicQueue(largest=True)
    ms = MinStack()
    tq: TwoStackQueue[int] = TwoStackQueue(gcd, 0)
    ref: list[int] = []
    st: list[int] = []
    for _ in range(2000):
        if ref and rng.random() < 0.4:
            q.pop()
            qmax.pop()
            tq.pop()
            ref.pop(0)
        else:
            x = rng.randint(1, 60)
            q.push(x)
            qmax.push(x)
            tq.push(x)
            ref.append(x)
        if ref:
            assert q.top() == min(ref) and qmax.top() == max(ref)
            g = 0
            for v in ref:
                g = gcd(g, v)
            assert tq.query() == g
        assert len(q) == len(ref) == len(tq)
        if st and rng.random() < 0.4:
            assert ms.pop() == st.pop()
        else:
            x = rng.randint(1, 60)
            ms.push(x)
            st.append(x)
        if st:
            assert ms.min() == min(st)
        assert len(ms) == len(st)


def test_sliding_windows(rng: random.Random) -> None:
    for _ in range(200):
        n = rng.randint(1, 15)
        a = [rng.randint(0, 6) for _ in range(n)]
        k = rng.randint(1, n)
        wins = [a[i : i + k] for i in range(n - k + 1)]
        assert sliding_window_sum(a, k) == [sum(w) for w in wins]
        assert sliding_window_min(a, k) == [min(w) for w in wins]
        xo, oo = [], []
        for w in wins:
            x = o = 0
            for v in w:
                x ^= v
                o |= v
            xo.append(x)
            oo.append(o)
        assert sliding_window_xor(a, k) == xo
        assert sliding_window_or(a, k) == oo
        assert sliding_window_distinct(a, k) == [len(set(w)) for w in wins]
        modes = []
        for w in wins:
            best = max(w.count(v) for v in w)
            modes.append(min(v for v in w if w.count(v) == best))
        assert sliding_window_mode(a, k) == modes
        mexes = []
        for w in wins:
            m = 0
            while m in w:
                m += 1
            mexes.append(m)
        assert sliding_window_mex(a, k) == mexes
        inv = [sum(1 for i in range(k) for j in range(i + 1, k) if w[i] > w[j]) for w in wins]
        assert sliding_window_inversions(a, k) == inv
    assert sliding_window_sum([1], 2) == []
    for _ in range(200):
        s = "".join(rng.choice("abcd") for _ in range(rng.randint(0, 12)))
        best = max(
            (
                j - i
                for i in range(len(s) + 1)
                for j in range(i, len(s) + 1)
                if len(set(s[i:j])) == j - i
            ),
            default=0,
        )
        assert longest_window_no_repeats(s) == best


def brute_isotonic(y: list[int]) -> Fraction:
    # точный минимум через PAV-независимый перебор разбиений на блоки
    n = len(y)
    best: Fraction | None = None
    for mask in range(1 << max(0, n - 1)):
        blocks, start = [], 0
        for i in range(n - 1):
            if mask >> i & 1:
                blocks.append((start, i + 1))
                start = i + 1
        blocks.append((start, n))
        means = [Fraction(sum(y[l:r]), r - l) for l, r in blocks]
        if all(means[i] <= means[i + 1] for i in range(len(means) - 1)):
            sse = sum(
                ((y[i] - m) ** 2 for (l, r), m in zip(blocks, means) for i in range(l, r)),
                Fraction(0),
            )
            best = sse if best is None or sse < best else best
    assert best is not None
    return best


def test_pav_vs_partitions(rng: random.Random) -> None:
    mod = 998244353
    for _ in range(200):
        y = [rng.randint(-5, 5) for _ in range(rng.randint(1, 8))]
        blocks = pav(y)
        means = [m for _, _, m in blocks]
        assert all(means[i] <= means[i + 1] for i in range(len(means) - 1))
        assert blocks[0][0] == 0 and blocks[-1][1] == len(y)
        exact = brute_isotonic(y)
        assert isotonic_sse_mod(y) == exact.numerator % mod * pow(exact.denominator, -1, mod) % mod
    w_blocks = pav([3, 1], [1, 3])
    assert w_blocks == [(0, 2, Fraction(6, 4))]


def test_subarray_mex_and_flip_runs(rng: random.Random) -> None:
    for _ in range(100):
        n = rng.randint(1, 15)
        a = [rng.randint(0, 6) for _ in range(n)]
        qs = [rand_range(rng, n) for _ in range(15)]
        exp = []
        for l, r in qs:
            m = 0
            while m in a[l:r]:
                m += 1
            exp.append(m)
        assert subarray_mex_offline(a, qs) == exp
        bits = [rng.randint(0, 1) for _ in range(n)]
        st = SegTreeFlipRuns(list(bits))
        for _ in range(40):
            l, r = rand_range(rng, n)
            if rng.random() < 0.5:
                st.flip(l, r)
                for i in range(l, r):
                    bits[i] ^= 1
            else:
                cnt = sum(1 for i in range(l, r) for j in range(i + 1, r + 1) if all(bits[i:j]))
                assert st.query(l, r) == cnt


def test_ds_stubs_raise() -> None:
    with pytest.raises(NotImplementedError):
        exclusions([0])
    with pytest.raises(NotImplementedError):
        generic_strings("a", 1)
