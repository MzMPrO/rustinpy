"""misc: short ICPC-UZ problems (all NOT VERIFIED), brute-force where an idea exists."""

from __future__ import annotations

import itertools
import random

import pytest

from rustinpy.misc import (
    a_plus_branding,
    a_problems_balloons,
    attacks_number,
    big_deadline,
    certainly_best,
    great_sign,
    hidden_pieces,
    laura_and_arrays,
    limit_the_arrow,
    minimum_number_of_tasks,
)


def test_attacks_number() -> None:
    inf = 10**9
    dp = [0] + [inf] * 60
    for n in range(1, 61):
        for s in (2, 3):
            if n >= s:
                dp[n] = min(dp[n], dp[n - s] + 1)
    for n in range(61):
        assert attacks_number(n) == (dp[n] if dp[n] < inf else -1)


def test_a_problems_balloons() -> None:
    for n in range(10):
        for k in range(10):
            assert a_problems_balloons(n, k) == min(n, k)


def test_limit_the_arrow(rng: random.Random) -> None:
    for _ in range(300):
        a = [rng.randint(1, 9) for _ in range(rng.randint(1, 8))]
        p = rng.randint(1, 30)
        want = []
        for i in range(1, len(a) + 1):
            best = -1
            for r in range(1, i + 1):
                if any(sum(c) >= p for c in itertools.combinations(a[:i], r)):
                    best = r
                    break
            want.append(best)
        assert limit_the_arrow(a, p) == want, (a, p)


def test_minimum_number_of_tasks() -> None:
    assert minimum_number_of_tasks("ZA") == 26
    assert minimum_number_of_tasks("AAAA") == 1
    assert minimum_number_of_tasks("a1") == 0


@pytest.mark.parametrize(
    ("fn", "arg"),
    [
        (a_plus_branding, (["A"],)),
        (big_deadline, ("DT",)),
        (certainly_best, (1,)),
        (great_sign, (10,)),
        (hidden_pieces, (["."],)),
        (laura_and_arrays, ([1], [1])),
    ],
)
def test_stubs_raise(fn: object, arg: tuple[object, ...]) -> None:
    with pytest.raises(NotImplementedError, match="statement not verified"):
        fn(*arg)  # type: ignore[operator]
