"""mathx: brute-force comparisons on random small inputs (AC-05, AC-06)."""

from __future__ import annotations

import itertools
import random
from fractions import Fraction
from math import comb, factorial, gcd, isqrt, perm

import pytest

from rustinpy.mathx import (
    Comb,
    bell_numbers,
    berlekamp_massey,
    bracket_sequences_prefix,
    candy_lottery,
    catalan,
    common_divisors_max_gcd,
    convolution,
    convolution_int,
    coprime_pairs_count,
    coprime_pairs_up_to,
    count_fib_representations,
    crt,
    deep_numbers_count,
    derangements,
    det_mod,
    dice_probability,
    divisor_analysis,
    divisor_count_table,
    divisors,
    euler_phi,
    exp_tower,
    ext_gcd,
    factorize,
    factorize_spf,
    fft_convolution_float,
    fib,
    floor_blocks,
    gauss_float,
    gauss_mod,
    gcd_sum_pairs,
    gcd_sum_with_n,
    grid_colorings_count,
    infinite_game_count,
    inversion_probability,
    is_prime,
    linear_recurrence_kth,
    linear_sieve,
    mat_mul,
    mat_pow,
    min_digit_changes_count,
    min_trials_for_probability,
    minplus_mat_pow,
    mobius_table,
    modinv,
    modpow,
    moving_robots,
    nCr_composite,
    nCr_lucas,
    nCr_pascal,
    necklaces_count,
    next_prime,
    ntt,
    phi_prefix_sum,
    phi_table,
    pollard_rho,
    prime_multiples_count,
    primes_up_to,
    segmented_sieve,
    sieve,
    stars_and_bars,
    stirling1_table,
    stirling2_table,
    sum_of_divisors_sum,
    sum_of_four_squares,
    throwing_dice,
    zeckendorf,
)

P = 10**9 + 7
Q = 998244353


def naive_is_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def naive_phi(n: int) -> int:
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)


# ------------------------------------------------------------------ modular


def test_modpow_ext_gcd_modinv_crt(rng: random.Random) -> None:
    for _ in range(500):
        a, e, m = rng.randint(0, 10**6), rng.randint(0, 10**4), rng.randint(1, 10**6)
        assert modpow(a, e, m) == pow(a, e, m)
        b = rng.randint(0, 10**6)
        g, x, y = ext_gcd(a, b)
        assert g == gcd(a, b) and a * x + b * y == g
        if gcd(a, m) == 1:
            assert a * modinv(a, m) % m == 1 % m
        elif m > 1:
            with pytest.raises(ValueError):
                modinv(a, m)
    for _ in range(300):
        mods = [rng.randint(1, 30) for _ in range(rng.randint(1, 4))]
        rems = [rng.randrange(m) for m in mods]
        res = crt(rems, mods)
        lcm = 1
        for m in mods:
            lcm = lcm * m // gcd(lcm, m)
        sols = [x for x in range(lcm) if all(x % m == r for r, m in zip(rems, mods))]
        if sols:
            assert res == (sols[0], lcm)
        else:
            assert res is None


def test_exp_tower_vs_bigint() -> None:
    for a in range(0, 6):
        for b in range(0, 5):
            for c in range(0, 4):
                assert exp_tower(a, b, c, 13) == pow(a, b**c, 13)


# ------------------------------------------------------------------ comb


def test_comb_class_and_pascal_and_composite(rng: random.Random) -> None:
    c = Comb(60, P)
    for n in range(61):
        for r in range(-1, n + 2):
            exp = comb(n, r) % P if 0 <= r <= n else 0
            assert c.nCr(n, r) == exp
            assert c.nPr(n, r) == (perm(n, r) % P if 0 <= r <= n else 0)
    assert c.multinomial([3, 2, 1]) == factorial(6) // (6 * 2) % P
    with pytest.raises(ValueError):
        Comb(10, 2112025)
    tri = nCr_pascal(40, 2112025)
    for n in range(41):
        assert tri[n] == [comb(n, r) % 2112025 for r in range(n + 1)]
    for _ in range(100):
        n = rng.randint(0, 300)
        r = rng.randint(-2, n + 2)
        m = rng.choice([2112025, 12, 2**10, 3**5 * 7, 1000, 97])
        assert nCr_composite(n, r, m) == (comb(n, r) % m if 0 <= r <= n else 0)
    for _ in range(200):
        p = rng.choice([2, 3, 5, 7, 13, 101])
        n = rng.randint(0, 3000)
        r = rng.randint(0, n)
        assert nCr_lucas(n, r, p) == comb(n, r) % p


