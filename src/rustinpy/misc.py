"""Short ICPC-UZ problems (2023-2025) that do not belong to a bigger topic.

Statements are not public: 2025 ideas follow the official tutorial
(neerc.ifmo.ru/archive/2025/uzbekistan/uzb-tutorial-en.pdf), the rest are stubs until the
statements are found. Everything here is NOT VERIFIED (see docs/PROGRESS.md).

Короткие задачи ICPC-UZ. Без условий: всё помечено NOT VERIFIED.
"""

from __future__ import annotations

import heapq

from rustinpy._registry import algo


@algo(tags=["greedy", "math"], icpc=["2023 A"], verified=False)
def attacks_number(n: int) -> int:
    """Fewest attacks worth 2 or 3 points that sum to exactly n.   # Число атак.

    When to use:  ICPC-UZ 2023 A as understood from the task list.
    Complexity:   O(1)
    Returns:      the minimal number of attacks, -1 if n cannot be reached (n = 1).
    Idea:         use as many 3s as possible: ceil(n / 3) works for every n >= 2 (replace one
                  3 + 1 by 2 + 2). NOT VERIFIED: statement not found, only "moves of 2 and 3
                  points, minimum number of successful attacks" is known.
    ICPC-UZ:      2023 A "Attacks Number".
    Example:
        >>> [attacks_number(n) for n in range(8)]
        [0, -1, 1, 1, 2, 2, 2, 3]
    """
    # NOT VERIFIED: условие 2023 A не найдено, реализация по описанию из задания
    if n == 1 or n < 0:
        return -1
    return (n + 2) // 3


@algo(tags=["greedy"], icpc=["2024 A"], verified=False, stub=True)
def a_plus_branding(tasks: list[str]) -> int:
    """ICPC-UZ 2024 A "A+Branding": fewest shared tasks.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return the minimal number of joint tasks.
    Idea:         count tasks by their A / B / C structure and match them greedily.
                  NOT VERIFIED: statement not found (only "minimum joint tasks by A/B/C").
    ICPC-UZ:      2024 A.
    Example:
        >>> a_plus_branding(["A"])
        Traceback (most recent call last):
        NotImplementedError: ICPC-UZ 2024 A: statement not verified yet
    """
    # NOT VERIFIED: заглушка, условие не найдено
    raise NotImplementedError("ICPC-UZ 2024 A: statement not verified yet")


@algo(tags=["combinatorics", "counting"], icpc=["2024 B"], verified=False, stub=True)
def big_deadline(order: str, mod: int = 998244353) -> int:
    """ICPC-UZ 2024 B "Big Deadline": count orders of two workers.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return the number of valid orders mod 998244353.
    Idea:         D-tasks must come before T-tasks: interleavings of two sequences counted
                  with binomials / DP. NOT VERIFIED: statement not found.
    ICPC-UZ:      2024 B.
    Example:
        >>> big_deadline("DT")
        Traceback (most recent call last):
        NotImplementedError: ICPC-UZ 2024 B: statement not verified yet
    """
    # NOT VERIFIED: заглушка, условие не найдено
    raise NotImplementedError("ICPC-UZ 2024 B: statement not verified yet")


@algo(tags=["combinatorics", "subsets", "greedy"], icpc=["2024 C"], verified=False, stub=True)
def certainly_best(n: int) -> int:
    """ICPC-UZ 2024 C "Certainly Best": distinct subsets, minimal total size.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return the minimal total cardinality.
    Idea:         take the distinct non-empty subsets in order of size (all singletons, then
                  pairs, ...). NOT VERIFIED: statement not found (size of the ground set?).
    ICPC-UZ:      2024 C.
    Example:
        >>> certainly_best(1)
        Traceback (most recent call last):
        NotImplementedError: ICPC-UZ 2024 C: statement not verified yet
    """
    # NOT VERIFIED: заглушка, условие не найдено
    raise NotImplementedError("ICPC-UZ 2024 C: statement not verified yet")


@algo(tags=["math", "bases", "construction"], icpc=["2024 G"], verified=False, stub=True)
def great_sign(b: int) -> int:
    """ICPC-UZ 2024 G "Great Sign": number using all b digits once.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return the minimal maximal number.
    Idea:         in base b the smallest pandigital number is 1 0 2 3 ... (b - 1).
                  NOT VERIFIED: what "minimal maximal" means is unknown.
    ICPC-UZ:      2024 G.
    Example:
        >>> great_sign(10)
        Traceback (most recent call last):
        NotImplementedError: ICPC-UZ 2024 G: statement not verified yet
    """
    # NOT VERIFIED: заглушка, условие не найдено
    raise NotImplementedError("ICPC-UZ 2024 G: statement not verified yet")


