"""Modular arithmetic: power, extended gcd, inverse, CRT.

Модульная арифметика.
"""

from __future__ import annotations

from rustinpy._registry import algo

MOD = 998244353
MOD7 = 10**9 + 7


@algo(tags=["modular", "power"], cses=["Exponentiation (1095)"], requires=["MOD"])
def modpow(a: int, e: int, mod: int = MOD) -> int:
    """a^e mod m by binary exponentiation.   # Быстрое возведение в степень по модулю.

    When to use:  a^e mod m; in Python the built-in pow(a, e, mod) is the same and faster.
    Complexity:   O(log e)
    Returns:      a^e mod m in [0, mod); 0^0 = 1.
    Pitfalls:     e < 0 is not supported -> modinv(a, mod) first.   # отрицательная степень
    Related:      modinv, mat_pow, exp_tower.
    CSES:         Exponentiation (1095).
    Example:
        >>> modpow(2, 10, 1000)
        24
        >>> modpow(0, 0, 7), modpow(3, 200, 1)
        (1, 0)
    """
    result = 1 % mod
    a %= mod
    while e > 0:
        if e & 1:  # младший бит степени -> домножаем ответ
            result = result * a % mod
        a = a * a % mod  # квадрат основания
        e >>= 1
    return result


@algo(tags=["modular", "gcd"], cses=["- (building block for modinv, crt)"])
def ext_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Extended Euclid: g = gcd(a, b) = a*x + b*y.   # Расширенный алгоритм Евклида.

    When to use:  modular inverse for any modulus, linear Diophantine equations, CRT.
    Complexity:   O(log min(a, b))
    Returns:      (g, x, y) with a*x + b*y == g >= 0.
    Pitfalls:     iterative on purpose: no recursion depth problems.
    Related:      modinv, crt.
    CSES:         - (building block for modinv, crt)
    Example:
        >>> g, x, y = ext_gcd(240, 46)
        >>> g, 240 * x + 46 * y
        (2, 2)
    """
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r  # шаг Евклида
        old_x, x = x, old_x - q * x  # те же операции над коэффициентами
        old_y, y = y, old_y - q * y
    if old_r < 0:
        old_r, old_x, old_y = -old_r, -old_x, -old_y
    return old_r, old_x, old_y


@algo(tags=["modular", "inverse"], cses=["- (everywhere)"], requires=["MOD", "ext_gcd"])
def modinv(a: int, mod: int = MOD) -> int:
    """Inverse of a modulo mod (mod need not be prime).   # Обратный элемент по модулю.

    When to use:  division modulo m; works for composite m when gcd(a, m) = 1.
    Complexity:   O(log m)
    Returns:      x in [0, mod) with a*x = 1 (mod m).
    Pitfalls:     gcd(a, m) != 1 -> ValueError (e.g. modulus 2112025 = 5^2 * 84481 in
                  ICPC-UZ 2025 B: multiples of 5 have no inverse).   # нет обратного
    Related:      ext_gcd, pow(a, -1, mod) (Python 3.8+), Comb.
    CSES:         - (everywhere)
    Example:
        >>> modinv(3, 7)
        5
        >>> modinv(10, 2112025)
        Traceback (most recent call last):
        ValueError: 10 has no inverse modulo 2112025
    """
    g, x, _ = ext_gcd(a % mod, mod)
    if g != 1:
        raise ValueError(f"{a} has no inverse modulo {mod}")
    return x % mod


@algo(tags=["modular", "crt"], cses=["- (number theory)"], requires=["ext_gcd"])
def crt(rems: list[int], mods: list[int]) -> tuple[int, int] | None:
    """Chinese remainder theorem, moduli not necessarily coprime.   # КТО для любых модулей.

    When to use:  x = r_i (mod m_i) for all i; combining answers modulo prime powers.
    Complexity:   O(k log M)
    Returns:      (x, lcm) with 0 <= x < lcm, or None if the system is inconsistent.
    Pitfalls:     lcm can be huge - Python ints handle it, but keep it in mind for speed.
    Related:      ext_gcd, nCr_composite.
    CSES:         - (number theory)
    Example:
        >>> crt([2, 3, 2], [3, 5, 7])
        (23, 105)
        >>> crt([1, 2], [4, 6]) is None
        True
    """
    x, m = 0, 1
    for r, mi in zip(rems, mods):
        g, p, _ = ext_gcd(m, mi)
        diff = r - x
        if diff % g != 0:
            return None  # противоречивая система
        # x + m * t = r (mod mi)  ->  t = diff / g * p (mod mi / g)
        step = mi // g
        t = diff // g * p % step
        x += m * t
        m *= step
        x %= m
    return x, m


@algo(tags=["modular", "power", "fermat"], cses=["Exponentiation II (1712)"], requires=["MOD7"])
def exp_tower(a: int, b: int, c: int, mod: int = MOD7) -> int:
    """a^(b^c) mod p for PRIME p via Fermat.   # Степень степени по простому модулю.

    When to use:  towers of exponents modulo a prime.
    Complexity:   O(log b + log c + log p)
    Returns:      a^(b^c) mod p, with 0^0 = 1.
    Pitfalls:     reduce the exponent modulo p - 1 only when a % p != 0.   # теорема Ферма
    Related:      modpow.
    CSES:         Exponentiation II (1712).
    Example:
        >>> exp_tower(3, 7, 1)
        2187
        >>> exp_tower(2, 3, 2), exp_tower(0, 0, 5), exp_tower(0, 5, 0)
        (512, 1, 0)
    """
    if a % mod == 0:
        exponent_is_zero = b == 0 and c > 0  # b^c = 0 только при b = 0, c > 0
        return 1 if exponent_is_zero else 0
    return pow(a, pow(b, c, mod - 1), mod)
