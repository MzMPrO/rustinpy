"""Smaller string problems: distinct subsequences, shortest non-subsequence, ICPC-UZ tasks.

Небольшие строковые задачи.
"""

from __future__ import annotations

from rustinpy._registry import algo

MOD7 = 10**9 + 7


@algo(
    tags=["strings", "subsequence", "dp", "counting"],
    cses=["Distinct Subsequences (1149)"],
    requires=["MOD7"],
)
def distinct_subsequences(s: str, mod: int = MOD7) -> int:
    """Number of distinct non-empty subsequences.   # Различные подпоследовательности.

    When to use:  count different subsequences (not positions).
    Complexity:   O(n)
    Returns:      count mod mod.
    Idea:         dp doubles with every character, minus what was counted when the same
                  character appeared last time.
    CSES:         Distinct Subsequences (1149).
    Example:
        >>> distinct_subsequences("aabac")
        19
    """
    dp = 1  # с пустой подпоследовательностью
    last: dict[str, int] = {}
    for ch in s:
        prev = dp
        dp = (2 * dp - last.get(ch, 0)) % mod  # повторы, уже кончавшиеся на ch
        last[ch] = prev
    return (dp - 1) % mod


@algo(tags=["strings", "subsequence", "greedy"], cses=["Shortest Subsequence (1087)"])
def shortest_non_subsequence(s: str, alphabet: str = "ACGT") -> str:
    """Shortest string that is NOT a subsequence of s.   # Кратчайшая не-подпоследовательность.

    When to use:  greedy blocks: each block contains every letter at least once.
    Complexity:   O(n)
    Returns:      one shortest such string.
    Idea:         cut s into blocks where all letters appear; take the letter that closes
                  each block, then a letter missing from the unfinished tail.
    CSES:         Shortest Subsequence (1087).
    Example:
        >>> shortest_non_subsequence("ACGTACGT")
        'TTA'
    """
    res = []
    seen: set[str] = set()
    for ch in s:
        if ch in alphabet:
            seen.add(ch)
            if len(seen) == len(alphabet):  # блок закрыт этим символом
                res.append(ch)
                seen = set()
    missing = next(c for c in alphabet if c not in seen)
    res.append(missing)
    return "".join(res)


@algo(tags=["strings", "greedy", "construction"], icpc=["2023 B"], verified=False)
def brands(s: str, vowels: str = "aeiou") -> str:
    """Fewest insertions so vowels and consonants alternate.   # Бренды.

    When to use:  ICPC-UZ 2023 B "Brands" as understood from its short description.
    Complexity:   O(n)
    Returns:      the shortest result, lexicographically smallest among the shortest.
    Idea:         between two vowels insert the smallest consonant ('b'), between two
                  consonants the smallest vowel ('a'); nothing else is ever needed.
    ICPC-UZ:      2023 B "Brands" (vowel set and alphabet NOT VERIFIED).
    Example:
        >>> brands("bratt"), brands("aoe")
        ('baratat', 'abobe')
    """
    # NOT VERIFIED: набор гласных (y?) и алфавит из условия 2023 B не сверены
    if not s:
        return s
    consonant = next(c for c in "abcdefghijklmnopqrstuvwxyz" if c not in vowels)
    vowel = min(vowels)
    res = [s[0]]
    for ch in s[1:]:
        a, b = res[-1] in vowels, ch in vowels
        if a == b:
            res.append(consonant if a else vowel)  # два одного типа подряд - вставка
        res.append(ch)
    return "".join(res)


@algo(tags=["strings", "formatting"], icpc=["2024 K"], verified=False, stub=True)
def apostrophe_number(s: str) -> str:
    """ICPC-UZ 2024 K: apostrophes in numbers.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return the formatted number.
    Idea:         digit grouping with apostrophes (like 1'000'000)? NOT VERIFIED - the rule is
                  unknown until the statement is checked.
    ICPC-UZ:      2024 K.
    Example:
        >>> apostrophe_number("1000")
        Traceback (most recent call last):
        NotImplementedError: ICPC-UZ 2024 K: statement not verified yet
    """
    # NOT VERIFIED: заглушка до сверки условия (этап 5)
    raise NotImplementedError("ICPC-UZ 2024 K: statement not verified yet")


@algo(
    tags=["strings", "prefix-function", "z-function", "construction"],
    cses=["String Functions"],
    verified=False,
    stub=True,
)
def string_functions(z: list[int]) -> str | None:
    """CSES String Functions - not implemented yet.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return a string with the given function values, or None.
    Idea:         build from the Z-array greedily: positions covered by a z-box copy their
                  letter, free positions get a new letter; verify with z_function.
                  NOT VERIFIED: which functions the CSES statement gives is unknown.
    CSES:         String Functions.
    Example:
        >>> string_functions([1])
        Traceback (most recent call last):
        NotImplementedError: CSES String Functions: statement not verified yet
    """
    # NOT VERIFIED: заглушка, условие задачи не сверено
    raise NotImplementedError("CSES String Functions: statement not verified yet")
