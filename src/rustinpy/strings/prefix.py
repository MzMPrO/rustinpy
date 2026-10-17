"""Prefix-based string algorithms: Z-function, prefix function (KMP), borders, periods,
minimal rotation, Lyndon factorization, KMP automaton DP.

Строковые алгоритмы на префиксах.
"""

from __future__ import annotations

from rustinpy._registry import algo

MOD7 = 10**9 + 7
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


@algo(tags=["strings", "z-function"], cses=["Finding Periods (1733)", "String Matching (1753)"])
def z_function(s: str) -> list[int]:
    """Z-array: z[i] = length of the longest common prefix of s and s[i:].   # Z-функция.

    When to use:  pattern matching (z of pat + '#' + text), periods, borders.
    Complexity:   O(n)
    Returns:      z with z[0] = len(s).
    Related:      prefix_function, periods.
    CSES:         Finding Periods (1733), String Matching (1753).
    Example:
        >>> z_function("aabxaab")
        [7, 1, 0, 0, 3, 1, 0]
    """
    n = len(s)
    z = [0] * n
    if n:
        z[0] = n
    l = r = 0  # самый правый найденный отрезок совпадения [l, r)
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])  # используем уже известное
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


@algo(tags=["strings", "prefix-function", "kmp"], cses=["Finding Borders (1732)"])
def prefix_function(s: str) -> list[int]:
    """pi[i] = length of the longest proper border of s[:i+1].   # Префикс-функция.

    When to use:  KMP matching, borders, period of a prefix, automaton for DP.
    Complexity:   O(n)
    Returns:      pi list.
    Related:      kmp_find_all, borders, z_function.
    CSES:         Finding Borders (1732).
    Example:
        >>> prefix_function("abacaba")
        [0, 0, 1, 0, 1, 2, 3]
    """
    pi = [0] * len(s)
    for i in range(1, len(s)):
        k = pi[i - 1]
        while k and s[i] != s[k]:
            k = pi[k - 1]  # откатываемся по цепочке границ
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


@algo(
    tags=["strings", "kmp", "matching"],
    cses=["String Matching (1753)"],
    requires=["prefix_function"],
)
def kmp_find_all(text: str, pat: str) -> list[int]:
    """All start positions of pat in text (overlaps included).   # Поиск подстроки (КМП).

    When to use:  exact pattern matching.
    Complexity:   O(|text| + |pat|)
    Returns:      sorted start indices; for an empty pattern every position 0..len(text).
    Related:      z_function, AhoCorasick (many patterns).
    CSES:         String Matching (1753) (answer = len of the list).
    Example:
        >>> kmp_find_all("saippuakauppias", "pp"), kmp_find_all("aaaa", "aa")
        ([3, 10], [0, 1, 2])
    """
    if not pat:
        return list(range(len(text) + 1))
    pi = prefix_function(pat)
    res = []
    k = 0
    m = len(pat)
    for i, ch in enumerate(text):
        while k and ch != pat[k]:
            k = pi[k - 1]
        if ch == pat[k]:
            k += 1
        if k == m:  # полное совпадение, заканчивается в i
            res.append(i - m + 1)
            k = pi[k - 1]
    return res


@algo(
    tags=["strings", "borders", "prefix-function"],
    cses=["Finding Borders (1732)"],
    requires=["prefix_function"],
)
def borders(s: str) -> list[int]:
    """Lengths of all borders (proper prefixes that are also suffixes).   # Границы строки.

    When to use:  "print all border lengths".
    Complexity:   O(n)
    Returns:      increasing list of border lengths.
    Related:      prefix_function, periods.
    CSES:         Finding Borders (1732).
    Example:
        >>> borders("abcababcab")
        [2, 5]
    """
    if not s:
        return []
    pi = prefix_function(s)
    res = []
    k = pi[-1]
    while k:  # цепочка границ последнего префикса
        res.append(k)
        k = pi[k - 1]
    return res[::-1]


