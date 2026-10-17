"""Matrices and linear recurrences: matrix power, Kitamasa, Berlekamp-Massey, Fibonacci.

Матрицы и линейные рекуррентности.
"""

from __future__ import annotations

from rustinpy._registry import algo

MOD = 998244353
MOD7 = 10**9 + 7
INF = 1 << 60


@algo(tags=["matrix"], cses=["Graph Paths I (1723)"], requires=["MOD"])
def mat_mul(a: list[list[int]], b: list[list[int]], mod: int = MOD) -> list[list[int]]:
    """Matrix product modulo mod.   # Произведение матриц.

    When to use:  building block of mat_pow; n up to ~100 in CPython.
    Complexity:   O(n * m * k)
    Returns:      a * b with entries reduced mod mod.
    Pitfalls:     zip(*b) once (columns) - 3-4x faster than index loops.
    Related:      mat_pow, minplus_mat_pow.
    CSES:         Graph Paths I (1723).
    Example:
        >>> mat_mul([[1, 2], [3, 4]], [[5, 6], [7, 8]], 1000)
        [[19, 22], [43, 50]]
    """
    cols = list(zip(*b))  # столбцы b
    return [[sum(x * y for x, y in zip(row, col)) % mod for col in cols] for row in a]


@algo(
    tags=["matrix", "power"],
    cses=["Graph Paths I (1723)", "Fibonacci Numbers (1722)"],
    requires=["MOD", "mat_mul"],
)
def mat_pow(m: list[list[int]], e: int, mod: int = MOD) -> list[list[int]]:
    """Square matrix to the power e modulo mod.   # Матричная экспонента.

    When to use:  linear recurrences with huge k, number of walks of length k in a graph.
    Complexity:   O(n^3 log e)
    Returns:      m^e (identity for e = 0).
    Python speed: n = 100, e = 10^9 -> ~30 matrix products of 10^6 ops: ~10 s, too slow;
                  n <= 30 is comfortable.
    Related:      mat_mul, linear_recurrence_kth (O(d^2 log k) instead of O(d^3 log k)).
    CSES:         Graph Paths I (1723), Fibonacci Numbers (1722), Throwing Dice (1096).
    Example:
        >>> mat_pow([[1, 1], [1, 0]], 10, 10**9 + 7)[0][1]
        55
    """
    n = len(m)
    res = [[int(i == j) for j in range(n)] for i in range(n)]
    base = m
    while e > 0:
        if e & 1:
            res = mat_mul(res, base, mod)
        base = mat_mul(base, base, mod)  # возводим в квадрат
        e >>= 1
    return res


@algo(
    tags=["matrix", "min-plus", "shortest-path"], cses=["Graph Paths II (1724)"], requires=["INF"]
)
def minplus_mat_pow(m: list[list[int]], e: int) -> list[list[int]]:
    """Min-plus (tropical) matrix power: cheapest walks with exactly e edges.   # Min-plus степень.

    When to use:  shortest walk using exactly k edges, k huge.
    Complexity:   O(n^3 log e)
    Input:        m[i][j] = edge weight or INF (= 1 << 60) if no edge.
    Returns:      r[i][j] = min cost of a walk i -> j with exactly e edges, INF if none.
    Related:      mat_pow, graph.floyd_warshall.
    CSES:         Graph Paths II (1724).
    Example:
        >>> X = 1 << 60
        >>> minplus_mat_pow([[X, 4], [1, X]], 3)[0][1]
        9
    """
    n = len(m)

    def mul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
        cols = list(zip(*b))
        return [[min(x + y for x, y in zip(row, col)) for col in cols] for row in a]

    res = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    base = m
    while e > 0:
        if e & 1:
            res = mul(res, base)
        base = mul(base, base)
        e >>= 1
    # значения >= INF считаем «нет пути»
    return [[INF if v >= INF else v for v in row] for row in res]


