"""Bitwise tricks: popcount, xor trie, linear basis over GF(2), SOS DP, Walsh-Hadamard transforms.

Битовые операции.
"""

from __future__ import annotations

from rustinpy._registry import algo

MOD7 = 10**9 + 7


@algo(tags=["bits", "popcount"], cses=["- (popcount)"])
def popcount(x: int) -> int:
    """Number of set bits of x >= 0 (works on Python 3.9).   # Число единичных битов.

    When to use:  everywhere; the int method bit_count exists only since Python 3.10.
    Complexity:   O(bits) in C
    Returns:      popcount.
    Related:      counting_bits_total.
    CSES:         - (popcount)
    Example:
        >>> popcount(0), popcount(255), popcount(2**100 + 1)
        (0, 8, 2)
    """
    return bin(x).count("1")  # bit_count() - только с 3.10


@algo(tags=["bits", "counting", "digits"], cses=["Counting Bits (1146)"])
def counting_bits_total(n: int) -> int:
    """Total number of ones in binary representations of 1..n.   # Подсчёт битов.

    When to use:  n up to 10^15: count per bit position.
    Complexity:   O(log n)
    Returns:      sum of popcount(i) for i = 1..n.
    Idea:         bit k is set in blocks of 2^k inside every 2^(k+1) numbers of 0..n.
    CSES:         Counting Bits (1146).
    Example:
        >>> counting_bits_total(7), counting_bits_total(10)
        (12, 17)
    """
    total = 0
    k = 0
    while (1 << k) <= n:
        period = 1 << (k + 1)
        full, rest = divmod(n + 1, period)  # полные периоды и остаток среди 0..n
        total += full * (1 << k) + max(0, rest - (1 << k))
        k += 1
    return total


@algo(tags=["bits", "xor", "trie"], cses=["Maximum Xor Subarray (1655)"])
class XorTrie:
    """Binary trie over fixed-width numbers: max / min xor with a query.   # Xor-бор.

    When to use:  "max a_i xor x" over a growing set; maximum xor subarray via prefix xors.
    Complexity:   O(B) per operation, B = bits (default 31)
    Methods:      insert(x); max_xor(x); min_xor(x) (the set must be non-empty)
    Related:      max_xor_subarray, XorBasis (xor of subsets).
    CSES:         Maximum Xor Subarray (1655).
    Example:
        >>> t = XorTrie()
        >>> for v in [3, 10, 5]: t.insert(v)
        >>> t.max_xor(8), t.min_xor(8)
        (13, 2)
    """

    def __init__(self, bits: int = 31) -> None:
        self.bits = bits
        self.ch = [[0, 0]]  # узел 0 - корень, 0 в ребёнке = нет ребёнка

    def insert(self, x: int) -> None:
        v = 0
        for b in range(self.bits - 1, -1, -1):
            d = x >> b & 1
            if not self.ch[v][d]:
                self.ch[v][d] = len(self.ch)
                self.ch.append([0, 0])
            v = self.ch[v][d]

    def max_xor(self, x: int) -> int:
        v, res = 0, 0
        for b in range(self.bits - 1, -1, -1):
            d = x >> b & 1
            if self.ch[v][d ^ 1]:  # жадно идём в противоположный бит
                res |= 1 << b
                v = self.ch[v][d ^ 1]
            else:
                v = self.ch[v][d]
        return res

    def min_xor(self, x: int) -> int:
        v, res = 0, 0
        for b in range(self.bits - 1, -1, -1):
            d = x >> b & 1
            if self.ch[v][d]:
                v = self.ch[v][d]
            else:
                res |= 1 << b
                v = self.ch[v][d ^ 1]
        return res


