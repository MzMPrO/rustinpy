"""Combinatorics: binomials (prime and composite modulus), Catalan, Stirling, Bell, Burnside.

Комбинаторика.
"""

from __future__ import annotations

from math import gcd

from rustinpy._registry import algo

MOD = 998244353
MOD7 = 10**9 + 7


@algo(
    tags=["combinatorics", "binomial", "factorial"],
    cses=["Binomial Coefficients (1079)"],
    icpc=["2025 B"],
    requires=["MOD"],
)
class Comb:
    """Factorials and inverse factorials up to n_max.   # nCr, nPr, мультиномиальные по модулю.

    When to use:  many nCr queries with n <= n_max (~10^6) modulo a PRIME.
    Complexity:   O(n_max) build, O(1) per query
    Methods:      nCr(n, r), nPr(n, r), multinomial(ks), fact[i], inv_fact[i]
    Pitfalls:     composite modulus (ICPC-UZ 2025 B: 2112025 = 5^2 * 84481) -> n! is not
                  invertible -> ValueError; use nCr_pascal or nCr_composite.   # составной модуль
    Related:      nCr_pascal, nCr_composite, nCr_lucas.
    CSES:         Binomial Coefficients (1079), Creating Strings II (1715).
    ICPC-UZ:      2025 B (composite modulus - see Pitfalls).
    Example:
        >>> c = Comb(10, 10**9 + 7)
        >>> c.nCr(10, 3), c.nPr(5, 2), c.multinomial([2, 1, 1])
        (120, 20, 12)
        >>> Comb(10, 2112025)
        Traceback (most recent call last):
        ValueError: 10! is not invertible modulo 2112025; use nCr_pascal or nCr_composite
    """

    def __init__(self, n_max: int, mod: int = MOD) -> None:
        self.mod = mod
        fact = [1] * (n_max + 1)
        for i in range(1, n_max + 1):
            fact[i] = fact[i - 1] * i % mod
        try:
            last = pow(fact[n_max], -1, mod)  # одна инверсия на всё
        except ValueError:
            raise ValueError(
                f"{n_max}! is not invertible modulo {mod}; use nCr_pascal or nCr_composite"
            ) from None
        inv = [1] * (n_max + 1)
        inv[n_max] = last
        for i in range(n_max, 0, -1):  # inv_fact[i-1] = inv_fact[i] * i
            inv[i - 1] = inv[i] * i % mod
        self.fact = fact
        self.inv_fact = inv

    def nCr(self, n: int, r: int) -> int:
        if r < 0 or r > n or n < 0:
            return 0
        return self.fact[n] * self.inv_fact[r] % self.mod * self.inv_fact[n - r] % self.mod

    def nPr(self, n: int, r: int) -> int:
        if r < 0 or r > n or n < 0:
            return 0
        return self.fact[n] * self.inv_fact[n - r] % self.mod

    def multinomial(self, ks: list[int]) -> int:
        res = self.fact[sum(ks)]
        for k in ks:
            res = res * self.inv_fact[k] % self.mod
        return res


@algo(tags=["combinatorics", "binomial", "composite-mod"], icpc=["2025 B"])
def nCr_pascal(n_max: int, mod: int) -> list[list[int]]:
    """Pascal triangle C[n][r] mod any modulus.   # Треугольник Паскаля по любому модулю.

    When to use:  composite or tiny modulus, n <= ~3000 (ICPC-UZ 2025 B, mod 2112025).
    Complexity:   O(n_max^2) time and memory
    Returns:      C with C[n][r] for 0 <= r <= n <= n_max.
    Pitfalls:     memory ~ n^2 / 2 ints: 5000 -> 12.5M numbers is already too much.
    Related:      Comb (prime mod), nCr_composite (big n, composite mod).
    ICPC-UZ:      2025 B.
    Example:
        >>> C = nCr_pascal(5, 2112025)
        >>> C[5]
        [1, 5, 10, 10, 5, 1]
    """
    C = [[1]]
    for n in range(1, n_max + 1):
        prev = C[-1]
        row = [1] * (n + 1)
        for r in range(1, n):
            row[r] = (prev[r - 1] + prev[r]) % mod  # C(n,r) = C(n-1,r-1) + C(n-1,r)
        C.append(row)
    return C