def brute_brackets(n: int, prefix: str) -> int:
    cnt = 0
    for s in itertools.product("()", repeat=n - len(prefix)):
        t = prefix + "".join(s)
        b = 0
        ok = True
        for ch in t:
            b += 1 if ch == "(" else -1
            if b < 0:
                ok = False
                break
        cnt += ok and b == 0
    return cnt


def test_catalan_and_bracket_prefix(rng: random.Random) -> None:
    for n in range(12):
        assert catalan(n) == comb(2 * n, n) // (n + 1) % P
    for _ in range(150):
        n = rng.randint(0, 12)
        k = rng.randint(0, n)
        prefix = "".join(rng.choice("()") for _ in range(k))
        assert bracket_sequences_prefix(n, prefix) == brute_brackets(n, prefix)


def test_stirling_bell_derangements_stars() -> None:
    def surj(n: int, k: int) -> int:
        return sum(1 for f in itertools.product(range(k), repeat=n) if len(set(f)) == k)

    def cycles(p: tuple[int, ...]) -> int:
        seen, c = set(), 0
        for i in range(len(p)):
            if i not in seen:
                c += 1
                j = i
                while j not in seen:
                    seen.add(j)
                    j = p[j]
        return c

    S = stirling2_table(6, P)
    s1 = stirling1_table(6, P)
    for n in range(7):
        for k in range(n + 1):
            assert S[n][k] * factorial(k) == surj(n, k)
            assert s1[n][k] == sum(1 for p in itertools.permutations(range(n)) if cycles(p) == k)
    assert bell_numbers(6, P) == [sum(S[n]) for n in range(7)]
    for n in range(8):
        der = sum(1 for p in itertools.permutations(range(n)) if all(p[i] != i for i in range(n)))
        assert derangements(n) == der
    for n in range(1, 5):
        for m in range(6):
            cnt = sum(1 for xs in itertools.product(range(m + 1), repeat=n) if sum(xs) == m)
            assert stars_and_bars(n, m) == cnt
    assert stars_and_bars(0, 0) == 1 and stars_and_bars(0, 3) == 0


def test_burnside_counts_vs_orbits() -> None:
    for n in range(1, 7):
        for m in range(1, 4):
            orbits = {
                min(t[i:] + t[:i] for i in range(n)) for t in itertools.product(range(m), repeat=n)
            }
            assert necklaces_count(n, m) == len(orbits)
    for n in range(1, 4):
        seen = set()
        for bits in itertools.product((0, 1), repeat=n * n):
            g = [bits[i * n : (i + 1) * n] for i in range(n)]
            rots = []
            cur = g
            for _ in range(4):
                cur = [tuple(cur[n - 1 - j][i] for j in range(n)) for i in range(n)]
                rots.append(tuple(cur))
            seen.add(min(rots))
        assert grid_colorings_count(n) == len(seen)


def test_inclusion_exclusion(rng: random.Random) -> None:
    for _ in range(100):
        n = rng.randint(1, 500)
        primes = rng.sample([2, 3, 5, 7, 11, 13, 17], rng.randint(1, 5))
        exp = sum(1 for x in range(1, n + 1) if any(x % p == 0 for p in primes))
        assert prime_multiples_count(n, primes) == exp
    for _ in range(50):
        a = [rng.randint(1, 60) for _ in range(rng.randint(0, 25))]
        exp = sum(1 for i in range(len(a)) for j in range(i) if gcd(a[i], a[j]) == 1)
        assert coprime_pairs_count(a) == exp


# ------------------------------------------------------------------ primes


