"""Suffix array, LCP (Kasai), suffix automaton, inverse suffix array, Burrows-Wheeler transform.

Суффиксные структуры.
"""

from __future__ import annotations

from rustinpy._registry import algo


@algo(tags=["strings", "suffix-array", "doubling"], cses=["- (suffix array)"])
def suffix_array(s: str) -> list[int]:
    """Suffix array by prefix doubling with C-level sorts.   # Суффиксный массив.

    When to use:  substring order problems, LCP-based counting, many-pattern search.
    Complexity:   O(n log^2 n) comparisons inside sorted() (fast in practice)
    Returns:      sa: start indices of suffixes in lexicographic order.
    Python speed: n = 10^5 ~ 0.2 s, n = 10^6 ~ 4-5 s.
    Related:      lcp_kasai, SuffixAutomaton.
    CSES:         - (suffix array; used by Distinct Substrings, Repeating Substring)
    Example:
        >>> suffix_array("banana")
        [5, 3, 1, 0, 4, 2]
    """
    n = len(s)
    alpha = {c: i for i, c in enumerate(sorted(set(s)))}
    rank = [alpha[c] for c in s]  # ранги < n, иначе упаковка ключа ниже сломается
    sa = list(range(n))
    k = 1
    while True:
        # ключ = (ранг первой половины, ранг второй половины), упакованный в одно число
        key = [rank[i] * (n + 2) + (rank[i + k] + 1 if i + k < n else 0) for i in range(n)]
        sa.sort(key=key.__getitem__)
        new = [0] * n
        for j in range(1, n):
            new[sa[j]] = new[sa[j - 1]] + (key[sa[j]] != key[sa[j - 1]])
        rank = new
        if n == 0 or rank[sa[-1]] == n - 1:  # все ранги различны
            return sa
        k *= 2


@algo(
    tags=["strings", "lcp", "kasai"], cses=["Distinct Substrings (2105)"], requires=["suffix_array"]
)
def lcp_kasai(s: str, sa: list[int]) -> list[int]:
    """LCP array: lcp[i] = lcp(sa[i-1], sa[i]), lcp[0] = 0.   # Массив LCP (Касаи).

    When to use:  together with suffix_array: distinct substrings, longest repeats.
    Complexity:   O(n)
    Returns:      lcp list of length n.
    Related:      suffix_array, distinct_substrings_count.
    CSES:         Distinct Substrings (2105).
    Example:
        >>> s = "banana"
        >>> lcp_kasai(s, suffix_array(s))
        [0, 1, 3, 0, 0, 2]
    """
    n = len(s)
    rank = [0] * n
    for i, p in enumerate(sa):
        rank[p] = i
    lcp = [0] * n
    h = 0
    for i in range(n):  # суффиксы в порядке позиций: h уменьшается не больше чем на 1
        if rank[i]:
            j = sa[rank[i] - 1]
            while i + h < n and j + h < n and s[i + h] == s[j + h]:
                h += 1
            lcp[rank[i]] = h
            if h:
                h -= 1
        else:
            h = 0
    return lcp


@algo(
    tags=["strings", "suffix-array", "counting"],
    cses=["Distinct Substrings (2105)"],
    requires=["suffix_array", "lcp_kasai"],
)
def distinct_substrings_count(s: str) -> int:
    """Number of distinct non-empty substrings.   # Число различных подстрок.

    When to use:  n(n+1)/2 minus the sum of LCP.
    Complexity:   O(n log^2 n)
    Returns:      count.
    Related:      SuffixAutomaton.distinct_count.
    CSES:         Distinct Substrings (2105).
    Example:
        >>> distinct_substrings_count("abaa")
        8
    """
    n = len(s)
    return n * (n + 1) // 2 - sum(lcp_kasai(s, suffix_array(s)))  # каждый повтор считался в LCP


