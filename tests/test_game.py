"""game: every rule checked by full game-tree search on small positions (AC-05, AC-06)."""

from __future__ import annotations

import itertools
from functools import cache

from rustinpy.game import (
    another_game_first_wins,
    grundy_dag,
    grundy_game_first_wins,
    grundy_subtraction,
    mex,
    misere_nim_first_wins,
    nim_first_wins,
    nim_k_first_wins,
    stair_game_first_wins,
)


@cache
def nim_win(piles: tuple[int, ...], k: int, misere: bool) -> bool:
    if all(p == 0 for p in piles):
        return misere  # в поддавки: соперник взял последний -> мы выиграли
    for i, p in enumerate(piles):
        for take in range(1, min(p, k) + 1):
            nxt = tuple(sorted((*piles[:i], p - take, *piles[i + 1 :])))
            if not nim_win(nxt, k, misere):
                return True
    return False


def test_nim_variants_vs_search() -> None:
    for piles in itertools.product(range(5), repeat=3):
        t = tuple(sorted(piles))
        assert nim_first_wins(list(piles)) == nim_win(t, 99, False)
        assert nim_k_first_wins(list(piles), 3) == nim_win(t, 3, False)
        assert misere_nim_first_wins(list(piles)) == nim_win(t, 99, True)


def test_mex_subtraction_dag() -> None:
    assert mex([0, 1, 2, 4]) == 3
    moves = [1, 3, 4]

    @cache
    def win(n: int) -> bool:
        return any(not win(n - m) for m in moves if m <= n)

    g = grundy_subtraction(60, moves)
    assert [x != 0 for x in g] == [win(n) for n in range(61)]
    adj = [[1, 2], [3], [3, 4], [], [3]]
    gd = grundy_dag(5, adj)
    for v in range(5):
        assert gd[v] == mex(gd[u] for u in adj[v])


def test_stair_game_vs_search() -> None:
    @cache
    def win(st: tuple[int, ...]) -> bool:
        for i in range(1, len(st)):  # с ступени i (0-based) можно спустить шары на i - 1
            for k in range(1, st[i] + 1):
                nxt = list(st)
                nxt[i] -= k
                nxt[i - 1] += k
                if not win(tuple(nxt)):
                    return True
        return False

    for st in itertools.product(range(3), repeat=4):
        assert stair_game_first_wins(list(st)) == win(st)


def test_grundy_game_vs_search() -> None:
    @cache
    def g(n: int) -> int:
        return mex(g(a) ^ g(n - a) for a in range(1, (n + 1) // 2))

    for n in range(1, 400):
        assert grundy_game_first_wins(n) == (g(n) != 0)
    zeros = [n for n in range(1, 1301) if not grundy_game_first_wins(n)]
    assert max(zeros) == 1222  # последняя проигрышная позиция в пределах таблицы
    assert grundy_game_first_wins(10**6)


def test_another_game_vs_search() -> None:
    @cache
    def win(h: tuple[int, ...]) -> bool:
        idx = [i for i, x in enumerate(h) if x]
        for r in range(1, len(idx) + 1):
            for sub in itertools.combinations(idx, r):
                nxt = list(h)
                for i in sub:
                    nxt[i] -= 1
                if not win(tuple(nxt)):
                    return True
        return False

    for h in itertools.product(range(4), repeat=3):
        assert another_game_first_wins(list(h)) == win(h)
