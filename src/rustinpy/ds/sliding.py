"""Sliding windows: monotonic queue, min stack, two-stack queue and window statistics.

Скользящее окно. Ответ для каждого окна a[i:i+k], i = 0..n-k.
"""

from __future__ import annotations

import heapq
from collections import deque
from typing import Callable, Generic, TypeVar

from rustinpy._registry import algo

T = TypeVar("T")


@algo(tags=["monotonic-queue", "sliding-window", "deque"], cses=["Sliding Window Minimum (3221)"])
class MonotonicQueue:
    """FIFO queue with O(1) amortised min (or max).   # Монотонная очередь.

    When to use:  sliding window minimum/maximum, DP with "min over the last k states".
    Complexity:   O(1) amortised per operation
    Methods:      push(x); pop() (removes the oldest element); top() -> min (or max); len(q)
    Related:      MinStack, TwoStackQueue, sliding_window_min.
    CSES:         Sliding Window Minimum (3221).
    Example:
        >>> q = MonotonicQueue()
        >>> for x in [4, 2, 5]: q.push(x)
        >>> q.top(); q.pop(); q.pop(); q.top()
        2
        5
    """

    def __init__(self, largest: bool = False) -> None:
        self.q: deque[tuple[int, int]] = deque()  # (значение, номер), значения монотонны
        self.head = 0
        self.tail = 0
        self.sign = -1 if largest else 1

    def push(self, x: int) -> None:
        v = x * self.sign
        q = self.q
        while q and q[-1][0] >= v:  # хвост хуже нового - он никогда не станет ответом
            q.pop()
        q.append((v, self.tail))
        self.tail += 1

    def pop(self) -> None:
        if self.q and self.q[0][1] == self.head:
            self.q.popleft()
        self.head += 1

    def top(self) -> int:
        return self.q[0][0] * self.sign

    def __len__(self) -> int:
        return self.tail - self.head


@algo(tags=["stack", "min-stack"], cses=["- (stack with minimum)"])
class MinStack:
    """Stack with O(1) minimum.   # Стек минимумов.

    When to use:  undo-able minimum; building block of the two-stack queue.
    Complexity:   O(1) per operation
    Methods:      push(x); pop() -> x; min(); len(s)
    Related:      MonotonicQueue, TwoStackQueue.
    CSES:         - (stack with minimum)
    Example:
        >>> s = MinStack()
        >>> for x in [3, 1, 2]: s.push(x)
        >>> s.min(), s.pop(), s.pop(), s.min()
        (1, 2, 1, 3)
    """

    def __init__(self) -> None:
        self.st: list[tuple[int, int]] = []  # (значение, минимум до него)

    def push(self, x: int) -> None:
        m = min(x, self.st[-1][1]) if self.st else x
        self.st.append((x, m))

    def pop(self) -> int:
        return self.st.pop()[0]

    def min(self) -> int:
        return self.st[-1][1]

    def __len__(self) -> int:
        return len(self.st)


@algo(
    tags=["queue", "two-stacks", "sliding-window", "monoid"],
    cses=["Sliding Window Or (3405)"],
    requires=["T"],
)
class TwoStackQueue(Generic[T]):
    """Queue with O(1) amortised aggregate for any associative op.   # Очередь на двух стеках.

    When to use:  window aggregate for ops without inverse: or, and, gcd, min, matrix product.
    Complexity:   O(1) amortised per operation
    Methods:      push(x); pop(); query() = op over all elements (oldest first); len(q)
    Related:      MonotonicQueue (min/max only), MinStack.
    CSES:         Sliding Window Or (3405).
    Example:
        >>> from math import gcd
        >>> q = TwoStackQueue(gcd, 0)
        >>> for x in [12, 18, 8]: q.push(x)
        >>> q.query(); q.pop(); q.query()
        2
        2
    """

    def __init__(self, op: Callable[[T, T], T], e: T) -> None:
        self.op, self.e = op, e
        self.front: list[tuple[T, T]] = []  # (значение, агрегат от него до конца front)
        self.back: list[T] = []
        self.back_agg = e

    def push(self, x: T) -> None:
        self.back.append(x)
        self.back_agg = self.op(self.back_agg, x)

    def pop(self) -> None:
        if not self.front:  # перекладываем back в front с суффиксными агрегатами
            agg = self.e
            for x in reversed(self.back):
                agg = self.op(x, agg)
                self.front.append((x, agg))
            self.back.clear()
            self.back_agg = self.e
        self.front.pop()

    def query(self) -> T:
        left = self.front[-1][1] if self.front else self.e
        return self.op(left, self.back_agg)

    def __len__(self) -> int:
        return len(self.front) + len(self.back)


