"""Primes: sieves, Miller-Rabin, Pollard rho, factorization.

Простые числа: решёта, проверка на простоту, факторизация.
"""

from __future__ import annotations

import random
from math import gcd, isqrt

from rustinpy._registry import algo


@algo(tags=["primes", "sieve"], cses=["- (prime tables)"])
def sieve(n: int) -> bytearray:
    """Sieve of Eratosthenes: is_prime flags for 0..n.   # Решето Эратосфена.

    When to use:  primality of all numbers up to ~10^7.
    Complexity:   O(n log log n), slice assignment makes it fast in CPython
    Returns:      bytearray f of length n + 1, f[x] == 1 iff x is prime.
    Python speed: n = 10^7 in about 0.5 s.
    Related:      primes_up_to, linear_sieve, segmented_sieve.
    CSES:         - (prime tables)
    Example:
        >>> [i for i, f in enumerate(sieve(20)) if f]
        [2, 3, 5, 7, 11, 13, 17, 19]
    """
    f = bytearray([1]) * (n + 1)
    f[: min(2, n + 1)] = bytearray(min(2, n + 1))  # 0 и 1 не простые
    for p in range(2, isqrt(n) + 1):
        if f[p]:
            f[p * p :: p] = bytearray(len(range(p * p, n + 1, p)))  # вычёркиваем кратные
    return f


@algo(tags=["primes", "sieve"], cses=["- (prime tables)"], requires=["sieve"])
def primes_up_to(n: int) -> list[int]:
    """All primes <= n.   # Список простых до n.

    When to use:  list of primes for trial division, inclusion-exclusion, etc.
    Complexity:   O(n log log n)
    Returns:      sorted list of primes p <= n.
    CSES:         - (prime tables)
    Example:
        >>> primes_up_to(30)
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    """
    return [i for i, f in enumerate(sieve(n)) if f]


@algo(tags=["primes", "sieve", "spf"], cses=["Counting Divisors (1713)"])
def linear_sieve(n: int) -> tuple[list[int], list[int]]:
    """Linear sieve: smallest prime factor of every x <= n.   # Линейное решето (spf).

    When to use:  many factorizations of numbers <= n (factorize_spf in O(log x)).
    Complexity:   O(n)
    Returns:      (spf, primes); spf[x] = smallest prime factor of x, spf[0] = spf[1] = 0.
    Python speed: n = 10^7 takes several seconds - prefer sieve() when spf is not needed.
    Related:      factorize_spf, phi_table, mobius_table.
    CSES:         Counting Divisors (1713).
    Example:
        >>> spf, pr = linear_sieve(12)
        >>> spf[12], spf[9], pr
        (2, 3, [2, 3, 5, 7, 11])
    """
    spf = [0] * (n + 1)
    primes: list[int] = []
    for i in range(2, n + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)
        si = spf[i]
        for p in primes:
            # каждое составное число вычёркивается ровно один раз своим spf
            if p > si or p * i > n:
                break
            spf[p * i] = p
    return spf, primes


@algo(tags=["primes", "phi", "totient"], cses=["- (phi tables)"], icpc=["2023 J"])
def phi_table(n: int) -> list[int]:
    """Euler's totient phi(x) for all x <= n.   # Функция Эйлера для всех чисел.

    When to use:  sums of phi, counting fractions / coprime pairs up to n.
    Complexity:   O(n log log n)
    Returns:      phi with phi[x] for 0 <= x <= n (phi[0] = 0).
    Related:      phi_prefix_sum (n up to 10^10), euler_phi (one number).
    CSES:         - (phi tables)
    ICPC-UZ:      2023 J (sum of phi).
    Example:
        >>> phi_table(10)
        [0, 1, 1, 2, 2, 4, 2, 6, 4, 6, 4]
    """
    phi = list(range(n + 1))
    for p in range(2, n + 1):
        if phi[p] == p:  # p простое: ещё не тронуто
            for m in range(p, n + 1, p):
                phi[m] -= phi[m] // p
    return phi