@algo(tags=["simulation", "chess"], icpc=["2024 H"], verified=False, stub=True)
def hidden_pieces(board: list[str]) -> list[str]:
    """ICPC-UZ 2024 H "Hidden Pieces": fog-of-war chess visibility.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return the board as seen by one side.
    Idea:         mark every cell attacked or occupied by own pieces (sliding pieces stop at
                  the first piece), hide the rest. NOT VERIFIED: statement not found.
    ICPC-UZ:      2024 H.
    Example:
        >>> hidden_pieces(["."])
        Traceback (most recent call last):
        NotImplementedError: ICPC-UZ 2024 H: statement not verified yet
    """
    # NOT VERIFIED: заглушка, условие не найдено
    raise NotImplementedError("ICPC-UZ 2024 H: statement not verified yet")


@algo(tags=["greedy", "randomized", "dot-product"], icpc=["2024 L"], verified=False, stub=True)
def laura_and_arrays(a: list[int], b: list[int]) -> int:
    """ICPC-UZ 2024 L "Laura and Arrays": maximal dot product.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return the maximal scalar product.
    Idea:         data is random, so a greedy that relies on randomness passes.
                  NOT VERIFIED: statement not found.
    ICPC-UZ:      2024 L.
    Example:
        >>> laura_and_arrays([1], [1])
        Traceback (most recent call last):
        NotImplementedError: ICPC-UZ 2024 L: statement not verified yet
    """
    # NOT VERIFIED: заглушка, условие не найдено
    raise NotImplementedError("ICPC-UZ 2024 L: statement not verified yet")


@algo(tags=["math", "easy"], icpc=["2025 A"], verified=False)
def a_problems_balloons(n: int, k: int) -> int:
    """Teams that get a balloon: n teams, k balloons.   # Задачи и шарики.

    When to use:  ICPC-UZ 2025 A as described by the official tutorial.
    Complexity:   O(1)
    Returns:      min(n, k).
    Idea:         if k >= n every team solves one problem; otherwise teams solve until the
                  balloons run out. NOT VERIFIED: statement (input format) not found.
    ICPC-UZ:      2025 A "A Problems and A Balloons".
    Example:
        >>> a_problems_balloons(5, 3), a_problems_balloons(2, 10)
        (3, 2)
    """
    # NOT VERIFIED: по разбору жюри, условие не найдено
    return min(n, k)


@algo(tags=["greedy", "heap", "prefix"], icpc=["2025 L"], verified=False)
def limit_the_arrow(a: list[int], p: int) -> list[int]:
    """For each prefix, fewest targets whose thickness sum reaches p.   # Ограничь стрелу.

    When to use:  ICPC-UZ 2025 L as described by the official tutorial.
    Complexity:   O(n log n)
    Returns:      f(i) for i = 1..n: minimal number of elements of a[:i] with sum >= p,
                  -1 if even the whole prefix is not enough.
    Idea:         keep a min-heap of chosen values; push a_i, then drop the smallest while the
                  sum stays >= p (for sorted input a plain queue, O(n)).
                  NOT VERIFIED: statement not found, f(i) taken from the tutorial.
    ICPC-UZ:      2025 L "Limit The Arrow".
    Example:
        >>> limit_the_arrow([3, 1, 4, 1, 5], 6)
        [-1, -1, 2, 2, 2]
    """
    # NOT VERIFIED: по разбору жюри, условие не найдено
    heap: list[int] = []
    s = 0
    res = []
    for x in a:
        heapq.heappush(heap, x)
        s += x
        while heap and s - heap[0] >= p:
            s -= heapq.heappop(heap)  # самый тонкий больше не нужен
        res.append(len(heap) if s >= p else -1)
    return res


@algo(tags=["strings", "easy"], icpc=["2025 M"], verified=False)
def minimum_number_of_tasks(letters: str) -> int:
    """Fewest problems in a contest given the letters that were submitted.   # Число задач.

    When to use:  ICPC-UZ 2025 M as described by the official tutorial.
    Complexity:   O(len)
    Returns:      index of the largest letter (A = 1), 0 for an empty string.
    Pitfalls:     letters are consecutive from A, so unseen letters before the maximum still
                  exist; ignore anything that is not A..Z.
    Idea:         NOT VERIFIED: statement not found, idea from the tutorial.
    ICPC-UZ:      2025 M "Minimum Number of Tasks".
    Example:
        >>> [minimum_number_of_tasks(s) for s in ("ACB", "D", "")]
        [3, 4, 0]
    """
    # NOT VERIFIED: по разбору жюри, условие не найдено
    best = 0
    for ch in letters:
        if "A" <= ch <= "Z":
            best = max(best, ord(ch) - ord("A") + 1)
    return best
