"""AC-12: interactive helpers against simulated interactors."""

from __future__ import annotations

import io
import random

import pytest

from rustinpy.interactive import (
    ADAPTIVE_NOTE,
    answer,
    colored_chairs,
    find_hidden_rectangle,
    hidden_permutation,
    interactive_bisect,
    inversion_sorting,
    kth_highest_score,
    make_ask,
    permuted_binary_strings,
)


def test_ac_12_make_ask_flushes_and_stops_on_minus_one_or_eof() -> None:
    out = io.StringIO()
    ask = make_ask(io.StringIO("10\n"), out)
    assert ask("? 1 2") == "10"
    assert out.getvalue() == "? 1 2\n"
    with pytest.raises(SystemExit):
        ask("? 3")  # EOF
    ask2 = make_ask(io.StringIO("-1\n"), io.StringIO())
    with pytest.raises(SystemExit):
        ask2("?")
    buf = io.StringIO()
    answer("! 5", buf)
    assert buf.getvalue() == "! 5\n"
    assert "flush" in ADAPTIVE_NOTE


def test_interactive_bisect_matches_linear_scan(rng: random.Random) -> None:
    for _ in range(300):
        lo = rng.randint(-50, 50)
        hi = lo + rng.randint(0, 60)
        t = rng.randint(lo, hi + 1)
        calls: list[int] = []

        def pred(x: int, t: int = t, calls: list[int] = calls) -> bool:
            calls.append(x)
            return x >= t

        assert interactive_bisect(lo, hi, pred) == t
        assert len(calls) <= (hi - lo + 1).bit_length() + 1


def test_find_hidden_rectangle_random(rng: random.Random) -> None:
    n = 10**9
    for _ in range(50):
        x1, x2 = sorted(rng.randint(1, n) for _ in range(2))
        y1, y2 = sorted(rng.randint(1, n) for _ in range(2))
        queries: list[int] = []
        rect = (x1, y1, x2, y2)

        def count(
            a: int, b: int, c: int, d: int, r: tuple[int, ...] = rect, q: list[int] = queries
        ) -> int:
            q.append(1)
            w = max(0, min(c, r[2]) - max(a, r[0]) + 1)
            h = max(0, min(d, r[3]) - max(b, r[1]) + 1)
            return w * h

        assert find_hidden_rectangle(n, count) == rect
        assert len(queries) <= 125


def test_hidden_permutation_random(rng: random.Random) -> None:
    for n in range(1, 60):
        p = list(range(1, n + 1))
        rng.shuffle(p)
        assert hidden_permutation(n, lambda i, j, p=p: p[i] < p[j]) == p


def test_kth_highest_score_vs_sorting(rng: random.Random) -> None:
    for _ in range(300):
        n, m = rng.randint(0, 8), rng.randint(0, 8)
        if n + m == 0:
            continue
        a = sorted((rng.randint(0, 20) for _ in range(n)), reverse=True)
        b = sorted((rng.randint(0, 20) for _ in range(m)), reverse=True)
        merged = sorted(a + b, reverse=True)
        for k in range(1, n + m + 1):
            assert kth_highest_score(n, m, k, a.__getitem__, b.__getitem__) == merged[k - 1]


def test_colored_chairs_all_odd_circles(rng: random.Random) -> None:
    for n in range(3, 40, 2):
        for _ in range(30):
            c = "".join(rng.choice("RB") for _ in range(n))
            asked: list[int] = []

            def color(i: int, c: str = c, asked: list[int] = asked) -> str:
                asked.append(i)
                return c[i]

            i = colored_chairs(n, color)
            assert c[i] == c[(i + 1) % n]
            assert len(asked) <= n.bit_length() + 3


def test_stubs_raise() -> None:
    with pytest.raises(NotImplementedError):
        permuted_binary_strings(2, lambda q: "")
    with pytest.raises(NotImplementedError):
        inversion_sorting(2, lambda q: "")