@algo(
    tags=["strings", "suffix-automaton"],
    cses=[
        "Distinct Substrings (2105)",
        "Substring Order I (2108)",
        "Substring Order II (2109)",
        "Repeating Substring (2106)",
        "Substring Distribution (2110)",
    ],
)
class SuffixAutomaton:
    """Suffix automaton with occurrence counts and k-th substring queries.   # Суффиксный автомат.

    When to use:  everything about the set of substrings of one string.
    Complexity:   O(n * |alphabet|) build (dict transitions), queries O(answer length * sigma)
    Methods:      distinct_count(); kth_distinct(k) (Substring Order I, k 1-based);
                  kth_with_repeats(k) (Substring Order II); longest_repeat();
                  length_distribution() -> list for lengths 1..n; occurrences(t)
    Python speed: n = 10^5 builds in ~0.2 s.
    Related:      suffix_array, distinct_substrings_count.
    CSES:         Distinct Substrings (2105), Substring Order I (2108), Substring Order II (2109),
                  Repeating Substring (2106), Substring Distribution (2110).
    Example:
        >>> sa = SuffixAutomaton("babaa")
        >>> sa.distinct_count(), sa.kth_distinct(3), sa.kth_with_repeats(3), sa.longest_repeat()
        (11, 'ab', 'a', 'ba')
        >>> sa.length_distribution(), sa.occurrences("ba")
        ([2, 3, 3, 2, 1], 2)
    """

    def __init__(self, s: str) -> None:
        self.s = s
        self.nxt: list[dict[str, int]] = [{}]
        self.link = [-1]
        self.length = [0]
        self.firstpos = [-1]
        self.is_clone = [False]
        last = 0
        for i, ch in enumerate(s):
            cur = len(self.nxt)
            self.nxt.append({})
            self.link.append(-1)
            self.length.append(self.length[last] + 1)
            self.firstpos.append(i)
            self.is_clone.append(False)
            p = last
            while p != -1 and ch not in self.nxt[p]:
                self.nxt[p][ch] = cur  # добавляем переход по ch из суффиксов last
                p = self.link[p]
            if p == -1:
                self.link[cur] = 0
            else:
                q = self.nxt[p][ch]
                if self.length[p] + 1 == self.length[q]:
                    self.link[cur] = q
                else:
                    clone = len(self.nxt)  # расщепляем состояние q
                    self.nxt.append(dict(self.nxt[q]))
                    self.link.append(self.link[q])
                    self.length.append(self.length[p] + 1)
                    self.firstpos.append(self.firstpos[q])
                    self.is_clone.append(True)
                    while p != -1 and self.nxt[p].get(ch) == q:
                        self.nxt[p][ch] = clone
                        p = self.link[p]
                    self.link[q] = self.link[cur] = clone
            last = cur
        # порядок по убыванию длины - для динамики «снизу вверх»
        self.order = sorted(range(len(self.nxt)), key=self.length.__getitem__, reverse=True)
        occ = [0 if c else 1 for c in self.is_clone]
        occ[0] = 0
        for v in self.order:
            if self.link[v] > 0:
                occ[self.link[v]] += occ[v]
        self.occ = occ
        self._dist: list[int] | None = None
        self._total: list[int] | None = None

    def distinct_count(self) -> int:
        return sum(self.length[v] - self.length[self.link[v]] for v in range(1, len(self.nxt)))

    def _paths(self) -> list[int]:
        if self._dist is None:
            d = [0] * len(self.nxt)  # число различных непустых строк, читаемых из v
            for v in self.order:
                d[v] = sum(1 + d[u] for u in self.nxt[v].values())
            self._dist = d
        return self._dist

    def kth_distinct(self, k: int) -> str:
        d = self._paths()
        v, res = 0, []
        while k > 0:
            for ch in sorted(self.nxt[v]):
                u = self.nxt[v][ch]
                if k <= 1 + d[u]:
                    res.append(ch)
                    k -= 1  # сама строка res
                    v = u
                    break
                k -= 1 + d[u]
            else:
                raise IndexError("k is larger than the number of distinct substrings")
        return "".join(res)

    def kth_with_repeats(self, k: int) -> str:
        if self._total is None:
            t = [0] * len(self.nxt)  # сумма вхождений всех строк, читаемых из v
            for v in self.order:
                t[v] = sum(self.occ[u] + t[u] for u in self.nxt[v].values())
            self._total = t
        t = self._total
        v, res = 0, []
        while k > 0:
            for ch in sorted(self.nxt[v]):
                u = self.nxt[v][ch]
                if k <= self.occ[u] + t[u]:
                    res.append(ch)
                    k -= self.occ[u]  # строка res встречается occ[u] раз
                    v = u
                    break
                k -= self.occ[u] + t[u]
            else:
                raise IndexError("k is larger than the number of substrings")
        return "".join(res)

    def longest_repeat(self) -> str:
        best = 0
        for v in range(1, len(self.nxt)):
            if self.occ[v] >= 2 and self.length[v] > self.length[best]:
                best = v
        if best == 0:
            return ""
        end = self.firstpos[best]
        return self.s[end - self.length[best] + 1 : end + 1]

    def length_distribution(self) -> list[int]:
        n = len(self.s)
        diff = [0] * (n + 2)
        for v in range(1, len(self.nxt)):  # состояние даёт длины (len(link), len(v)]
            diff[self.length[self.link[v]] + 1] += 1
            diff[self.length[v] + 1] -= 1
        res = []
        cur = 0
        for L in range(1, n + 1):
            cur += diff[L]
            res.append(cur)
        return res

    def occurrences(self, t: str) -> int:
        v = 0
        for ch in t:
            if ch not in self.nxt[v]:
                return 0
            v = self.nxt[v][ch]
        return self.occ[v] if t else len(self.s) + 1