@algo(
    tags=["recurrence", "kitamasa", "polynomial"], cses=["Throwing Dice (1096)"], requires=["MOD"]
)
def linear_recurrence_kth(coef: list[int], init: list[int], k: int, mod: int = MOD) -> int:
    """k-th term of a_n = sum_{i=1}^{d} coef[i-1] * a_{n-i} (Kitamasa).   # k-й член рекуррентности.

    When to use:  linear recurrence of order d <= ~500 and k up to 10^18.
    Complexity:   O(d^2 log k)
    Input:        coef = [c_1, ..., c_d], init = [a_0, ..., a_{d-1}].
    Returns:      a_k mod mod.
    Idea:         x^k mod charpoly(x) = sum r_j x^j  ->  a_k = sum r_j a_j.
    Related:      berlekamp_massey (find coef from the first 2d terms), mat_pow.
    CSES:         Throwing Dice (1096).
    Example:
        >>> linear_recurrence_kth([1, 1], [0, 1], 10, 10**9 + 7)
        55
    """
    d = len(coef)
    if k < len(init):
        return init[k] % mod

    def mulmod(a: list[int], b: list[int]) -> list[int]:
        res = [0] * (2 * d - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    res[i + j] += x * y
        for i in range(2 * d - 2, d - 1, -1):  # x^i = sum_j c_j x^(i-j)
            v = res[i] % mod
            if v:
                for j in range(1, d + 1):
                    res[i - j] += v * coef[j - 1]
        return [x % mod for x in res[:d]]

    result = [1] + [0] * (d - 1)  # многочлен 1
    base = [0, 1] + [0] * (d - 2) if d > 1 else [coef[0] % mod]  # x mod P
    while k > 0:
        if k & 1:
            result = mulmod(result, base)
        base = mulmod(base, base)
        k >>= 1
    return sum(r * a for r, a in zip(result, init)) % mod


@algo(tags=["recurrence", "berlekamp-massey"], cses=["- (guess a recurrence)"], requires=["MOD"])
def berlekamp_massey(seq: list[int], mod: int = MOD) -> list[int]:
    """Shortest linear recurrence of a sequence modulo a prime.   # Берлекэмп-Месси.

    When to use:  answer is a linear recurrence of unknown order d: compute 2d+ terms by
                  brute force / DP, find coef, then linear_recurrence_kth.
    Complexity:   O(n^2)
    Returns:      coef = [c_1, ..., c_d] with seq[n] = sum c_i * seq[n - i] (mod prime).
    Pitfalls:     give at least 2d terms, better 2d + 10; mod must be prime.
    Related:      linear_recurrence_kth.
    CSES:         - (guess a recurrence)
    Example:
        >>> berlekamp_massey([0, 1, 1, 2, 3, 5, 8, 13], 10**9 + 7)
        [1, 1]
    """
    C, B = [1], [1]
    L, m, b = 0, 1, 1
    for n in range(len(seq)):
        d = seq[n] % mod  # невязка
        for i in range(1, L + 1):
            d = (d + C[i] * seq[n - i]) % mod
        if d == 0:
            m += 1
            continue
        T = C[:]
        coef = d * pow(b, mod - 2, mod) % mod
        if len(C) < len(B) + m:
            C += [0] * (len(B) + m - len(C))
        for i, bi in enumerate(B):
            C[i + m] = (C[i + m] - coef * bi) % mod
        if 2 * L <= n:
            L, B, b, m = n + 1 - L, T, d, 1
        else:
            m += 1
    return [(-c) % mod for c in C[1 : L + 1]]


@algo(tags=["fibonacci", "doubling"], cses=["Fibonacci Numbers (1722)"], requires=["MOD7"])
def fib(n: int, mod: int = MOD7) -> int:
    """F(n) mod mod by fast doubling, F(0) = 0, F(1) = 1.   # Быстрый Фибоначчи.

    When to use:  n up to 10^18.
    Complexity:   O(log n)
    Returns:      F(n) mod mod.
    Idea:         F(2k) = F(k) * (2F(k+1) - F(k)), F(2k+1) = F(k)^2 + F(k+1)^2.
    Related:      mat_pow, zeckendorf.
    CSES:         Fibonacci Numbers (1722).
    Example:
        >>> [fib(i) for i in range(10)], fib(10**18) < 10**9 + 7
        ([0, 1, 1, 2, 3, 5, 8, 13, 21, 34], True)
    """
    a, b = 0, 1  # F(k), F(k+1), k = 0
    for bit in bin(n)[2:]:  # биты от старшего к младшему
        a, b = a * (2 * b - a) % mod, (a * a + b * b) % mod  # k -> 2k
        if bit == "1":
            a, b = b, (a + b) % mod  # 2k -> 2k + 1
    return a


@algo(
    tags=["recurrence", "dice"],
    cses=["Throwing Dice (1096)"],
    requires=["MOD7", "linear_recurrence_kth"],
)
def throwing_dice(n: int, mod: int = MOD7) -> int:
    """Ways to get sum n with dice throws 1..6 (ordered).   # Броски кубика с суммой n.

    When to use:  n up to 10^18.
    Complexity:   O(36 log n)
    Returns:      f(n) mod mod, f(n) = f(n-1) + ... + f(n-6), f(0) = 1.
    Related:      linear_recurrence_kth, dp.dice_combinations (small n).
    CSES:         Throwing Dice (1096).
    Example:
        >>> throwing_dice(8)
        125
    """
    return linear_recurrence_kth([1] * 6, [1, 1, 2, 4, 8, 16], n, mod)


@algo(tags=["fibonacci", "zeckendorf"], icpc=["2023 H", "2025 J"])
def zeckendorf(n: int) -> list[int]:
    """Zeckendorf representation: n as a sum of non-adjacent Fibonacci numbers.   # Цекендорф.

    When to use:  Fibonacci number system, games and counting on Fibonacci sums.
    Complexity:   O(log n)
    Returns:      Fibonacci numbers (1, 2, 3, 5, 8, ...) in decreasing order, summing to n.
    Idea:         greedy: always take the largest Fibonacci number <= remainder.
    Related:      count_fib_representations, fib.
    ICPC-UZ:      2023 H, 2025 J.
    Example:
        >>> zeckendorf(100), zeckendorf(0)
        ([89, 8, 3], [])
    """
    fibs = [1, 2]
    while fibs[-1] <= n:
        fibs.append(fibs[-1] + fibs[-2])
    res = []
    for f in reversed(fibs):
        if f <= n:
            res.append(f)  # жадно берём наибольшее
            n -= f
    return res


@algo(tags=["fibonacci", "zeckendorf", "dp"], icpc=["2023 H", "2025 J"], verified=False)
def count_fib_representations(n: int) -> int:
    """Ways to write n as a sum of DISTINCT Fibonacci numbers 1, 2, 3, 5, ...   # Число разложений.

    When to use:  "how many representations as sums of distinct Fibonacci numbers", n ~ 10^18.
    Complexity:   O(log n)
    Returns:      number of sets of distinct Fibonacci numbers (1 counted once) with sum n.
    Idea:         Zeckendorf indices p_1 < ... < p_k (F_1 = 1, F_2 = 2); a term can be kept
                  or split down; with gap d = p_i - p_{i-1}:
                  keep_i = keep + split, split_i = keep * ((d - 1) // 2) + split * (d // 2).
    Related:      zeckendorf.
    ICPC-UZ:      2023 H, 2025 J (exact statements NOT VERIFIED).
    Example:
        >>> [count_fib_representations(x) for x in range(1, 11)]
        [1, 1, 2, 1, 2, 2, 1, 3, 2, 2]
    """
    # NOT VERIFIED: формула сверена перебором, условия 2023 H / 2025 J не сверены
    if n == 0:
        return 1
    fibs = [1, 2]
    while fibs[-1] <= n:
        fibs.append(fibs[-1] + fibs[-2])
    pos = []
    for i in range(len(fibs) - 1, -1, -1):
        if fibs[i] <= n:
            pos.append(i + 1)  # индекс в последовательности 1, 2, 3, 5, ...
            n -= fibs[i]
    pos.reverse()
    keep, split, prev = 1, 0, 0
    for p in pos:
        d = p - prev
        keep, split = keep + split, keep * ((d - 1) // 2) + split * (d // 2)
        prev = p
    return keep + split
