"""introductory: brute-force checks of enumerations and constructions (AC-05, AC-06)."""

from __future__ import annotations

import itertools
import random

import pytest

from rustinpy.introductory import (
    apple_division,
    beautiful_permutation,
    chess_tournament,
    coin_piles,
    de_bruijn,
    digit_queries,
    filling_trominos,
    gray_code,
    grid_path_description,
    hanoi_moves,
    inverse_inversions,
    knight_moves_grid,
    mex_grid_construction,
    monotone_subsequences,
    n_queens,
    next_permutation,
    number_spiral,
    palindrome_reorder,
    prufer_decode,
    prufer_encode,
    string_permutations,
    string_reorder,
    submasks,
    subsets,
    trailing_zeros,
    two_knights,
    two_sets,
    weird_algorithm,
)


def test_simple_formulas(rng: random.Random) -> None:
    assert weird_algorithm(1) == [1] and weird_algorithm(3)[-1] == 1
    # спираль из условия CSES Number Spiral
    table = [
        [1, 2, 9, 10, 25],
        [4, 3, 8, 11, 24],
        [5, 6, 7, 12, 23],
        [16, 15, 14, 13, 22],
        [17, 18, 19, 20, 21],
    ]
    for y in range(1, 6):
        for x in range(1, 6):
            assert number_spiral(y, x) == table[y - 1][x - 1]
    for k in range(1, 7):
        cells = [(r, c) for r in range(k) for c in range(k)]
        ok = sum(
            1
            for a, b in itertools.combinations(cells, 2)
            if sorted((abs(a[0] - b[0]), abs(a[1] - b[1]))) != [1, 2]
        )
        assert two_knights(k)[-1] == ok
    for n in range(1, 30):
        r = two_sets(n)
        if n * (n + 1) // 2 % 2:
            assert r is None
        else:
            assert (
                r is not None
                and sum(r[0]) == sum(r[1])
                and sorted(r[0] + r[1]) == list(range(1, n + 1))
            )
    f = 1
    for n in range(1, 60):
        f *= n
        s = str(f)
        assert trailing_zeros(n) == len(s) - len(s.rstrip("0"))
    for a in range(10):
        for b in range(10):
            from functools import cache

            @cache
            def can(x: int, y: int) -> bool:
                if x == 0 and y == 0:
                    return True
                return (x >= 1 and y >= 2 and can(x - 1, y - 2)) or (
                    x >= 2 and y >= 1 and can(x - 2, y - 1)
                )

            assert coin_piles(a, b) == can(a, b)
    digits = "".join(str(i) for i in range(1, 3000))
    for k in range(1, len(digits) + 1, 7):
        assert digit_queries(k) == int(digits[k - 1])
    assert digit_queries(10**18) in range(10)


def test_strings_and_permutations(rng: random.Random) -> None:
    for _ in range(100):
        s = "".join(
            rng.choice("AAB C"[: rng.randint(2, 4)].replace(" ", ""))
            for _ in range(rng.randint(1, 7))
        )
        r = palindrome_reorder(s)
        exists = any(p == p[::-1] for p in ("".join(t) for t in set(itertools.permutations(s))))
        if exists:
            assert r is not None and r == r[::-1] and sorted(r) == sorted(s)
            assert r == min(
                "".join(t) for t in set(itertools.permutations(s)) if "".join(t) == "".join(t)[::-1]
            )
        else:
            assert r is None
        perms = sorted({"".join(t) for t in itertools.permutations(s)})
        assert string_permutations(s) == perms
        good = [p for p in perms if all(x != y for x, y in zip(p, p[1:]))]
        assert string_reorder(s) == (good[0] if good else None)
    a = [1, 2, 2, 3]
    seen = [list(a)]
    while next_permutation(a):
        seen.append(list(a))
    assert seen == [list(p) for p in sorted(set(itertools.permutations([1, 2, 2, 3])))]
    for n in range(1, 9):
        p = beautiful_permutation(n)
        ok = any(
            all(abs(x - y) != 1 for x, y in zip(q, q[1:]))
            for q in itertools.permutations(range(1, n + 1))
        )
        if ok:
            assert p is not None and sorted(p) == list(range(1, n + 1))
            assert all(abs(x - y) != 1 for x, y in zip(p, p[1:]))
        else:
            assert p is None


def test_bit_enumerations_and_grids() -> None:
    for n in range(1, 7):
        g = gray_code(n)
        assert len(set(g)) == 1 << n
        assert all(sum(a != b for a, b in zip(x, y)) == 1 for x, y in zip(g, g[1:]))
    for mask in range(64):
        assert sorted(submasks(mask)) == [s for s in range(64) if s & mask == s]
    assert list(subsets(3)) == [[], [0], [1], [0, 1], [2], [0, 2], [1, 2], [0, 1, 2]]
    for n in range(1, 6):
        g = mex_grid_construction(n)
        for i in range(n):
            for j in range(n):
                seen = {g[i][k] for k in range(j)} | {g[k][j] for k in range(i)}
                m = 0
                while m in seen:
                    m += 1
                assert g[i][j] == m
    for n in range(1, 7):
        d = knight_moves_grid(n)
        assert d[0][0] == 0
        for r in range(n):
            for c in range(n):
                if d[r][c] > 0:
                    assert any(
                        0 <= r + dr < n and 0 <= c + dc < n and d[r + dr][c + dc] == d[r][c] - 1
                        for dr, dc in (
                            (1, 2),
                            (2, 1),
                            (-1, 2),
                            (-2, 1),
                            (1, -2),
                            (2, -1),
                            (-1, -2),
                            (-2, -1),
                        )
                    )


