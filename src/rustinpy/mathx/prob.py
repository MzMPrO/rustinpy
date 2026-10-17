"""Probability and expected value.

Вероятности и математическое ожидание.
"""

from __future__ import annotations

from math import ceil, log1p

from rustinpy._registry import algo


@algo(tags=["probability", "dp", "dice"], cses=["Dice Probability (1725)"])
def dice_probability(n: int, a: int, b: int) -> float:
    """Probability that the sum of n dice lies in [a, b].   # Вероятность суммы кубиков.

    When to use:  distribution of a sum of independent small variables.
    Complexity:   O(n * 6n * 6)
    Returns:      P(a <= sum <= b) as float.
    Pitfalls:     CSES wants exactly 6 digits with round-half-even: f"{x:.6f}".
    CSES:         Dice Probability (1725).
    Example:
        >>> round(dice_probability(2, 9, 10), 6)
        0.194444
    """
    dp = [1.0]  # распределение суммы: dp[s]
    for _ in range(n):
        new = [0.0] * (len(dp) + 6)
        for s, p in enumerate(dp):
            if p:
                for f in range(1, 7):
                    new[s + f] += p / 6
        dp = new
    return sum(dp[max(a, 0) : b + 1])


@algo(tags=["probability", "expected-value", "grid"], cses=["Moving Robots (1726)"])
def moving_robots(k: int) -> float:
    """Expected number of empty squares after k random robot moves on 8x8.   # Роботы на доске.

    When to use:  linearity of expectation over cells; per-robot distributions.
    Complexity:   O(64 * k * 64 * 4)
    Returns:      E[number of empty cells] after k moves (one robot per cell at start).
    Idea:         E = sum_cells prod_robots (1 - P_robot(cell)).
    CSES:         Moving Robots (1726).
    Example:
        >>> f"{moving_robots(10):.6f}"
        '23.120740'
    """
    N = 8
    neigh: list[list[int]] = []
    for c in range(N * N):
        r, cc = divmod(c, N)
        lst = [
            (r + dr) * N + cc + dc
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
            if 0 <= r + dr < N and 0 <= cc + dc < N
        ]
        neigh.append(lst)
    empty = [1.0] * (N * N)
    for start in range(N * N):
        p = [0.0] * (N * N)
        p[start] = 1.0
        for _ in range(k):  # распределение этого робота
            q = [0.0] * (N * N)
            for c in range(N * N):
                if p[c]:
                    share = p[c] / len(neigh[c])
                    for d in neigh[c]:
                        q[d] += share
            p = q
        for c in range(N * N):
            empty[c] *= 1 - p[c]  # клетка пуста, если этот робот не там
    return sum(empty)


@algo(tags=["probability", "expected-value"], cses=["Candy Lottery (1727)"])
def candy_lottery(n: int, k: int) -> float:
    """Expected maximum of n uniform values from 1..k.   # Ожидаемый максимум.

    When to use:  E[max] = sum_x x * (P(max <= x) - P(max <= x - 1)).
    Complexity:   O(k)
    Returns:      expected maximum as float.
    CSES:         Candy Lottery (1727).
    Example:
        >>> round(candy_lottery(2, 3), 6)
        2.444444
    """
    return sum(x * ((x / k) ** n - ((x - 1) / k) ** n) for x in range(1, k + 1))


@algo(tags=["probability", "expected-value", "inversions"], cses=["Inversion Probability (1728)"])
def inversion_probability(r: list[int]) -> float:
    """Expected inversions when x_i is uniform in [1, r_i].   # Ожидаемое число инверсий.

    When to use:  linearity of expectation over pairs (n <= ~1000).
    Complexity:   O(n^2)
    Returns:      E[#(i < j with x_i > x_j)].
    Idea:         P(x_i > x_j) = (r_i - 1) / (2 r_j) if r_i <= r_j,
                  else (r_j - 1) / (2 r_i) + (r_i - r_j) / r_i.
    CSES:         Inversion Probability (1728).
    Example:
        >>> round(inversion_probability([5, 2, 7]), 6)
        1.057143
    """
    total = 0.0
    n = len(r)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = r[i], r[j]
            if a <= b:
                total += (a - 1) / (2 * b)
            else:
                total += (b - 1) / (2 * a) + (a - b) / a
    return total


@algo(tags=["probability", "logarithm", "precision"], icpc=["2023 D"], verified=False)
def min_trials_for_probability(p: float, q: float) -> int:
    """Smallest K with 1 - (1 - q)^K >= p.   # Минимум попыток, чтобы вероятность успеха была >= p.

    When to use:  "how many independent tries with success q are needed to succeed with
                  probability at least p".
    Complexity:   O(1)
    Returns:      K >= 0; ValueError when impossible (q = 0 < p, or p >= 1 with q < 1).
    Pitfalls:     K = ceil(ln(1 - p) / ln(1 - q)) suffers from rounding near integers;
                  use log1p and re-check K - 1 and K with the same comparison.
    ICPC-UZ:      2023 D (exact statement and precision rules NOT VERIFIED).
    Example:
        >>> min_trials_for_probability(0.5, 0.5), min_trials_for_probability(0.75, 0.5)
        (1, 2)
        >>> min_trials_for_probability(0.9, 0.1)
        22
    """
    # NOT VERIFIED: условие 2023 D и требования к точности не сверены
    if p <= 0:
        return 0
    if q >= 1:
        return 1
    if q <= 0 or p >= 1:
        raise ValueError("probability p is unreachable")
    lp, lq = log1p(-p), log1p(-q)  # оба < 0; условие: K * lq <= lp
    k = max(0, ceil(lp / lq - 1e-12))
    while k > 0 and (k - 1) * lq <= lp:
        k -= 1
    while k * lq > lp:
        k += 1
    return k
