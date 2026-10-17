"""CSES Sorting and Searching: binary search on the answer, two pointers, sweeps, greedy
scheduling, Josephus, nested ranges, subarray counting, meet in the middle, window medians.

Сортировка и поиск. Индексы 0-based (CSES часто печатает 1-based - прибавьте 1).
"""

from __future__ import annotations

import heapq
from bisect import bisect_left, bisect_right
from collections import deque
from typing import Callable

from rustinpy._registry import algo


@algo(tags=["binary-search", "answer"], cses=["Factory Machines (1620)", "Array Division (1085)"])
def bisect_answer(lo: int, hi: int, ok: Callable[[int], bool]) -> int:
    """Smallest x in [lo, hi] with ok(x) True (ok monotone).   # Бинпоиск по ответу.

    When to use:  "minimal time / size / capacity such that it works".
    Complexity:   O(log(hi - lo)) calls of ok
    Returns:      first x with ok(x); hi + 1 if none.
    Pitfalls:     make sure ok is monotone; pick hi so that ok(hi) is surely True.
    Related:      bisect_answer_max, bisect_real, interactive.interactive_bisect.
    CSES:         Factory Machines (1620), Array Division (1085).
    Example:
        >>> bisect_answer(0, 100, lambda x: x * x >= 50)
        8
    """
    hi += 1
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid  # ответ не правее mid
        else:
            lo = mid + 1
    return lo