@algo(
    tags=["bits", "xor", "trie", "prefix"],
    cses=["Maximum Xor Subarray (1655)"],
    requires=["XorTrie"],
)
def max_xor_subarray(a: list[int]) -> int:
    """Maximum xor of a non-empty subarray.   # Максимальный xor подмассива.

    When to use:  xor of a[l:r] = p[r] ^ p[l]: maximise over pairs with a trie.
    Complexity:   O(n * B)
    Returns:      maximal subarray xor.
    Related:      XorTrie.
    CSES:         Maximum Xor Subarray (1655).
    Example:
        >>> max_xor_subarray([5, 1, 5, 9])
        13
    """
    bits = max(1, max(a, default=0).bit_length())
    t = XorTrie(bits)
    t.insert(0)
    best, p = 0, 0
    for x in a:
        p ^= x  # префиксный xor
        best = max(best, t.max_xor(p))
        t.insert(p)
    return best


@algo(
    tags=["bits", "xor-basis", "gf2", "linear-algebra"],
    cses=["Maximum Xor Subset (3191)", "Number of Subset Xors (3211)"],
)
class XorBasis:
    """Linear basis over GF(2) (Gaussian elimination on bits).   # Линейный базис (xor-базис).

    When to use:  xors of subsets: maximum, k-th, count, representability.
    Complexity:   O(B) per insert / query, B = bits
    Methods:      insert(x) -> bool (False if x was already representable); can_make(x);
                  max_xor(); kth_smallest(k) (0-based among DISTINCT values, 0 included);
                  rank; size() = number of distinct subset xors = 2^rank
    Related:      max_xor_subset, number_of_subset_xors, k_subset_xors.
    CSES:         Maximum Xor Subset (3191), Number of Subset Xors (3211).
    Example:
        >>> b = XorBasis()
        >>> [b.insert(x) for x in [1, 3, 2]]
        [True, True, False]
        >>> b.max_xor(), b.size(), [b.kth_smallest(k) for k in range(4)], b.can_make(5)
        (3, 4, [0, 1, 2, 3], False)
    """

    def __init__(self, bits: int = 64) -> None:
        self.bits = bits
        self.basis = [0] * bits  # basis[b] - вектор со старшим битом b
        self.rank = 0

    def insert(self, x: int) -> bool:
        for b in range(self.bits - 1, -1, -1):
            if not x >> b & 1:
                continue
            if not self.basis[b]:
                self.basis[b] = x
                self.rank += 1
                return True
            x ^= self.basis[b]  # исключаем старший бит
        return False

    def can_make(self, x: int) -> bool:
        for b in range(self.bits - 1, -1, -1):
            if x >> b & 1 and self.basis[b]:
                x ^= self.basis[b]
        return x == 0

    def max_xor(self) -> int:
        res = 0
        for b in range(self.bits - 1, -1, -1):
            if (res ^ self.basis[b]) > res:
                res ^= self.basis[b]
        return res

    def _reduced(self) -> list[int]:
        """Basis in reduced row echelon form, sorted by leading bit ascending."""
        vec = list(self.basis)
        for b in range(self.bits):
            if vec[b]:
                for c in range(b + 1, self.bits):
                    if vec[c] >> b & 1:
                        vec[c] ^= vec[b]  # каждый старший бит - только в своём векторе
        return [v for v in vec if v]

    def kth_smallest(self, k: int) -> int:
        red = self._reduced()
        if k >= 1 << len(red):
            raise IndexError("k is out of range")
        res = 0
        for i, v in enumerate(red):  # биты k выбирают векторы приведённого базиса
            if k >> i & 1:
                res ^= v
        return res

    def size(self) -> int:
        return 1 << self.rank


@algo(tags=["bits", "xor-basis"], cses=["Maximum Xor Subset (3191)"], requires=["XorBasis"])
def max_xor_subset(a: list[int]) -> int:
    """Maximum xor of a subset (empty subset gives 0).   # Максимальный xor подмножества.

    When to use:  basis + greedy from the top bit.
    Complexity:   O(n * B)
    Returns:      maximal subset xor.
    Related:      XorBasis.
    CSES:         Maximum Xor Subset (3191).
    Example:
        >>> max_xor_subset([2, 6, 4, 1])
        7
    """
    b = XorBasis(max(1, max(a, default=0).bit_length()))
    for x in a:
        b.insert(x)
    return b.max_xor()


