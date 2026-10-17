"""Game theory: Nim and its variants, Sprague-Grundy values, CSES games.

Теория игр. Везде «первый выигрывает?» при оптимальной игре обоих.
"""

from __future__ import annotations

from collections.abc import Iterable

from rustinpy._registry import algo


@algo(tags=["games", "mex", "grundy"], cses=["- (mex helper)"])
def mex(values: Iterable[int]) -> int:
    """Minimum excluded non-negative integer.   # Mex множества.

    When to use:  Grundy value = mex of the Grundy values of the moves.
    Complexity:   O(k)
    Returns:      smallest non-negative integer not in values.
    Related:      grundy_subtraction, grundy_dag.
    CSES:         - (mex helper)
    Example:
        >>> mex([0, 1, 3]), mex([]), mex([1, 2])
        (2, 0, 0)
    """
    s = set(values)
    m = 0
    while m in s:
        m += 1
    return m


@algo(tags=["games", "nim"], cses=["Nim Game I (1730)"])
def nim_first_wins(piles: list[int]) -> bool:
    """Classic Nim: take any positive number from one pile.   # Ним.

    When to use:  Nim and everything that reduces to it by Sprague-Grundy.
    Complexity:   O(n)
    Returns:      True iff the xor of the piles is non-zero.
    Related:      misere_nim_first_wins, nim_k_first_wins.
    CSES:         Nim Game I (1730).
    Example:
        >>> nim_first_wins([5, 7, 3]), nim_first_wins([1, 2, 3])
        (True, False)
    """
    x = 0
    for p in piles:
        x ^= p  # теорема Бутона
    return x != 0


@algo(tags=["games", "nim", "subtraction"], cses=["Nim Game II (1098)"])
def nim_k_first_wins(piles: list[int], k: int = 3) -> bool:
    """Nim where a move takes 1..k sticks from one pile.   # Ним с ограничением хода.

    When to use:  bounded Nim: Grundy value of a pile p is p mod (k + 1).
    Complexity:   O(n)
    Returns:      True iff xor of p mod (k + 1) is non-zero.
    Related:      grundy_subtraction.
    CSES:         Nim Game II (1098) (k = 3).
    Example:
        >>> nim_k_first_wins([4, 8]), nim_k_first_wins([5, 6])
        (False, True)
    """
    x = 0
    for p in piles:
        x ^= p % (k + 1)  # гранди кучи
    return x != 0


@algo(tags=["games", "nim", "misere"], cses=["- (misere Nim)"])
def misere_nim_first_wins(piles: list[int]) -> bool:
    """Misere Nim: whoever takes the last stick LOSES.   # Ним в поддавки.

    When to use:  Nim with the reversed last-move rule.
    Complexity:   O(n)
    Returns:      True iff the first player wins.
    Idea:         if every pile <= 1, the parity of non-empty piles decides (even -> first
                  wins); otherwise play normal Nim (xor != 0).
    Related:      nim_first_wins.
    CSES:         - (misere Nim)
    Example:
        >>> misere_nim_first_wins([1, 1]), misere_nim_first_wins([1]), misere_nim_first_wins([2, 2])
        (True, False, False)
    """
    if all(p <= 1 for p in piles):
        return sum(piles) % 2 == 0  # остались только единицы
    x = 0
    for p in piles:
        x ^= p
    return x != 0


@algo(tags=["games", "grundy", "subtraction"], cses=["Stick Game (1729)"], requires=["mex"])
def grundy_subtraction(n_max: int, moves: list[int]) -> list[int]:
    """Grundy values of a subtraction game (remove one of the allowed amounts).   # Игра вычитания.

    When to use:  one pile, allowed moves = fixed set; sums of piles = xor of values.
    Complexity:   O(n_max * |moves|)
    Returns:      g[0..n_max]; position n is winning iff g[n] != 0.
    Related:      mex, grundy_dag.
    CSES:         Stick Game (1729) (print W if g[n] else L).
    Example:
        >>> "".join("W" if g else "L" for g in grundy_subtraction(10, [1, 3, 4])[1:])
        'WLWWWWLWLW'
    """
    g = [0] * (n_max + 1)
    for n in range(1, n_max + 1):
        g[n] = mex(g[n - m] for m in moves if m <= n)  # все ходы из n
    return g


