"""Templates for interactive problems.

Интерактивные задачи: каждый запрос печатаем с flush, на "-1" или EOF сразу выходим.

Adaptive interactor notes (see ADAPTIVE_NOTE).
"""

from __future__ import annotations

import sys
from functools import cmp_to_key
from typing import Callable, TextIO

from rustinpy._registry import algo

__all__ = [
    "ADAPTIVE_NOTE",
    "answer",
    "colored_chairs",
    "find_hidden_rectangle",
    "hidden_permutation",
    "interactive_bisect",
    "inversion_sorting",
    "kth_highest_score",
    "make_ask",
    "permuted_binary_strings",
]

ADAPTIVE_NOTE = """\
Adaptive interactor (адаптивный интерактор):
- the hidden answer may change while staying consistent with all previous replies;
  so the strategy must be correct for EVERY consistent answer (worst case), not on average.
- randomised strategies help only against a fixed hidden answer, never against adaptive ones.
- count queries: binary search over [1, 10^9] needs 30, over two coordinates 60, four sides 120.
- always flush after each query; read "-1" -> exit immediately (otherwise you get TLE, not WA).
- never read the whole input at once (FastReader) - it blocks waiting for EOF.
"""


@algo(tags=["interactive", "template"], icpc=["2023 I", "2024 F", "2024 J", "2025 J"])
def make_ask(inp: TextIO | None = None, out: TextIO | None = None) -> Callable[[str], str]:
    """Build ask(query) -> reply with flush and -1/EOF handling.   # Запрос к интерактору.

    When to use:  every interactive problem; pass ask into your solving function.
    Complexity:   O(1) per query (plus I/O latency)
    Returns:      function ask(query: str) -> str (stripped reply line).
    Pitfalls:     reply "-1" or EOF -> SystemExit(0) at once; reading on would hang (TLE).
    Related:      answer, interactive_bisect, ADAPTIVE_NOTE.
    CSES:         Hidden Integer and the whole Interactive Problems section.
    ICPC-UZ:      2023 I, 2024 F, 2024 J, 2025 J.
    Example:
        >>> import io
        >>> sent = io.StringIO()
        >>> ask = make_ask(io.StringIO("YES\\n-1\\n"), sent)
        >>> ask("? 5")
        'YES'
        >>> sent.getvalue()
        '? 5\\n'
        >>> try:
        ...     ask("? 6")
        ... except SystemExit as e:
        ...     print("exit", e.code)
        exit 0
    """
    fin = inp if inp is not None else sys.stdin
    fout = out if out is not None else sys.stdout

    def ask(query: str) -> str:
        fout.write(query + "\n")
        fout.flush()  # без flush интерактор не увидит запрос
        line = fin.readline()
        if not line or line.strip() == "-1":
            raise SystemExit(0)  # ошибка или конец ввода: выходим сразу
        return line.strip()

    return ask


@algo(tags=["interactive"], cses=["- (all interactive problems)"])
def answer(line: str, out: TextIO | None = None) -> None:
    """Print the final answer line and flush.   # Вывести ответ с flush.

    When to use:  "! x" at the end of an interactive solution.
    Complexity:   O(len(line))
    Returns:      None
    CSES:         - (all interactive problems)
    Example:
        >>> import io
        >>> buf = io.StringIO()
        >>> answer("! 7", buf)
        >>> buf.getvalue()
        '! 7\\n'
    """
    fout = out if out is not None else sys.stdout
    fout.write(line + "\n")
    fout.flush()