@algo(
    tags=["bits", "xor-basis", "counting"],
    cses=["Number of Subset Xors (3211)"],
    requires=["XorBasis"],
)
def number_of_subset_xors(a: list[int]) -> int:
    """How many DISTINCT subset xors exist (0 included).   # Число различных xor подмножеств.

    When to use:  answer is 2^rank of the xor basis.
    Complexity:   O(n * B)
    Returns:      2^rank.
    Related:      XorBasis.
    CSES:         Number of Subset Xors (3211).
    Example:
        >>> number_of_subset_xors([3, 5, 6])
        4
    """
    b = XorBasis(max(1, max(a, default=0).bit_length()))
    for x in a:
        b.insert(x)
    return b.size()


@algo(
    tags=["bits", "xor-basis", "kth"],
    cses=["K Subset Xors (3192)"],
    requires=["XorBasis"],
    verified=False,
)
def k_subset_xors(a: list[int], k: int) -> list[int]:
    """The k smallest xors over all 2^n subsets.   # k наименьших xor подмножеств.

    When to use:  each distinct subset xor appears exactly 2^(n - rank) times.
    Complexity:   O(n * B + k * B)
    Returns:      sorted list of the k smallest values (with repetitions).
    Idea:         reduced basis: the i-th distinct value is the xor of vectors chosen by the
                  bits of i; repeat each 2^(n - rank) times.
    Related:      XorBasis.kth_smallest.
    CSES:         K Subset Xors (3192) (exact statement NOT VERIFIED).
    Example:
        >>> k_subset_xors([3, 5, 6], 6)
        [0, 0, 3, 3, 5, 5]
    """
    # NOT VERIFIED: формат задачи CSES (с повторами или без) не сверен
    b = XorBasis(max(1, max(a, default=0).bit_length()))
    for x in a:
        b.insert(x)
    red = b._reduced()
    rep = 1 << (len(a) - b.rank)  # кратность каждого значения
    res: list[int] = []
    i = 0
    while len(res) < k and i < 1 << len(red):
        v = 0
        for j, vec in enumerate(red):
            if i >> j & 1:
                v ^= vec
        res.extend([v] * min(rep, k - len(res)))
        i += 1
    return res


@algo(
    tags=["bits", "xor", "fwht", "prefix"],
    cses=["All Subarray Xors (3233)"],
    requires=["fwht_xor"],
    verified=False,
)
def all_subarray_xors(a: list[int]) -> list[int]:
    """All distinct values of xor over non-empty subarrays.   # Все xor подмассивов.

    When to use:  values are small (< 2^17 or so): xor of a[l:r] = p[l] ^ p[r].
    Complexity:   O(V log V + n), V = next power of two above max value
    Returns:      sorted distinct values.
    Idea:         cnt = indicator of prefix xors; FWHT-xor self-convolution counts pairs
                  (p_i, p_j) with given xor; the value 0 needs a pair i != j.
    CSES:         All Subarray Xors (3233) (exact statement NOT VERIFIED).
    Example:
        >>> all_subarray_xors([1, 2, 3])
        [0, 1, 2, 3]
    """
    # NOT VERIFIED: формат задачи CSES не сверен
    V = 1
    while V <= max(a, default=0):
        V <<= 1
    cnt = [0] * V
    p = 0
    cnt[0] = 1
    for x in a:
        p ^= x
        cnt[p] += 1  # частоты префиксных xor
    f = list(cnt)
    fwht_xor(f, False)
    f = [x * x for x in f]
    fwht_xor(f, True)
    zero_pairs = sum(c * c for c in cnt) - sum(cnt)  # упорядоченные пары i != j с одинаковым p
    res = [v for v in range(1, V) if f[v]]
    return ([0] if zero_pairs else []) + res