@algo(tags=["sliding-window", "prefix-sums"], cses=["Sliding Window Sum (3220)"])
def sliding_window_sum(a: list[int], k: int) -> list[int]:
    """Sum of every window of length k.   # Сумма в окне.

    When to use:  window sums; generalises to any invertible op (xor, + mod p).
    Complexity:   O(n)
    Returns:      list of n - k + 1 sums.
    Related:      sliding_window_xor, prefix_sums.
    CSES:         Sliding Window Sum (3220).
    Example:
        >>> sliding_window_sum([1, 2, 3, 4, 5], 3)
        [6, 9, 12]
    """
    s = sum(a[:k])
    res = [s]
    for i in range(k, len(a)):
        s += a[i] - a[i - k]  # вошёл справа, вышел слева
        res.append(s)
    return res if k <= len(a) else []


@algo(tags=["sliding-window", "deque", "range-min"], cses=["Sliding Window Minimum (3221)"])
def sliding_window_min(a: list[int], k: int) -> list[int]:
    """Minimum of every window of length k (monotonic deque).   # Минимум в окне.

    When to use:  window minimum / maximum (negate for maximum).
    Complexity:   O(n)
    Returns:      list of n - k + 1 minima.
    Related:      MonotonicQueue, SparseTable.
    CSES:         Sliding Window Minimum (3221).
    Example:
        >>> sliding_window_min([4, 2, 5, 1, 3], 2)
        [2, 2, 1, 1]
    """
    dq: deque[int] = deque()  # индексы, значения возрастают
    res = []
    for i, x in enumerate(a):
        while dq and a[dq[-1]] >= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()  # вышел из окна
        if i >= k - 1:
            res.append(a[dq[0]])
    return res


@algo(tags=["sliding-window", "xor", "prefix-sums"], cses=["Sliding Window Xor (3426)"])
def sliding_window_xor(a: list[int], k: int) -> list[int]:
    """Xor of every window of length k.   # Xor в окне.

    When to use:  xor is its own inverse: prefix xors.
    Complexity:   O(n)
    Returns:      list of n - k + 1 xors.
    CSES:         Sliding Window Xor (3426).
    Example:
        >>> sliding_window_xor([1, 2, 3, 4], 2)
        [3, 1, 7]
    """
    x = 0
    res = []
    for i, v in enumerate(a):
        x ^= v
        if i >= k:
            x ^= a[i - k]  # убираем вышедший элемент
        if i >= k - 1:
            res.append(x)
    return res


@algo(
    tags=["sliding-window", "or", "two-stacks"],
    cses=["Sliding Window Or (3405)"],
    requires=["T", "TwoStackQueue"],
)
def sliding_window_or(a: list[int], k: int) -> list[int]:
    """Bitwise or of every window of length k (two-stack queue).   # Or в окне.

    When to use:  window aggregate of a non-invertible op.
    Complexity:   O(n) amortised
    Returns:      list of n - k + 1 values.
    Related:      TwoStackQueue.
    CSES:         Sliding Window Or (3405).
    Example:
        >>> sliding_window_or([1, 2, 4, 1], 2)
        [3, 6, 5]
    """
    q: TwoStackQueue[int] = TwoStackQueue(lambda x, y: x | y, 0)
    res = []
    for i, v in enumerate(a):
        q.push(v)
        if i >= k:
            q.pop()  # окно не длиннее k
        if i >= k - 1:
            res.append(q.query())
    return res


@algo(
    tags=["sliding-window", "distinct", "counting"], cses=["Sliding Window Distinct Values (3222)"]
)
def sliding_window_distinct(a: list[int], k: int) -> list[int]:
    """Number of distinct values in every window.   # Различные значения в окне.

    When to use:  counts in a moving window.
    Complexity:   O(n) expected
    Returns:      list of n - k + 1 counts.
    CSES:         Sliding Window Distinct Values (3222).
    Example:
        >>> sliding_window_distinct([1, 2, 1, 3, 3], 3)
        [2, 3, 2]
    """
    cnt: dict[int, int] = {}
    res = []
    for i, v in enumerate(a):
        cnt[v] = cnt.get(v, 0) + 1
        if i >= k:
            old = a[i - k]
            cnt[old] -= 1
            if cnt[old] == 0:
                del cnt[old]  # значение ушло из окна
        if i >= k - 1:
            res.append(len(cnt))
    return res


