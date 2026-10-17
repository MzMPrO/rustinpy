"""ICPC Uzbekistan problems that need number theory or combinatorics.

Задачи ICPC-UZ. Условий нет: заглушки или реализации по разбору жюри 2025 (NOT VERIFIED).
"""

from __future__ import annotations

from rustinpy._registry import algo

MOD = 998244353


@algo(tags=["combinatorics", "blocks", "composite-mod"], icpc=["2025 B"], verified=False)
def min_digit_changes_count(counts: list[int], mod: int = 2112025) -> int:
    """Arrangements of a multiset with the fewest neighbour changes.   # Мин. число смен цифр.

    When to use:  ICPC-UZ 2025 B as described by the official tutorial.
    Complexity:   O(len(counts))
    Input:        counts[d] = how many times symbol d occurs.
    Returns:      k! mod mod, k = number of distinct symbols (1 for an empty multiset).
    Pitfalls:     2112025 = 5^2 * 84481 is composite: only multiply, never divide. If the
                  real statement forbids a leading zero, the answer becomes (k - 1) * (k - 1)!.
    Idea:         the minimum (k - 1 changes) is reached only when every symbol forms one
                  block; the blocks can be ordered in k! ways. Checked by brute force.
                  NOT VERIFIED: statement not found (leading zeros?).
    ICPC-UZ:      2025 B "Big Alphanumeric String".
    Example:
        >>> min_digit_changes_count([2, 1, 0, 3]), min_digit_changes_count([5])
        (6, 1)
    """
    # NOT VERIFIED: по разбору жюри, условие не найдено (ведущие нули?)
    res = 1 % mod
    k = 0
    for c in counts:
        if c > 0:
            k += 1
            res = res * k % mod  # k! без делений: модуль составной
    return res


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


@algo(tags=["dp", "matrix", "games"], icpc=["2025 I"], requires=["MOD"], verified=False)
def infinite_game_count(n: int, rem: int = 0, last: int = 0, mod: int = MOD) -> int:
    """Number of positions after n moves of the digit game.   # Бесконечная игра.

    When to use:  ICPC-UZ 2025 I as described by the official tutorial.
    Complexity:   O(9^3 log n)
    Input:        a move appends a digit 0, 1 or 2 that differs from the last digit and does
                  not make the digit sum divisible by 3; the start state is (sum mod 3, last).
    Returns:      the number of different move sequences of length n, mod mod.
    Idea:         9 states (sum mod 3, last digit), a move can always be made (at most two
                  digits are forbidden), so count paths of length n: 9 x 9 matrix power. The
                  tutorial also notes a Fibonacci closed form after a short prefix.
                  NOT VERIFIED: statement not found (start state and output format).
    ICPC-UZ:      2025 I "Infinite Game".
    Example:
        >>> [infinite_game_count(n) for n in range(7)]
        [1, 2, 2, 2, 4, 6, 10]
    """
    # NOT VERIFIED: по разбору жюри, условие не найдено
    m = [[0] * 9 for _ in range(9)]
    for r in range(3):
        for d in range(3):
            for x in range(3):
                nr = (r + x) % 3
                if x != d and nr != 0:
                    m[r * 3 + d][nr * 3 + x] += 1  # ход: дописать цифру x
    vec = [0] * 9
    vec[rem % 3 * 3 + last] = 1
    while n > 0:
        if n & 1:
            vec = [sum(vec[i] * m[i][j] for i in range(9)) % mod for j in range(9)]
        m = [[sum(m[i][t] * m[t][j] for t in range(9)) % mod for j in range(9)] for i in range(9)]
        n >>= 1
    return sum(vec) % mod