@algo(tags=["bits", "lucas", "parity", "pyramid"], cses=["Xor Pyramid Peak (3194)"])
def xor_pyramid_peak(a: list[int]) -> int:
    """Top of the xor pyramid built from the bottom row a.   # Вершина xor-пирамиды.

    When to use:  "each cell is xor of the two below": the top is xor of a[i] with C(n-1, i) odd.
    Complexity:   O(n)
    Returns:      the top value.
    Idea:         Lucas mod 2: C(n-1, i) is odd iff (i & (n - 1)) == i.
    CSES:         Xor Pyramid Peak (3194).
    Example:
        >>> xor_pyramid_peak([2, 10, 5, 12, 9])  # 2 ^ 9
        11
    """
    m = len(a) - 1
    res = 0
    for i, x in enumerate(a):
        if i & m == i:  # нечётный биномиальный коэффициент
            res ^= x
    return res


@algo(tags=["bits", "sos-dp", "subsets"], cses=["SOS Bit Problem (1654)"])
def sos_subset_sum(f: list[int], bits: int) -> list[int]:
    """g[mask] = sum of f over all submasks of mask (zeta transform).   # SOS DP по подмножествам.

    When to use:  "sum / count over all submasks" for every mask at once.
    Complexity:   O(bits * 2^bits)
    Returns:      new list g of length 2^bits.
    Related:      sos_superset_sum, sos_bit_problem, fwht_or.
    CSES:         SOS Bit Problem (1654).
    Example:
        >>> sos_subset_sum([1, 2, 3, 4], 2)
        [1, 3, 4, 10]
    """
    g = list(f)
    for b in range(bits):
        step = 1 << b
        for mask in range(1 << bits):
            if mask & step:
                g[mask] += g[mask ^ step]  # добавляем подмаски без бита b
    return g


@algo(tags=["bits", "sos-dp", "supersets"], cses=["SOS Bit Problem (1654)"])
def sos_superset_sum(f: list[int], bits: int) -> list[int]:
    """g[mask] = sum of f[sup] over all supermasks sup of mask.   # SOS DP по надмножествам.

    When to use:  "how many numbers contain all bits of mask".
    Complexity:   O(bits * 2^bits)
    Returns:      new list g.
    Related:      sos_subset_sum, and_subset_count.
    CSES:         SOS Bit Problem (1654).
    Example:
        >>> sos_superset_sum([1, 2, 3, 4], 2)
        [10, 6, 7, 4]
    """
    g = list(f)
    for b in range(bits):
        step = 1 << b
        for mask in range(1 << bits):
            if not mask & step:
                g[mask] += g[mask | step]  # добавляем надмаски с битом b
    return g


@algo(
    tags=["bits", "sos-dp"],
    cses=["SOS Bit Problem (1654)"],
    requires=["sos_subset_sum", "sos_superset_sum"],
)
def sos_bit_problem(a: list[int]) -> list[tuple[int, int, int]]:
    """For each x: #y with x|y == x, #y with x&y == x, #y with x&y != 0.   # Задача SOS Bit Problem.

    When to use:  the classic SOS DP trio.
    Complexity:   O(n + B 2^B), B = bit length of max(a)
    Returns:      list of triples in input order.
    Idea:         x|y == x: y is a submask of x; x&y == x: y is a supermask;
                  x&y != 0 = n - #(y submask of ~x).
    Related:      sos_subset_sum, sos_superset_sum.
    CSES:         SOS Bit Problem (1654).
    Example:
        >>> sos_bit_problem([3, 7, 2, 9, 2])
        [(3, 2, 5), (4, 1, 5), (2, 4, 4), (1, 1, 3), (2, 4, 4)]
    """
    B = max(1, max(a, default=0).bit_length())
    full = (1 << B) - 1
    cnt = [0] * (1 << B)
    for x in a:
        cnt[x] += 1
    sub = sos_subset_sum(cnt, B)
    sup = sos_superset_sum(cnt, B)
    n = len(a)
    return [(sub[x], sup[x], n - sub[full ^ x]) for x in a]  # дополнение - не пересекается