@algo(tags=["binary-search", "answer"], cses=["- (largest feasible value)"])
def bisect_answer_max(lo: int, hi: int, ok: Callable[[int], bool]) -> int:
    """Largest x in [lo, hi] with ok(x) True (ok monotone).   # Бинпоиск: максимум.

    When to use:  "maximal value that still works".
    Complexity:   O(log(hi - lo)) calls of ok
    Returns:      last x with ok(x); lo - 1 if none.
    Related:      bisect_answer.
    CSES:         - (largest feasible value)
    Example:
        >>> bisect_answer_max(0, 100, lambda x: x * x <= 50)
        7
    """
    lo -= 1
    while lo < hi:
        mid = (lo + hi + 1) // 2  # верхняя середина, чтобы не зациклиться
        if ok(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


@algo(tags=["binary-search", "real"], cses=["- (real-valued answers)"])
def bisect_real(lo: float, hi: float, ok: Callable[[float], bool], iters: int = 100) -> float:
    """Boundary of a monotone predicate on reals.   # Бинпоиск по вещественным числам.

    When to use:  real answers with required absolute / relative precision.
    Complexity:   O(iters) calls of ok
    Returns:      approximately the smallest x with ok(x).
    Pitfalls:     iterate a fixed number of times, not "while hi - lo > eps" (may hang).
    Related:      bisect_answer.
    CSES:         - (real-valued answers)
    Example:
        >>> round(bisect_real(0.0, 2.0, lambda x: x * x >= 2), 9)
        1.414213562
    """
    for _ in range(iters):
        mid = (lo + hi) / 2
        if ok(mid):
            hi = mid
        else:
            lo = mid
    return hi


@algo(tags=["two-pointers", "greedy", "sorting"], cses=["Ferris Wheel (1090)"])
def ferris_wheel(w: list[int], x: int) -> int:
    """Min gondolas, each holds <= 2 children with total weight <= x.   # Колесо обозрения.

    When to use:  pair the heaviest with the lightest when possible.
    Complexity:   O(n log n)
    Returns:      number of gondolas.
    CSES:         Ferris Wheel (1090).
    Example:
        >>> ferris_wheel([7, 2, 3, 9], 10)
        3
    """
    a = sorted(w)
    i, j = 0, len(a) - 1
    res = 0
    while i <= j:
        if i < j and a[i] + a[j] <= x:
            i += 1  # самый лёгкий едет с самым тяжёлым
        j -= 1
        res += 1
    return res


@algo(tags=["two-pointers", "greedy", "matching"], cses=["Apartments (1084)"])
def apartments(want: list[int], sizes: list[int], k: int) -> int:
    """Max applicants matched to apartments with |size - want| <= k.   # Квартиры.

    When to use:  greedy matching of two sorted lists.
    Complexity:   O(n log n + m log m)
    Returns:      maximal number of matches.
    CSES:         Apartments (1084).
    Example:
        >>> apartments([60, 45, 80, 60], [30, 60, 75], 5)
        2
    """
    a, b = sorted(want), sorted(sizes)
    i = j = res = 0
    while i < len(a) and j < len(b):
        if abs(a[i] - b[j]) <= k:
            res += 1  # подходит - заселяем
            i += 1
            j += 1
        elif b[j] < a[i] - k:
            j += 1  # квартира слишком мала для всех оставшихся
        else:
            i += 1  # претендент не получит квартиру
    return res


@algo(tags=["dsu", "greedy", "binary-search"], cses=["Concert Tickets (1091)"])
def concert_tickets(prices: list[int], max_pay: list[int]) -> list[int]:
    """Each customer buys the most expensive ticket not above their limit.   # Билеты на концерт.

    When to use:  multiset "predecessor and delete": sorted array + DSU skipping sold tickets.
    Complexity:   O((n + m) log n)
    Returns:      price paid by every customer or -1.
    Related:      ds.SortedList.
    CSES:         Concert Tickets (1091).
    Example:
        >>> concert_tickets([5, 3, 7, 8, 5], [4, 8, 3])
        [3, 8, -1]
    """
    h = sorted(prices)
    parent = list(range(len(h) + 1))  # parent[i + 1] - ближайший непроданный слева, 0 - нет

    def find(x: int) -> int:
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:  # сжатие путей
            parent[x], x = root, parent[x]
        return root

    res = []
    for t in max_pay:
        i = find(bisect_right(h, t))  # позиция (1-based) самого дорогого допустимого
        if i == 0:
            res.append(-1)
        else:
            res.append(h[i - 1])
            parent[i] = i - 1  # билет продан
    return res


@algo(tags=["sweep-line", "events"], cses=["Restaurant Customers (1619)"])
def restaurant_customers(intervals: list[tuple[int, int]]) -> int:
    """Maximum number of simultaneous visitors (arrive a, leave b).   # Посетители ресторана.

    When to use:  max overlap of intervals via sorted events.
    Complexity:   O(n log n)
    Input:        intervals (a, b); a visitor is present on [a, b) - leaving at t happens
                  before arriving at t (CSES has distinct times anyway).
    Returns:      maximal overlap.
    Related:      room_allocation.
    CSES:         Restaurant Customers (1619).
    Example:
        >>> restaurant_customers([(5, 8), (2, 4), (3, 9)])
        2
    """
    events = sorted([(a, 1) for a, _ in intervals] + [(b, -1) for _, b in intervals])
    cur = best = 0
    for _, d in events:  # при равенстве времени -1 идёт раньше +1
        cur += d
        best = max(best, cur)
    return best


@algo(tags=["greedy", "intervals", "scheduling"], cses=["Movie Festival (1629)"])
def movie_festival(intervals: list[tuple[int, int]]) -> int:
    """Max number of non-overlapping movies [a, b) (greedy by end).   # Кинофестиваль.

    When to use:  interval scheduling.
    Complexity:   O(n log n)
    Returns:      maximal number of movies.
    Related:      movie_festival_k, ds.movie_festival_queries.
    CSES:         Movie Festival (1629).
    Example:
        >>> movie_festival([(3, 5), (4, 9), (5, 8)])
        2
    """
    res, end = 0, -(1 << 62)
    for a, b in sorted(intervals, key=lambda x: x[1]):
        if a >= end:  # фильм начинается после конца предыдущего
            res += 1
            end = b
    return res


@algo(tags=["greedy", "intervals", "scheduling", "multiset"], cses=["Movie Festival II (1632)"])
def movie_festival_k(intervals: list[tuple[int, int]], k: int) -> int:
    """Max movies watched in total by k club members.   # Кинофестиваль II.

    When to use:  greedy by end; give a movie to the member who got free latest but in time.
    Complexity:   O(n log n) (+ list insertions)
    Returns:      maximal total number of watched movies.
    Related:      movie_festival.
    CSES:         Movie Festival II (1632).
    Example:
        >>> movie_festival_k([(1, 5), (8, 10), (3, 6), (2, 5), (6, 9)], 2)
        4
    """
    free: list[int] = []  # моменты освобождения участников, по возрастанию
    res = 0
    for a, b in sorted(intervals, key=lambda x: x[1]):
        i = bisect_right(free, a) - 1  # освободился позже всех, но не позже a
        if i >= 0:
            free.pop(i)
            free.insert(bisect_left(free, b), b)
            res += 1
        elif len(free) < k:
            free.insert(bisect_left(free, b), b)
            res += 1
    return res


@algo(tags=["greedy", "heap", "intervals"], cses=["Room Allocation (1164)"])
def room_allocation(intervals: list[tuple[int, int]]) -> tuple[int, list[int]]:
    """Minimal number of rooms; a room is reused only after its last day.   # Распределение комнат.

    When to use:  interval partitioning (days [a, b] inclusive).
    Complexity:   O(n log n)
    Returns:      (rooms, room number 1..rooms for every customer in input order).
    Related:      restaurant_customers.
    CSES:         Room Allocation (1164).
    Example:
        >>> room_allocation([(1, 2), (2, 4), (4, 4)])
        (2, [1, 2, 1])
    """
    order = sorted(range(len(intervals)), key=lambda i: intervals[i])
    busy: list[tuple[int, int]] = []  # (последний день, номер комнаты)
    room = [0] * len(intervals)
    rooms = 0
    for i in order:
        a, b = intervals[i]
        if busy and busy[0][0] < a:  # самая рано освободившаяся комната свободна
            _, r = heapq.heappop(busy)
        else:
            rooms += 1
            r = rooms
        room[i] = r
        heapq.heappush(busy, (b, r))
    return rooms, room


@algo(tags=["hashing", "two-sum"], cses=["Sum of Two Values (1640)"])
def sum_of_two_values(a: list[int], x: int) -> tuple[int, int] | None:
    """Two distinct indices with a[i] + a[j] = x.   # Сумма двух чисел.

    When to use:  hash map of seen values.
    Complexity:   O(n)
    Returns:      (i, j) with i < j, or None.
    Related:      sum_of_three_values, sum_of_four_values.
    CSES:         Sum of Two Values (1640).
    Example:
        >>> sum_of_two_values([2, 7, 5, 1], 8)
        (1, 3)
    """
    seen: dict[int, int] = {}
    for j, v in enumerate(a):
        i = seen.get(x - v)
        if i is not None:
            return i, j
        seen.setdefault(v, j)  # первое вхождение значения
    return None


@algo(tags=["two-pointers", "three-sum"], cses=["Sum of Three Values (1641)"])
def sum_of_three_values(a: list[int], x: int) -> tuple[int, int, int] | None:
    """Three distinct indices with a[i] + a[j] + a[k] = x.   # Сумма трёх чисел.

    When to use:  sort + two pointers for each first element.
    Complexity:   O(n^2)
    Returns:      sorted index triple or None.
    CSES:         Sum of Three Values (1641).
    Example:
        >>> sum_of_three_values([2, 7, 5, 1], 8)
        (0, 2, 3)
    """
    idx = sorted(range(len(a)), key=a.__getitem__)
    v = [a[i] for i in idx]
    n = len(v)
    for i in range(n - 2):
        lo, hi = i + 1, n - 1
        need = x - v[i]
        while lo < hi:  # два указателя на остатке
            s = v[lo] + v[hi]
            if s == need:
                return tuple(sorted((idx[i], idx[lo], idx[hi])))  # type: ignore[return-value]
            if s < need:
                lo += 1
            else:
                hi -= 1
    return None


@algo(tags=["hashing", "meet-in-the-middle", "four-sum"], cses=["Sum of Four Values (1642)"])
def sum_of_four_values(a: list[int], x: int) -> tuple[int, int, int, int] | None:
    """Four distinct indices with sum x (pair sums in a hash map).   # Сумма четырёх чисел.

    When to use:  n <= ~1000.
    Complexity:   O(n^2) expected
    Returns:      sorted index quadruple or None.
    Idea:         for every j, pairs (j, k) with k > j look up x - a[j] - a[k] among pairs
                  (p, q) with q < j; then add the pairs (i, j).
    CSES:         Sum of Four Values (1642).
    Example:
        >>> sum_of_four_values([2, 7, 5, 1, 3], 11)
        (0, 2, 3, 4)
    """
    pairs: dict[int, tuple[int, int]] = {}  # сумма -> пара индексов слева от j
    n = len(a)
    for j in range(n):
        for k in range(j + 1, n):
            p = pairs.get(x - a[j] - a[k])
            if p is not None:
                return tuple(sorted((*p, j, k)))  # type: ignore[return-value]
        for i in range(j):
            pairs.setdefault(a[i] + a[j], (i, j))
    return None


@algo(tags=["kadane", "subarray"], cses=["Maximum Subarray Sum (1643)"])
def max_subarray_sum(a: list[int]) -> int:
    """Maximum sum of a non-empty subarray (Kadane).   # Максимальная сумма подмассива.

    When to use:  classic one-pass DP.
    Complexity:   O(n)
    Returns:      maximal sum.
    Related:      max_subarray_sum_range, ds.SegTreeMaxSubarray.
    CSES:         Maximum Subarray Sum (1643).
    Example:
        >>> max_subarray_sum([-1, 3, -2, 5, 3, -5, 2, 2])
        9
    """
    best = cur = a[0]
    for v in a[1:]:
        cur = max(v, cur + v)  # продолжить или начать заново
        best = max(best, cur)
    return best


@algo(tags=["monotonic-deque", "prefix-sums", "subarray"], cses=["Maximum Subarray Sum II (1644)"])
def max_subarray_sum_range(a: list[int], lo: int, hi: int) -> int:
    """Maximum sum of a subarray with length in [lo, hi].   # Макс. сумма подмассива длины lo..hi.

    When to use:  prefix sums + sliding window minimum over the allowed starts.
    Complexity:   O(n)
    Returns:      maximal sum (requires 1 <= lo <= hi <= len(a)).
    Related:      max_subarray_sum, ds.MonotonicQueue.
    CSES:         Maximum Subarray Sum II (1644).
    Example:
        >>> max_subarray_sum_range([-1, 3, -2, 5, 3, -5, 2, 2], 1, 2)
        8
    """
    n = len(a)
    p = [0] * (n + 1)
    for i, v in enumerate(a):
        p[i + 1] = p[i] + v
    dq: deque[int] = deque()  # кандидаты l с возрастающими p[l]
    best = -(1 << 62)
    for r in range(lo, n + 1):
        l_new = r - lo
        while dq and p[dq[-1]] >= p[l_new]:
            dq.pop()
        dq.append(l_new)
        if dq[0] < r - hi:
            dq.popleft()  # слишком длинный подмассив
        best = max(best, p[r] - p[dq[0]])
    return best


@algo(tags=["median", "greedy"], cses=["Stick Lengths (1074)"])
def stick_lengths(p: list[int]) -> int:
    """Min total cost to make all sticks equal (cost = |change|).   # Длины палочек.

    When to use:  sum |x - c| is minimised at a median.
    Complexity:   O(n log n)
    Returns:      minimal cost.
    CSES:         Stick Lengths (1074).
    Example:
        >>> stick_lengths([2, 3, 1, 5, 2])
        5
    """
    s = sorted(p)
    m = s[len(s) // 2]  # медиана
    return sum(abs(x - m) for x in s)


@algo(tags=["greedy", "sorting"], cses=["Missing Coin Sum (2183)"])
def missing_coin_sum(a: list[int]) -> int:
    """Smallest sum not formed by a subset of coins.   # Наименьшая непредставимая сумма.

    When to use:  sorted greedy: reachable 1..s, next coin <= s + 1 extends the range.
    Complexity:   O(n log n)
    Returns:      the smallest non-representable positive sum.
    Related:      ds.missing_coin_sum_queries.
    CSES:         Missing Coin Sum (2183).
    Example:
        >>> missing_coin_sum([2, 9, 1, 2, 7])
        6
    """
    s = 0
    for x in sorted(a):
        if x > s + 1:
            break  # дыра в диапазоне
        s += x
    return s + 1


@algo(tags=["permutation", "counting"], cses=["Collecting Numbers (2216)"])
def collecting_numbers(a: list[int]) -> int:
    """Rounds needed to collect 1, 2, ..., n scanning left to right repeatedly.   # Сбор чисел.

    When to use:  a is a permutation of 1..n; a new round starts when pos[k+1] < pos[k].
    Complexity:   O(n)
    Returns:      number of rounds.
    CSES:         Collecting Numbers (2216).
    Example:
        >>> collecting_numbers([4, 2, 1, 5, 3])
        3
    """
    pos = [0] * (len(a) + 1)
    for i, v in enumerate(a):
        pos[v] = i
    return 1 + sum(1 for k in range(1, len(a)) if pos[k + 1] < pos[k])  # разрыв = новый проход


@algo(tags=["two-pointers", "distinct", "window"], cses=["Playlist (1141)"])
def playlist(a: list[int]) -> int:
    """Longest contiguous segment with distinct values.   # Плейлист.

    When to use:  two pointers with last-occurrence map.
    Complexity:   O(n)
    Returns:      maximal length.
    Related:      ds.longest_window_no_repeats.
    CSES:         Playlist (1141).
    Example:
        >>> playlist([1, 2, 1, 3, 2, 7, 4, 2])
        5
    """
    last: dict[int, int] = {}
    best = left = 0
    for i, v in enumerate(a):
        if last.get(v, -1) >= left:
            left = last[v] + 1  # повтор - левый край за предыдущее вхождение
        last[v] = i
        best = max(best, i - left + 1)
    return best


@algo(tags=["greedy", "binary-search", "patience"], cses=["Towers (1073)"])
def towers(a: list[int]) -> int:
    """Min number of towers (each strictly smaller cube on top) placing cubes in order.   # Башни.

    When to use:  patience sorting: put a cube on the tower with the smallest top > cube.
    Complexity:   O(n log n)
    Returns:      number of towers.
    Related:      dp.lis (dual problem).
    CSES:         Towers (1073).
    Example:
        >>> towers([3, 8, 2, 1, 5])
        2
    """
    tops: list[int] = []  # вершины башен по возрастанию
    for x in a:
        i = bisect_right(tops, x)
        if i < len(tops):
            tops[i] = x  # кладём на наименьшую вершину > x
        else:
            tops.append(x)
    return len(tops)


@algo(tags=["offline", "linked-list", "gaps"], cses=["Traffic Lights (1163)"])
def traffic_lights(x: int, positions: list[int]) -> list[int]:
    """Longest light-free passage on [0, x] after each traffic light is added.   # Светофоры.

    When to use:  offline: remove lights in reverse; gaps only grow when removing.
    Complexity:   O(n log n)
    Returns:      answers after each addition.
    CSES:         Traffic Lights (1163).
    Example:
        >>> traffic_lights(8, [3, 6, 2])
        [5, 3, 3]
    """
    pts = sorted({0, x, *positions})
    idx = {p: i for i, p in enumerate(pts)}
    prv = list(range(-1, len(pts) - 1))
    nxt = list(range(1, len(pts) + 1))
    best = max((pts[i + 1] - pts[i] for i in range(len(pts) - 1)), default=x)
    res = []
    for p in reversed(positions):  # снимаем светофоры в обратном порядке
        res.append(best)
        i = idx[p]
        a, b = prv[i], nxt[i]
        nxt[a], prv[b] = b, a
        best = max(best, pts[b] - pts[a])  # промежуток слился
    return res[::-1]


@algo(tags=["josephus", "formula"], cses=["Josephus Problem I (2162)"])
def josephus_survivor(n: int, k: int) -> int:
    """Last remaining child when every k-th is removed (children 1..n).   # Задача Иосифа: выживший.

    When to use:  survivor only: J(n) = (J(n-1) + k) mod n.
    Complexity:   O(n)
    Returns:      label 1..n of the survivor.
    Related:      josephus_order, josephus_queries.
    CSES:         Josephus Problem I (2162) (k = 2, the whole order is asked there).
    Example:
        >>> josephus_survivor(7, 2), josephus_survivor(5, 3)
        (7, 4)
    """
    res = 0
    for i in range(2, n + 1):
        res = (res + k) % i  # пересчёт номера после удаления
    return res + 1


@algo(tags=["josephus", "fenwick", "kth"], cses=["Josephus Problem II (2163)"])
def josephus_order(n: int, k: int) -> list[int]:
    """Removal order when every k-th child is removed.   # Порядок удаления (Иосиф).

    When to use:  full order for n up to 2 * 10^5 and any k.
    Complexity:   O(n log n)
    Returns:      labels 1..n in removal order.
    Pitfalls:     CSES Josephus II "skips k" -> call with k + 1.
    Related:      josephus_survivor, ds.Fenwick.
    CSES:         Josephus Problem II (2163), Josephus Problem I (k = 2).
    Example:
        >>> josephus_order(7, 2)
        [2, 4, 6, 1, 5, 3, 7]
    """
    t = [0] * (n + 1)
    for i in range(1, n + 1):  # Фенвик из единиц за O(n)
        t[i] += 1
        j = i + (i & -i)
        if j <= n:
            t[j] += t[i]
    LOG = 1 << n.bit_length()
    res = []
    cur = 0
    for remaining in range(n, 0, -1):
        cur = (cur + k - 1) % remaining  # номер удаляемого среди оставшихся
        pos, step, kk = 0, LOG, cur
        while step:
            if pos + step <= n and t[pos + step] <= kk:
                pos += step
                kk -= t[pos]
            step >>= 1
        res.append(pos + 1)
        i = pos + 1
        while i <= n:
            t[i] -= 1
            i += i & -i
    return res


@algo(tags=["josephus", "recursion-free"], cses=["Josephus Queries (2164)"])
def josephus_queries(n: int, k: int) -> int:
    """The k-th removed child when every second child is removed (n up to 10^9).   # Запросы Иосифа.

    When to use:  many queries with huge n; O(log n) each.
    Complexity:   O(log n)
    Returns:      label 1..n of the k-th removed child.
    Idea:         the first pass removes 2, 4, 6, ... (and 1 if n is odd); the rest is the
                  same game on n // 2 children with labels 2c + 1 (n odd) or 2c - 1 (n even).
    Related:      josephus_order.
    CSES:         Josephus Queries (2164).
    Example:
        >>> [josephus_queries(7, k) for k in range(1, 8)]
        [2, 4, 6, 1, 5, 3, 7]
    """
    maps: list[int] = []  # чётности n на каждом уровне спуска
    while True:
        first = (n + 1) // 2  # удалено за первый проход
        if n == 1:
            res = 1
            break
        if k <= first:
            res = 1 if 2 * k > n else 2 * k
            break
        maps.append(n % 2)
        k -= first
        n //= 2
    for odd in reversed(maps):  # обратно переводим номер в исходную нумерацию
        res = 2 * res + 1 if odd else 2 * res - 1
    return res


def _nested_counts(ranges: list[tuple[int, int]]) -> tuple[list[int], list[int]]:
    """(contains_count, contained_count) with identical ranges handled as groups."""
    n = len(ranges)
    rs = sorted({r for _, r in ranges})
    ridx = {r: i for i, r in enumerate(rs)}
    m = len(rs)
    order = sorted(range(n), key=lambda i: (ranges[i][0], -ranges[i][1]))
    groups: list[list[int]] = []
    for i in order:
        if groups and ranges[groups[-1][0]] == ranges[i]:
            groups[-1].append(i)
        else:
            groups.append([i])

    def run(seq: list[list[int]], count_greater: bool) -> list[int]:
        t = [0] * (m + 1)
        res = [0] * n
        inserted = 0
        for g in seq:
            r = ridx[ranges[g[0]][1]]
            s, j = 0, r + (0 if count_greater else 1)  # число вставленных с r' < r (или <= r)
            while j > 0:
                s += t[j]
                j -= j & -j
            q = inserted - s if count_greater else s
            for i in g:
                res[i] = q + len(g) - 1  # плюс одинаковые отрезки
            j = r + 1
            while j <= m:
                t[j] += len(g)
                j += j & -j
            inserted += len(g)
        return res

    contained = run(groups, True)  # слева по порядку: l' <= l, ищем r' >= r
    contains = run(groups[::-1], False)  # справа: l' >= l, ищем r' <= r
    return contains, contained


@algo(
    tags=["sorting", "nested-ranges", "fenwick"],
    cses=["Nested Ranges Check (2168)"],
    requires=["_nested_counts"],
)
def nested_ranges(ranges: list[tuple[int, int]]) -> tuple[list[bool], list[bool]]:
    """For each range: contains another / is contained in another.   # Вложенные отрезки.

    When to use:  sort by (l asc, r desc), prefix maximum / Fenwick over r.
    Complexity:   O(n log n)
    Returns:      (contains[i], contained[i]); identical ranges contain each other.
    Related:      nested_ranges_count.
    CSES:         Nested Ranges Check (2168).
    Example:
        >>> nested_ranges([(1, 6), (2, 4), (4, 8), (3, 6)])
        ([True, False, False, False], [False, True, False, True])
    """
    a, b = _nested_counts(ranges)
    return [x > 0 for x in a], [x > 0 for x in b]


@algo(
    tags=["sorting", "nested-ranges", "fenwick"],
    cses=["Nested Ranges Count (2169)"],
    requires=["_nested_counts"],
)
def nested_ranges_count(ranges: list[tuple[int, int]]) -> tuple[list[int], list[int]]:
    """For each range: how many it contains / how many contain it.   # Подсчёт вложенных отрезков.

    When to use:  counting version of nested_ranges.
    Complexity:   O(n log n)
    Returns:      (contains_count[i], contained_count[i]).
    Related:      nested_ranges.
    CSES:         Nested Ranges Count (2169).
    Example:
        >>> nested_ranges_count([(1, 6), (2, 4), (4, 8), (3, 6)])
        ([2, 0, 0, 0], [0, 1, 0, 1])
    """
    return _nested_counts(ranges)


@algo(
    tags=["binary-search", "answer"], cses=["Factory Machines (1620)"], requires=["bisect_answer"]
)
def factory_machines(k: int, t: list[int]) -> int:
    """Minimal time for machines with periods t to produce k products.   # Фабрика.

    When to use:  binary search on time: sum(T // t_i) >= k.
    Complexity:   O(n log(k * min t))
    Returns:      minimal time.
    Related:      bisect_answer.
    CSES:         Factory Machines (1620).
    Example:
        >>> factory_machines(7, [3, 2, 5])
        8
    """
    return bisect_answer(0, min(t) * k, lambda T: sum(T // x for x in t) >= k)


@algo(tags=["greedy", "scheduling"], cses=["Tasks and Deadlines (1630)"])
def tasks_and_deadlines(tasks: list[tuple[int, int]]) -> int:
    """Max total reward sum(d - finish) doing all tasks (duration, deadline).   # Задачи и дедлайны.

    When to use:  the order of deadlines is irrelevant: do short tasks first.
    Complexity:   O(n log n)
    Returns:      total reward (may be negative).
    CSES:         Tasks and Deadlines (1630).
    Example:
        >>> tasks_and_deadlines([(6, 10), (8, 15), (5, 12)])
        2
    """
    t = 0
    total = 0
    for a, d in sorted(tasks):  # по длительности
        t += a
        total += d - t
    return total


@algo(tags=["greedy", "math"], cses=["Reading Books (1631)"])
def reading_books(t: list[int]) -> int:
    """Minimal time for two readers to read every book.   # Чтение книг.

    When to use:  answer max(sum, 2 * max).
    Complexity:   O(n)
    Returns:      minimal total time.
    CSES:         Reading Books (1631).
    Example:
        >>> reading_books([2, 8, 3]), reading_books([2, 3, 4])
        (16, 9)
    """
    return max(sum(t), 2 * max(t))  # самая длинная книга может быть узким местом


@algo(
    tags=["binary-search", "answer", "greedy"],
    cses=["Array Division (1085)"],
    requires=["bisect_answer"],
)
def array_division(a: list[int], k: int) -> int:
    """Split into k contiguous parts minimising the maximum part sum.   # Деление массива.

    When to use:  binary search on the answer + greedy check.
    Complexity:   O(n log S)
    Returns:      minimal possible maximum sum.
    Related:      bisect_answer.
    CSES:         Array Division (1085).
    Example:
        >>> array_division([2, 4, 7, 3, 5], 3)
        8
    """

    def ok(lim: int) -> bool:
        parts, cur = 1, 0
        for v in a:
            if v > lim:
                return False
            if cur + v > lim:  # начинаем новую часть
                parts += 1
                cur = 0
            cur += v
        return parts <= k

    return bisect_answer(max(a), sum(a), ok)


@algo(tags=["prefix-sums", "hashing", "subarray"], cses=["Subarray Sums II (1661)"])
def subarray_sums_count(a: list[int], x: int) -> int:
    """Number of subarrays with sum exactly x (any signs).   # Подмассивы с суммой x.

    When to use:  prefix sums + counter of previous prefixes.
    Complexity:   O(n)
    Returns:      count.
    CSES:         Subarray Sums I (1660), Subarray Sums II (1661).
    Example:
        >>> subarray_sums_count([2, -1, 3, 5, -2], 2)
        2
    """
    cnt = {0: 1}
    s = total = 0
    for v in a:
        s += v
        total += cnt.get(s - x, 0)  # префиксы, дающие сумму x
        cnt[s] = cnt.get(s, 0) + 1
    return total


@algo(tags=["prefix-sums", "modular", "subarray"], cses=["Subarray Divisibility (1662)"])
def subarray_divisibility(a: list[int]) -> int:
    """Number of subarrays whose sum is divisible by n = len(a).   # Делимость подмассивов.

    When to use:  equal prefix sums modulo n.
    Complexity:   O(n)
    Returns:      count.
    CSES:         Subarray Divisibility (1662).
    Example:
        >>> subarray_divisibility([3, 1, 2, 7, 4])
        1
    """
    n = len(a)
    cnt = [0] * n
    cnt[0] = 1
    s = total = 0
    for v in a:
        s = (s + v) % n
        total += cnt[s]  # пары равных остатков
        cnt[s] += 1
    return total


@algo(tags=["two-pointers", "distinct", "subarray"], cses=["Subarray Distinct Values (2428)"])
def subarray_distinct_values(a: list[int], k: int) -> int:
    """Number of subarrays with at most k distinct values.   # Подмассивы с <= k различными.

    When to use:  two pointers: for each right end, the window shrinks monotonically.
    Complexity:   O(n)
    Returns:      count.
    CSES:         Subarray Distinct Values (2428).
    Example:
        >>> subarray_distinct_values([1, 2, 3, 1, 1], 2)
        10
    """
    cnt: dict[int, int] = {}
    left = total = 0
    for r, v in enumerate(a):
        cnt[v] = cnt.get(v, 0) + 1
        while len(cnt) > k:  # сдвигаем левый край
            u = a[left]
            cnt[u] -= 1
            if cnt[u] == 0:
                del cnt[u]
            left += 1
        total += r - left + 1
    return total


@algo(tags=["monotonic-stack", "nearest-smaller"], cses=["Nearest Smaller Values (1645)"])
def nearest_smaller_values(a: list[int]) -> list[int]:
    """Index of the nearest strictly smaller element to the left.   # Ближайшие меньшие.

    When to use:  monotonic stack; also for histograms and "next greater".
    Complexity:   O(n)
    Returns:      list of indices (CSES prints index + 1, 0 if none).
    CSES:         Nearest Smaller Values (1645).
    Example:
        >>> nearest_smaller_values([2, 5, 1, 4, 8, 3, 2, 5])
        [-1, 0, -1, 2, 3, 2, 2, 6]
    """
    st: list[int] = []
    res = []
    for i, v in enumerate(a):
        while st and a[st[-1]] >= v:
            st.pop()  # больше или равные никогда не ответ для правых
        res.append(st[-1] if st else -1)
        st.append(i)
    return res


@algo(tags=["meet-in-the-middle", "subset-sum"], cses=["Meet in the Middle (1628)"])
def meet_in_middle_count(a: list[int], x: int) -> int:
    """Number of subsets with sum exactly x, n <= 40.   # Встреча посередине.

    When to use:  2^n too big, 2^(n/2) fine: enumerate halves, match by hashing.
    Complexity:   O(2^(n/2))
    Returns:      count of subsets (empty subset counts if x == 0).
    Python speed: n = 40 ~ 0.6 s (two lists of 2^20 sums + a dict).
    CSES:         Meet in the Middle (1628).
    Example:
        >>> meet_in_middle_count([2, 4, 1, 2], 5)  # {4, 1} и {2, 1, 2}
        2
    """
    half = len(a) // 2

    def sums(part: list[int]) -> list[int]:
        res = [0]
        for v in part:
            res += [s + v for s in res]  # удвоение списка сумм
        return res

    left = sums(a[:half])
    cnt: dict[int, int] = {}
    for s in sums(a[half:]):
        cnt[s] = cnt.get(s, 0) + 1
    return sum(cnt.get(x - s, 0) for s in left)


class _MedianWindow:
    """Two heaps with lazy deletion: low (max) holds ceil(size / 2) smallest values."""

    def __init__(self) -> None:
        self.low: list[int] = []  # отрицательные значения (макс-куча)
        self.high: list[int] = []
        self.delayed: dict[int, int] = {}
        self.ls = self.hs = 0  # реальные размеры
        self.lsum = self.hsum = 0

    def _prune(self, heap: list[int], sign: int) -> None:
        while heap:
            v = heap[0] * sign
            if self.delayed.get(v, 0):
                self.delayed[v] -= 1
                heapq.heappop(heap)
            else:
                break

    def _balance(self) -> None:
        if self.ls > self.hs + 1:
            v = -heapq.heappop(self.low)
            self.ls -= 1
            self.lsum -= v
            heapq.heappush(self.high, v)
            self.hs += 1
            self.hsum += v
            self._prune(self.low, -1)
        elif self.ls < self.hs:
            v = heapq.heappop(self.high)
            self.hs -= 1
            self.hsum -= v
            heapq.heappush(self.low, -v)
            self.ls += 1
            self.lsum += v
            self._prune(self.high, 1)

    def add(self, v: int) -> None:
        if not self.low or v <= -self.low[0]:
            heapq.heappush(self.low, -v)
            self.ls += 1
            self.lsum += v
        else:
            heapq.heappush(self.high, v)
            self.hs += 1
            self.hsum += v
        self._balance()

    def remove(self, v: int) -> None:
        self.delayed[v] = self.delayed.get(v, 0) + 1
        if v <= -self.low[0]:
            self.ls -= 1
            self.lsum -= v
            if v == -self.low[0]:
                self._prune(self.low, -1)
        else:
            self.hs -= 1
            self.hsum -= v
            if self.high and v == self.high[0]:
                self._prune(self.high, 1)
        self._balance()

    def median(self) -> int:
        return -self.low[0]

    def cost(self) -> int:
        m = self.median()
        return m * self.ls - self.lsum + self.hsum - m * self.hs


@algo(
    tags=["sliding-window", "median", "heap"],
    cses=["Sliding Window Median (1076)"],
    requires=["_MedianWindow"],
)
def sliding_window_median(a: list[int], k: int) -> list[int]:
    """Median of every window of length k (lower median for even k).   # Медиана в окне.

    When to use:  two heaps with lazy deletion.
    Complexity:   O(n log n)
    Returns:      list of n - k + 1 medians.
    Related:      sliding_window_cost, ds.SortedList.
    CSES:         Sliding Window Median (1076).
    Example:
        >>> sliding_window_median([2, 4, 3, 5, 8, 1, 2, 1], 3)
        [3, 4, 5, 5, 2, 1]
    """
    w = _MedianWindow()
    res = []
    for i, v in enumerate(a):
        w.add(v)
        if i >= k:
            w.remove(a[i - k])  # элемент вышел из окна
        if i >= k - 1:
            res.append(w.median())
    return res


@algo(
    tags=["sliding-window", "median", "heap"],
    cses=["Sliding Window Cost (1077)"],
    requires=["_MedianWindow"],
)
def sliding_window_cost(a: list[int], k: int) -> list[int]:
    """Min cost to make each window equal: sum |x - median|.   # Стоимость окна.

    When to use:  sliding_window_median + the sums of both halves.
    Complexity:   O(n log n)
    Returns:      list of n - k + 1 costs.
    Related:      sliding_window_median, stick_lengths.
    CSES:         Sliding Window Cost (1077).
    Example:
        >>> sliding_window_cost([2, 4, 3, 5, 8, 1, 2, 1], 3)
        [2, 2, 5, 7, 7, 1]
    """
    w = _MedianWindow()
    res = []
    for i, v in enumerate(a):
        w.add(v)
        if i >= k:
            w.remove(a[i - k])
        if i >= k - 1:
            res.append(w.cost())  # |x - медиана| по обеим половинам
    return res
