"""strings: brute-force comparisons on small random strings (AC-05, AC-06)."""

from __future__ import annotations

import itertools
import random

import pytest

from rustinpy.strings import (
    AhoCorasick,
    PalindromeQueries,
    StringHash,
    StringHashDouble,
    SuffixAutomaton,
    Trie,
    apostrophe_number,
    borders,
    brands,
    bwt,
    distinct_subsequences,
    distinct_substrings_count,
    inverse_bwt,
    inverse_suffix_array,
    kmp_find_all,
    lcp_kasai,
    longest_palindrome,
    longest_palindrome_ending_at,
    lyndon_factorization,
    manacher,
    min_rotation,
    periods,
    prefix_function,
    required_substring,
    shortest_non_subsequence,
    string_functions,
    suffix_array,
    word_combinations,
    z_function,
)


def rs(rng: random.Random, n: int, alpha: str = "ab") -> str:
    return "".join(rng.choice(alpha) for _ in range(n))


def is_pal(t: str) -> bool:
    return t == t[::-1]


def test_prefix_functions_vs_naive(rng: random.Random) -> None:
    for _ in range(300):
        s = rs(rng, rng.randint(0, 12), "abc"[: rng.randint(1, 3)])
        n = len(s)
        z = z_function(s)
        for i in range(n):
            k = 0
            while i + k < n and s[k] == s[i + k]:
                k += 1
            assert z[i] == k
        pi = prefix_function(s)
        for i in range(n):
            t = s[: i + 1]
            assert pi[i] == max(k for k in range(i + 1) if t[:k] == t[i + 1 - k :])
        pat = rs(rng, rng.randint(0, 3), "abc"[: rng.randint(1, 3)])
        assert kmp_find_all(s, pat) == [
            i for i in range(n - len(pat) + 1) if s[i : i + len(pat)] == pat
        ]
        assert borders(s) == [k for k in range(1, n) if s[:k] == s[n - k :]]
        assert periods(s) == [
            p for p in range(1, n + 1) if all(s[i] == s[i + p] for i in range(n - p))
        ]
        if s:
            i = min_rotation(s)
            rots = [s[j:] + s[:j] for j in range(n)]
            assert s[i:] + s[:i] == min(rots) and i == rots.index(min(rots))
        words = lyndon_factorization(s)
        assert "".join(words) == s
        assert all(w < w[j:] + w[:j] for w in words for j in range(1, len(w)))
        assert all(words[i] >= words[i + 1] for i in range(len(words) - 1))


def test_required_substring_vs_brute(rng: random.Random) -> None:
    for _ in range(60):
        n = rng.randint(0, 7)
        pat = rs(rng, rng.randint(1, 3), "AB")
        cnt = sum(1 for t in itertools.product("AB", repeat=n) if pat in "".join(t))
        assert required_substring(n, pat, alphabet="AB") == cnt
    assert required_substring(2, "A") == 26 * 26 - 25 * 25


def test_hashes_and_palindrome_queries(rng: random.Random) -> None:
    for _ in range(100):
        s = rs(rng, rng.randint(1, 15))
        h = StringHash(s)
        d = StringHashDouble(s)
        for _ in range(30):
            l1 = rng.randrange(len(s) + 1)
            r1 = rng.randint(l1, len(s))
            l2 = rng.randrange(len(s) + 1)
            r2 = rng.randint(l2, len(s))
            same = s[l1:r1] == s[l2:r2]
            assert h.equal(l1, r1, l2, r2) == same
            if r1 - l1 == r2 - l2:
                assert (d.get(l1, r1) == d.get(l2, r2)) == same
        pq = PalindromeQueries(s)
        cur = list(s)
        for _ in range(30):
            if rng.random() < 0.4:
                i, c = rng.randrange(len(s)), rng.choice("ab")
                pq.set_char(i, c)
                cur[i] = c
            l = rng.randrange(len(s))
            r = rng.randint(l + 1, len(s))
            assert pq.is_palindrome(l, r) == is_pal("".join(cur[l:r]))


def count_overlapping(text: str, pat: str) -> int:
    return sum(1 for i in range(len(text) - len(pat) + 1) if text.startswith(pat, i))


def test_trie_and_aho_corasick(rng: random.Random) -> None:
    for _ in range(150):
        words = [rs(rng, rng.randint(1, 4)) for _ in range(rng.randint(1, 6))]
        t = Trie()
        for w in words:
            t.insert(w)
        for _ in range(10):
            q = rs(rng, rng.randint(0, 4))
            assert t.contains(q) == (q in words)
            assert t.count_prefix(q) == sum(1 for w in words if w.startswith(q))
        s = rs(rng, rng.randint(0, 10))
        uniq = sorted(set(words))
        ways = [0] * (len(s) + 1)
        ways[0] = 1
        for i in range(len(s)):
            for w in uniq:
                if ways[i] and s.startswith(w, i):
                    ways[i + len(w)] += ways[i]
        assert word_combinations(s, words) == ways[len(s)]
        ac = AhoCorasick(words)
        text = rs(rng, rng.randint(0, 20))
        assert ac.count(text) == [count_overlapping(text, w) for w in words]
        assert ac.first_pos(text) == [text.find(w) for w in words]