@algo(
    tags=["bits", "sos-dp", "inclusion-exclusion", "counting"],
    cses=["And Subset Count (3141)"],
    requires=["MOD7", "sos_superset_sum"],
)
def and_subset_count(a: list[int], mod: int = MOD7) -> list[int]:
    """For every x: non-empty subsets whose AND equals x.   # Подмножества с данным AND.

    When to use:  AND-statistics over all subsets.
    Complexity:   O(n + B 2^B)
    Returns:      list of counts mod mod, index = AND value (B = bit length of max(a)).
    Idea:         subsets whose AND contains x: 2^(#supersets of x) - 1; Mobius over supersets.
    Related:      sos_superset_sum.
    CSES:         And Subset Count (3141).
    Example:
        >>> and_subset_count([1, 3, 2])
        [2, 2, 2, 1]
    """
    B = max(1, max(a, default=0).bit_length())
    cnt = [0] * (1 << B)
    for x in a:
        cnt[x] += 1
    sup = sos_superset_sum(cnt, B)
    g = [(pow(2, c, mod) - 1) % mod for c in sup]  # AND содержит все биты маски
    for b in range(B):  # обратное преобразование по надмножествам
        step = 1 << b
        for mask in range(1 << B):
            if not mask & step:
                g[mask] = (g[mask] - g[mask | step]) % mod
    return g


@algo(tags=["bits", "hamming", "popcount"], cses=["Hamming Distance (2136)"], requires=["popcount"])
def min_hamming_distance(words: list[int]) -> int:
    """Minimum Hamming distance between two bit strings (as ints).   # Расстояние Хэмминга.

    When to use:  n bit strings of length k <= 30; equal strings give 0 at once.
    Complexity:   O(n^2) popcounts
    Returns:      minimal distance over pairs (needs at least two words).
    Python speed: n = 2 * 10^4 is 2 * 10^8 pairs - far too slow; n <= ~3000 in CPython.
    Related:      popcount.
    CSES:         Hamming Distance (2136) (convert strings with int(s, 2)).
    Example:
        >>> min_hamming_distance([0b00111, 0b01101, 0b11001, 0b00101])  # 00111 и 00101
        1
    """
    if len(set(words)) < len(words):
        return 0  # одинаковые слова
    best = 1 << 60
    for i in range(len(words)):
        wi = words[i]
        for j in range(i + 1, len(words)):
            d = bin(wi ^ words[j]).count("1")
            if d < best:
                best = d
    return best


@algo(tags=["bits", "fwht", "xor-convolution"], cses=["- (xor convolution)"], icpc=["2025 K"])
def fwht_xor(a: list[int], invert: bool, mod: int | None = None) -> None:
    """In-place Walsh-Hadamard transform for XOR convolution.   # Преобразование Уолша-Адамара.

    When to use:  c[k] = sum_{i ^ j = k} a[i] b[j] for len = 2^B.
    Complexity:   O(N log N), N = len(a) (power of two)
    Returns:      None; a is transformed (inverse divides by N, modular if mod is given).
    Pitfalls:     inverse with mod needs N invertible (odd modulus or prime != 2).
    Related:      xor_convolution, fwht_and, fwht_or.
    CSES:         - (xor convolution)
    ICPC-UZ:      2025 K (xor of subsets with values <= 511).
    Example:
        >>> a = [1, 2, 3, 4]
        >>> fwht_xor(a, False); a
        [10, -2, -4, 0]
        >>> fwht_xor(a, True); a
        [1, 2, 3, 4]
    """
    n = len(a)
    h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                x, y = a[j], a[j + h]
                a[j], a[j + h] = x + y, x - y  # бабочка: сумма и разность
        h *= 2
    if mod is not None:
        for i in range(n):
            a[i] %= mod
    if invert:
        if mod is None:
            for i in range(n):
                a[i] //= n
        else:
            inv = pow(n, -1, mod)
            for i in range(n):
                a[i] = a[i] * inv % mod