@algo(tags=["combinatorics", "binomial", "lucas"], cses=["- (big n, small prime p)"])
def nCr_lucas(n: int, r: int, p: int) -> int:
    """C(n, r) mod small prime p by Lucas' theorem.   # Теорема Люка.

    When to use:  n up to 10^18, prime p up to ~10^5.
    Complexity:   O(p + log_p n) per call (digit binomials by multiplicative formula)
    Returns:      C(n, r) mod p.
    Pitfalls:     p must be prime; for prime powers use nCr_composite.
    Related:      nCr_composite, Comb.
    CSES:         - (big n, small prime p)
    Example:
        >>> nCr_lucas(10, 3, 7), 120 % 7
        (1, 1)
        >>> from math import comb
        >>> nCr_lucas(1000, 300, 13) == comb(1000, 300) % 13
        True
    """
    res = 1
    while n or r:
        ni, ri = n % p, r % p  # цифры в системе счисления p
        if ri > ni:
            return 0
        num = den = 1
        for i in range(ri):
            num = num * (ni - i) % p
            den = den * (i + 1) % p
        res = res * num % p * pow(den, p - 2, p) % p
        n //= p
        r //= p
    return res


@algo(tags=["combinatorics", "binomial", "composite-mod", "crt"], icpc=["2025 B"])
def nCr_composite(n: int, r: int, mod: int) -> int:
    """C(n, r) modulo any composite modulus via prime powers + CRT.   # nCr по составному модулю.

    When to use:  composite modulus and n up to ~10^6 (ICPC-UZ 2025 B: 2112025 = 5^2 * 84481).
    Complexity:   O(n * omega(mod) + sqrt(mod))
    Returns:      C(n, r) mod mod.
    Idea:         for each p^e | mod: n! without factors p (mod p^e) is invertible;
                  multiply by p^(v_p(n!) - v_p(r!) - v_p((n-r)!)); combine by CRT.
    Related:      nCr_pascal, Comb, crt.
    ICPC-UZ:      2025 B.
    Example:
        >>> from math import comb
        >>> nCr_composite(30, 12, 2112025) == comb(30, 12) % 2112025
        True
        >>> nCr_composite(5, 7, 12)
        0
    """
    if r < 0 or r > n:
        return 0
    # разложение модуля пробным делением
    factors: list[tuple[int, int]] = []
    m, d = mod, 2
    while d * d <= m:
        if m % d == 0:
            e = 0
            while m % d == 0:
                m //= d
                e += 1
            factors.append((d, e))
        d += 1
    if m > 1:
        factors.append((m, 1))
    x, M = 0, 1
    for p, e in factors:
        pe = p**e

        # v_p(k!) по формуле Лежандра
        def vp(k: int, p: int = p) -> int:
            s = 0
            while k:
                k //= p
                s += k
            return s

        v = vp(n) - vp(r) - vp(n - r)
        if v >= e:
            val = 0
        else:
            # факториалы без множителей p по модулю p^e (один проход до n)
            f_r = f_nr = 1
            prod = 1
            for i in range(1, n + 1):
                t = i
                while t % p == 0:
                    t //= p
                prod = prod * t % pe
                if i == r:
                    f_r = prod
                if i == n - r:
                    f_nr = prod
            val = prod * pow(f_r * f_nr % pe, -1, pe) % pe * pow(p, v, pe) % pe
        # склейка по КТО (модули взаимно просты)
        t = (val - x) * pow(M, -1, pe) % pe
        x += M * t
        M *= pe
    return x % mod