@algo(tags=["interactive", "binary-search"], cses=["Hidden Integer (3112)"])
def interactive_bisect(lo: int, hi: int, pred: Callable[[int], bool]) -> int:
    """Smallest x in [lo, hi] with pred(x) True, pred monotone.   # Бинпоиск по ответу.

    When to use:  "guess the number" style queries: pred(x) = ask(f"? {x}") == "YES".
    Complexity:   ceil(log2(hi - lo + 1)) calls of pred
    Input:        pred is False...False True...True on [lo, hi].
    Returns:      first x with pred(x); hi + 1 if pred is never True (pred(hi) is never asked
                  twice, but it IS asked if needed).
    Pitfalls:     think which side the reply refers to: "x > hidden" vs "x >= hidden".
    Related:      sorting.bisect_answer (offline version).
    CSES:         Hidden Integer (3112).
    Example:
        >>> hidden = 37
        >>> asked = []
        >>> def pred(x):
        ...     asked.append(x)
        ...     return x >= hidden
        >>> interactive_bisect(1, 10**9, pred), len(asked) <= 30
        (37, True)
    """
    hi += 1  # ищем на полуинтервале [lo, hi)
    while lo < hi:
        mid = (lo + hi) // 2
        if pred(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


@algo(
    tags=["interactive", "binary-search", "2d"],
    icpc=["2024 F"],
    requires=["interactive_bisect"],
    verified=False,
)
def find_hidden_rectangle(
    n: int, count: Callable[[int, int, int, int], int]
) -> tuple[int, int, int, int]:
    """Locate a hidden axis-parallel rectangle by 4 binary searches.   # Поиск прямоугольника.

    When to use:  hidden rectangle in [1, n] x [1, n], query = "how many of its cells lie in
                  my rectangle (x1, y1, x2, y2)" (or "does it intersect").
    Complexity:   4 * ceil(log2 n) queries: n = 10^9 -> 120 <= 125
    Input:        count(x1, y1, x2, y2) > 0 iff the query rectangle meets the hidden one.
    Returns:      (x1, y1, x2, y2) of the hidden rectangle, 1-based, inclusive.
    Pitfalls:     only the "> 0" property is used; with "contains entirely" replies the
                  searches must be rewritten.
    Idea:         left edge = first x with count(1, 1, x, n) > 0; right edge = last x with
                  count(x, 1, n, n) > 0; the same for y.
    ICPC-UZ:      2024 F (10^9 x 10^9, 125 queries).
    Example:
        >>> X1, Y1, X2, Y2 = 3, 5, 8, 6
        >>> def count(a, b, c, d):
        ...     w = max(0, min(c, X2) - max(a, X1) + 1)
        ...     h = max(0, min(d, Y2) - max(b, Y1) + 1)
        ...     return w * h
        >>> find_hidden_rectangle(10, count)
        (3, 5, 8, 6)
    """
    # NOT VERIFIED: точный тип запроса в 2024 F неизвестен, шаблон для ответа "пересекает ли"
    x1 = interactive_bisect(1, n, lambda x: count(1, 1, x, n) > 0)
    y1 = interactive_bisect(1, n, lambda y: count(1, 1, n, y) > 0)
    # правый край: последний x с count(x, 1, n, n) > 0 = (первый x с нулём) - 1
    x2 = interactive_bisect(1, n, lambda x: count(x, 1, n, n) == 0) - 1
    y2 = interactive_bisect(1, n, lambda y: count(1, y, n, n) == 0) - 1
    return x1, y1, x2, y2


@algo(tags=["interactive", "sorting"], cses=["Hidden Permutation (3139)"])
def hidden_permutation(n: int, less: Callable[[int, int], bool]) -> list[int]:
    """Recover a permutation from "is p[i] < p[j]?" queries.   # Восстановить перестановку.

    When to use:  only pairwise comparisons of hidden values are allowed.
    Complexity:   O(n log n) queries (Timsort comparisons)
    Input:        less(i, j) for 0-based positions i != j.
    Returns:      p with values 1..n.
    Pitfalls:     cache replies if the same pair can be asked twice and queries are scarce.
    CSES:         Hidden Permutation (3139).
    Example:
        >>> hidden = [3, 1, 4, 2]
        >>> hidden_permutation(4, lambda i, j: hidden[i] < hidden[j])
        [3, 1, 4, 2]
    """

    def cmp(i: int, j: int) -> int:
        return -1 if less(i, j) else 1  # один запрос на сравнение

    order = sorted(range(n), key=cmp_to_key(cmp))
    p = [0] * n
    for rank, idx in enumerate(order, 1):  # позиция в порядке = значение
        p[idx] = rank
    return p


@algo(tags=["interactive", "binary-search"], cses=["K-th Highest Score (3305)"], verified=False)
def kth_highest_score(
    n: int, m: int, k: int, get_a: Callable[[int], int], get_b: Callable[[int], int]
) -> int:
    """k-th largest value of two hidden descending arrays.   # k-й максимум двух массивов.

    When to use:  two sorted hidden lists, only point reads, O(log) reads allowed.
    Complexity:   O(log min(n, m)) reads
    Input:        a (length n) and b (length m) sorted descending; 1 <= k <= n + m.
    Returns:      the k-th largest element of the union (with repetitions).
    Idea:         binary search on i = how many come from a: valid when
                  a[i-1] >= b[k-i] and b[k-i-1] >= a[i].
    CSES:         K-th Highest Score (3305) - exact interaction format NOT VERIFIED.
    Example:
        >>> a, b = [9, 7, 3], [8, 4, 2, 1]
        >>> [kth_highest_score(3, 4, k, a.__getitem__, b.__getitem__) for k in range(1, 8)]
        [9, 8, 7, 4, 3, 2, 1]
    """
    # NOT VERIFIED: номер и формат задачи CSES не сверены с условием
    neg = -(1 << 62)
    pos = 1 << 62

    def a_at(i: int) -> int:
        return pos if i < 0 else (neg if i >= n else get_a(i))

    def b_at(j: int) -> int:
        return pos if j < 0 else (neg if j >= m else get_b(j))

    lo, hi = max(0, k - m), min(k, n)
    while lo < hi:
        i = (lo + hi) // 2  # i элементов из a, k - i из b
        if a_at(i) > b_at(k - i - 1):
            lo = i + 1  # из a можно взять больше
        else:
            hi = i
    i = lo
    return min(a_at(i - 1), b_at(k - i - 1))


@algo(tags=["interactive", "binary-search"], cses=["Colored Chairs (3273)"], verified=False)
def colored_chairs(n: int, color: Callable[[int], str]) -> int:
    """Find i with color(i) == color((i+1) % n) on an odd circle.   # Соседние одинаковые стулья.

    When to use:  odd cycle of two colours, few queries: such a pair always exists.
    Complexity:   about log2(n) + 2 queries
    Input:        n odd, chairs 0..n-1 around a circle.
    Returns:      i such that chairs i and (i + 1) % n have the same colour.
    Idea:         on a path l..r a perfect alternation gives c[l] == c[r] iff r - l is even;
                  if this fails, an equal adjacent pair is inside; halve the path.
    CSES:         Colored Chairs (3273) - exact interaction format NOT VERIFIED.
    Example:
        >>> chairs = "RBRBBRB"
        >>> i = colored_chairs(7, chairs.__getitem__)
        >>> chairs[i] == chairs[(i + 1) % 7]
        True
    """
    # NOT VERIFIED: номер и формат задачи CSES не сверены с условием
    lo, hi = 0, n - 1
    c_lo, c_hi = color(lo), color(hi)
    if c_lo == c_hi:
        return n - 1  # стулья n-1 и 0 соседние
    # инвариант: на пути lo..hi чередование нарушено
    while hi - lo > 1:
        mid = (lo + hi) // 2
        c_mid = color(mid)
        if (c_lo == c_mid) != ((mid - lo) % 2 == 0):
            hi, c_hi = mid, c_mid
        else:
            lo, c_lo = mid, c_mid
    return lo


@algo(tags=["interactive"], cses=["Permuted Binary Strings"], verified=False, stub=True)
def permuted_binary_strings(n: int, ask: Callable[[str], str]) -> list[int]:
    """CSES Permuted Binary Strings - not implemented yet.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return the hidden permutation.
    Idea:         query strings whose bit k is the k-th bit of the index (log n queries) and
                  read the permuted bits back - NOT VERIFIED, statement not checked.
    CSES:         Permuted Binary Strings.
    Example:
        >>> permuted_binary_strings(1, lambda q: "")
        Traceback (most recent call last):
        NotImplementedError: Permuted Binary Strings: statement not verified yet
    """
    # NOT VERIFIED: заглушка, условие задачи не сверено
    raise NotImplementedError("Permuted Binary Strings: statement not verified yet")


@algo(tags=["interactive"], cses=["Inversion Sorting"], verified=False, stub=True)
def inversion_sorting(n: int, ask: Callable[[str], str]) -> None:
    """CSES Inversion Sorting - not implemented yet.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      None
    Idea:         unknown yet - statement not checked (NOT VERIFIED).
    CSES:         Inversion Sorting.
    Example:
        >>> inversion_sorting(1, lambda q: "")
        Traceback (most recent call last):
        NotImplementedError: Inversion Sorting: statement not verified yet
    """
    # NOT VERIFIED: заглушка, условие задачи не сверено
    raise NotImplementedError("Inversion Sorting: statement not verified yet")