@algo(
    tags=["strings", "periods", "z-function"],
    cses=["Finding Periods (1733)"],
    requires=["z_function"],
)
def periods(s: str) -> list[int]:
    """All periods p (s[i] == s[i + p] for all valid i), 1 <= p <= n.   # Периоды строки.

    When to use:  "print all period lengths" (the last one may be partial).
    Complexity:   O(n)
    Returns:      increasing list, always ends with n.
    Related:      borders (period = n - border), z_function.
    CSES:         Finding Periods (1733).
    Example:
        >>> periods("abcabca")
        [3, 6, 7]
    """
    n = len(s)
    z = z_function(s)
    return [p for p in range(1, n + 1) if p == n or z[p] == n - p]  # хвост совпал с началом


@algo(tags=["strings", "rotation", "lexicographic"], cses=["Minimal Rotation (1110)"])
def min_rotation(s: str) -> int:
    """Start index of the lexicographically smallest rotation.   # Минимальный циклический сдвиг.

    When to use:  canonical form of a cyclic string.
    Complexity:   O(n)
    Returns:      index i such that s[i:] + s[:i] is minimal (smallest such i).
    Idea:         two candidates i < j and matched length k; on mismatch the loser jumps
                  past the compared block (the "minimum expression" algorithm, like Booth).
    Related:      lyndon_factorization.
    CSES:         Minimal Rotation (1110).
    Example:
        >>> s = "acab"
        >>> i = min_rotation(s); s[i:] + s[:i]
        'abac'
    """
    n = len(s)
    i, j, k = 0, 1, 0
    while i < n and j < n and k < n:
        a, b = s[(i + k) % n], s[(j + k) % n]
        if a == b:
            k += 1
            continue
        if a > b:
            i += k + 1  # кандидат i и всё, что за ним в блоке, проигрывают
        else:
            j += k + 1
        if i == j:
            j += 1
        k = 0
    return min(i, j) if n else 0


@algo(tags=["strings", "lyndon", "duval"], cses=["- (Lyndon factorization)"])
def lyndon_factorization(s: str) -> list[str]:
    """Duval: s = w1 w2 ... wk with Lyndon words w1 >= w2 >= ... >= wk.   # Разложение Линдона.

    When to use:  minimal rotation, string combinatorics.
    Complexity:   O(n)
    Returns:      the Lyndon words in order.
    Related:      min_rotation.
    CSES:         - (Lyndon factorization)
    Example:
        >>> lyndon_factorization("abaabab")
        ['ab', 'aabab']
    """
    n = len(s)
    res = []
    i = 0
    while i < n:
        j, k = i + 1, i
        while j < n and s[k] <= s[j]:
            k = i if s[k] < s[j] else k + 1  # продолжаем текущее «предслово»
            j += 1
        while i <= k:
            res.append(s[i : i + j - k])
            i += j - k
    return res


@algo(
    tags=["strings", "kmp-automaton", "dp", "counting"],
    cses=["Required Substring (1112)"],
    requires=["MOD7", "UPPER", "prefix_function"],
)
def required_substring(n: int, pattern: str, mod: int = MOD7, alphabet: str = UPPER) -> int:
    """Number of strings of length n over alphabet containing pattern.   # Обязательная подстрока.

    When to use:  count strings with / without a forbidden substring (KMP automaton DP).
    Complexity:   O(n * m * |alphabet|)
    Returns:      count mod mod.
    Idea:         dp over automaton states 0..m-1 counts strings AVOIDING pattern;
                  answer = |alphabet|^n - avoiding.
    Related:      prefix_function, AhoCorasick (many patterns).
    CSES:         Required Substring (1112).
    Example:
        >>> required_substring(2, "A")
        51
    """
    m = len(pattern)
    pi = prefix_function(pattern)
    go = [[0] * len(alphabet) for _ in range(m)]  # переходы автомата КМП
    for st in range(m):
        for ci, ch in enumerate(alphabet):
            k = st
            while k and pattern[k] != ch:
                k = pi[k - 1]
            go[st][ci] = k + 1 if pattern[k] == ch else 0
    dp = [0] * m
    dp[0] = 1
    for _ in range(n):
        new = [0] * m
        for st, v in enumerate(dp):
            if v:
                for nxt in go[st]:
                    if nxt < m:  # состояние m - образец найден, такие не считаем
                        new[nxt] += v
        dp = [x % mod for x in new]
    return (pow(len(alphabet), n, mod) - sum(dp)) % mod