@algo(
    tags=["combinatorics", "catalan", "brackets"],
    cses=["Bracket Sequences I (2064)"],
    requires=["MOD7"],
)
def catalan(n: int, mod: int = MOD7) -> int:
    """n-th Catalan number C(2n, n) / (n + 1) mod prime.   # Числа Каталана.

    When to use:  correct bracket sequences of n pairs, binary trees with n nodes, Dyck paths.
    Complexity:   O(n)
    Returns:      Catalan(n) mod mod (prime mod > 2n).
    Pitfalls:     bracket sequence of LENGTH n has n / 2 pairs -> catalan(n // 2), 0 if n odd.
    Related:      bracket_sequences_prefix, Comb.
    CSES:         Bracket Sequences I (2064).
    Example:
        >>> [catalan(i) for i in range(7)]
        [1, 1, 2, 5, 14, 42, 132]
    """
    num = den = 1
    for i in range(1, n + 1):
        num = num * (n + i) % mod  # (2n)! / n!
        den = den * i % mod  # n!
    den = den * (n + 1) % mod
    return num * pow(den, -1, mod) % mod


@algo(
    tags=["combinatorics", "catalan", "brackets", "reflection"],
    cses=["Bracket Sequences II (2187)"],
    requires=["MOD7"],
)
def bracket_sequences_prefix(n: int, prefix: str, mod: int = MOD7) -> int:
    """Number of correct bracket sequences of length n starting with prefix.   # Скобки с префиксом.

    When to use:  count completions of a partial bracket sequence.
    Complexity:   O(n)
    Returns:      count mod mod (prime > n).
    Idea:         k = n - len(prefix) steps from height b to 0 never below 0:
                  C(k, x) - C(k, x - 1), x = (k - b) / 2 opening brackets (reflection).
    Related:      catalan.
    CSES:         Bracket Sequences II (2187).
    Example:
        >>> bracket_sequences_prefix(6, "(()")
        2
        >>> bracket_sequences_prefix(4, "())"), bracket_sequences_prefix(5, "")
        (0, 0)
    """
    b = 0
    for ch in prefix:
        b += 1 if ch == "(" else -1
        if b < 0:
            return 0  # префикс уже некорректен
    k = n - len(prefix)
    if k < 0 or (k - b) % 2 != 0 or b > k:
        return 0
    x = (k - b) // 2  # сколько ещё открывающих
    fact = [1] * (k + 1)
    for i in range(1, k + 1):
        fact[i] = fact[i - 1] * i % mod

    def C(a: int, c: int) -> int:
        if c < 0 or c > a:
            return 0
        return fact[a] * pow(fact[c] * fact[a - c] % mod, -1, mod) % mod

    return (C(k, x) - C(k, x - 1)) % mod


@algo(tags=["combinatorics", "stirling"], cses=["- (permutations by cycles)"], requires=["MOD"])
def stirling1_table(n: int, mod: int = MOD) -> list[list[int]]:
    """Unsigned Stirling numbers of the first kind c(i, k).   # Стирлинг 1-го рода.

    When to use:  permutations of i elements with exactly k cycles.
    Complexity:   O(n^2)
    Returns:      s with s[i][k] for 0 <= k <= i <= n.
    Related:      stirling2_table, bell_numbers.
    CSES:         - (permutations by cycles)
    Example:
        >>> stirling1_table(4)[4]
        [0, 6, 11, 6, 1]
    """
    s = [[1]]
    for i in range(1, n + 1):
        prev = s[-1]
        row = [0] * (i + 1)
        for k in range(1, i + 1):
            # новый элемент: отдельный цикл или вставка после одного из i-1 элементов
            row[k] = (prev[k - 1] + (i - 1) * (prev[k] if k < i else 0)) % mod
        s.append(row)
    return s


