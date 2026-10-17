"""roman: conversions round trip, validity, splitting (AC-05, AC-06)."""

from __future__ import annotations

import itertools
import random

import pytest

from rustinpy.roman import (
    from_roman,
    is_valid_roman,
    roman_product_unique,
    roman_split_min_max,
    roman_symmetry,
    scroogius_shortest,
    to_roman,
)


def test_round_trip_and_validity(rng: random.Random) -> None:
    valid = set()
    for n in range(1, 4000):
        r = to_roman(n)
        assert from_roman(r) == n and is_valid_roman(r)
        valid.add(r)
    assert len(valid) == 3999
    for bad in (0, 4000, -1):
        with pytest.raises(ValueError):
            to_roman(bad)
    for _ in range(3000):
        s = "".join(rng.choice("IVXLCDM") for _ in range(rng.randint(0, 6)))
        assert is_valid_roman(s) == (s in valid)
    for bad_s in ("IIII", "VV", "IC", "XM", "", "ABC", "MMMM"):
        assert not is_valid_roman(bad_s)
        with pytest.raises(ValueError):
            from_roman(bad_s)


def test_split_min_max_vs_brute(rng: random.Random) -> None:
    valid = {to_roman(v) for v in range(1, 4000)}
    for _ in range(300):
        s = "".join(rng.choice("IVX") for _ in range(rng.randint(1, 8)))
        counts = []
        for cuts in itertools.product((0, 1), repeat=len(s) - 1):
            parts, start = [], 0
            for i, c in enumerate(cuts, 1):
                if c:
                    parts.append(s[start:i])
                    start = i
            parts.append(s[start:])
            if all(p in valid for p in parts):
                counts.append(len(parts))
        exp = (min(counts), max(counts)) if counts else None
        assert roman_split_min_max(s) == exp
    assert roman_split_min_max("") is None


def test_roman_stubs_raise() -> None:
    for f, arg in ((roman_symmetry, "X"), (roman_product_unique, 6)):
        with pytest.raises(NotImplementedError):
            f(arg)  # type: ignore[operator]


def split_sum_range(s: str, valid: dict[str, int]) -> tuple[int, int] | None:
    """Перебор: минимальная и максимальная сумма разбиения s на римские числа."""
    n = len(s)
    lo: list[float] = [float("inf")] * (n + 1)
    hi: list[float] = [-1.0] * (n + 1)
    lo[0] = hi[0] = 0
    for j in range(1, n + 1):
        for i in range(max(0, j - 15), j):
            v = valid.get(s[i:j])
            if v is not None and hi[i] >= 0:
                lo[j] = min(lo[j], lo[i] + v)
                hi[j] = max(hi[j], hi[i] + v)
    return (int(lo[n]), int(hi[n])) if hi[n] >= 0 else None


def test_scroogius_shortest() -> None:
    valid = {to_roman(v): v for v in range(1, 4000)}
    best: dict[int, str] = {}
    for length in range(1, 6):
        for t in itertools.product(sorted("IVXLCDM"), repeat=length):
            r = split_sum_range("".join(t), valid)
            if r is not None:
                best.setdefault(r[1] - r[0], "".join(t))  # первая по длине и алфавиту
    for n in range(1, 500):
        got = scroogius_shortest(n)
        if got is not None and len(got) <= 5:
            assert best.get(n) == got, n
        elif n in best:
            assert got is not None and len(got) <= len(best[n]), n
    for n in range(1, 4000, 2):
        assert n not in best
    with pytest.raises(ValueError):
        scroogius_shortest(0)
