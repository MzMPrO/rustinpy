"""Roman numerals and the ICPC Uzbekistan problems built on them.

Римские числа (1..3999, каноническая запись).
"""

from __future__ import annotations

from rustinpy._registry import algo

_ROMAN = (
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
    (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
)  # fmt: skip
_VALUE = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


@algo(tags=["roman", "conversion"], icpc=["2023 C", "2024 E", "2025 G"], requires=["_ROMAN"])
def to_roman(n: int) -> str:
    """Canonical Roman numeral of 1 <= n <= 3999.   # Число в римскую запись.

    When to use:  output in Roman numerals; building the set of valid numerals.
    Complexity:   O(1)
    Returns:      e.g. 1994 -> 'MCMXCIV'.
    Pitfalls:     there is no zero and nothing above 3999 in the classic system -> ValueError.
    Related:      from_roman, is_valid_roman.
    ICPC-UZ:      2023 C, 2024 E, 2025 G.
    Example:
        >>> to_roman(1994), to_roman(3999), to_roman(4)
        ('MCMXCIV', 'MMMCMXCIX', 'IV')
    """
    if not 1 <= n <= 3999:
        raise ValueError(f"{n} is outside 1..3999")
    res = []
    for value, sym in _ROMAN:  # жадно от больших к меньшим
        while n >= value:
            res.append(sym)
            n -= value
    return "".join(res)


@algo(
    tags=["roman", "conversion", "validation"],
    icpc=["2023 C", "2024 E", "2025 G"],
    requires=["_ROMAN", "_VALUE", "to_roman"],
)
def from_roman(s: str) -> int:
    """Value of a CANONICAL Roman numeral; ValueError for anything else.   # Римская запись в число.

    When to use:  parse input numerals strictly ("IIII", "IC", "VV" are rejected).
    Complexity:   O(len)
    Returns:      integer 1..3999.
    Idea:         subtractive parse (smaller before larger is subtracted), then require
                  to_roman(value) == s - this rejects every non-canonical spelling.
    Related:      to_roman, is_valid_roman.
    ICPC-UZ:      2023 C, 2024 E, 2025 G.
    Example:
        >>> from_roman("MCMXCIV"), from_roman("XLII")
        (1994, 42)
        >>> from_roman("IIII")
        Traceback (most recent call last):
        ValueError: 'IIII' is not a canonical Roman numeral
    """
    total = 0
    for i, ch in enumerate(s):
        v = _VALUE.get(ch)
        if v is None:
            raise ValueError(f"{s!r} is not a canonical Roman numeral")
        nxt = _VALUE.get(s[i + 1], 0) if i + 1 < len(s) else 0
        total += -v if v < nxt else v  # меньшая цифра перед большей вычитается
    if not 1 <= total <= 3999 or to_roman(total) != s:
        raise ValueError(f"{s!r} is not a canonical Roman numeral")
    return total


@algo(
    tags=["roman", "validation"],
    icpc=["2023 C", "2024 E", "2025 G"],
    requires=["_ROMAN", "_VALUE", "to_roman", "from_roman"],
)
def is_valid_roman(s: str) -> bool:
    """Is s a canonical Roman numeral of 1..3999?   # Корректна ли римская запись.

    When to use:  splitting strings into numerals, validation.
    Complexity:   O(len)
    Returns:      True / False.
    Related:      from_roman.
    ICPC-UZ:      2023 C, 2024 E, 2025 G.
    Example:
        >>> [is_valid_roman(x) for x in ["XIV", "XIIII", "IL", "MMMM", ""]]
        [True, False, False, False, False]
    """
    try:
        from_roman(s)
    except ValueError:
        return False
    return True


@algo(
    tags=["roman", "dp", "partition"],
    icpc=["2025 G"],
    requires=["_ROMAN", "to_roman"],
    verified=False,
)
def roman_split_min_max(s: str) -> tuple[int, int] | None:
    """Fewest and most parts when cutting s into numerals.   # Разбиение на римские числа.

    When to use:  ICPC-UZ 2025 G "Governor Scroogius" as understood from its description.
    Complexity:   O(n * 15) (a numeral has at most 15 letters: MMMDCCCLXXXVIII)
    Returns:      (min parts, max parts), or None if s cannot be split.
    Idea:         dp over prefixes; a cut s[i:j] is allowed iff it is a canonical numeral.
    ICPC-UZ:      2025 G (what exactly is minimised / maximised is NOT VERIFIED).
    Example:
        >>> roman_split_min_max("XIV"), roman_split_min_max("IIII"), roman_split_min_max("A")
        ((1, 3), (2, 4), None)
    """
    # NOT VERIFIED: что именно считается в 2025 G (части или значения) - не сверено
    valid = {to_roman(v) for v in range(1, 4000)}  # все 3999 записей
    n = len(s)
    big = n + 1
    lo = [big] * (n + 1)
    hi = [-1] * (n + 1)
    lo[0] = hi[0] = 0
    for j in range(1, n + 1):
        for i in range(max(0, j - 15), j):
            if hi[i] >= 0 and s[i:j] in valid:
                lo[j] = min(lo[j], lo[i] + 1)
                hi[j] = max(hi[j], hi[i] + 1)
    return (lo[n], hi[n]) if hi[n] >= 0 and n else None


@algo(tags=["roman", "symmetry"], icpc=["2023 C"], verified=False, stub=True)
def roman_symmetry(s: str) -> bool:
    """ICPC-UZ 2023 C: symmetry of Roman numerals.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return the answer of the problem.
    Idea:         unknown which symmetry (mirror letters I, V, X, M are symmetric?) -
                  NOT VERIFIED until the statement is checked.
    ICPC-UZ:      2023 C.
    Example:
        >>> roman_symmetry("XIX")
        Traceback (most recent call last):
        NotImplementedError: ICPC-UZ 2023 C: statement not verified yet
    """
    # NOT VERIFIED: заглушка до сверки условия (этап 5)
    raise NotImplementedError("ICPC-UZ 2023 C: statement not verified yet")


@algo(tags=["roman", "factorization"], icpc=["2024 E"], verified=False, stub=True)
def roman_product_unique(n: int) -> bool:
    """ICPC-UZ 2024 E: is n uniquely a product of Roman numbers > 1?   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return whether the representation is unique.
    Idea:         factors are 2..3999; factorize n (mathx.factorize, n <= 10^18) and count
                  multiplicative partitions into factors <= 3999. NOT VERIFIED: statement
                  details (ordered or not, what "Roman" adds) unknown.
    ICPC-UZ:      2024 E.
    Example:
        >>> roman_product_unique(6)
        Traceback (most recent call last):
        NotImplementedError: ICPC-UZ 2024 E: statement not verified yet
    """
    # NOT VERIFIED: заглушка до сверки условия (этап 5)
    raise NotImplementedError("ICPC-UZ 2024 E: statement not verified yet")


@algo(tags=["roman", "construction"], icpc=["2025 G"], verified=False, stub=True)
def scroogius_shortest(n: int) -> str:
    """ICPC-UZ 2025 G: shortest lexicographically smallest string with difference n.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return the string.
    Idea:         difference of max and min splits (roman_split_min_max) equals n; search
                  by length with BFS over automaton states. NOT VERIFIED: statement unknown.
    ICPC-UZ:      2025 G "Governor Scroogius".
    Example:
        >>> scroogius_shortest(1)
        Traceback (most recent call last):
        NotImplementedError: ICPC-UZ 2025 G: statement not verified yet
    """
    # NOT VERIFIED: заглушка до сверки условия (этап 5)
    raise NotImplementedError("ICPC-UZ 2025 G: statement not verified yet")