@algo(tags=["bits", "fwht", "and-convolution"], cses=["- (and convolution)"])
def fwht_and(a: list[int], invert: bool) -> None:
    """In-place transform for AND convolution (superset sums).   # Преобразование для AND-свёртки.

    When to use:  c[k] = sum_{i & j = k} a[i] b[j].
    Complexity:   O(N log N)
    Returns:      None.
    Related:      and_convolution, sos_superset_sum.
    CSES:         - (and convolution)
    Example:
        >>> a = [1, 2, 3, 4]
        >>> fwht_and(a, False); a
        [10, 6, 7, 4]
    """
    n = len(a)
    h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                if invert:
                    a[j] -= a[j + h]
                else:
                    a[j] += a[j + h]  # к маске без бита прибавляем маску с битом
        h *= 2


@algo(tags=["bits", "fwht", "or-convolution"], cses=["- (or convolution)"])
def fwht_or(a: list[int], invert: bool) -> None:
    """In-place transform for OR convolution (subset sums).   # Преобразование для OR-свёртки.

    When to use:  c[k] = sum_{i | j = k} a[i] b[j].
    Complexity:   O(N log N)
    Returns:      None.
    Related:      or_convolution, sos_subset_sum.
    CSES:         - (or convolution)
    Example:
        >>> a = [1, 2, 3, 4]
        >>> fwht_or(a, False); a
        [1, 3, 4, 10]
    """
    n = len(a)
    h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                if invert:
                    a[j + h] -= a[j]
                else:
                    a[j + h] += a[j]  # к маске с битом прибавляем маску без бита
        h *= 2


@algo(tags=["bits", "fwht", "xor-convolution"], cses=["- (xor convolution)"], requires=["fwht_xor"])
def xor_convolution(a: list[int], b: list[int], mod: int | None = None) -> list[int]:
    """c[k] = sum over i ^ j = k of a[i] * b[j] (lengths padded to a power of two).   # Xor-свёртка.

    When to use:  combine distributions under xor.
    Complexity:   O(N log N)
    Returns:      list of length N (power of two >= max(len(a), len(b))).
    Related:      fwht_xor, and_convolution, or_convolution.
    CSES:         - (xor convolution)
    Example:
        >>> xor_convolution([1, 1], [0, 1])
        [1, 1]
    """
    n = 1
    while n < max(len(a), len(b)):
        n <<= 1
    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))
    fwht_xor(fa, False, mod)
    fwht_xor(fb, False, mod)
    fc = [x * y for x, y in zip(fa, fb)]  # поточечно в пространстве Уолша
    fwht_xor(fc, True, mod)
    return fc


@algo(tags=["bits", "fwht", "and-convolution"], cses=["- (and convolution)"], requires=["fwht_and"])
def and_convolution(a: list[int], b: list[int]) -> list[int]:
    """c[k] = sum over i & j = k of a[i] * b[j].   # AND-свёртка.

    When to use:  combine distributions under bitwise and.
    Complexity:   O(N log N)
    Returns:      list of length N (power of two).
    Related:      fwht_and.
    CSES:         - (and convolution)
    Example:
        >>> and_convolution([1, 1], [1, 1])
        [3, 1]
    """
    n = 1
    while n < max(len(a), len(b)):
        n <<= 1
    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))
    fwht_and(fa, False)
    fwht_and(fb, False)
    fc = [x * y for x, y in zip(fa, fb)]  # поточечное произведение
    fwht_and(fc, True)
    return fc


