"""Polynomial multiplication: decimal packing (fastest in CPython), NTT, complex FFT.

Умножение многочленов (свёртка).
"""

from __future__ import annotations

import cmath
import decimal

from rustinpy._registry import algo

MOD = 998244353


@algo(
    tags=["ntt", "fft", "polynomial"], cses=["- (convolution modulo 998244353)"], requires=["MOD"]
)
def ntt(a: list[int], invert: bool, mod: int = MOD) -> None:
    """In-place number theoretic transform (iterative).   # Быстрое преобразование (NTT).

    When to use:  building block of convolution_ntt; template to port to C++ / PyPy.
    Complexity:   O(n log n), len(a) must be a power of two
    Input:        mod = c * 2^k + 1 with primitive root 3: 998244353, 469762049, 167772161.
    Returns:      None; a is replaced by its transform (inverse transform if invert).
    Pitfalls:     10^9 + 7 is NOT an NTT prime -> use convolution (any modulus).
    Python speed: n = 2^18 ~ 1.5-2 s per transform; in CPython convolution() is ~8x faster.
    Related:      convolution_ntt, convolution, fft_convolution_float.
    CSES:         - (convolution modulo 998244353)
    Example:
        >>> a = [1, 2, 3, 0]
        >>> ntt(a, False); ntt(a, True); a
        [1, 2, 3, 0]
    """
    n = len(a)
    j = 0
    for i in range(1, n):  # бит-реверсная перестановка
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        w = pow(3, (mod - 1) // length, mod)  # корень степени length из 1
        if invert:
            w = pow(w, mod - 2, mod)
        half = length // 2
        ws = [1] * half
        for k in range(1, half):
            ws[k] = ws[k - 1] * w % mod
        for i in range(0, n, length):
            lo = a[i : i + half]
            hi = [x * y % mod for x, y in zip(a[i + half : i + length], ws)]
            a[i : i + half] = [(x + y) % mod for x, y in zip(lo, hi)]  # бабочки блоком
            a[i + half : i + length] = [(x - y) % mod for x, y in zip(lo, hi)]
        length <<= 1
    if invert:
        inv_n = pow(n, mod - 2, mod)
        a[:] = [x * inv_n % mod for x in a]


@algo(
    tags=["ntt", "convolution", "polynomial"],
    cses=["- (polynomial product)"],
    requires=["MOD", "ntt"],
)
def convolution_ntt(a: list[int], b: list[int], mod: int = MOD) -> list[int]:
    """c[k] = sum a[i] * b[k - i] modulo an NTT prime, via ntt().   # Свёртка через NTT.

    When to use:  the classic NTT convolution (to port to C++ / run under PyPy).
    Complexity:   O((n + m) log(n + m)); naive for short inputs
    Returns:      list of length len(a) + len(b) - 1 ([] if one is empty).
    Python speed: 2 * 10^5 terms ~ 14 s in CPython -> use convolution() (decimal, ~2 s).
    Related:      ntt, convolution, convolution_int.
    CSES:         - (polynomial product)
    Example:
        >>> convolution_ntt([1, 2, 3], [4, 5])
        [4, 13, 22, 15]
    """
    if not a or not b:
        return []
    n_res = len(a) + len(b) - 1
    if min(len(a), len(b)) <= 32:  # короткие - наивно быстрее
        res = [0] * n_res
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    res[i + j] += x * y
        return [x % mod for x in res]
    size = 1
    while size < n_res:
        size <<= 1
    fa = [x % mod for x in a] + [0] * (size - len(a))
    fb = [x % mod for x in b] + [0] * (size - len(b))
    ntt(fa, False, mod)
    ntt(fb, False, mod)
    fc = [x * y % mod for x, y in zip(fa, fb)]  # поточечное произведение
    ntt(fc, True, mod)
    return fc[:n_res]


@algo(tags=["convolution", "decimal", "polynomial"], cses=["- (exact convolution)"])
def convolution_int(a: list[int], b: list[int]) -> list[int]:
    """Exact convolution of NON-NEGATIVE ints via one decimal product.   # Точная свёртка.

    When to use:  exact polynomial products in CPython; the fastest pure-Python way.
    Complexity:   O(N log N) inside libmpdec (it multiplies huge numbers with an NTT in C)
    Returns:      exact c of length len(a) + len(b) - 1.
    Pitfalls:     negative numbers are not supported - shift them first.   # только >= 0
    Python speed: 2 * 10^5 x 2 * 10^5 values < 10^9: ~2 s (pure NTT 14 s, big int 16 s).
    Idea:         write a and b as decimal strings with w digits per coefficient
                  (w > digits of the largest result cell), multiply two Decimals with
                  precision MAX_PREC, cut the product back into w-digit cells.
    Related:      convolution (mod), convolution_ntt, fft_convolution_float.
    CSES:         - (exact convolution)
    Example:
        >>> convolution_int([1, 2, 3], [4, 5])
        [4, 13, 22, 15]
        >>> convolution_int([10**12], [10**12])
        [1000000000000000000000000]
    """
    if not a or not b:
        return []
    bound = max(a) * max(b) * min(len(a), len(b))  # максимум одной ячейки
    w = len(str(bound)) + 1  # десятичных цифр на коэффициент
    fmt = f"0{w}d"
    A = decimal.Decimal("".join(format(x, fmt) for x in reversed(a)))
    B = decimal.Decimal("".join(format(x, fmt) for x in reversed(b)))
    ctx = decimal.Context(prec=decimal.MAX_PREC, Emax=decimal.MAX_EMAX)
    n_res = len(a) + len(b) - 1
    s = str(ctx.multiply(A, B)).rjust(n_res * w, "0")  # умножение в C (libmpdec)
    L = len(s)
    return [int(s[L - (i + 1) * w : L - i * w]) for i in range(n_res)]  # режем на ячейки


@algo(
    tags=["convolution", "decimal", "polynomial", "modular"],
    cses=["- (polynomial product modulo any m)"],
    requires=["MOD", "convolution_int"],
)
def convolution(a: list[int], b: list[int], mod: int = MOD) -> list[int]:
    """c[k] = sum a[i] * b[k - i] modulo ANY modulus.   # Свёртка по модулю.

    When to use:  polynomial multiplication, counting sums of pairs, any mod (10^9 + 7 too).
    Complexity:   one exact convolution of values < mod, then % mod
    Returns:      list of length len(a) + len(b) - 1 ([] if one is empty).
    Python speed: 2 * 10^5 x 2 * 10^5 ~ 2 s in CPython.
    Related:      convolution_int, convolution_ntt, bits.xor_convolution.
    CSES:         - (polynomial product modulo any m)
    Example:
        >>> convolution([1, 2, 3], [4, 5])
        [4, 13, 22, 15]
        >>> convolution([10**9, 1], [10**9, 1], 10**9 + 7)
        [49, 999999993, 1]
    """
    if not a or not b:
        return []
    if min(len(a), len(b)) <= 32:  # короткие - наивно быстрее
        res = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    res[i + j] += x * y
        return [x % mod for x in res]
    exact = convolution_int([x % mod for x in a], [x % mod for x in b])
    return [x % mod for x in exact]


@algo(tags=["fft", "convolution", "polynomial", "float"], cses=["- (real-valued convolution)"])
def fft_convolution_float(a: list[float], b: list[float]) -> list[float]:
    """Convolution of real sequences via complex FFT.   # Свёртка вещественных чисел.

    When to use:  probabilities / real weights; for integers prefer convolution_int (exact).
    Complexity:   O(n log n)
    Returns:      list of floats of length len(a) + len(b) - 1.
    Pitfalls:     rounding error ~ 1e-9 * max|c|; never round big integer results from it.
    Related:      convolution, convolution_int.
    CSES:         - (real-valued convolution)
    Example:
        >>> [round(x, 6) for x in fft_convolution_float([0.5, 0.5], [0.5, 0.5])]
        [0.25, 0.5, 0.25]
    """
    if not a or not b:
        return []
    n_res = len(a) + len(b) - 1
    size = 1
    while size < n_res:
        size <<= 1

    def fft(x: list[complex], invert: bool) -> None:
        n = len(x)
        j = 0
        for i in range(1, n):
            bit = n >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j ^= bit
            if i < j:
                x[i], x[j] = x[j], x[i]  # бит-реверс
        length = 2
        while length <= n:
            ang = (2 if invert else -2) * cmath.pi / length
            half = length // 2
            ws = [cmath.exp(1j * ang * k) for k in range(half)]  # корни из единицы
            for i in range(0, n, length):
                lo = x[i : i + half]
                hi = [p * q for p, q in zip(x[i + half : i + length], ws)]
                x[i : i + half] = [p + q for p, q in zip(lo, hi)]
                x[i + half : i + length] = [p - q for p, q in zip(lo, hi)]
            length <<= 1

    fa = [complex(v) for v in a] + [0j] * (size - len(a))
    fb = [complex(v) for v in b] + [0j] * (size - len(b))
    fft(fa, False)
    fft(fb, False)
    fc = [p * q for p, q in zip(fa, fb)]  # свёртка = поточечное произведение
    fft(fc, True)
    return [v.real / size for v in fc[:n_res]]