def test_hanoi_valid_and_optimal() -> None:
    for n in range(1, 9):
        pegs = [list(range(n, 0, -1)), [], []]
        moves = hanoi_moves(n)
        assert len(moves) == 2**n - 1
        for a, b in moves:
            disk = pegs[a - 1].pop()
            assert not pegs[b - 1] or pegs[b - 1][-1] > disk
            pegs[b - 1].append(disk)
        assert pegs[2] == list(range(n, 0, -1))


def brute_queens(n: int, blocked: list[str]) -> int:
    cnt = 0
    for cols in itertools.permutations(range(n)):
        if any(blocked[r][c] == "*" for r, c in enumerate(cols)):
            continue
        if (
            len({r + c for r, c in enumerate(cols)}) == n
            and len({r - c for r, c in enumerate(cols)}) == n
        ):
            cnt += 1
    return cnt


def test_queens_and_grid_paths(rng: random.Random) -> None:
    for n in range(1, 8):
        blocked = ["".join(rng.choice("....*") for _ in range(n)) for _ in range(n)]
        assert n_queens(n, blocked) == brute_queens(n, blocked)
        assert n_queens(n) == brute_queens(n, ["." * n] * n)
    for n in (2, 3, 4):
        paths = []
        stack = [((0, 0), "", {(0, 0)})]
        while stack:
            (r, c), s, vis = stack.pop()
            if len(s) == n * n - 1:
                if (r, c) == (n - 1, 0):
                    paths.append(s)
                continue
            for ch, (dr, dc) in {"D": (1, 0), "U": (-1, 0), "L": (0, -1), "R": (0, 1)}.items():
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in vis:
                    stack.append(((nr, nc), s + ch, vis | {(nr, nc)}))
        assert grid_path_description("?" * (n * n - 1), n) == len(paths)
        for p in paths[:5]:
            pat = "".join(ch if rng.random() < 0.5 else "?" for ch in p)
            exp = sum(1 for q in paths if all(a in ("?", b) for a, b in zip(pat, q)))
            assert grid_path_description(pat, n) == exp
    with pytest.raises(ValueError):
        grid_path_description("??", 3)


def test_apple_division_vs_brute(rng: random.Random) -> None:
    for _ in range(100):
        p = [rng.randint(1, 20) for _ in range(rng.randint(1, 8))]
        best = min(
            abs(sum(p) - 2 * sum(c))
            for k in range(len(p) + 1)
            for c in itertools.combinations(p, k)
        )
        assert apple_division(p) == best


def test_prufer_round_trip(rng: random.Random) -> None:
    for _ in range(200):
        n = rng.randint(2, 9)
        code = [rng.randrange(n) for _ in range(n - 2)]
        edges = prufer_decode(code)
        assert len(edges) == n - 1
        assert prufer_encode(n, edges) == code


def test_de_bruijn_contains_every_word() -> None:
    for k in (2, 3):
        for n in range(1, 6 if k == 2 else 4):
            s = de_bruijn(n, k)
            assert len(s) == k**n + n - 1
            words = {s[i : i + n] for i in range(len(s) - n + 1)}
            assert len(words) == k**n


def test_inversions_monotone_tournament(rng: random.Random) -> None:
    for n in range(1, 8):
        for k in range(n * (n - 1) // 2 + 1):
            p = inverse_inversions(n, k)
            assert sorted(p) == list(range(1, n + 1))
            assert sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j]) == k
    for n in range(1, 8):
        for k in range(1, n + 1):
            p = monotone_subsequences(n, k)

            def longest(seq: list[int], inc: bool) -> int:
                best = 0
                for r in range(1, len(seq) + 1):
                    for idx in itertools.combinations(range(len(seq)), r):
                        vals = [seq[i] for i in idx]
                        if all((a < b) == inc for a, b in zip(vals, vals[1:])):
                            best = max(best, r)
                return best

            if k * k < n:
                assert p is None
            else:
                assert p is not None and max(longest(p, True), longest(p, False)) == k
    for _ in range(200):
        n = rng.randint(1, 6)
        deg = [rng.randint(0, n - 1) for _ in range(n)]
        pairs = list(itertools.combinations(range(n), 2))
        exists = any(
            all(sum(1 for e in sub if v in e) == deg[v] for v in range(n))
            for r in range(len(pairs) + 1)
            for sub in itertools.combinations(pairs, r)
            if 2 * r == sum(deg)
        )
        got = chess_tournament(deg)
        if exists:
            assert got is not None and len(set(got)) == len(got)
            assert all(sum(1 for e in got if v in e) == deg[v] for v in range(n))
        else:
            assert got is None


def test_intro_stub_raises() -> None:
    with pytest.raises(NotImplementedError):
        filling_trominos(2, 3)
