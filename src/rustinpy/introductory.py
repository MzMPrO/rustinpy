"""CSES Introductory Problems and constructive tasks: enumeration, backtracking, Prufer codes,
de Bruijn sequences, inversion / monotone constructions, degree sequences.

Вводные задачи и конструктивы. Перебор без рекурсии.
"""

from __future__ import annotations

import heapq
from collections import deque
from collections.abc import Iterator

from rustinpy._registry import algo


@algo(tags=["introductory", "simulation"], cses=["Weird Algorithm (1068)"])
def weird_algorithm(n: int) -> list[int]:
    """Collatz sequence from n down to 1.   # Странный алгоритм (Коллатц).

    When to use:  warm-up simulation.
    Complexity:   O(length)
    Returns:      the sequence including n and 1.
    CSES:         Weird Algorithm (1068).
    Example:
        >>> weird_algorithm(3)
        [3, 10, 5, 16, 8, 4, 2, 1]
    """
    res = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1  # чётное делим, нечётное 3n + 1
        res.append(n)
    return res


@algo(tags=["introductory", "formula"], cses=["Number Spiral (1071)"])
def number_spiral(y: int, x: int) -> int:
    """Value at row y, column x (1-based) of the CSES number spiral.   # Числовая спираль.

    When to use:  O(1) formula by the layer max(x, y).
    Complexity:   O(1)
    Returns:      the number in the cell.
    CSES:         Number Spiral (1071).
    Example:
        >>> number_spiral(2, 3), number_spiral(1, 1), number_spiral(4, 2)
        (8, 1, 15)
    """
    k = max(x, y)  # номер «слоя»
    if k % 2 == 0:
        return k * k - x + 1 if y == k else (k - 1) ** 2 + y
    return k * k - y + 1 if x == k else (k - 1) ** 2 + x