def test_sieves_vs_naive() -> None:
    N = 2000
    flags = sieve(N)
    assert [i for i in range(N + 1) if flags[i]] == [i for i in range(N + 1) if naive_is_prime(i)]
    assert primes_up_to(N) == [i for i in range(N + 1) if naive_is_prime(i)]
    assert sieve(0) == bytearray(b"\x00") and sieve(1) == bytearray(2)
    spf, pr = linear_sieve(N)
    assert pr == primes_up_to(N)
    for x in range(2, N + 1):
        assert spf[x] == min(p for p in pr if x % p == 0)
        f = factorize_spf(x, spf)
        prod = 1
        for p, e in f.items():
            prod *= p**e
        assert prod == x
    phi = phi_table(300)
    assert phi[1:] == [naive_phi(k) for k in range(1, 301)]
    mu = mobius_table(300)
    for x in range(1, 301):
        f = factorize(x)
        exp = 0 if any(e > 1 for e in f.values()) else (-1) ** len(f)
        assert mu[x] == exp
    assert segmented_sieve(1000, 1300) == [p for p in range(1000, 1301) if naive_is_prime(p)]
    assert segmented_sieve(0, 30) == primes_up_to(30)
    assert segmented_sieve(10, 5) == []


def test_miller_rabin_pollard_factorize(rng: random.Random) -> None:
    for x in range(-5, 5000):
        assert is_prime(x) == naive_is_prime(x)
    big_primes = [10**9 + 7, 998244353, 2**61 - 1, 1000000000000000003, 4611686018427387847]
    for p in big_primes:
        assert is_prime(p)
    carmichael = [561, 1105, 1729, 2465, 2821, 6601, 8911, 3215031751, 3825123056546413051]
    for c in carmichael:
        assert not is_prime(c)
    for _ in range(200):
        n = rng.randint(1, 10**6)
        f = factorize(n)
        prod = 1
        for p, e in f.items():
            assert naive_is_prime(p)
            prod *= p**e
        assert prod == n
    for a, b in [(10**9 + 7, 10**9 + 9), (999999937, 999999929), (2**31 - 1, 2**31 - 1)]:
        n = a * b
        d = pollard_rho(n)
        assert d in (a, b)
        assert factorize(n) == ({a: 2} if a == b else dict(sorted({a: 1, b: 1}.items())))
    assert factorize(1) == {}
    assert next_prime(0) == 2 and next_prime(2) == 3 and next_prime(89) == 97


# ------------------------------------------------------------------ numtheory


def test_divisor_functions(rng: random.Random) -> None:
    for n in range(1, 500):
        divs = [d for d in range(1, n + 1) if n % d == 0]
        assert divisors(n) == divs
        assert euler_phi(n) == naive_phi(n)
        assert gcd_sum_with_n(n) == sum(gcd(i, n) for i in range(1, n + 1))
    tbl = divisor_count_table(300)
    assert tbl[1:] == [len(divisors(n)) for n in range(1, 301)]
    for n in range(0, 200):
        exp = sum(sum(divisors(i)) for i in range(1, n + 1))
        assert sum_of_divisors_sum(n) == exp % P
    for _ in range(100):
        pe = [(p, rng.randint(1, 3)) for p in rng.sample([2, 3, 5, 7, 11], rng.randint(1, 3))]
        N = 1
        for p, e in pe:
            N *= p**e
        ds = divisors(N)
        prod = 1
        for d in ds:
            prod = prod * d % P
        assert divisor_analysis(pe) == (len(ds) % P, sum(ds) % P, prod)
    for _ in range(100):
        a = [rng.randint(1, 100) for _ in range(rng.randint(2, 15))]
        exp = max(gcd(a[i], a[j]) for i in range(len(a)) for j in range(i))
        assert common_divisors_max_gcd(a) == exp


def test_floor_blocks_cover() -> None:
    for n in range(0, 300):
        seen = []
        for l, r, q in floor_blocks(n):
            for i in range(l, r + 1):
                assert n // i == q
                seen.append(i)
        assert seen == list(range(1, n + 1))


def test_phi_sums_vs_naive() -> None:
    phi = phi_table(3000)
    pref = [0] * 3001
    for i in range(1, 3001):
        pref[i] = pref[i - 1] + phi[i]
    for n in [*range(0, 200), 999, 1000, 2047, 3000]:
        assert phi_prefix_sum(n) == pref[n]
    for n in range(1, 40):
        assert coprime_pairs_up_to(n) == sum(
            1 for i in range(1, n + 1) for j in range(1, n + 1) if gcd(i, j) == 1
        )
        assert gcd_sum_pairs(n) == sum(gcd(i, j) for i in range(1, n + 1) for j in range(1, n + 1))
    assert gcd_sum_pairs(10, 7) == gcd_sum_pairs(10) % 7
    assert coprime_pairs_up_to(0) == 0
    # большой n: сверка с решетом
    big = 10**6
    phi_big = phi_table(big)
    assert phi_prefix_sum(big) == sum(phi_big)