def test_suffix_array_lcp_distinct(rng: random.Random) -> None:
    for _ in range(200):
        s = rs(rng, rng.randint(0, 15), "abc"[: rng.randint(1, 3)])
        sa = suffix_array(s)
        assert sa == sorted(range(len(s)), key=lambda i: s[i:])
        lcp = lcp_kasai(s, sa)
        for i in range(1, len(s)):
            a, b = s[sa[i - 1] :], s[sa[i] :]
            k = 0
            while k < min(len(a), len(b)) and a[k] == b[k]:
                k += 1
            assert lcp[i] == k
        subs = {s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)}
        assert distinct_substrings_count(s) == len(subs)
    big = rs(rng, 3000, "ab")
    assert suffix_array(big) == sorted(range(3000), key=lambda i: big[i:])


def test_suffix_automaton_vs_sets(rng: random.Random) -> None:
    for _ in range(150):
        s = rs(rng, rng.randint(1, 12), "abc"[: rng.randint(1, 3)])
        sam = SuffixAutomaton(s)
        allsub = [s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)]
        distinct = sorted(set(allsub))
        assert sam.distinct_count() == len(distinct)
        for k in range(1, len(distinct) + 1):
            assert sam.kth_distinct(k) == distinct[k - 1]
        with_rep = sorted(allsub)
        for k in range(1, len(with_rep) + 1):
            assert sam.kth_with_repeats(k) == with_rep[k - 1]
        rep = sam.longest_repeat()
        best = max((len(t) for t in distinct if count_overlapping(s, t) >= 2), default=0)
        assert len(rep) == best and (not rep or count_overlapping(s, rep) >= 2)
        assert sam.length_distribution() == [
            sum(1 for t in distinct if len(t) == L) for L in range(1, len(s) + 1)
        ]
        q = rs(rng, rng.randint(1, 3), "abc")
        assert sam.occurrences(q) == count_overlapping(s, q)
    with pytest.raises(IndexError):
        SuffixAutomaton("ab").kth_distinct(4)


def test_inverse_suffix_array_and_bwt(rng: random.Random) -> None:
    for _ in range(150):
        n = rng.randint(1, 6)
        s = rs(rng, n, "abc")
        sa = suffix_array(s)
        got = inverse_suffix_array(sa)
        assert got is not None and suffix_array(got) == sa
        best = min(
            "".join(t)
            for t in itertools.product("abcdef"[:n], repeat=n)
            if suffix_array("".join(t)) == sa
        )
        assert got == best
        assert inverse_bwt(bwt(s)) == s
        t = s + "#"
        rot = sorted(t[i:] + t[:i] for i in range(len(t)))
        assert bwt(s) == "".join(r[-1] for r in rot)
    assert inverse_suffix_array([0, 0]) is None


def test_palindromes_vs_naive(rng: random.Random) -> None:
    for _ in range(200):
        s = rs(rng, rng.randint(0, 14), "abc"[: rng.randint(1, 3)])
        n = len(s)
        d1, d2 = manacher(s)
        for i in range(n):
            assert d1[i] == max(
                k
                for k in range(1, n + 1)
                if i - k + 1 >= 0 and i + k <= n and is_pal(s[i - k + 1 : i + k])
            )
            assert d2[i] == max(
                k for k in range(0, n + 1) if i - k >= 0 and i + k <= n and is_pal(s[i - k : i + k])
            )
        lp = longest_palindrome(s)
        assert is_pal(lp) and lp in s
        assert len(lp) == max(
            (j - i for i in range(n) for j in range(i + 1, n + 1) if is_pal(s[i:j])), default=0
        )
        assert longest_palindrome_ending_at(s) == [
            max(j + 1 - i for i in range(j + 1) if is_pal(s[i : j + 1])) for j in range(n)
        ]


def test_subsequence_problems(rng: random.Random) -> None:
    for _ in range(150):
        s = rs(rng, rng.randint(0, 9), "abc")
        subs = {"".join(c) for k in range(1, len(s) + 1) for c in itertools.combinations(s, k)}
        assert distinct_subsequences(s) == len(subs)
        t = rs(rng, rng.randint(0, 12), "ACGT")
        ans = shortest_non_subsequence(t)

        def is_sub(x: str, y: str) -> bool:
            it = iter(y)
            return all(c in it for c in x)

        assert not is_sub(ans, t)
        L = len(ans)
        assert all(is_sub("".join(p), t) for p in itertools.product("ACGT", repeat=L - 1))


def test_brands_properties(rng: random.Random) -> None:
    v = "aeiou"
    for _ in range(200):
        s = rs(rng, rng.randint(0, 8), "abeoz")
        r = brands(s)
        assert all((x in v) != (y in v) for x, y in zip(r, r[1:]))
        extra = sum(1 for x, y in zip(s, s[1:]) if (x in v) == (y in v))
        assert len(r) == len(s) + extra
        it = iter(r)
        assert all(c in it for c in s)


def test_string_stubs_raise() -> None:
    with pytest.raises(NotImplementedError):
        apostrophe_number("1")
    with pytest.raises(NotImplementedError):
        string_functions([1])