@algo(tags=["introductory", "combinatorics", "chess"], cses=["Two Knights (1072)"])
def two_knights(n: int) -> list[int]:
    """Ways to place two non-attacking knights on k x k boards, k = 1..n.   # Два коня.

    When to use:  total pairs minus attacking pairs (each 2 x 3 block has 2 attacks).
    Complexity:   O(n)
    Returns:      list of answers for k = 1..n.
    CSES:         Two Knights (1072).
    Example:
        >>> two_knights(5)
        [0, 6, 28, 96, 252]
    """
    return [k * k * (k * k - 1) // 2 - 4 * (k - 1) * (k - 2) for k in range(1, n + 1)]


@algo(tags=["introductory", "construction", "partition"], cses=["Two Sets (1092)"])
def two_sets(n: int) -> tuple[list[int], list[int]] | None:
    """Split 1..n into two sets with equal sums.   # Два множества.

    When to use:  greedy from n downwards.
    Complexity:   O(n)
    Returns:      (A, B) or None if n(n+1)/2 is odd.
    CSES:         Two Sets (1092).
    Example:
        >>> two_sets(7), two_sets(6)
        (([7, 6, 1], [5, 4, 3, 2]), None)
    """
    total = n * (n + 1) // 2
    if total % 2:
        return None
    need = total // 2
    a, b = [], []
    for x in range(n, 0, -1):
        if x <= need:
            a.append(x)  # жадно берём крупное в первое множество
            need -= x
        else:
            b.append(x)
    return a, b


@algo(tags=["introductory", "math"], cses=["Trailing Zeros (1618)"])
def trailing_zeros(n: int) -> int:
    """Number of trailing zeros of n! (Legendre for p = 5).   # Нули в конце факториала.

    When to use:  n up to 10^18.
    Complexity:   O(log n)
    Returns:      count of trailing zeros.
    CSES:         Trailing Zeros (1618).
    Example:
        >>> trailing_zeros(20), trailing_zeros(100)
        (4, 24)
    """
    res = 0
    while n:
        n //= 5  # сколько множителей 5
        res += n
    return res


@algo(tags=["introductory", "math"], cses=["Coin Piles (1754)"])
def coin_piles(a: int, b: int) -> bool:
    """Can both piles be emptied removing (1, 2) or (2, 1) coins each move?   # Кучи монет.

    When to use:  invariant: (a + b) divisible by 3 and the bigger pile <= 2 * smaller.
    Complexity:   O(1)
    Returns:      True / False.
    CSES:         Coin Piles (1754).
    Example:
        >>> coin_piles(2, 1), coin_piles(2, 2), coin_piles(3, 3)
        (True, False, True)
    """
    return (a + b) % 3 == 0 and max(a, b) <= 2 * min(a, b)


@algo(tags=["introductory", "strings", "palindrome"], cses=["Palindrome Reorder (1755)"])
def palindrome_reorder(s: str) -> str | None:
    """Rearrange letters into the smallest palindrome.   # Перестановка в палиндром.

    When to use:  at most one letter with an odd count.
    Complexity:   O(n + sigma log sigma)
    Returns:      the palindrome, or None.
    CSES:         Palindrome Reorder (1755) (any palindrome is accepted).
    Example:
        >>> palindrome_reorder("AAAACACBA"), palindrome_reorder("AB")
        ('AAACBCAAA', None)
    """
    cnt: dict[str, int] = {}
    for ch in s:
        cnt[ch] = cnt.get(ch, 0) + 1
    odd = [c for c, k in cnt.items() if k % 2]
    if len(odd) > 1:
        return None
    half = "".join(c * (cnt[c] // 2) for c in sorted(cnt))
    mid = odd[0] if odd else ""
    return half + mid + half[::-1]  # левая половина + центр + зеркало


@algo(tags=["introductory", "subsets", "brute-force"], cses=["Apple Division (1623)"])
def apple_division(p: list[int]) -> int:
    """Minimal difference of sums when splitting into two groups.   # Деление яблок.

    When to use:  n <= 20: enumerate all subset sums.
    Complexity:   O(2^n)
    Returns:      min |sum(A) - sum(B)|.
    Python speed: n = 20 ~ 0.2 s (subset sums are built by list doubling).
    Related:      sorting.meet_in_middle_count.
    CSES:         Apple Division (1623).
    Example:
        >>> apple_division([3, 2, 7, 4, 1])
        1
    """
    sums = [0]
    for x in p:
        sums += [s + x for s in sums]  # суммы всех подмножеств
    total = sum(p)
    return min(abs(total - 2 * s) for s in sums)


@algo(tags=["introductory", "digits"], cses=["Digit Queries (2431)"])
def digit_queries(k: int) -> int:
    """k-th digit (1-based) of 123456789101112...   # Цифра на позиции k.

    When to use:  k up to 10^18: skip whole blocks of numbers with the same length.
    Complexity:   O(log k)
    Returns:      the digit.
    CSES:         Digit Queries (2431).
    Example:
        >>> [digit_queries(k) for k in (7, 19, 12)]
        [7, 4, 1]
    """
    length, count, start = 1, 9, 1
    while k > length * count:  # пропускаем блок чисел длины length
        k -= length * count
        length += 1
        count *= 10
        start *= 10
    num = start + (k - 1) // length
    return int(str(num)[(k - 1) % length])


@algo(tags=["introductory", "construction", "permutation"], cses=["Permutations (1070)"])
def beautiful_permutation(n: int) -> list[int] | None:
    """Permutation of 1..n with no adjacent values differing by 1.   # Красивая перестановка.

    When to use:  evens first, then odds (n = 2, 3 impossible).
    Complexity:   O(n)
    Returns:      permutation or None.
    CSES:         Permutations (1070).
    Example:
        >>> beautiful_permutation(5), beautiful_permutation(3)
        ([2, 4, 1, 3, 5], None)
    """
    if n in (2, 3):
        return None
    return list(range(2, n + 1, 2)) + list(range(1, n + 1, 2))  # чётные, потом нечётные


@algo(tags=["introductory", "strings", "greedy"], cses=["String Reorder (1743)"])
def string_reorder(s: str) -> str | None:
    """Smallest rearrangement without equal adjacent letters.   # Перестановка строки.

    When to use:  greedy: take the smallest letter that keeps the rest feasible.
    Complexity:   O(n * sigma)
    Returns:      the string, or None if impossible.
    Idea:         after placing a letter, the remaining multiset of size m is arrangeable
                  (with the new previous letter) iff max count <= (m + 1) // 2, and the
                  letter equal to the previous one may hold at most m // 2.
    CSES:         String Reorder (1743).
    Example:
        >>> string_reorder("HATTIVATTI"), string_reorder("AAB"), string_reorder("AAA")
        ('AHATITITVT', 'ABA', None)
    """
    cnt: dict[str, int] = {}
    for ch in s:
        cnt[ch] = cnt.get(ch, 0) + 1
    letters = sorted(cnt)
    res = []
    prev = ""
    for left in range(len(s), 0, -1):
        for c in letters:
            if not cnt[c] or c == prev:
                continue
            cnt[c] -= 1
            m = left - 1  # сколько останется
            ok = True
            for d in letters:
                lim = m // 2 if d == c else (m + 1) // 2  # d == c не может стоять сразу
                if cnt[d] > lim:
                    ok = False
                    break
            if ok:
                res.append(c)
                prev = c
                break
            cnt[c] += 1
        else:
            return None
    return "".join(res)


@algo(tags=["introductory", "construction", "mex", "xor"], cses=["Mex Grid Construction (3419)"])
def mex_grid_construction(n: int) -> list[list[int]]:
    """n x n grid where each cell is the mex of the values above and to the left.   # Сетка mex.

    When to use:  the answer is cell (i, j) = i xor j (Nim-sum of two heaps).
    Complexity:   O(n^2)
    Returns:      the grid.
    CSES:         Mex Grid Construction (3419).
    Example:
        >>> mex_grid_construction(3)
        [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
    """
    return [[i ^ j for j in range(n)] for i in range(n)]  # mex строки и столбца = xor


@algo(tags=["introductory", "bfs", "knight"], cses=["Knight Moves Grid (3217)"])
def knight_moves_grid(n: int) -> list[list[int]]:
    """Minimal knight moves from the top-left corner to every cell of n x n.   # Ходы коня по сетке.

    When to use:  BFS on the implicit knight graph.
    Complexity:   O(n^2)
    Returns:      dist grid (-1 if unreachable, e.g. tiny boards).
    CSES:         Knight Moves Grid (3217).
    Example:
        >>> knight_moves_grid(3)
        [[0, 3, 2], [3, -1, 1], [2, 1, 4]]
    """
    dist = [[-1] * n for _ in range(n)]
    dist[0][0] = 0
    q = deque([(0, 0)])
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and dist[nr][nc] < 0:
                dist[nr][nc] = dist[r][c] + 1  # BFS: первый раз - минимум
                q.append((nr, nc))
    return dist


@algo(tags=["introductory", "gray-code", "bits"], cses=["Gray Code (2205)"])
def gray_code(n: int) -> list[str]:
    """All n-bit strings where neighbours differ in exactly one bit.   # Код Грея.

    When to use:  i xor (i >> 1) enumerates the reflected Gray code.
    Complexity:   O(2^n * n)
    Returns:      list of 2^n bit strings.
    CSES:         Gray Code (2205).
    Example:
        >>> gray_code(2)
        ['00', '01', '11', '10']
    """
    return [format(i ^ (i >> 1), f"0{n}b") for i in range(1 << n)]  # отражённый код


@algo(tags=["introductory", "hanoi", "iterative"], cses=["Tower of Hanoi (2165)"])
def hanoi_moves(n: int) -> list[tuple[int, int]]:
    """Optimal Tower of Hanoi moves from stack 1 to stack 3 (iterative).   # Ханойская башня.

    When to use:  2^n - 1 moves, no recursion.
    Complexity:   O(2^n)
    Returns:      list of (from, to) with stacks 1, 2, 3.
    Idea:         move m (1-based) goes from peg (m & (m - 1)) % 3 to ((m | (m - 1)) + 1) % 3
                  (pegs 0, 1, 2); this ends on peg 2 for odd n and on peg 1 for even n, so
                  for even n pegs 1 and 2 are swapped.
    CSES:         Tower of Hanoi (2165).
    Example:
        >>> hanoi_moves(2)
        [(1, 2), (1, 3), (2, 3)]
    """
    swap = (0, 2, 1) if n % 2 == 0 else (0, 1, 2)  # для чётного n меняем стержни 2 и 3
    res = []
    for m in range(1, 1 << n):
        a, b = (m & (m - 1)) % 3, ((m | (m - 1)) + 1) % 3  # формула m-го хода
        res.append((swap[a] + 1, swap[b] + 1))
    return res


@algo(
    tags=["introductory", "permutations", "strings"],
    cses=["Creating Strings (1622)"],
    requires=["next_permutation"],
)
def string_permutations(s: str) -> list[str]:
    """All distinct permutations of s in lexicographic order.   # Все перестановки строки.

    When to use:  n <= 8; next_permutation skips duplicates automatically.
    Complexity:   O(n * number of permutations)
    Returns:      sorted list of distinct strings.
    Related:      next_permutation.
    CSES:         Creating Strings (1622).
    Example:
        >>> string_permutations("aab")
        ['aab', 'aba', 'baa']
    """
    a = sorted(s)
    res = ["".join(a)]
    while next_permutation(a):  # type: ignore[arg-type]
        res.append("".join(a))
    return res


@algo(tags=["introductory", "permutations"], cses=["Creating Strings (1622)"])
def next_permutation(a: list[int]) -> bool:
    """Transform a into the next lexicographic permutation in place.   # Следующая перестановка.

    When to use:  enumerate permutations (with repeats) without recursion.
    Complexity:   O(n)
    Returns:      False (and a sorted ascending) if a was the last permutation.
    Related:      string_permutations.
    CSES:         Creating Strings (1622).
    Example:
        >>> a = [1, 2, 3]
        >>> next_permutation(a), a
        (True, [1, 3, 2])
        >>> b = [3, 2, 1]
        >>> next_permutation(b), b
        (False, [1, 2, 3])
    """
    i = len(a) - 2
    while i >= 0 and a[i] >= a[i + 1]:  # ищем последний подъём
        i -= 1
    if i < 0:
        a.reverse()
        return False
    j = len(a) - 1
    while a[j] <= a[i]:
        j -= 1
    a[i], a[j] = a[j], a[i]
    a[i + 1 :] = reversed(a[i + 1 :])  # хвост в возрастающий порядок
    return True


@algo(tags=["introductory", "bitmask", "subsets"], cses=["- (submask enumeration)"])
def submasks(mask: int) -> Iterator[int]:
    """All submasks of mask in decreasing order (including mask and 0).   # Перебор подмасок.

    When to use:  sum over submasks; all submasks of all masks is O(3^n).
    Complexity:   O(2^popcount(mask))
    Returns:      iterator of submasks.
    Related:      subsets, bits.sos_subset_sum.
    CSES:         - (submask enumeration)
    Example:
        >>> list(submasks(0b101))
        [5, 4, 1, 0]
    """
    s = mask
    while True:
        yield s
        if s == 0:
            return
        s = (s - 1) & mask  # следующая меньшая подмаска


@algo(tags=["introductory", "bitmask", "subsets"], cses=["- (subset enumeration)"])
def subsets(n: int) -> Iterator[list[int]]:
    """All subsets of {0, ..., n-1} as lists, by increasing bitmask.   # Перебор подмножеств.

    When to use:  brute force for n <= 20.
    Complexity:   O(2^n * n)
    Returns:      iterator of index lists.
    Related:      submasks.
    CSES:         - (subset enumeration)
    Example:
        >>> list(subsets(2))
        [[], [0], [1], [0, 1]]
    """
    for mask in range(1 << n):
        yield [i for i in range(n) if mask >> i & 1]  # биты маски - элементы


@algo(tags=["introductory", "backtracking", "queens"], cses=["Chessboard and Queens (1624)"])
def n_queens(n: int = 8, blocked: list[str] | None = None) -> int:
    """Number of ways to place n non-attacking queens (iterative backtracking).   # Ферзи.

    When to use:  n <= ~12; blocked rows of '.' / '*' ('*' cannot hold a queen).
    Complexity:   O(n!) worst case, bitmasks make it fast
    Returns:      number of placements.
    CSES:         Chessboard and Queens (1624).
    Example:
        >>> n_queens(8), n_queens(4, ["....", "...*", "....", "...."])
        (92, 1)
    """
    full = (1 << n) - 1
    bad = [0] * n
    if blocked:
        for r, row in enumerate(blocked):
            for c, ch in enumerate(row):
                if ch == "*":
                    bad[r] |= 1 << c
    count = 0
    # стек: (строка, занятые столбцы, диагонали /, диагонали \)
    stack = [(0, 0, 0, 0)]
    while stack:
        r, cols, d1, d2 = stack.pop()
        if r == n:
            count += 1
            continue
        free = full & ~(cols | d1 | d2 | bad[r])
        while free:
            bit = free & -free
            free ^= bit
            stack.append((r + 1, cols | bit, ((d1 | bit) << 1) & full, (d2 | bit) >> 1))
    return count


@algo(tags=["introductory", "backtracking", "grid"], cses=["Grid Path Description (1625)"])
def grid_path_description(pattern: str, n: int = 7) -> int:
    """Hamiltonian grid paths matching a pattern.   # Описание пути по сетке.

    When to use:  CSES Grid Path Description (n = 7, pattern of D/U/L/R/?).
    Complexity:   exponential with strong pruning (dead ends, splitting walls)
    Returns:      number of matching paths.
    Python speed: all '?' on 7 x 7 takes minutes in CPython (88418 paths); fixed patterns are
                  fast.
    Idea:         iterative DFS; prune when the target is reached early, and when the walk
                  hits a wall or visited cell while both side cells are free (grid splits).
    CSES:         Grid Path Description (1625).
    Example:
        >>> grid_path_description("????????", 3), grid_path_description("RRDDLULD", 3)
        (2, 1)
    """
    total_steps = n * n - 1
    if len(pattern) != total_steps:
        raise ValueError("pattern must have n * n - 1 characters")
    moves = {"D": (1, 0), "U": (-1, 0), "L": (0, -1), "R": (0, 1)}
    vis = [[False] * n for _ in range(n)]

    def free(rr: int, cc: int) -> bool:
        return 0 <= rr < n and 0 <= cc < n and not vis[rr][cc]

    count = 0
    order = "DURL"
    vis[0][0] = True
    stack: list[list[int]] = [[0, 0, 0, 0]]  # кадры: (r, c, шаг, номер следующего хода)
    while stack:
        top = stack[-1]
        r, c, step, k = top
        dead = k >= 4
        if k == 0:  # первый заход в клетку: финиш и отсечения
            if (r, c) == (n - 1, 0):
                count += step == total_steps
                dead = True
            elif (
                not free(r + 1, c) and not free(r - 1, c) and free(r, c - 1) and free(r, c + 1)
            ) or (not free(r, c + 1) and not free(r, c - 1) and free(r - 1, c) and free(r + 1, c)):
                dead = True  # путь разрезал поле на две части - не обойти обе
        if dead:
            stack.pop()
            vis[r][c] = False  # откат
            continue
        top[3] = k + 1
        ch = order[k]
        if pattern[step] not in ("?", ch):
            continue
        dr, dc = moves[ch]
        nr, nc = r + dr, c + dc
        if free(nr, nc):
            vis[nr][nc] = True
            stack.append([nr, nc, step + 1, 0])
    return count


@algo(tags=["construction", "prufer", "tree"], cses=["Prufer Code (1134)"])
def prufer_encode(n: int, edges: list[tuple[int, int]]) -> list[int]:
    """Prufer code of a labelled tree on 0..n-1.   # Код Прюфера (кодирование).

    When to use:  bijection between labelled trees and sequences of length n - 2.
    Complexity:   O(n log n) with a heap of leaves
    Returns:      code of length n - 2.
    Related:      prufer_decode.
    CSES:         Prufer Code (1134) (labels 1-based there).
    Example:
        >>> prufer_encode(5, [(0, 1), (0, 2), (0, 3), (3, 4)])
        [0, 0, 3]
    """
    adj: list[set[int]] = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    leaves = [v for v in range(n) if len(adj[v]) == 1]
    heapq.heapify(leaves)
    code = []
    for _ in range(n - 2):
        leaf = heapq.heappop(leaves)  # наименьший лист
        (parent,) = adj[leaf]
        code.append(parent)
        adj[parent].discard(leaf)
        if len(adj[parent]) == 1:
            heapq.heappush(leaves, parent)
    return code


@algo(tags=["construction", "prufer", "tree"], cses=["Prufer Code (1134)"])
def prufer_decode(code: list[int]) -> list[tuple[int, int]]:
    """Tree edges from a Prufer code (vertices 0..len(code)+1).   # Код Прюфера (декодирование).

    When to use:  build a tree with prescribed degrees (deg = 1 + occurrences in code).
    Complexity:   O(n log n)
    Returns:      list of n - 1 edges (leaf, attached vertex).
    Related:      prufer_encode.
    CSES:         Prufer Code (1134).
    Example:
        >>> prufer_decode([0, 0, 3])
        [(1, 0), (2, 0), (0, 3), (3, 4)]
    """
    n = len(code) + 2
    deg = [1] * n
    for v in code:
        deg[v] += 1
    leaves = [v for v in range(n) if deg[v] == 1]
    heapq.heapify(leaves)
    edges = []
    for v in code:
        leaf = heapq.heappop(leaves)
        edges.append((leaf, v))  # наименьший лист прикрепляем к v
        deg[v] -= 1
        if deg[v] == 1:
            heapq.heappush(leaves, v)
    a = heapq.heappop(leaves)
    b = heapq.heappop(leaves)
    edges.append((a, b))
    return edges


@algo(tags=["construction", "de-bruijn", "lyndon"], cses=["De Bruijn Sequence (1692)"])
def de_bruijn(n: int, k: int = 2) -> str:
    """Shortest string containing every length-n word.   # Последовательность де Брёйна.

    When to use:  CSES De Bruijn Sequence (binary, length 2^n + n - 1).
    Complexity:   O(k^n)
    Returns:      string of length k^n + n - 1 over digits '0'..str(k-1).
    Idea:         concatenate Lyndon words of length dividing n in lexicographic order
                  (FKM algorithm, iterative), then append the first n - 1 symbols.
    Related:      graph.euler_path_directed (the other classical construction).
    CSES:         De Bruijn Sequence (1692).
    Example:
        >>> de_bruijn(2), de_bruijn(3)
        ('00110', '0001011100')
    """
    seq: list[int] = []
    w = [-1]
    while w:
        w[-1] += 1
        m = len(w)
        if n % m == 0:
            seq.extend(w)  # слово Линдона длины, делящей n
        while len(w) < n:
            w.append(w[len(w) - m])
        while w and w[-1] == k - 1:
            w.pop()
    cyc = "".join(map(str, seq))
    return cyc + cyc[: n - 1]


@algo(tags=["construction", "inversions", "permutation"], cses=["Inverse Inversions (2214)"])
def inverse_inversions(n: int, k: int) -> list[int]:
    """Permutation of 1..n with exactly k inversions.   # Перестановка с k инверсиями.

    When to use:  greedy: the largest remaining value goes first while k allows.
    Complexity:   O(n)
    Returns:      a permutation.
    CSES:         Inverse Inversions (2214).
    Example:
        >>> inverse_inversions(5, 4)
        [5, 1, 2, 3, 4]
    """
    res = []
    lo, hi = 1, n
    for i in range(n):
        rest = n - 1 - i  # сколько чисел после текущего
        if k >= rest:
            res.append(hi)  # наибольшее даёт rest инверсий
            hi -= 1
            k -= rest
        else:
            res.append(lo)
            lo += 1
    return res


@algo(
    tags=["construction", "monotone", "erdos-szekeres"],
    cses=["Monotone Subsequences (2215)"],
    verified=False,
)
def monotone_subsequences(n: int, k: int) -> list[int] | None:
    """Permutation whose longest monotone subsequence is k.   # Монотонные подпоследовательности.

    When to use:  Erdos-Szekeres: possible iff k * k >= n (and k <= n).
    Complexity:   O(n)
    Returns:      a permutation or None.
    Idea:         decreasing blocks of size k (the last one smaller), blocks in increasing
                  order: LDS = k, LIS = number of blocks <= k.
    CSES:         Monotone Subsequences (2215) (whether "monotone" means increasing only is
                  NOT VERIFIED).
    Example:
        >>> monotone_subsequences(5, 3), monotone_subsequences(5, 2)
        ([3, 2, 1, 5, 4], None)
    """
    # NOT VERIFIED: «монотонная» в условии CSES - только возрастающая или любая
    if k * k < n or k > n or k < 1:
        return None
    res: list[int] = []
    start = 1
    while start <= n:
        end = min(n, start + k - 1)
        res.extend(range(end, start - 1, -1))  # убывающий блок
        start = end + 1
    return res


@algo(
    tags=["construction", "graph", "degree-sequence", "havel-hakimi"],
    cses=["Chess Tournament (1697)"],
)
def chess_tournament(degrees: list[int]) -> list[tuple[int, int]] | None:
    """Simple graph with the given degree sequence (Havel-Hakimi).   # Шахматный турнир.

    When to use:  "player i plays exactly d_i games, every pair at most once".
    Complexity:   O(m log n)
    Returns:      list of games (pairs of players), or None if impossible.
    Idea:         repeatedly take the player with the largest remaining degree d and pair
                  them with the d next largest.
    CSES:         Chess Tournament (1697).
    Example:
        >>> sorted(chess_tournament([2, 1, 1]))
        [(0, 1), (0, 2)]
        >>> chess_tournament([2, 2, 0]) is None
        True
    """
    pq = [(-d, i) for i, d in enumerate(degrees) if d > 0]
    heapq.heapify(pq)
    games = []
    while pq:
        d, v = heapq.heappop(pq)
        d = -d
        if d > len(pq):
            return None  # не хватает соперников
        taken = [heapq.heappop(pq) for _ in range(d)]
        for du, u in taken:
            games.append((min(u, v), max(u, v)))
            if du + 1 < 0:  # ещё остались игры у u
                heapq.heappush(pq, (du + 1, u))
    return games


@algo(
    tags=["construction", "tilings", "trominoes"],
    cses=["Filling Trominos (2423)"],
    verified=False,
    stub=True,
)
def filling_trominos(n: int, m: int) -> list[str] | None:
    """CSES Filling Trominos - not implemented yet.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return a tiling of an n x m grid with L-trominoes (letters) or None.
    Idea:         n * m divisible by 3; tile with 2 x 3 blocks and handle odd sides with
                  special 3 x 5 / 5 x 9 patterns. NOT VERIFIED: statement not checked.
    CSES:         Filling Trominos (2423).
    Example:
        >>> filling_trominos(2, 3)
        Traceback (most recent call last):
        NotImplementedError: CSES Filling Trominos: statement not verified yet
    """
    # NOT VERIFIED: заглушка, условие задачи не сверено
    raise NotImplementedError("CSES Filling Trominos: statement not verified yet")
