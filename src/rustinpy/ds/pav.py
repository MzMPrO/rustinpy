"""Isotonic regression (pool adjacent violators).

Монотонная подгонка методом наименьших квадратов (PAV).
"""

from __future__ import annotations

from fractions import Fraction

from rustinpy._registry import algo

MOD = 998244353


@algo(tags=["isotonic-regression", "pav", "stack", "least-squares"], icpc=["2023 L"])
def pav(y: list[int], w: list[int] | None = None) -> list[tuple[int, int, Fraction]]:
    """Best non-decreasing least-squares fit as blocks of equal values.   # Изотоническая регрессия.

    When to use:  minimise sum w_i (x_i - y_i)^2 subject to x_0 <= x_1 <= ... <= x_{n-1}.
    Complexity:   O(n) amortised (stack of blocks)
    Returns:      blocks (l, r, mean) with half-open [l, r); x_i = mean on the block.
    Pitfalls:     means are exact Fractions - convert at the end if floats suffice.
    Idea:         push each point as a block; while the last block's mean is smaller than
                  the previous one's, merge them (weighted mean).   # слияние нарушителей
    Related:      isotonic_sse_mod.
    ICPC-UZ:      2023 L (monotone least-squares fit).
    Example:
        >>> [(l, r, str(m)) for l, r, m in pav([1, 3, 2, 4])]
        [(0, 1, '1'), (1, 3, '5/2'), (3, 4, '4')]
    """
    ws = w if w is not None else [1] * len(y)
    blocks: list[tuple[int, int, int, int]] = []  # (l, r, сумма w*y, сумма w)
    for i, (v, wi) in enumerate(zip(y, ws)):
        l, r, s, c = i, i + 1, v * wi, wi
        # предыдущий блок со средним больше текущего - сливаем
        while blocks and blocks[-1][2] * c > s * blocks[-1][3]:
            pl, _, ps, pc = blocks.pop()
            l, s, c = pl, s + ps, c + pc
        blocks.append((l, r, s, c))
    return [(l, r, Fraction(s, c)) for l, r, s, c in blocks]


@algo(
    tags=["isotonic-regression", "pav", "modular"],
    icpc=["2023 L"],
    requires=["MOD", "pav"],
    verified=False,
)
def isotonic_sse_mod(y: list[int], mod: int = MOD) -> int:
    """Least squares error of the best non-decreasing fit, mod prime.   # Ошибка подгонки по модулю.

    When to use:  answer is a rational number printed as p * q^(-1) mod prime.
    Complexity:   O(n)
    Returns:      SSE = sum (y_i - x_i)^2 of the best fit, as an element of Z_mod.
    Idea:         per block: sum y^2 - (sum y)^2 / len; sum over blocks exactly with
                  Fractions, then p * q^(-1) mod.
    ICPC-UZ:      2023 L (the query part of the statement is NOT VERIFIED).
    Example:
        >>> isotonic_sse_mod([1, 3, 2, 4])
        499122177
        >>> 499122177 * 2 % 998244353
        1
    """
    # NOT VERIFIED: условие 2023 L (какие запросы) не сверено, реализована только подгонка
    total = Fraction(0)
    for l, r, mean in pav(y):
        for i in range(l, r):
            total += (y[i] - mean) ** 2  # точная дробь
    return total.numerator % mod * pow(total.denominator, -1, mod) % mod
