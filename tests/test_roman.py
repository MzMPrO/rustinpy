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
    for f, arg in ((roman_symmetry, "X"), (roman_product_unique, 6), (scroogius_shortest, 1)):
        with pytest.raises(NotImplementedError):
            f(arg)  # type: ignore[operator]
