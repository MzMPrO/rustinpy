"""bits: brute-force comparisons on small random inputs (AC-05, AC-06)."""

from __future__ import annotations

import random

import pytest

from rustinpy.bits import (
    XorBasis,
    XorTrie,
    all_subarray_xors,
    and_convolution,
    and_subset_count,
    counting_bits_total,
    fwht_and,
    fwht_or,
    fwht_xor,
    k_subset_xors,
    kenobi_skywalker,
    max_xor_subarray,
    max_xor_subset,
    min_hamming_distance,
    number_of_subset_xors,
    or_convolution,
    popcount,
    sos_bit_problem,
    sos_subset_sum,
    sos_superset_sum,
    xor_convolution,
    xor_pyramid_peak,
)


def subset_xors(a: list[int]) -> list[int]:
    res = []
    for m in range(1 << len(a)):
        x = 0
        for i, v in enumerate(a):
            if m >> i & 1:
                x ^= v
        res.append(x)
    return sorted(res)


def test_popcount_and_counting_bits() -> None:
    total = 0
    for n in range(0, 3000):
        assert popcount(n) == bin(n).count("1")
        total += popcount(n)
        assert counting_bits_total(n) == total
    assert counting_bits_total(10**15) > 0


def test_xor_trie_and_subarray(rng: random.Random) -> None:
    for _ in range(100):
        a = [rng.randint(0, 63) for _ in range(rng.randint(1, 10))]
        t = XorTrie(6)
        for v in a:
            t.insert(v)
        x = rng.randint(0, 63)
        assert t.max_xor(x) == max(v ^ x for v in a)
        assert t.min_xor(x) == min(v ^ x for v in a)
        best = 0
        for i in range(len(a)):
            acc = 0
            for j in range(i, len(a)):
                acc ^= a[j]
                best = max(best, acc)
        assert max_xor_subarray(a) == best
        subs = set()
        for i in range(len(a)):
            acc = 0
            for j in range(i, len(a)):
                acc ^= a[j]
                subs.add(acc)
        assert all_subarray_xors(a) == sorted(subs)


def test_xor_basis_family(rng: random.Random) -> None:
    for _ in range(150):
        a = [rng.randint(0, 31) for _ in range(rng.randint(0, 8))]
        allx = subset_xors(a)
        distinct = sorted(set(allx))
        b = XorBasis(5)
        for v in a:
            b.insert(v)
        assert b.size() == len(distinct) == number_of_subset_xors(a)
        assert b.max_xor() == max(distinct) == max_xor_subset(a)
        assert [b.kth_smallest(k) for k in range(len(distinct))] == distinct
        for x in range(32):
            assert b.can_make(x) == (x in distinct)
        k = rng.randint(1, len(allx))
        assert k_subset_xors(a, k) == allx[:k]
    with pytest.raises(IndexError):
        XorBasis(3).kth_smallest(1)


def test_pyramid_sos_and_hamming(rng: random.Random) -> None:
    for _ in range(100):
        a = [rng.randint(0, 50) for _ in range(rng.randint(1, 10))]
        row = list(a)
        while len(row) > 1:
            row = [x ^ y for x, y in zip(row, row[1:])]
        assert xor_pyramid_peak(a) == row[0]
        B = 4
        f = [rng.randint(0, 5) for _ in range(1 << B)]
        assert sos_subset_sum(f, B) == [
            sum(f[s] for s in range(1 << B) if s & m == s) for m in range(1 << B)
        ]
        assert sos_superset_sum(f, B) == [
            sum(f[s] for s in range(1 << B) if s & m == m) for m in range(1 << B)
        ]
        vals = [rng.randint(0, 15) for _ in range(rng.randint(1, 8))]
        exp = [
            (
                sum(1 for y in vals if x | y == x),
                sum(1 for y in vals if x & y == x),
                sum(1 for y in vals if x & y),
            )
            for x in vals
        ]
        assert sos_bit_problem(vals) == exp
        Bv = max(1, max(vals).bit_length())
        cnt = [0] * (1 << Bv)
        for m in range(1, 1 << len(vals)):
            acc = -1
            for i, v in enumerate(vals):
                if m >> i & 1:
                    acc &= v
            cnt[acc] += 1
        assert and_subset_count(vals) == cnt
        words = [rng.randint(0, 31) for _ in range(rng.randint(2, 8))]
        best = min(popcount(words[i] ^ words[j]) for i in range(len(words)) for j in range(i))
        assert min_hamming_distance(words) == best


def test_transforms_and_convolutions(rng: random.Random) -> None:
    for _ in range(100):
        n = 1 << rng.randint(0, 4)
        a = [rng.randint(-5, 9) for _ in range(n)]
        b = [rng.randint(-5, 9) for _ in range(n)]
        for op, conv in (
            (lambda i, j: i ^ j, xor_convolution),
            (lambda i, j: i & j, and_convolution),
            (lambda i, j: i | j, or_convolution),
        ):
            exp = [0] * n
            for i in range(n):
                for j in range(n):
                    exp[op(i, j)] += a[i] * b[j]
            assert conv(a, b) == exp
        m = 998244353
        exp = [0] * n
        for i in range(n):
            for j in range(n):
                exp[i ^ j] += a[i] * b[j]
        assert xor_convolution(a, b, m) == [x % m for x in exp]
        for tr in (fwht_and, fwht_or):
            c = list(a)
            tr(c, False)
            tr(c, True)
            assert c == a
        c = list(a)
        fwht_xor(c, False)
        fwht_xor(c, True)
        assert c == a


def test_kenobi_skywalker(rng: random.Random) -> None:
    for _ in range(150):
        a = [rng.randint(0, 7) for _ in range(rng.randint(0, 8))]
        can = set()
        for mask in range(1 << len(a)):
            x = 0
            for i in range(len(a)):
                if mask >> i & 1:
                    x ^= a[i]
            can.add((bin(mask).count("1"), x))
        qs = [(c, x) for c in range(-1, len(a) + 2) for x in range(9)]
        assert kenobi_skywalker(a, qs) == [q in can for q in qs], a