def test_sum_of_four_squares(rng: random.Random) -> None:
    for n in list(range(0, 2000)) + [rng.randint(1, 10**7) for _ in range(200)]:
        a, b, c, d = sum_of_four_squares(n)
        assert a * a + b * b + c * c + d * d == n


# ------------------------------------------------------------------ matrix


def test_matrix_and_recurrences(rng: random.Random) -> None:
    for _ in range(50):
        n = rng.randint(1, 5)
        m = [[rng.randint(0, 9) for _ in range(n)] for _ in range(n)]
        e = rng.randint(0, 6)
        exp = [[int(i == j) for j in range(n)] for i in range(n)]
        for _ in range(e):
            exp = mat_mul(exp, m, P)
        assert mat_pow(m, e, P) == exp
    X = 1 << 60
    for _ in range(50):
        n = rng.randint(1, 4)
        w = [[rng.choice([X, rng.randint(0, 9)]) for _ in range(n)] for _ in range(n)]
        e = rng.randint(0, 4)
        for i in range(n):
            for j in range(n):
                best = X
                for path in itertools.product(range(n), repeat=max(e - 1, 0)):
                    seq = [i, *path, j] if e > 0 else [i]
                    if e == 0 and i != j:
                        continue
                    cost = sum(w[a][b] for a, b in zip(seq, seq[1:]))
                    if all(w[a][b] < X for a, b in zip(seq, seq[1:])):
                        best = min(best, cost)
                assert minplus_mat_pow(w, e)[i][j] == best
    for _ in range(100):
        d = rng.randint(1, 4)
        coef = [rng.randint(0, 5) for _ in range(d)]
        init = [rng.randint(0, 5) for _ in range(d)]
        seq = init[:]
        for k in range(d, 60):
            seq.append(sum(coef[i] * seq[k - 1 - i] for i in range(d)) % P)
        for k in range(60):
            assert linear_recurrence_kth(coef, init, k, P) == seq[k] % P
        found = berlekamp_massey(seq[: 2 * d + 8], P)
        for k in range(len(found), 60):
            assert seq[k] == sum(found[i] * seq[k - 1 - i] for i in range(len(found))) % P
    f = [0, 1]
    for _ in range(200):
        f.append(f[-1] + f[-2])
    assert [fib(i, P) for i in range(200)] == [x % P for x in f[:200]]
    dice = [1]
    for n in range(1, 60):
        dice.append(sum(dice[max(0, n - 6) : n]))
    assert [throwing_dice(n) for n in range(60)] == [x % P for x in dice]


def test_zeckendorf_and_fib_representations() -> None:
    fibs = [1, 2]
    while fibs[-1] < 2000:
        fibs.append(fibs[-1] + fibs[-2])
    counts = [0] * 2001
    for mask in range(1 << len(fibs)):
        s = sum(fibs[i] for i in range(len(fibs)) if mask >> i & 1)
        if s <= 2000:
            counts[s] += 1
    for n in range(0, 2001):
        z = zeckendorf(n)
        assert sum(z) == n
        idx = [fibs.index(x) for x in z]
        assert all(a - b >= 2 for a, b in zip(idx, idx[1:]))
        assert count_fib_representations(n) == counts[n]


# ------------------------------------------------------------------ poly


def naive_conv(a: list[int], b: list[int]) -> list[int]:
    if not a or not b:
        return []
    res = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            res[i + j] += x * y
    return res


def test_convolutions_vs_naive(rng: random.Random) -> None:
    for _ in range(60):
        a = [rng.randint(0, 10**9) for _ in range(rng.randint(0, 80))]
        b = [rng.randint(0, 10**9) for _ in range(rng.randint(0, 80))]
        exp = naive_conv(a, b)
        assert convolution(a, b) == [x % Q for x in exp]
        assert convolution_int(a, b) == exp
        fa = [rng.random() for _ in range(len(a))]
        fb = [rng.random() for _ in range(len(b))]
        got = fft_convolution_float(fa, fb)
        want = (
            [
                sum(fa[i] * fb[k - i] for i in range(len(fa)) if 0 <= k - i < len(fb))
                for k in range(len(fa) + len(fb) - 1)
            ]
            if fa and fb
            else []
        )
        assert len(got) == len(want)
        assert all(abs(x - y) < 1e-6 for x, y in zip(got, want))
    a = [rng.randrange(Q) for _ in range(64)]
    t = a[:]
    ntt(t, False)
    ntt(t, True)
    assert t == a
    assert convolution_int([0, 0], [0]) == [0, 0]


