"""Palindromes: Manacher, longest palindrome, longest palindrome ending at every position.

Палиндромы.
"""

from __future__ import annotations

from rustinpy._registry import algo


@algo(tags=["strings", "palindrome", "manacher"], cses=["Longest Palindrome (1111)"])
def manacher(s: str) -> tuple[list[int], list[int]]:
    """Manacher: radii of odd and even palindromes at every center.   # Алгоритм Манакера.

    When to use:  all palindromic substrings in linear time.
    Complexity:   O(n)
    Returns:      (d1, d2): d1[i] = number of odd palindromes centred at i (s[i-k+1:i+k] for
                  k <= d1[i]); d2[i] = number of even palindromes with right center i
                  (s[i-k:i+k] for k <= d2[i]).
    Related:      longest_palindrome, longest_palindrome_ending_at, PalindromeQueries.
    CSES:         Longest Palindrome (1111).
    Example:
        >>> manacher("abaab")
        ([1, 2, 1, 1, 1], [0, 0, 0, 2, 0])
    """
    n = len(s)
    d1 = [0] * n
    l, r = 0, -1
    for i in range(n):
        k = 1 if i > r else min(d1[l + r - i], r - i + 1)  # зеркальная позиция
        while i - k >= 0 and i + k < n and s[i - k] == s[i + k]:
            k += 1
        d1[i] = k
        if i + k - 1 > r:
            l, r = i - k + 1, i + k - 1
    d2 = [0] * n
    l, r = 0, -1
    for i in range(n):
        k = 0 if i > r else min(d2[l + r - i + 1], r - i + 1)
        while i - k - 1 >= 0 and i + k < n and s[i - k - 1] == s[i + k]:
            k += 1
        d2[i] = k
        if i + k - 1 > r:
            l, r = i - k, i + k - 1
    return d1, d2


@algo(
    tags=["strings", "palindrome", "manacher"],
    cses=["Longest Palindrome (1111)"],
    requires=["manacher"],
)
def longest_palindrome(s: str) -> str:
    """Longest palindromic substring (the leftmost one).   # Самый длинный палиндром.

    When to use:  one maximal palindrome.
    Complexity:   O(n)
    Returns:      the substring ("" for an empty string).
    Related:      manacher.
    CSES:         Longest Palindrome (1111).
    Example:
        >>> longest_palindrome("aybabtu"), longest_palindrome("abba")
        ('bab', 'abba')
    """
    d1, d2 = manacher(s)
    best_len, best_l = 0, 0
    for i in range(len(s)):
        if 2 * d1[i] - 1 > best_len:
            best_len, best_l = 2 * d1[i] - 1, i - d1[i] + 1  # нечётный
        if 2 * d2[i] > best_len:
            best_len, best_l = 2 * d2[i], i - d2[i]  # чётный
    return s[best_l : best_l + best_len]


@algo(
    tags=["strings", "palindrome", "manacher", "two-pointers"],
    cses=["All Palindromes (3138)"],
    requires=["manacher"],
)
def longest_palindrome_ending_at(s: str) -> list[int]:
    """Longest palindrome ending at every position.   # Длиннейший палиндром с концом в i.

    When to use:  per-position palindrome statistics.
    Complexity:   O(n)
    Returns:      res[j] = max length of a palindrome s[i:j+1].
    Idea:         for end j the best odd center is the smallest i <= j with i + d1[i] - 1 >= j;
                  this center only moves right as j grows -> two pointers (same for even).
    Related:      manacher.
    CSES:         All Palindromes (3138).
    Example:
        >>> longest_palindrome_ending_at("aybabtu")  # "bab" = s[2:5]
        [1, 1, 1, 1, 3, 1, 1]
    """
    n = len(s)
    d1, d2 = manacher(s)
    res = [1] * n
    c = 0
    for j in range(n):  # нечётные: центр c, правый конец c + d1[c] - 1
        while c + d1[c] - 1 < j:
            c += 1
        res[j] = max(res[j], 2 * (j - c) + 1)
    c = 0
    for j in range(n):  # чётные: правый центр c, правый конец c + d2[c] - 1
        while c <= j and c + d2[c] - 1 < j:
            c += 1
        if c <= j:
            res[j] = max(res[j], 2 * (j - c + 1))
    return res