@algo(tags=["sliding-window", "mode", "heap"], cses=["Sliding Window Mode (3224)"])
def sliding_window_mode(a: list[int], k: int) -> list[int]:
    """Most frequent value of every window (smallest on ties).   # Мода в окне.

    When to use:  window mode; lazy-deletion heap keyed by (-count, value).
    Complexity:   O(n log n)
    Returns:      list of n - k + 1 modes.
    Related:      sliding_window_distinct.
    CSES:         Sliding Window Mode (3224).
    Example:
        >>> sliding_window_mode([1, 2, 2, 1, 1], 3)
        [2, 2, 1]
    """
    cnt: dict[int, int] = {}
    heap: list[tuple[int, int]] = []
    res = []
    for i, v in enumerate(a):
        cnt[v] = cnt.get(v, 0) + 1
        heapq.heappush(heap, (-cnt[v], v))
        if i >= k:
            old = a[i - k]
            cnt[old] -= 1
            heapq.heappush(heap, (-cnt[old], old))
        if i >= k - 1:
            while -heap[0][0] != cnt[heap[0][1]]:  # устаревшая запись
                heapq.heappop(heap)
            res.append(heap[0][1])
    return res


@algo(tags=["sliding-window", "mex", "heap"], cses=["Sliding Window Mex (3219)"])
def sliding_window_mex(a: list[int], k: int) -> list[int]:
    """Mex (smallest missing non-negative integer) of every window.   # Mex в окне.

    When to use:  window mex; only values 0..k matter (mex <= k).
    Complexity:   O(n log k)
    Returns:      list of n - k + 1 values.
    Related:      subarray_mex_offline.
    CSES:         Sliding Window Mex (3219).
    Example:
        >>> sliding_window_mex([0, 1, 3, 0, 2], 3)
        [2, 2, 1]
    """
    cnt = [0] * (k + 1)
    missing = list(range(k + 1))  # куча кандидатов в mex (с ленивым удалением)
    res = []
    for i, v in enumerate(a):
        if v <= k:
            cnt[v] += 1
        if i >= k:
            old = a[i - k]
            if old <= k:
                cnt[old] -= 1
                if cnt[old] == 0:
                    heapq.heappush(missing, old)
        if i >= k - 1:
            while cnt[missing[0]]:
                heapq.heappop(missing)
            res.append(missing[0])
    return res


@algo(tags=["sliding-window", "inversions", "fenwick"], cses=["Sliding Window Inversions (3223)"])
def sliding_window_inversions(a: list[int], k: int) -> list[int]:
    """Number of inversions inside every window.   # Инверсии в окне.

    When to use:  window inversions; Fenwick over compressed values.
    Complexity:   O(n log n)
    Returns:      list of n - k + 1 inversion counts.
    Related:      Fenwick.
    CSES:         Sliding Window Inversions (3223).
    Example:
        >>> sliding_window_inversions([3, 1, 2, 5, 4], 3)
        [2, 0, 1]
    """
    comp = {v: i for i, v in enumerate(sorted(set(a)))}
    b = [comp[x] for x in a]
    m = len(comp)
    t = [0] * (m + 1)

    def add(i: int, d: int) -> None:
        i += 1
        while i <= m:
            t[i] += d
            i += i & -i

    def pref(i: int) -> int:  # сколько элементов окна со значением < i
        s = 0
        while i > 0:
            s += t[i]
            i -= i & -i
        return s

    inv = 0
    size = 0
    res = []
    for i, v in enumerate(b):
        inv += size - pref(v + 1)  # новый справа: больших слева
        add(v, 1)
        size += 1
        if i >= k:
            old = b[i - k]
            add(old, -1)
            size -= 1
            inv -= pref(old)  # уходит слева: меньших справа
        if i >= k - 1:
            res.append(inv)
    return res


@algo(tags=["two-pointers", "distinct", "window"], icpc=["2023 G"], cses=["Playlist (1141)"])
def longest_window_no_repeats(s: str) -> int:
    """Length of the longest substring without repeated characters.   # Окно без повторов.

    When to use:  two pointers with "no duplicates" condition (building block of ICPC-UZ
                  2023 G "Generic Strings").
    Complexity:   O(n)
    Returns:      maximum window length (0 for an empty string).
    Related:      sliding_window_distinct, sorting.playlist.
    CSES:         Playlist (1141).
    ICPC-UZ:      2023 G (building block).
    Example:
        >>> longest_window_no_repeats("abcabcbb"), longest_window_no_repeats("")
        (3, 0)
    """
    last: dict[str, int] = {}
    best = left = 0
    for i, ch in enumerate(s):
        if last.get(ch, -1) >= left:
            left = last[ch] + 1  # сдвигаем левый край за повтор
        last[ch] = i
        best = max(best, i - left + 1)
    return best