# ------------------------------------------------------------------ linalg


def test_gauss_mod_random_systems(rng: random.Random) -> None:
    p = 7
    for _ in range(300):
        n, m = rng.randint(1, 4), rng.randint(1, 4)
        a = [[rng.randrange(p) for _ in range(m)] for _ in range(n)]
        b = [rng.randrange(p) for _ in range(n)]
        res = gauss_mod(a, b, p)
        has = any(
            all(sum(a[i][j] * x[j] for j in range(m)) % p == b[i] for i in range(n))
            for x in itertools.product(range(p), repeat=m)
        )
        if res is None:
            assert not has
        else:
            assert all(sum(a[i][j] * res[j] for j in range(m)) % p == b[i] for i in range(n))


def test_gauss_float_and_det(rng: random.Random) -> None:
    for _ in range(100):
        n = rng.randint(1, 5)
        x = [rng.uniform(-5, 5) for _ in range(n)]
        a = [[rng.uniform(-5, 5) for _ in range(n)] for _ in range(n)]
        b = [sum(a[i][j] * x[j] for j in range(n)) for i in range(n)]
        got = gauss_float(a, b)
        assert got is not None
        assert all(abs(sum(a[i][j] * got[j] for j in range(n)) - b[i]) < 1e-6 for i in range(n))
    assert gauss_float([[1.0, 1.0], [1.0, 1.0]], [1.0, 2.0]) is None

    def det_exact(m: list[list[int]]) -> int:
        n = len(m)
        tot = 0
        for p in itertools.permutations(range(n)):
            inv = sum(1 for i in range(n) for j in range(i) if p[j] > p[i])
            prod = 1
            for i in range(n):
                prod *= m[i][p[i]]
            tot += (-1) ** inv * prod
        return tot

    for _ in range(100):
        n = rng.randint(1, 5)
        m = [[rng.randint(-5, 5) for _ in range(n)] for _ in range(n)]
        assert det_mod(m, P) == det_exact(m) % P


# ------------------------------------------------------------------ probability


def test_probability_functions_vs_exact() -> None:
    for n in range(1, 5):
        for a in range(n, 6 * n + 1, 3):
            for b in range(a, 6 * n + 1, 4):
                exact = Fraction(
                    sum(1 for t in itertools.product(range(1, 7), repeat=n) if a <= sum(t) <= b),
                    6**n,
                )
                assert abs(dice_probability(n, a, b) - float(exact)) < 1e-12
    for n in range(1, 4):
        for k in range(1, 5):
            exact = Fraction(
                sum(max(t) for t in itertools.product(range(1, k + 1), repeat=n)), k**n
            )
            assert abs(candy_lottery(n, k) - float(exact)) < 1e-12
    for r in ([1], [2, 3], [3, 1, 2], [4, 4, 1, 2]):
        tot = Fraction(0)
        cnt = 0
        for xs in itertools.product(*[range(1, v + 1) for v in r]):
            cnt += 1
            tot += sum(1 for i in range(len(xs)) for j in range(i + 1, len(xs)) if xs[i] > xs[j])
        assert abs(inversion_probability(list(r)) - float(tot / cnt)) < 1e-12
    assert abs(moving_robots(0) - 0.0) < 1e-12
    assert 0 < moving_robots(1) < 64


def test_min_trials_for_probability_vs_scan() -> None:
    for p10 in range(0, 100, 7):
        for q10 in range(1, 100, 9):
            p, q = p10 / 100, q10 / 100
            k = 0
            while 1 - (1 - q) ** k < p - 1e-15:
                k += 1
            assert min_trials_for_probability(p, q) == k
    with pytest.raises(ValueError):
        min_trials_for_probability(0.5, 0.0)
    assert min_trials_for_probability(0.3, 1.0) == 1


def test_icpc_stubs_raise() -> None:
    for f, args in (
        (min_digit_changes_count, ([1, 1],)),
        (deep_numbers_count, (10,)),
        (infinite_game_count, (3,)),
    ):
        with pytest.raises(NotImplementedError):
            f(*args)
