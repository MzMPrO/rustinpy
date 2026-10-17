"""Bucket-based sorted list: the practical order-statistics tree for CPython.

Отсортированный список на корзинах (sqrt-блоках). Замена std::multiset / ordered_set.
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right, insort
from collections.abc import Iterable, Iterator
from math import ceil, sqrt

from rustinpy._registry import algo


@algo(
    tags=["sorted-list", "ordered-set", "order-statistics", "multiset"],
    cses=["Concert Tickets (1091)", "Salary Queries (1144)", "Sliding Window Median (1076)"],
)
class SortedList:
    """Sorted multiset: add / remove / k-th / rank, bucket-based.   # Мультимножество.

    When to use:  ordered multiset with order statistics: medians, k-th, "next >= x".
    Complexity:   O(sqrt n) per operation, but buckets are C-level lists -> fast in practice
    Methods:      add(x); discard(x) -> bool; remove(x); pop(i=-1); s[i]; len(s); x in s;
                  bisect_left(x) = #(< x); bisect_right(x) = #(<= x); count(x);
                  lt(x) / le(x) / gt(x) / ge(x) -> neighbour or None
    Pitfalls:     all elements must be mutually comparable (no mixing str and int).
    Python speed: ~5-8 us per operation: 2 * 10^5 adds + 10^5 removals ~ 2.5 s.
    Related:      Treap, Fenwick.kth (when values are small integers).
    CSES:         Concert Tickets (1091), Salary Queries (1144), Sliding Window Median (1076).
    Example:
        >>> s = SortedList([5, 1, 3, 3])
        >>> s.add(4); list(s), s[1], s[-1]
        ([1, 3, 3, 4, 5], 3, 5)
        >>> s.bisect_left(3), s.bisect_right(3), s.count(3), s.ge(4), s.lt(1)
        (1, 3, 2, 4, None)
        >>> s.discard(3), s.pop(0), list(s)
        (True, 1, [3, 4, 5])
    """

    BUCKET_RATIO = 16
    SPLIT_RATIO = 24

    def __init__(self, a: Iterable[int] = ()) -> None:
        items = sorted(a)
        n = len(items)
        nb = ceil(sqrt(n / self.BUCKET_RATIO)) if n else 0
        # корзины примерно по sqrt(16 n) элементов
        self.a: list[list[int]] = [items[n * i // nb : n * (i + 1) // nb] for i in range(nb)]
        self.size = n

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[int]:
        for bucket in self.a:
            yield from bucket

    def _bucket(self, x: int) -> tuple[list[int], int]:
        for i, b in enumerate(self.a):  # первая корзина, где может лежать x
            if x <= b[-1]:
                return b, i
        return self.a[-1], len(self.a) - 1

    def __contains__(self, x: int) -> bool:
        if not self.size:
            return False
        b, _ = self._bucket(x)
        i = bisect_left(b, x)
        return i != len(b) and b[i] == x

    def add(self, x: int) -> None:
        if not self.size:
            self.a = [[x]]
            self.size = 1
            return
        b, i = self._bucket(x)
        insort(b, x)
        self.size += 1
        if len(b) > len(self.a) * self.SPLIT_RATIO:  # корзина разрослась - делим
            mid = len(b) >> 1
            self.a[i : i + 1] = [b[:mid], b[mid:]]

    def _pop_at(self, b: list[int], bi: int, i: int) -> int:
        x = b.pop(i)
        self.size -= 1
        if not b:
            del self.a[bi]
        return x

    def discard(self, x: int) -> bool:
        if not self.size:
            return False
        b, bi = self._bucket(x)
        i = bisect_left(b, x)
        if i == len(b) or b[i] != x:
            return False
        self._pop_at(b, bi, i)
        return True

    def remove(self, x: int) -> None:
        if not self.discard(x):
            raise ValueError(f"{x} not in SortedList")

    def __getitem__(self, i: int) -> int:
        if i < 0:
            for b in reversed(self.a):
                i += len(b)
                if i >= 0:
                    return b[i]
        else:
            for b in self.a:
                if i < len(b):
                    return b[i]
                i -= len(b)
        raise IndexError("SortedList index out of range")

    def pop(self, i: int = -1) -> int:
        if i < 0:
            for bi in range(len(self.a) - 1, -1, -1):
                b = self.a[bi]
                i += len(b)
                if i >= 0:
                    return self._pop_at(b, bi, i)
        else:
            for bi, b in enumerate(self.a):
                if i < len(b):
                    return self._pop_at(b, bi, i)
                i -= len(b)
        raise IndexError("pop index out of range")

    def bisect_left(self, x: int) -> int:
        res = 0
        for b in self.a:
            if b[-1] >= x:
                return res + bisect_left(b, x)
            res += len(b)
        return res

    def bisect_right(self, x: int) -> int:
        res = 0
        for b in self.a:
            if b[-1] > x:
                return res + bisect_right(b, x)
            res += len(b)
        return res

    def count(self, x: int) -> int:
        return self.bisect_right(x) - self.bisect_left(x)

    def lt(self, x: int) -> int | None:
        for b in reversed(self.a):
            if b[0] < x:
                return b[bisect_left(b, x) - 1]
        return None

    def le(self, x: int) -> int | None:
        for b in reversed(self.a):
            if b[0] <= x:
                return b[bisect_right(b, x) - 1]
        return None

    def gt(self, x: int) -> int | None:
        for b in self.a:
            if b[-1] > x:
                return b[bisect_right(b, x)]
        return None

    def ge(self, x: int) -> int | None:
        for b in self.a:
            if b[-1] >= x:
                return b[bisect_left(b, x)]
        return None