@algo(
    tags=["strings", "suffix-array", "construction"],
    cses=["- (inverse suffix array)"],
    verified=False,
)
def inverse_suffix_array(sa: list[int], alphabet: str = "abcdefghijklmnopqrstuvwxyz") -> str | None:
    """Smallest string with the given suffix array.   # Строка по суффиксному массиву.

    When to use:  construct a string from its suffix array.
    Complexity:   O(n)
    Returns:      the string, or None if sa is not a permutation / needs too many letters.
    Idea:         s[sa[i+1]] > s[sa[i]] is forced iff rank(sa[i] + 1) > rank(sa[i+1] + 1)
                  (the empty suffix has rank -1); otherwise keep the same letter.
    CSES:         - (inverse suffix array; exact CSES statement NOT VERIFIED)
    Example:
        >>> inverse_suffix_array([5, 3, 1, 0, 4, 2])
        'bacaca'
    """
    # NOT VERIFIED: формат задачи CSES (алфавит, вывод) не сверен
    n = len(sa)
    if sorted(sa) != list(range(n)):
        return None
    rank = [0] * (n + 1)
    rank[n] = -1  # пустой суффикс меньше всех
    for i, p in enumerate(sa):
        rank[p] = i
    letters = [0] * n
    cur = 0
    for i in range(n - 1):
        a, b = sa[i], sa[i + 1]
        if rank[a + 1] > rank[b + 1]:
            cur += 1  # иначе суффикс a не был бы меньше
        letters[b] = cur
    if cur >= len(alphabet):
        return None
    return "".join(alphabet[x] for x in letters)


@algo(tags=["strings", "bwt", "burrows-wheeler"], cses=["String Transform (1113)"])
def bwt(s: str) -> str:
    """Burrows-Wheeler transform of s + '#'.   # Преобразование Барроуза-Уилера.

    When to use:  compression tasks; inverse is CSES String Transform.
    Complexity:   O(n log^2 n) via sorted rotations of the doubled string
    Returns:      last column of the sorted rotations of s + '#'.
    Related:      inverse_bwt, suffix_array.
    CSES:         String Transform (1113) (asks for inverse_bwt).
    Example:
        >>> bwt("abaab")
        'bba#aa'
    """
    t = s + "#"
    n = len(t)
    order = sorted(range(n), key=lambda i: t[i:] + t[:i])  # все циклические сдвиги
    return "".join(t[(i - 1) % n] for i in order)


@algo(tags=["strings", "bwt", "burrows-wheeler"], cses=["String Transform (1113)"])
def inverse_bwt(t: str) -> str:
    """Recover s from the Burrows-Wheeler transform of s + '#'.   # Обратное преобразование BWT.

    When to use:  CSES String Transform.
    Complexity:   O(n log n)
    Returns:      original string (without '#').
    Idea:         stable sort of the last column gives the first column; follow the
                  LF-mapping starting from the row that begins with '#'.
    Related:      bwt.
    CSES:         String Transform (1113).
    Example:
        >>> inverse_bwt("bba#aa")
        'abaab'
    """
    n = len(t)
    nxt = sorted(range(n), key=lambda i: (t[i], i))  # i-я строка первого столбца -> позиция в t
    res = []
    row = 0  # строка, начинающаяся с '#'
    for _ in range(n - 1):
        row = nxt[row]  # следующий циклический сдвиг (начинается на символ позже)
        res.append(t[nxt[row]])  # первый символ строки row
    return "".join(res)
