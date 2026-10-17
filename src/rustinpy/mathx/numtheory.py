"""Number theory: divisors, floor(n / i) blocks, phi sums, gcd sums, four squares.

Теория чисел.
"""

from __future__ import annotations

from collections.abc import Iterator
from math import isqrt

from rustinpy._registry import algo

MOD7 = 10**9 + 7


@algo(tags=["divisors"], cses=["- (divisors of one number)"])
def divisors(n: int) -> list[int]:
    """All divisors of n by trial division up to sqrt(n).   # Делители числа.

    When to use:  one number up to ~10^12.
    Complexity:   O(sqrt n)
    Returns:      sorted list of divisors of n >= 1.
    Pitfalls:     for n ~ 10^18 factorize first and generate divisors from the factorization.
    Related:      factorize, divisor_count_table.
    CSES:         - (divisors of one number)
    Example:
        >>> divisors(36)
        [1, 2, 3, 4, 6, 9, 12, 18, 36]
    """
    small, big = [], []
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            small.append(d)
            if d != n // d:
                big.append(n // d)  # парный делитель
    return small + big[::-1]


@algo(tags=["divisors", "sieve"], cses=["Counting Divisors (1713)"])
def divisor_count_table(n: int) -> list[int]:
    """Number of divisors d(x) for all x <= n.   # Количество делителей для всех чисел.

    When to use:  many "how many divisors does x have" queries, x <= 10^6.
    Complexity:   O(n log n)
    Returns:      d with d[x] = number of divisors of x (d[0] = 0).
    Python speed: n = 10^6 about 1 s.
    Related:      linear_sieve + factorize_spf.
    CSES:         Counting Divisors (1713).
    Example:
        >>> divisor_count_table(12)[1:]
        [1, 2, 2, 3, 2, 4, 2, 4, 3, 4, 2, 6]
    """
    d = [0] * (n + 1)
    for i in range(1, n + 1):
        for j in range(i, n + 1, i):  # i делит все свои кратные
            d[j] += 1
    return d


@algo(tags=["divisors", "floor-blocks"], cses=["Sum of Divisors (1082)"], requires=["MOD7"])
def sum_of_divisors_sum(n: int, mod: int = MOD7) -> int:
    """sum_{i=1}^{n} sigma(i) = sum_d d * floor(n / d).   # Сумма сумм делителей.

    When to use:  n up to 10^12 (CSES Sum of Divisors).
    Complexity:   O(sqrt n)
    Returns:      the sum mod mod.
    Idea:         d contributes d to every multiple -> d * floor(n/d); group equal floor(n/d).
    Related:      floor_blocks.
    CSES:         Sum of Divisors (1082).
    Example:
        >>> sum_of_divisors_sum(5)
        21
    """
    total = 0
    l = 1
    while l <= n:
        q = n // l
        r = n // q  # все d в [l, r] имеют одно значение n // d
        total += q * ((l + r) * (r - l + 1) // 2)
        l = r + 1
    return total % mod


@algo(tags=["divisors"], cses=["Divisor Analysis (2182)"], requires=["MOD7"])
def divisor_analysis(pe: list[tuple[int, int]], mod: int = MOD7) -> tuple[int, int, int]:
    """Count, sum and product of divisors from the factorization.   # Анализ делителей.

    When to use:  N given as prod p_i^e_i (huge N).
    Complexity:   O(k log)
    Input:        pe = [(p_1, e_1), ...], distinct primes, mod prime and > every p.
    Returns:      (d(N) mod, sigma(N) mod, product of divisors mod).
    Idea:         product = N^(d(N)/2); keep d(N) modulo mod - 1 for the exponent (Fermat).
    CSES:         Divisor Analysis (2182).
    Example:
        >>> divisor_analysis([(2, 2), (3, 1)])
        (6, 28, 1728)
    """
    cnt = 1  # d(N) по модулю mod
    cnt_e = 1  # d(N) по модулю mod - 1 (для показателя)
    s = 1
    prod = 1
    for p, e in pe:
        cnt = cnt * (e + 1) % mod
        if p % mod == 1:
            s = s * (e + 1) % mod
        else:
            s = s * (pow(p, e + 1, mod) - 1) % mod * pow(p - 1, -1, mod) % mod
        # произведение делителей: prod^(e+1) * p^(e(e+1)/2 * d_old)
        prod = pow(prod, e + 1, mod) * pow(p, e * (e + 1) // 2 * cnt_e % (mod - 1), mod) % mod
        cnt_e = cnt_e * (e + 1) % (mod - 1)
    return cnt, s, prod


@algo(tags=["divisors", "gcd"], cses=["Common Divisors (1081)"])
def common_divisors_max_gcd(a: list[int]) -> int:
    """Maximum gcd over all pairs of the array.   # Максимальный НОД пары.

    When to use:  n up to 2 * 10^5, values up to 10^6.
    Complexity:   O(M log M), M = max(a)
    Returns:      max gcd(a_i, a_j) over i < j (needs len(a) >= 2).
    Idea:         go d from M down; the first d with >= 2 multiples in a is the answer.
    CSES:         Common Divisors (1081).
    Example:
        >>> common_divisors_max_gcd([3, 14, 15, 7, 9])
        7
    """
    M = max(a)
    cnt = [0] * (M + 1)
    for x in a:
        cnt[x] += 1
    for d in range(M, 0, -1):
        c = 0
        for m in range(d, M + 1, d):  # кратные d
            c += cnt[m]
            if c >= 2:
                return d
    return 1


@algo(tags=["phi", "totient"], cses=["- (phi of one number)"])
def euler_phi(n: int) -> int:
    """Euler's totient of one number by trial division.   # Функция Эйлера одного числа.

    When to use:  phi(n) for a single n up to ~10^12.
    Complexity:   O(sqrt n)
    Returns:      phi(n); phi(1) = 1.
    Related:      phi_table, phi_prefix_sum.
    CSES:         - (phi of one number)
    Example:
        >>> euler_phi(36), euler_phi(97), euler_phi(1)
        (12, 96, 1)
    """
    res, p = n, 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            res -= res // p  # множитель (1 - 1/p)
        p += 1
    if n > 1:
        res -= res // n
    return res


@algo(tags=["floor-blocks", "harmonic"], icpc=["2023 J", "2025 C"])
def floor_blocks(n: int) -> Iterator[tuple[int, int, int]]:
    """Blocks [l, r] where n // i is constant.   # Блоки одинаковых floor(n / i).

    When to use:  sums like sum_{i<=n} f(i) * g(n // i) in O(sqrt n).
    Complexity:   O(sqrt n) blocks (at most 2 * sqrt n)
    Returns:      iterator of (l, r, n // l) covering 1..n.
    Pitfalls:     n // i for i > n is 0 - not produced.
    Related:      sum_of_divisors_sum, phi_prefix_sum, gcd_sum_pairs.
    ICPC-UZ:      2023 J, 2025 C.
    Example:
        >>> list(floor_blocks(10))
        [(1, 1, 10), (2, 2, 5), (3, 3, 3), (4, 5, 2), (6, 10, 1)]
    """
    l = 1
    while l <= n:
        q = n // l
        r = n // q
        yield l, r, q
        l = r + 1


def _phi_prefix_all(n: int) -> dict[int, int]:
    """Phi(v) = sum_{i<=v} phi(i) for every v of the form n // k (Du's sieve, iterative)."""
    limit = min(n, max(1, round(n ** (2 / 3))))
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:
            for m in range(p, limit + 1, p):
                phi[m] -= phi[m] // p
    small = [0] * (limit + 1)
    for i in range(1, limit + 1):
        small[i] = small[i - 1] + phi[i]
    vals = []
    l = 1
    while l <= n:
        q = n // l
        vals.append(q)
        l = n // q + 1
    res: dict[int, int] = {0: 0}
    for v in sorted(vals):  # по возрастанию: меньшие значения уже посчитаны
        if v <= limit:
            res[v] = small[v]
            continue
        s = v * (v + 1) // 2  # sum_{d} Phi(v // d) = v(v+1)/2
        l = 2
        while l <= v:
            q = v // l
            r = v // q
            s -= (r - l + 1) * res[q]
            l = r + 1
        res[v] = s
    return res


@algo(
    tags=["phi", "totient", "du-sieve", "floor-blocks"],
    icpc=["2023 J"],
    requires=["_phi_prefix_all"],
    verified=False,
)
def phi_prefix_sum(n: int) -> int:
    """sum_{i=1}^{n} phi(i) for n up to ~10^10 (Du's sieve).   # Сумма функции Эйлера.

    When to use:  coprime pairs / reduced fractions up to n when n is too big for a sieve.
    Complexity:   O(n^(2/3))
    Returns:      Phi(n) = phi(1) + ... + phi(n).
    Python speed: n = 10^9 about 2 s, 10^10 about 10 s (sieve up to n^(2/3)).
    Idea:         sum_{d=1}^{v} Phi(v // d) = v(v+1)/2 -> Phi(v) = v(v+1)/2 - sum_{d>=2};
                  values v // d are again of the form n // k, compute them in increasing order.
    Related:      coprime_pairs_up_to, phi_table, floor_blocks.
    ICPC-UZ:      2023 J (exact statement NOT VERIFIED).
    Example:
        >>> phi_prefix_sum(10), phi_prefix_sum(1000)
        (32, 304192)
    """
    # NOT VERIFIED: формула проверена тестами, но условие 2023 J не сверено
    return _phi_prefix_all(n)[n] if n > 0 else 0


@algo(tags=["phi", "gcd", "coprime"], icpc=["2023 J"], requires=["_phi_prefix_all"], verified=False)
def coprime_pairs_up_to(n: int) -> int:
    """Ordered pairs (i, j), 1 <= i, j <= n, with gcd(i, j) = 1.   # Взаимно простые пары до n.

    When to use:  count coprime pairs in a square, n up to ~10^10.
    Complexity:   O(n^(2/3))
    Returns:      2 * Phi(n) - 1 (the pair (1, 1) is counted once).
    Pitfalls:     unordered pairs i < j: Phi(n) - 1.
    Related:      phi_prefix_sum, coprime_pairs_count (pairs inside an array).
    ICPC-UZ:      2023 J (exact statement NOT VERIFIED).
    Example:
        >>> coprime_pairs_up_to(3)
        7
    """
    # NOT VERIFIED: какие пары считает 2023 J (упорядоченные или нет) - не сверено
    if n <= 0:
        return 0
    return 2 * _phi_prefix_all(n)[n] - 1


@algo(
    tags=["gcd", "phi", "floor-blocks"],
    icpc=["2025 C"],
    requires=["_phi_prefix_all"],
    verified=False,
)
def gcd_sum_pairs(n: int, mod: int | None = None) -> int:
    """sum_{i=1}^{n} sum_{j=1}^{n} gcd(i, j).   # Сумма НОД всех пар.

    When to use:  gcd sums over a square, n up to ~10^10.
    Complexity:   O(n^(2/3))
    Returns:      the sum (mod mod if given).
    Idea:         gcd(i, j) = sum_{d | i, d | j} phi(d) -> sum_d phi(d) * (n // d)^2,
                  grouped by blocks of n // d with Phi prefix sums.
    Related:      phi_prefix_sum, gcd_sum_with_n, floor_blocks.
    ICPC-UZ:      2025 C "Count The Sum Of GCD" (exact statement NOT VERIFIED).
    Example:
        >>> gcd_sum_pairs(3)
        12
    """
    # NOT VERIFIED: формула проверена перебором, но условие 2025 C не сверено
    P = _phi_prefix_all(n)
    total = 0
    l = 1
    while l <= n:
        q = n // l
        r = n // q
        total += (P[r] - P[l - 1]) * q * q  # l - 1 тоже вида n // k
        l = r + 1
    return total % mod if mod is not None else total


@algo(tags=["gcd", "pillai"], cses=["- (gcd sums)"])
def gcd_sum_with_n(n: int) -> int:
    """Pillai's function sum_{i=1}^{n} gcd(i, n).   # Сумма gcd(i, n).

    When to use:  gcd sums against a fixed n (multiplicative function).
    Complexity:   O(sqrt n)
    Returns:      sum of gcd(i, n) for i = 1..n.
    Idea:         for p^a: (a + 1) * p^a - a * p^(a - 1); multiply over primes.
    Related:      gcd_sum_pairs, euler_phi.
    CSES:         - (gcd sums)
    Example:
        >>> gcd_sum_with_n(6), gcd_sum_with_n(1)
        (15, 1)
    """
    res, p = 1, 2
    while p * p <= n:
        if n % p == 0:
            a = 0
            while n % p == 0:  # показатель p в n
                n //= p
                a += 1
            res *= (a + 1) * p**a - a * p ** (a - 1)  # мультипликативность
        p += 1
    if n > 1:
        res *= 2 * n - 1  # a = 1: 2p - 1
    return res


@algo(tags=["squares", "lagrange"], cses=["Sum of Four Squares (3355)"])
def sum_of_four_squares(n: int) -> tuple[int, int, int, int]:
    """n = a^2 + b^2 + c^2 + d^2 (Lagrange), a >= b >= c >= d >= 0.   # Сумма четырёх квадратов.

    When to use:  constructive four-square representation, n up to ~10^7.
    Complexity:   fast in practice (a few sqrt checks), worst case O(n^(3/4))
    Returns:      (a, b, c, d) with a^2 + b^2 + c^2 + d^2 == n.
    Idea:         take a near sqrt(n); skip remainders of the form 4^k (8m + 7) (not sums of
                  three squares); then brute b, c and check d with isqrt.
    CSES:         Sum of Four Squares (3355).
    Example:
        >>> a, b, c, d = sum_of_four_squares(7)
        >>> a*a + b*b + c*c + d*d
        7
    """
    for a in range(isqrt(n), -1, -1):
        r = n - a * a
        t = r
        while t and t % 4 == 0:
            t //= 4
        if t % 8 == 7:
            continue  # r не сумма трёх квадратов
        for b in range(min(a, isqrt(r)), -1, -1):
            s = r - b * b
            if s > 2 * b * b:
                break  # c, d <= b не дотянут
            for c in range(min(b, isqrt(s)), -1, -1):
                t2 = s - c * c
                if t2 > c * c:
                    break
                d = isqrt(t2)
                if d * d == t2:
                    return a, b, c, d
    raise AssertionError("unreachable: every n >= 0 is a sum of four squares")