@algo(
    tags=["combinatorics", "stirling", "partitions"], cses=["Counting Sequences"], requires=["MOD"]
)
def stirling2_table(n: int, mod: int = MOD) -> list[list[int]]:
    """Stirling numbers of the second kind S(i, k).   # Стирлинг 2-го рода.

    When to use:  partitions of i labelled items into k non-empty unlabelled groups;
                  surjections i -> k equal k! * S(i, k).
    Complexity:   O(n^2)
    Returns:      S with S[i][k] for 0 <= k <= i <= n.
    Related:      stirling1_table, bell_numbers.
    CSES:         Counting Sequences (surjections).
    Example:
        >>> stirling2_table(4)[4]
        [0, 1, 7, 6, 1]
    """
    S = [[1]]
    for i in range(1, n + 1):
        prev = S[-1]
        row = [0] * (i + 1)
        for k in range(1, i + 1):
            # новый элемент: отдельная группа или в одну из k групп
            row[k] = (prev[k - 1] + k * (prev[k] if k < i else 0)) % mod
        S.append(row)
    return S


@algo(tags=["combinatorics", "bell", "partitions"], cses=["- (set partitions)"], requires=["MOD"])
def bell_numbers(n: int, mod: int = MOD) -> list[int]:
    """Bell numbers B_0..B_n (set partitions) via the Bell triangle.   # Числа Белла.

    When to use:  number of ways to split a labelled set into any number of groups.
    Complexity:   O(n^2)
    Returns:      [B_0, ..., B_n] mod mod.
    Related:      stirling2_table (B_n = sum_k S(n, k)).
    CSES:         - (set partitions)
    Example:
        >>> bell_numbers(6)
        [1, 1, 2, 5, 15, 52, 203]
    """
    res = [1]
    row = [1]
    for _ in range(n):
        new = [row[-1]]  # строка начинается с последнего элемента предыдущей
        for v in row:
            new.append((new[-1] + v) % mod)
        row = new
        res.append(row[0])
    return res


@algo(tags=["combinatorics", "derangements"], cses=["Christmas Party (1717)"], requires=["MOD7"])
def derangements(n: int, mod: int = MOD7) -> int:
    """Permutations without fixed points D(n).   # Беспорядки (никто не получил свой подарок).

    When to use:  "nobody gets their own gift".
    Complexity:   O(n)
    Returns:      D(n) mod mod; D(0) = 1, D(1) = 0.
    Idea:         D(n) = (n - 1) * (D(n - 1) + D(n - 2)).
    CSES:         Christmas Party (1717).
    Example:
        >>> [derangements(i) for i in range(7)]
        [1, 0, 1, 2, 9, 44, 265]
    """
    a, b = 1, 0  # D(0), D(1)
    if n == 0:
        return 1 % mod
    for i in range(2, n + 1):
        a, b = b, (i - 1) * (a + b) % mod
    return b % mod


@algo(
    tags=["combinatorics", "stars-and-bars"], cses=["Distributing Apples (1716)"], requires=["MOD7"]
)
def stars_and_bars(n: int, m: int, mod: int = MOD7) -> int:
    """Ways to give m identical apples to n children: C(n + m - 1, m).   # Шары и перегородки.

    When to use:  non-negative integer solutions of x_1 + ... + x_n = m.
    Complexity:   O(n + m)
    Returns:      C(n + m - 1, n - 1) mod prime mod.
    Pitfalls:     positive solutions (x_i >= 1): stars_and_bars(n, m - n).
    CSES:         Distributing Apples (1716).
    Example:
        >>> stars_and_bars(3, 2)
        6
    """
    if n == 0:
        return 1 if m == 0 else 0
    if m < 0:
        return 0
    top = n + m - 1
    num = den = 1
    for i in range(1, n):  # C(top, n-1)
        num = num * (top - i + 1) % mod
        den = den * i % mod
    return num * pow(den, -1, mod) % mod