@algo(tags=["primes", "mobius"], cses=["Counting Coprime Pairs (2417)"])
def mobius_table(n: int) -> list[int]:
    """Mobius function mu(x) for all x <= n.   # Функция Мёбиуса.

    When to use:  Mobius inversion, counting coprime tuples.
    Complexity:   O(n log log n)
    Returns:      mu with mu[x] in {-1, 0, 1}; mu[0] = 0.
    Related:      coprime_pairs_count, phi_table.
    CSES:         Counting Coprime Pairs (2417).
    Example:
        >>> mobius_table(10)
        [0, 1, -1, -1, 0, -1, 1, -1, 0, 0, 1]
    """
    mu = [1] * (n + 1)
    if n >= 0:
        mu[0] = 0
    is_comp = bytearray(n + 1)
    for p in range(2, n + 1):
        if not is_comp[p]:
            for q in range(2 * p, n + 1, p):
                is_comp[q] = 1
            for q in range(p, n + 1, p):
                mu[q] = -mu[q]  # ещё один простой делитель
            for q in range(p * p, n + 1, p * p):
                mu[q] = 0  # делится на квадрат
    return mu


@algo(tags=["primes", "sieve", "segmented"], cses=["- (primes in [lo, hi], hi ~ 10^12)"])
def segmented_sieve(lo: int, hi: int) -> list[int]:
    """Primes in [lo, hi] for big hi and moderate hi - lo.   # Сегментированное решето.

    When to use:  hi up to ~10^12, hi - lo up to ~10^7.
    Complexity:   O(sqrt(hi) + (hi - lo) log log hi)
    Returns:      sorted primes p with lo <= p <= hi.
    Related:      sieve, is_prime.
    CSES:         - (primes in [lo, hi], hi ~ 10^12)
    Example:
        >>> segmented_sieve(100, 130)
        [101, 103, 107, 109, 113, 127]
    """
    lo = max(lo, 2)
    if hi < lo:
        return []
    r = isqrt(hi)
    base = bytearray([1]) * (r + 1)
    small: list[int] = []
    for p in range(2, r + 1):
        if base[p]:
            small.append(p)
            base[p * p :: p] = bytearray(len(range(p * p, r + 1, p)))
    seg = bytearray([1]) * (hi - lo + 1)
    for p in small:
        start = max(p * p, (lo + p - 1) // p * p)  # первое кратное p в отрезке
        if start <= hi:
            seg[start - lo :: p] = bytearray(len(range(start, hi + 1, p)))
    return [lo + i for i, f in enumerate(seg) if f]


@algo(tags=["primes", "miller-rabin"], cses=["- (primality up to 2^64)"], icpc=["2024 E"])
def is_prime(n: int) -> bool:
    """Deterministic Miller-Rabin for n < 3.3 * 10^24.   # Проверка простоты Миллера-Рабина.

    When to use:  primality of a single big number (up to 10^18 and more).
    Complexity:   O(12 * log^3 n) bit operations
    Returns:      True iff n is prime (deterministic for n < 3.3e24, bases 2..37).
    Pitfalls:     for n <= 10^7 and many queries a sieve is faster.
    Related:      pollard_rho, factorize, sieve.
    CSES:         - (primality up to 2^64)
    ICPC-UZ:      2024 E (numbers up to 10^18).
    Example:
        >>> [x for x in range(30) if is_prime(x)]
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        >>> is_prime(10**9 + 7), is_prime(2**61 - 1), is_prime(561)
        (True, True, False)
    """
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:  # n - 1 = d * 2^s
        d //= 2
        s += 1
    for a in small:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False  # a - свидетель составности
    return True


@algo(tags=["primes", "pollard-rho", "factorization"], icpc=["2024 E"], requires=["is_prime"])
def pollard_rho(n: int) -> int:
    """A non-trivial divisor of composite n (Pollard rho, Brent).   # Ро-алгоритм Полларда.

    When to use:  factor numbers up to 10^18 and beyond where trial division is too slow.
    Complexity:   expected O(n^(1/4)) multiplications
    Input:        n composite (n > 1, not prime).
    Returns:      d with 1 < d < n and n % d == 0.
    Pitfalls:     randomized; do not pass a prime (infinite search) - check is_prime first.
    Related:      factorize, is_prime.
    ICPC-UZ:      2024 E.
    Example:
        >>> d = pollard_rho(1000000016000000063)
        >>> d in (1000000007, 1000000009)
        True
    """
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    while True:
        c = random.randrange(1, n)
        y = random.randrange(0, n)
        m, g, r, q = 128, 1, 1, 1
        x = ys = y
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n  # копим произведение, один gcd на пачку
                g = gcd(q, n)
                k += m
            r *= 2
        if g == n:  # пачка «перескочила» - откатываемся по одному шагу
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = gcd(abs(x - ys), n)
        if g != n:
            return g


@algo(
    tags=["primes", "factorization"],
    cses=["- (factorization up to 10^18)"],
    icpc=["2024 E"],
    requires=["is_prime", "pollard_rho"],
)
def factorize(n: int) -> dict[int, int]:
    """Prime factorization of n >= 1 (trial division + Pollard rho).   # Разложение на простые.

    When to use:  one or a few numbers up to 10^18.
    Complexity:   O(B + n^(1/4)) expected, B = 1000 trial divisions
    Returns:      {prime: exponent}, sorted by prime; {} for n = 1.
    Python speed: ~1 ms per 10^18 number -> 2 * 10^5 queries are too slow in CPython;
                  look for structure in the problem (ICPC-UZ 2024 E).
    Related:      pollard_rho, is_prime, factorize_spf, divisors.
    CSES:         - (factorization up to 10^18)
    ICPC-UZ:      2024 E.
    Example:
        >>> factorize(360)
        {2: 3, 3: 2, 5: 1}
        >>> factorize(1000000016000000063)
        {1000000007: 1, 1000000009: 1}
    """
    res: dict[int, int] = {}
    for p in range(2, 1000):  # сначала мелкие делители
        if p * p > n:
            break
        while n % p == 0:
            res[p] = res.get(p, 0) + 1
            n //= p
    stack = [n] if n > 1 else []
    while stack:  # итеративно: раскалываем, пока не останутся простые
        x = stack.pop()
        if is_prime(x):
            res[x] = res.get(x, 0) + 1
            continue
        d = pollard_rho(x)
        stack += [d, x // d]
    return dict(sorted(res.items()))


@algo(tags=["primes", "factorization", "spf"], cses=["Counting Divisors (1713)"])
def factorize_spf(x: int, spf: list[int]) -> dict[int, int]:
    """Factorize x <= n with a precomputed spf table.   # Разложение по таблице spf.

    When to use:  up to 10^6 factorizations of numbers <= 10^7.
    Complexity:   O(log x)
    Input:        spf from linear_sieve(n), 1 <= x <= n.
    Returns:      {prime: exponent}.
    Related:      linear_sieve.
    CSES:         Counting Divisors (1713).
    Example:
        >>> spf = [0, 0, 2, 3, 2, 5, 2, 7, 2, 3, 2, 11, 2]
        >>> factorize_spf(12, spf)
        {2: 2, 3: 1}
    """
    res: dict[int, int] = {}
    while x > 1:
        p = spf[x]
        x //= p
        res[p] = res.get(p, 0) + 1
    return res


@algo(tags=["primes"], cses=["- (next prime)"], requires=["is_prime"])
def next_prime(n: int) -> int:
    """Smallest prime strictly greater than n.   # Следующее простое.

    When to use:  hash moduli, table sizes, "next prime" queries.
    Complexity:   O(log^2 n) expected primality tests (prime gaps are small)
    Returns:      p > n, p prime.
    Related:      is_prime.
    CSES:         - (next prime)
    Example:
        >>> next_prime(1), next_prime(13), next_prime(10**9)
        (2, 17, 1000000007)
    """
    x = max(n + 1, 2)
    while not is_prime(x):
        x += 1
    return x