@algo(tags=["bits", "fwht", "or-convolution"], cses=["- (or convolution)"], requires=["fwht_or"])
def or_convolution(a: list[int], b: list[int]) -> list[int]:
    """c[k] = sum over i | j = k of a[i] * b[j].   # OR-свёртка.

    When to use:  combine distributions under bitwise or.
    Complexity:   O(N log N)
    Returns:      list of length N (power of two).
    Related:      fwht_or.
    CSES:         - (or convolution)
    Example:
        >>> or_convolution([1, 1], [1, 1])
        [1, 3]
    """
    n = 1
    while n < max(len(a), len(b)):
        n <<= 1
    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))
    fwht_or(fa, False)
    fwht_or(fb, False)
    fc = [x * y for x, y in zip(fa, fb)]  # поточечное произведение
    fwht_or(fc, True)
    return fc


@algo(tags=["bits", "xor", "dp", "subsets"], icpc=["2025 K"], verified=False)
def kenobi_skywalker(a: list[int], queries: list[tuple[int, int]]) -> list[bool]:
    """Is there a sub-multiset of exactly c elements with xor x?   # Кеноби и Скайуокер.

    When to use:  ICPC-UZ 2025 K as described by the official tutorial; small values (<= 511).
    Complexity:   O(D^2 * M + q log D), D = distinct values, M = 2^bits of max(a)
    Returns:      answers for queries (c, x).
    Python speed: D = M = 512 ~ 17 s in CPython; D = 60, M = 64 ~ 0.03 s.
    Idea:         adding two more copies of a value keeps the xor. Let U = values taken an odd
                  number of times, u = |U|: sizes u, u + 2, ..., up to
                  dp[x][u] = max sum of odd(cnt) over U + even(cnt) over the rest are all
                  reachable. dp over values; per (x, parity) merge the segments [u, dp] and
                  answer by binary search. Checked by brute force.
                  NOT VERIFIED: statement not found (limits, empty subset allowed?).
    ICPC-UZ:      2025 K "Kenobi and Skywalker".
    Example:
        >>> kenobi_skywalker([1, 2, 3, 3], [(2, 3), (3, 0), (1, 0), (4, 3)])
        [True, True, False, True]
    """
    # NOT VERIFIED: по разбору жюри, условие не найдено
    cnt: dict[int, int] = {}
    for v in a:
        cnt[v] = cnt.get(v, 0) + 1
    size = 1 << max(1, max(a, default=0).bit_length())
    d = len(cnt)
    neg = -1
    dp = [[neg] * (d + 1) for _ in range(size)]
    dp[0][0] = 0
    for v, c in cnt.items():
        ev = c - c % 2  # наибольшее чётное <= c
        od = c if c % 2 else c - 1  # наибольшее нечётное <= c
        new = []
        for x in range(size):
            row = dp[x]
            alt = dp[x ^ v]
            out = [row[u] + ev if row[u] >= 0 else neg for u in range(d + 1)]
            for u in range(1, d + 1):
                if alt[u - 1] >= 0 and alt[u - 1] + od > out[u]:
                    out[u] = alt[u - 1] + od  # v берём нечётное число раз
            new.append(out)
        dp = new
    segs: dict[tuple[int, int], tuple[list[int], list[int]]] = {}
    for x in range(size):
        for par in range(2):
            starts: list[int] = []
            ends: list[int] = []
            for u in range(par, d + 1, 2):
                e = dp[x][u]
                if e < 0:
                    continue
                if starts and u <= ends[-1] + 2:
                    ends[-1] = max(ends[-1], e)  # отрезки одной чётности сливаются
                else:
                    starts.append(u)
                    ends.append(e)
            segs[x, par] = (starts, ends)
    res = []
    for c, x in queries:
        if c < 0 or x >= size:
            res.append(False)
            continue
        starts, ends = segs[x, c % 2]
        lo, hi = 0, len(starts)
        while lo < hi:  # последний отрезок с началом <= c
            mid = (lo + hi) // 2
            if starts[mid] <= c:
                lo = mid + 1
            else:
                hi = mid
        res.append(lo > 0 and c <= ends[lo - 1])
    return res