@algo(
    tags=["combinatorics", "burnside", "necklaces"],
    cses=["Counting Necklaces (2209)"],
    requires=["MOD7"],
)
def necklaces_count(n: int, m: int, mod: int = MOD7) -> int:
    """Necklaces of n beads in m colours up to rotation (Burnside).   # Лемма Бернсайда.

    When to use:  count colourings up to a symmetry group: average fixed points.
    Complexity:   O(n log n)
    Returns:      (1/n) * sum_{i=0}^{n-1} m^gcd(i, n) mod prime mod.
    Pitfalls:     with reflections too (bracelets) add the n reflection terms and divide by 2n.
    Related:      grid_colorings_count.
    CSES:         Counting Necklaces (2209).
    Example:
        >>> necklaces_count(4, 3)
        24
    """
    total = 0
    for i in range(n):
        total += pow(m, gcd(i, n), mod)  # поворот на i: gcd(i, n) циклов
    return total % mod * pow(n, -1, mod) % mod


@algo(tags=["combinatorics", "burnside"], cses=["Counting Grids (2210)"], requires=["MOD7"])
def grid_colorings_count(n: int, mod: int = MOD7) -> int:
    """Black/white n x n grids up to rotation (Burnside).   # Сетки с точностью до поворота.

    When to use:  rotations by 0/90/180/270 degrees.
    Complexity:   O(log n)
    Returns:      (2^(n^2) + 2 * 2^ceil(n^2/4) + 2^ceil(n^2/2)) / 4 mod prime mod.
    Related:      necklaces_count.
    CSES:         Counting Grids (2210).
    Example:
        >>> grid_colorings_count(2), grid_colorings_count(4)
        (6, 16456)
    """
    c = n * n
    total = pow(2, c, mod) + 2 * pow(2, (c + 3) // 4, mod) + pow(2, (c + 1) // 2, mod)
    return total % mod * pow(4, -1, mod) % mod


@algo(tags=["inclusion-exclusion"], cses=["Prime Multiples (2185)"])
def prime_multiples_count(n: int, primes: list[int]) -> int:
    """How many of 1..n are divisible by at least one given prime.   # Включения-исключения.

    When to use:  k <= 20 distinct primes, n up to 10^18.
    Complexity:   O(number of subsets with product <= n) <= O(2^k)
    Returns:      count of x in [1, n] divisible by some p in primes.
    Pitfalls:     prune products > n early - avoids huge ints and saves time.   # отсечение
    CSES:         Prime Multiples (2185).
    Example:
        >>> prime_multiples_count(20, [2, 5])
        12
    """
    subsets: list[tuple[int, int]] = []  # (произведение, знак)
    for p in primes:
        new = [(p, 1)] if p <= n else []
        for prod, sign in subsets:
            if prod * p <= n:
                new.append((prod * p, -sign))
        subsets += new
    return sum(sign * (n // prod) for prod, sign in subsets)


@algo(tags=["inclusion-exclusion", "mobius", "gcd"], cses=["Counting Coprime Pairs (2417)"])
def coprime_pairs_count(a: list[int]) -> int:
    """Pairs i < j with gcd(a_i, a_j) = 1 (Mobius over divisors).   # Взаимно простые пары.

    When to use:  n up to 10^5, values up to 10^6.
    Complexity:   O(M log M), M = max(a)
    Returns:      number of unordered pairs with gcd 1.
    Idea:         answer = sum_d mu(d) * C(cnt_d, 2), cnt_d = how many a_i are divisible by d.
    Related:      mobius_table, phi_prefix_sum.
    CSES:         Counting Coprime Pairs (2417).
    Example:
        >>> coprime_pairs_count([5, 4, 20, 1, 16, 17, 5, 15])
        19
    """
    if not a:
        return 0
    M = max(a)
    freq = [0] * (M + 1)
    for x in a:
        freq[x] += 1
    # функция Мёбиуса решетом
    mu = [1] * (M + 1)
    is_comp = bytearray(M + 1)
    for p in range(2, M + 1):
        if not is_comp[p]:
            for q in range(p, M + 1, p):
                if q > p:
                    is_comp[q] = 1
                mu[q] = -mu[q]
            for q in range(p * p, M + 1, p * p):
                mu[q] = 0
    total = 0
    for d in range(1, M + 1):
        if mu[d]:
            c = sum(freq[d::d])  # сколько чисел делится на d
            total += mu[d] * (c * (c - 1) // 2)
    return total
