"""Polynomial string hashing (mod 2^61 - 1 and double) and palindrome queries with updates.

Полиномиальные хеши строк.
"""

from __future__ import annotations

import random

from rustinpy._registry import algo

M61 = (1 << 61) - 1


@algo(
    tags=["strings", "hashing", "polynomial-hash"],
    cses=["- (substring comparison)"],
    requires=["M61"],
)
class StringHash:
    """Polynomial hash modulo 2^61 - 1 with a random base.   # Хеш строки по модулю 2^61-1.

    When to use:  compare substrings in O(1), find repeats, binary search + hash.
    Complexity:   O(n) build, O(1) per get
    Methods:      get(l, r) -> hash of s[l:r]; equal(l1, r1, l2, r2)
    Pitfalls:     the base is random per instance: compare hashes only within ONE object
                  (or pass the same base=). Anti-hash tests cannot target a random base.
    Related:      StringHashDouble, PalindromeQueries, suffix_array.
    CSES:         - (substring comparison)
    Example:
        >>> h = StringHash("abcabc")
        >>> h.get(0, 3) == h.get(3, 6), h.equal(0, 2, 1, 3)
        (True, False)
    """

    def __init__(self, s: str, base: int | None = None) -> None:
        self.base = base if base is not None else random.randrange(10**5, M61 - 1)
        n = len(s)
        h = [0] * (n + 1)
        p = [1] * (n + 1)
        b = self.base
        for i, ch in enumerate(s):
            h[i + 1] = (h[i] * b + ord(ch)) % M61  # схема Горнера
            p[i + 1] = p[i] * b % M61
        self.h, self.p = h, p

    def get(self, l: int, r: int) -> int:
        return (self.h[r] - self.h[l] * self.p[r - l]) % M61

    def equal(self, l1: int, r1: int, l2: int, r2: int) -> bool:
        return r1 - l1 == r2 - l2 and self.get(l1, r1) == self.get(l2, r2)


@algo(tags=["strings", "hashing", "double-hash"], cses=["- (substring comparison)"])
class StringHashDouble:
    """Double polynomial hash (mods 10^9 + 7 and 998244353).   # Двойной хеш.

    When to use:  when 2^61 - 1 arithmetic is unwanted (e.g. porting to C++ with 64-bit ints).
    Complexity:   O(n) build, O(1) per get
    Methods:      get(l, r) -> (h1, h2) of s[l:r]
    Related:      StringHash.
    CSES:         - (substring comparison)
    Example:
        >>> h = StringHashDouble("abab")
        >>> h.get(0, 2) == h.get(2, 4), h.get(0, 1) == h.get(1, 2)
        (True, False)
    """

    def __init__(self, s: str, base: int | None = None) -> None:
        self.m1, self.m2 = 10**9 + 7, 998244353
        b = base if base is not None else random.randrange(1000, 10**9)
        n = len(s)
        self.h1 = [0] * (n + 1)
        self.h2 = [0] * (n + 1)
        self.p1 = [1] * (n + 1)
        self.p2 = [1] * (n + 1)
        for i, ch in enumerate(s):
            c = ord(ch)
            self.h1[i + 1] = (self.h1[i] * b + c) % self.m1  # два независимых модуля
            self.h2[i + 1] = (self.h2[i] * b + c) % self.m2
            self.p1[i + 1] = self.p1[i] * b % self.m1
            self.p2[i + 1] = self.p2[i] * b % self.m2

    def get(self, l: int, r: int) -> tuple[int, int]:
        x = (self.h1[r] - self.h1[l] * self.p1[r - l]) % self.m1
        y = (self.h2[r] - self.h2[l] * self.p2[r - l]) % self.m2
        return x, y


@algo(
    tags=["strings", "hashing", "fenwick", "palindrome"],
    cses=["Palindrome Queries (2420)"],
    requires=["M61"],
)
class PalindromeQueries:
    """Character updates + "is s[l:r] a palindrome?".   # Запросы палиндромов.

    When to use:  palindrome checks on a changing string.
    Complexity:   O(n log n) build, O(log n) per operation
    Methods:      set_char(i, c); is_palindrome(l, r) for the half-open s[l:r]
    Idea:         forward hash sum c_i B^i and backward sum c_i B^(n-1-i); compare after
                  aligning the powers: F(l, r) * B^(n-r) == R(l, r) * B^l.
    Related:      StringHash, manacher (static string).
    CSES:         Palindrome Queries (2420).
    Example:
        >>> pq = PalindromeQueries("aybabtu")
        >>> pq.is_palindrome(1, 4), pq.is_palindrome(0, 3)
        (False, False)
        >>> pq.is_palindrome(2, 5), pq.set_char(4, "a"), pq.is_palindrome(2, 5)
        (True, None, False)
    """

    def __init__(self, s: str, base: int | None = None) -> None:
        n = len(s)
        self.n = n
        self.b = base if base is not None else random.randrange(10**5, M61 - 1)
        self.pw = [1] * (n + 1)
        for i in range(n):
            self.pw[i + 1] = self.pw[i] * self.b % M61
        self.s = list(s)
        self.fw = [0] * (n + 1)  # Фенвик прямого хеша
        self.bw = [0] * (n + 1)  # Фенвик обратного хеша
        for i, ch in enumerate(s):
            self._add(i, ord(ch))

    def _add(self, i: int, c: int) -> None:
        df = c * self.pw[i] % M61
        db = c * self.pw[self.n - 1 - i] % M61
        j = i + 1
        while j <= self.n:
            self.fw[j] = (self.fw[j] + df) % M61
            self.bw[j] = (self.bw[j] + db) % M61
            j += j & -j

    def _pref(self, t: list[int], i: int) -> int:
        s = 0
        while i > 0:
            s += t[i]
            i -= i & -i
        return s % M61

    def set_char(self, i: int, c: str) -> None:
        self._add(i, (ord(c) - ord(self.s[i])) % M61)  # добавляем разницу символов
        self.s[i] = c

    def is_palindrome(self, l: int, r: int) -> bool:
        f = (self._pref(self.fw, r) - self._pref(self.fw, l)) % M61
        b = (self._pref(self.bw, r) - self._pref(self.bw, l)) % M61
        return f * self.pw[self.n - r] % M61 == b * self.pw[l] % M61  # выравниваем степени
