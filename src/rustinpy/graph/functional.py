"""Functional graphs (every vertex has exactly one outgoing edge f[v]).

Функциональные графы: двоичные подъёмы, циклы, расстояния.
"""

from __future__ import annotations

from rustinpy._registry import algo


@algo(tags=["functional-graph", "binary-lifting"], cses=["Planets Queries I (1750)"])
def build_lifting(f: list[int], max_steps: int) -> list[list[int]]:
    """Jump table up[j][x] = f applied 2^j times to x.   # Двоичные подъёмы по функции.

    When to use:  k-th successor queries with k up to 10^18 in a functional graph.
    Complexity:   O(n log K) time and memory
    Returns:      up with enough levels for any k <= max_steps.
    Python speed: n = 2 * 10^5, K = 10^9 (30 levels): ~1 s, 6 * 10^6 ints of memory.
    Related:      kth_successor, tree.LCA.
    CSES:         Planets Queries I (1750).
    Example:
        >>> up = build_lifting([1, 2, 0, 0], 10)
        >>> len(up), up[1]
        (4, [2, 0, 1, 1])
    """
    up = [list(f)]
    while (1 << len(up)) <= max_steps:
        prev = up[-1]
        up.append([prev[y] for y in prev])  # 2^(j+1) = 2^j + 2^j
    return up


@algo(
    tags=["functional-graph", "binary-lifting"],
    cses=["Planets Queries I (1750)"],
    requires=["build_lifting"],
)
def kth_successor(up: list[list[int]], x: int, k: int) -> int:
    """f^k(x) using a table from build_lifting.   # k-й преемник.

    When to use:  after build_lifting(f, max_k).
    Complexity:   O(log k)
    Returns:      vertex reached after k steps.
    Pitfalls:     k must not exceed the max_steps given to build_lifting.
    Related:      build_lifting.
    CSES:         Planets Queries I (1750).
    Example:
        >>> up = build_lifting([1, 2, 0, 0], 100)
        >>> kth_successor(up, 3, 5), kth_successor(up, 0, 0)
        (1, 0)
    """
    j = 0
    while k:
        if k & 1:
            x = up[j][x]  # берём прыжок 2^j
        k >>= 1
        j += 1
    return x


@algo(tags=["functional-graph", "cycles"], cses=["Planets Cycles (1751)"])
def cycle_steps(f: list[int]) -> list[int]:
    """Steps from each start until a vertex repeats (tail + cycle).   # Длина пути до повтора.

    When to use:  "how many teleports until a planet is visited twice".
    Complexity:   O(n)
    Returns:      ans[v] = number of distinct vertices visited starting from v.
    Related:      functional_distance.
    CSES:         Planets Cycles (1751).
    Example:
        >>> cycle_steps([1, 2, 0, 0, 3])
        [3, 3, 3, 4, 5]
    """
    n = len(f)
    ans = [0] * n
    state = [0] * n  # 0 - не были, 1 - в текущем пути, 2 - посчитано
    pos = [0] * n
    for s in range(n):
        if state[s]:
            continue
        path: list[int] = []
        v = s
        while state[v] == 0:
            state[v] = 1
            pos[v] = len(path)
            path.append(v)
            v = f[v]
        if state[v] == 1:  # нашли новый цикл
            j = pos[v]
            length = len(path) - j
            for u in path[j:]:
                ans[u] = length
                state[u] = 2
            path = path[:j]
        for u in reversed(path):  # хвост: на один шаг больше следующей
            ans[u] = ans[f[u]] + 1
            state[u] = 2
    return ans


@algo(tags=["functional-graph", "distance", "euler-tour"], cses=["Planets Queries II (1160)"])
def functional_distance(f: list[int], queries: list[tuple[int, int]]) -> list[int]:
    """Minimal number of steps from a to b, or -1.   # Расстояние в функциональном графе.

    When to use:  many "teleport from a to b" queries.
    Complexity:   O(n + q)
    Returns:      answers in query order.
    Idea:         every component = cycle + trees hanging on it. b on the cycle:
                  depth(a) + cyclic distance from root(a) to b; b in a tree: b must be an
                  ancestor of a (Euler tour of the reversed forest) -> depth(a) - depth(b).
    Related:      cycle_steps, kth_successor.
    CSES:         Planets Queries II (1160).
    Example:
        >>> f = [1, 2, 0, 0, 3]
        >>> functional_distance(f, [(4, 1), (3, 3), (0, 4), (4, 3), (2, 1)])
        [3, 0, -1, 1, 2]
    """
    n = len(f)
    # 1. циклы: номер цикла, позиция, длина
    cyc_id = [-1] * n
    cyc_pos = [0] * n
    cyc_len: list[int] = []
    state = [0] * n
    for s in range(n):
        if state[s]:
            continue
        path = []
        v = s
        while state[v] == 0:
            state[v] = 1
            path.append(v)
            v = f[v]
        if state[v] == 1:
            j = path.index(v)
            cid = len(cyc_len)
            cyc_len.append(len(path) - j)
            for i, u in enumerate(path[j:]):
                cyc_id[u] = cid
                cyc_pos[u] = i
        for u in path:
            state[u] = 2
    # 2. обратный лес: деревья растут из вершин цикла
    children: list[list[int]] = [[] for _ in range(n)]
    for v in range(n):
        if cyc_id[v] == -1:
            children[f[v]].append(v)
    root = list(range(n))
    depth = [0] * n
    tin = [0] * n
    tout = [0] * n
    timer = 0
    for r in range(n):
        if cyc_id[r] == -1:
            continue
        stack = [(r, False)]
        while stack:  # эйлеров обход без рекурсии
            v, done = stack.pop()
            if done:
                tout[v] = timer
                continue
            tin[v] = timer
            timer += 1
            stack.append((v, True))
            for c in children[v]:
                root[c] = r
                depth[c] = depth[v] + 1
                stack.append((c, False))
    res = []
    for a, b in queries:
        ra, rb = root[a], root[b]
        if cyc_id[ra] != cyc_id[rb]:
            res.append(-1)
        elif cyc_id[b] != -1:  # b на цикле
            L = cyc_len[cyc_id[b]]
            res.append(depth[a] + (cyc_pos[b] - cyc_pos[ra]) % L)
        elif ra == rb and tin[b] <= tin[a] < tout[b]:  # b - предок a в лесу
            res.append(depth[a] - depth[b])
        else:
            res.append(-1)
    return res


@algo(tags=["functional-graph", "updates"], icpc=["2023 E"], verified=False, stub=True)
def escalators(f: list[int], queries: list[tuple[int, int, int]]) -> list[int]:
    """ICPC-UZ 2023 E "Escalators": movement graph with single-vertex changes.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return the answers to the queries.
    Idea:         a functional graph where a vertex either exits or ends in a cycle; queries
                  change one f[v]. Static part: cycle_steps / functional_distance; with
                  changes - offline / sqrt rebuild. NOT VERIFIED: statement unknown.
    ICPC-UZ:      2023 E.
    Example:
        >>> escalators([0], [])
        Traceback (most recent call last):
        NotImplementedError: ICPC-UZ 2023 E: statement not verified yet
    """
    # NOT VERIFIED: заглушка до сверки условия (этап 5)
    raise NotImplementedError("ICPC-UZ 2023 E: statement not verified yet")
