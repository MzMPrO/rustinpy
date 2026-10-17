"""ICPC Uzbekistan problems that need number theory or combinatorics.

Задачи ICPC-UZ. Условия ещё не сверены (этап 5), поэтому здесь честные заглушки.
"""

from __future__ import annotations

from rustinpy._registry import algo

MOD = 998244353


@algo(
    tags=["combinatorics", "multinomial", "composite-mod"],
    icpc=["2025 B"],
    verified=False,
    stub=True,
)
def min_digit_changes_count(counts: list[int], mod: int = 2112025) -> int:
    """ICPC-UZ 2025 B: count digit strings with the minimum number of digit changes.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return the count modulo 2112025.
    Pitfalls:     2112025 = 5^2 * 84481 is composite: no factorial inverses -> nCr_pascal or
                  nCr_composite.
    Idea:         the minimum number of changes is reached when equal digits form blocks;
                  count block orders / multinomials. NOT VERIFIED: statement not checked yet.
    ICPC-UZ:      2025 B.
    Example:
        >>> min_digit_changes_count([1, 1])
        Traceback (most recent call last):
        NotImplementedError: ICPC-UZ 2025 B: statement not verified yet
    """
    # NOT VERIFIED: заглушка до сверки условия (этап 5)
    raise NotImplementedError("ICPC-UZ 2025 B: statement not verified yet")


@algo(tags=["primes", "subsequence", "digit-dp"], icpc=["2024 D"], verified=False, stub=True)
def deep_numbers_count(n: int) -> int:
    """ICPC-UZ 2024 D "Deep Numbers": numbers without a prime digit subsequence.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return how many "deep" numbers are <= n.
    Idea:         a number has no prime subsequence iff it avoids all 26 "minimal primes"
                  (2, 3, 5, 7, 11, 19, 41, 61, 89, 409, 449, 499, 881, 991, 6469, 6949,
                  9001, 9049, 9649, 9949, 60649, 666649, 946669, 60000049, 66000049,
                  66600049) as subsequences; so only digits 0, 1, 4, 6, 8, 9 remain and the
                  set is small - generate it by DFS with a subsequence automaton.
                  NOT VERIFIED: do leading zeros / the number itself count - statement unknown.
    ICPC-UZ:      2024 D.
    Example:
        >>> deep_numbers_count(10)
        Traceback (most recent call last):
        NotImplementedError: ICPC-UZ 2024 D: statement not verified yet
    """
    # NOT VERIFIED: заглушка до сверки условия (этап 5)
    raise NotImplementedError("ICPC-UZ 2024 D: statement not verified yet")


@algo(tags=["dp", "matrix", "games"], icpc=["2025 I"], requires=["MOD"], verified=False, stub=True)
def infinite_game_count(n: int, mod: int = MOD) -> int:
    """ICPC-UZ 2025 I "Infinite Game": count games of length n.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return the number of games of length n mod mod.
    Idea:         state = (sum mod 3, last digit) -> a 30 x 30 transition matrix, answer =
                  vector * M^n (mat_pow). NOT VERIFIED: rules of the game unknown.
    ICPC-UZ:      2025 I.
    Example:
        >>> infinite_game_count(1)
        Traceback (most recent call last):
        NotImplementedError: ICPC-UZ 2025 I: statement not verified yet
    """
    # NOT VERIFIED: заглушка до сверки условия (этап 5)
    raise NotImplementedError("ICPC-UZ 2025 I: statement not verified yet")
