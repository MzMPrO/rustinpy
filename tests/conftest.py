from __future__ import annotations

import random

import pytest


@pytest.fixture
def rng() -> random.Random:
    """Deterministic random generator for brute-force comparisons."""
    return random.Random(20261017)