@algo(tags=["games", "grundy", "dag"], cses=["- (games on DAGs)"], requires=["mex"])
def grundy_dag(n: int, adj: list[list[int]]) -> list[int]:
    """Sprague-Grundy values of every vertex of a game DAG (moves = edges).   # Гранди на DAG.

    When to use:  any impartial game given as an acyclic position graph.
    Complexity:   O(n + m)
    Returns:      g[v]; vertex with no moves has 0 (losing for the player to move).
    Pitfalls:     the graph must be acyclic (no draws).
    Related:      mex, grundy_subtraction.
    CSES:         - (games on DAGs)
    Example:
        >>> grundy_dag(4, [[1, 2], [3], [3], []])
        [0, 1, 1, 0]
    """
    outdeg = [len(a) for a in adj]
    radj: list[list[int]] = [[] for _ in range(n)]
    for u in range(n):
        for v in adj[u]:
            radj[v].append(u)
    g = [0] * n
    stack = [v for v in range(n) if outdeg[v] == 0]
    while stack:  # обратный топологический порядок: все ходы из u уже посчитаны
        v = stack.pop()
        g[v] = mex(g[u] for u in adj[v])
        for u in radj[v]:
            outdeg[u] -= 1
            if outdeg[u] == 0:
                stack.append(u)
    return g


@algo(tags=["games", "nim", "staircase"], cses=["Stair Game (1099)"])
def stair_game_first_wins(piles: list[int]) -> bool:
    """Staircase Nim: move balls from stair k to k - 1 (stair 1 is final).   # Ним на лестнице.

    When to use:  piles[i] = balls on stair i + 1; moving balls down one stair.
    Complexity:   O(n)
    Returns:      True iff xor over EVEN stairs (2, 4, ... i.e. odd indices) is non-zero.
    Idea:         moves from odd stairs can be mirrored; even stairs act as Nim piles.
    Related:      nim_first_wins.
    CSES:         Stair Game (1099).
    Example:
        >>> stair_game_first_wins([0, 2, 1]), stair_game_first_wins([1, 0, 1])
        (True, False)
    """
    x = 0
    for i in range(1, len(piles), 2):  # ступени 2, 4, 6, ...
        x ^= piles[i]
    return x != 0


@algo(tags=["games", "grundy", "split"], cses=["Grundy's Game (2207)"], requires=["mex"])
def grundy_game_first_wins(n: int) -> bool:
    """Grundy's game: split a heap into two non-empty UNEQUAL heaps.   # Игра Гранди.

    When to use:  CSES Grundy's Game, n up to 10^6.
    Complexity:   O(min(n, 1300)^2)
    Returns:      True iff the first player wins.
    Pitfalls:     the "n > 1222 wins" fact is computational, not a proof.
    Idea:         compute Grundy values up to 1300; the last losing heap size is 1222
                  (checked by computation far beyond 10^6), so every n > 1222 wins.
    Related:      mex.
    CSES:         Grundy's Game (2207).
    Example:
        >>> [n for n in range(1, 25) if not grundy_game_first_wins(n)]
        [1, 2, 4, 7, 10, 20, 23]
    """
    if n > 1300:
        return True
    g = [0] * (n + 1)
    for m in range(3, n + 1):
        g[m] = mex(g[a] ^ g[m - a] for a in range(1, (m + 1) // 2))  # a < m - a
    return g[n] != 0


@algo(tags=["games", "parity"], cses=["Another Game (2208)"])
def another_game_first_wins(piles: list[int]) -> bool:
    """Each move removes one coin from every heap of a chosen non-empty subset.   # Ещё одна игра.

    When to use:  CSES Another Game.
    Complexity:   O(n)
    Returns:      True iff some heap is odd.
    Idea:         all heaps even is losing: any move makes some heap odd, and from a
                  position with odd heaps you can make all even again.
    CSES:         Another Game (2208).
    Example:
        >>> another_game_first_wins([2, 4]), another_game_first_wins([1, 2])
        (False, True)
    """
    return any(p % 2 for p in piles)
