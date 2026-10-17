"""Trie, word combinations and Aho-Corasick automaton.

Бор и алгоритм Ахо-Корасик.
"""

from __future__ import annotations

from collections import deque

from rustinpy._registry import algo

MOD7 = 10**9 + 7


@algo(tags=["strings", "trie", "prefix"], cses=["Word Combinations (1731)"])
class Trie:
    """Prefix tree of words.   # Бор (префиксное дерево).

    When to use:  prefix queries, dictionary walks in DP.
    Complexity:   O(|word|) per operation
    Methods:      insert(word); contains(word); count_prefix(p) -> number of inserted words
                  starting with p (with multiplicity)
    Related:      word_combinations, AhoCorasick.
    CSES:         Word Combinations (1731).
    Example:
        >>> t = Trie()
        >>> for w in ["ab", "abc", "b"]: t.insert(w)
        >>> t.contains("ab"), t.contains("a"), t.count_prefix("ab"), t.count_prefix("")
        (True, False, 2, 3)
    """

    def __init__(self) -> None:
        self.nxt: list[dict[str, int]] = [{}]
        self.end = [0]  # сколько слов заканчивается в узле
        self.passing = [0]  # сколько слов проходит через узел

    def insert(self, word: str) -> None:
        v = 0
        self.passing[0] += 1
        for ch in word:
            u = self.nxt[v].get(ch)
            if u is None:
                u = len(self.nxt)  # новый узел
                self.nxt[v][ch] = u
                self.nxt.append({})
                self.end.append(0)
                self.passing.append(0)
            v = u
            self.passing[v] += 1
        self.end[v] += 1

    def _walk(self, s: str) -> int:
        v = 0
        for ch in s:
            u = self.nxt[v].get(ch)
            if u is None:
                return -1
            v = u
        return v

    def contains(self, word: str) -> bool:
        v = self._walk(word)
        return v >= 0 and self.end[v] > 0

    def count_prefix(self, p: str) -> int:
        v = self._walk(p)
        return self.passing[v] if v >= 0 else 0


@algo(
    tags=["strings", "trie", "dp", "counting"], cses=["Word Combinations (1731)"], requires=["MOD7"]
)
def word_combinations(s: str, words: list[str], mod: int = MOD7) -> int:
    """Ways to write s as a concatenation of dictionary words.   # Комбинации слов.

    When to use:  dp over positions with a trie walk from each position.
    Complexity:   O(|s| * max word length)
    Returns:      count mod mod.
    Related:      Trie, AhoCorasick.
    CSES:         Word Combinations (1731).
    Example:
        >>> word_combinations("ababc", ["ab", "abab", "c", "cb"])
        2
    """
    nxt: list[dict[str, int]] = [{}]
    end = [False]
    for w in words:
        v = 0
        for ch in w:
            if ch not in nxt[v]:
                nxt[v][ch] = len(nxt)
                nxt.append({})
                end.append(False)
            v = nxt[v][ch]
        end[v] = True
    n = len(s)
    dp = [0] * (n + 1)
    dp[n] = 1  # dp[i] - способов разбить суффикс s[i:]
    for i in range(n - 1, -1, -1):
        v, total = 0, 0
        for j in range(i, n):  # идём по бору, пока совпадает
            u = nxt[v].get(s[j])
            if u is None:
                break
            v = u
            if end[v]:
                total += dp[j + 1]
        dp[i] = total % mod
    return dp[0]


@algo(
    tags=["strings", "aho-corasick", "matching", "automaton"],
    cses=["Finding Patterns (2102)", "Counting Patterns (2103)", "Pattern Positions (2104)"],
)
class AhoCorasick:
    """Aho-Corasick automaton for many patterns at once.   # Ахо-Корасик.

    When to use:  search many patterns in one text; DP over the automaton.
    Complexity:   O(sum |patterns| + |text|) (+ alphabet in dict transitions)
    Methods:      count(text) -> occurrences of every pattern (overlaps counted);
                  first_pos(text) -> first start index of every pattern or -1
    Pitfalls:     equal patterns share a node - both get the same answers.
    Related:      kmp_find_all (one pattern), Trie.
    CSES:         Finding Patterns (2102), Counting Patterns (2103), Pattern Positions (2104).
    Example:
        >>> ac = AhoCorasick(["a", "ab", "bab", "c"])
        >>> ac.count("abab"), ac.first_pos("abab")
        ([2, 2, 1, 0], [0, 0, 1, -1])
    """

    def __init__(self, patterns: list[str]) -> None:
        nxt: list[dict[str, int]] = [{}]
        self.term: list[int] = []  # узел, где кончается i-й образец
        for p in patterns:
            v = 0
            for ch in p:
                if ch not in nxt[v]:
                    nxt[v][ch] = len(nxt)
                    nxt.append({})
                v = nxt[v][ch]
            self.term.append(v)
        self.lens = [len(p) for p in patterns]
        fail = [0] * len(nxt)
        order = []
        q = deque(nxt[0].values())
        while q:  # BFS: суффиксные ссылки по уровням
            v = q.popleft()
            order.append(v)
            for ch, u in nxt[v].items():
                f = fail[v]
                while f and ch not in nxt[f]:
                    f = fail[f]
                fail[u] = nxt[f].get(ch, 0) if nxt[f].get(ch, 0) != u else 0
                q.append(u)
        self.nxt, self.fail, self.order = nxt, fail, order

    def _states(self, text: str) -> list[int]:
        nxt, fail = self.nxt, self.fail
        v = 0
        res = []
        for ch in text:
            while v and ch not in nxt[v]:
                v = fail[v]  # откат по суффиксным ссылкам
            v = nxt[v].get(ch, 0)
            res.append(v)
        return res

    def count(self, text: str) -> list[int]:
        hits = [0] * len(self.nxt)
        for v in self._states(text):
            hits[v] += 1
        for v in reversed(self.order):  # проталкиваем по дереву ссылок к корню
            hits[self.fail[v]] += hits[v]
        return [hits[t] if t else 0 for t in self.term]

    def first_pos(self, text: str) -> list[int]:
        inf = len(text) + 1
        first = [inf] * len(self.nxt)  # самый ранний конец вхождения в узле
        for i, v in enumerate(self._states(text)):
            if first[v] == inf:
                first[v] = i
        for v in reversed(self.order):
            f = self.fail[v]
            if first[v] < first[f]:
                first[f] = first[v]
        return [
            first[t] - L + 1 if t and first[t] < inf else -1 for t, L in zip(self.term, self.lens)
        ]
