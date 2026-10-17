"""Polynomial multiplication: NTT, big-int packing, complex FFT.

Умножение многочленов (свёртка).
"""

from __future__ import annotations

import cmath

from rustinpy._registry import algo

MOD = 998244353


@algo(
    tags=["ntt", "fft", "polynomial"], cses=["- (convolution modulo 998244353)"], requires=["MOD"]
)
def ntt(a: list[int], invert: bool, mod: int = MOD) -> None:
    """In-place number theoretic transform (iterative).   # Быстрое преобразование (NTT).

    When to use:  building block of convolution modulo an NTT prime.
    Complexity:   O(n log n), len(a) must be a power of two
    Input:        mod = c * 2^k + 1 with primitive root 3: 998244353, 469762049, 167772161.
    Returns:      None; a is replaced by its transform (inverse transform if invert).
    Pitfalls:     10^9 + 7 is NOT an NTT prime -> use convolution_int (exact) instead.
    Python speed: n = 2^18 about 1.5 s; for exact integer products convolution_int is faster.
    Related:      convolution, convolution_int, fft_convolution_float.
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
def convolution(a: list[int], b: list[int], mod: int = MOD) -> list[int]:
    """c[k] = sum a[i] * b[k - i] modulo an NTT prime.   # Свёртка по модулю.

    When to use:  polynomial multiplication, counting sums of pairs, modulo 998244353.
    Complexity:   O((n + m) log(n + m)); naive for short inputs
    Returns:      list of length len(a) + len(b) - 1 ([] if one is empty).
    Python speed: 2 * 10^5 terms ~ 3 s in CPython; convolution_int then % mod is often faster.
    Related:      ntt, convolution_int, bits.xor_convolution.
    CSES:         - (polynomial product)
    Example:
        >>> convolution([1, 2, 3], [4, 5])
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


@algo(tags=["convolution", "big-int", "polynomial"], cses=["- (exact convolution)"])
def convolution_int(a: list[int], b: list[int]) -> list[int]:
    """Exact convolution of NON-NEGATIVE ints via one big-int product.   # Свёртка через big int.

    When to use:  exact products / any modulus (take % mod after); often the fastest
                  convolution in CPython because big-int multiply is done in C.
    Complexity:   one multiplication of numbers with (n + m) * w bits
    Returns:      exact c of length len(a) + len(b) - 1.
    Pitfalls:     negative numbers are not supported - shift them first.   # только >= 0
    Related:      convolution, fft_convolution_float.
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
    nbytes = max(1, (bound.bit_length() + 8) // 8)
    A = int.from_bytes(b"".join(x.to_bytes(nbytes, "little") for x in a), "little")
    B = int.from_bytes(b"".join(x.to_bytes(nbytes, "little") for x in b), "little")
    n_res = len(a) + len(b) - 1
    raw = (A * B).to_bytes(n_res * nbytes, "little")  # ячейки не перекрываются
    return [int.from_bytes(raw[i * nbytes : (i + 1) * nbytes], "little") for i in range(n_res)]


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
