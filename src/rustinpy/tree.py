"""Trees: traversal orders, diameter, rerooting, LCA, Euler tour, HLD, centroid decomposition,
small-to-large, isomorphism.

Деревья. Вершины 0..n-1, adj[u] = соседи (дерево неориентированное). Всё без рекурсии.
"""

from __future__ import annotations

from collections import deque

from rustinpy._registry import algo

NEG_INF = -(1 << 60)


@algo(tags=["tree", "bfs", "order"], cses=["Subordinates (1674)"])
def tree_parents_order(n: int, adj: list[list[int]], root: int = 0) -> tuple[list[int], list[int]]:
    """BFS order and parents of a rooted tree (base of tree DP).   # Порядок обхода дерева.

    When to use:  instead of recursive DFS: process `order` for top-down, reversed for bottom-up.
    Complexity:   O(n)
    Returns:      (order, parent): order[0] = root, parent[root] = -1.
    Related:      subtree_sizes, euler_tour.
    CSES:         Subordinates (1674).
    Example:
        >>> tree_parents_order(5, [[1, 2], [0, 3, 4], [0], [1], [1]])
        ([0, 1, 2, 3, 4], [-1, 0, 0, 1, 1])
    """
    parent = [-1] * n
    order = [root]
    for u in order:  # список растёт во время обхода - это BFS
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                order.append(v)
    return order, parent


@algo(tags=["tree", "subtree", "dp"], cses=["Subordinates (1674)"], requires=["tree_parents_order"])
def subtree_sizes(n: int, adj: list[list[int]], root: int = 0) -> list[int]:
    """Size of every subtree.   # Размеры поддеревьев.

    When to use:  subordinates count, centroid search, rerooting.
    Complexity:   O(n)
    Returns:      size[v] (number of vertices in the subtree of v).
    Pitfalls:     CSES Subordinates asks size - 1.
    Related:      tree_parents_order, find_centroid.
    CSES:         Subordinates (1674).
    Example:
        >>> subtree_sizes(5, [[1, 2], [0, 3, 4], [0], [1], [1]])
        [5, 3, 1, 1, 1]
    """
    order, parent = tree_parents_order(n, adj, root)
    size = [1] * n
    for v in reversed(order):  # снизу вверх
        if parent[v] >= 0:
            size[parent[v]] += size[v]
    return size


def _bfs_dist(n: int, adj: list[list[int]], s: int) -> list[int]:
    dist = [-1] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] < 0:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


@algo(tags=["tree", "diameter", "bfs"], cses=["Tree Diameter (1131)"], requires=["_bfs_dist"])
def tree_diameter(n: int, adj: list[list[int]]) -> tuple[int, int, int]:
    """Longest path of a tree (in edges) by two BFS.   # Диаметр дерева.

    When to use:  diameter, its endpoints, farthest vertices.
    Complexity:   O(n)
    Returns:      (length, a, b) with dist(a, b) = length.
    Pitfalls:     weighted trees: the same two passes with Dijkstra / DFS sums.
    Related:      tree_farthest.
    CSES:         Tree Diameter (1131).
    Example:
        >>> tree_diameter(5, [[1, 2], [0, 3, 4], [0], [1], [1]])
        (3, 3, 2)
    """
    d0 = _bfs_dist(n, adj, 0)
    a = max(range(n), key=d0.__getitem__)  # самая дальняя от произвольной
    da = _bfs_dist(n, adj, a)
    b = max(range(n), key=da.__getitem__)
    return da[b], a, b


@algo(
    tags=["tree", "diameter", "eccentricity"],
    cses=["Tree Distances I (1132)"],
    requires=["_bfs_dist", "tree_diameter"],
)
def tree_farthest(n: int, adj: list[list[int]]) -> list[int]:
    """Distance from every vertex to the farthest vertex.   # Расстояние до самой дальней вершины.

    When to use:  eccentricities; the farthest vertex is always an end of a diameter.
    Complexity:   O(n)
    Returns:      ecc[v].
    Related:      tree_diameter, tree_distance_sums.
    CSES:         Tree Distances I (1132).
    Example:
        >>> tree_farthest(5, [[1, 2], [0, 3, 4], [0], [1], [1]])
        [2, 2, 3, 3, 3]
    """
    _, a, b = tree_diameter(n, adj)
    da, db = _bfs_dist(n, adj, a), _bfs_dist(n, adj, b)
    return [max(x, y) for x, y in zip(da, db)]  # ближе к одному из концов диаметра


@algo(
    tags=["tree", "rerooting", "dp"],
    cses=["Tree Distances II (1133)"],
    requires=["tree_parents_order"],
)
def tree_distance_sums(n: int, adj: list[list[int]]) -> list[int]:
    """Sum of distances from every vertex to all others.   # Суммы расстояний (перекорневание).

    When to use:  classic rerooting DP template.
    Complexity:   O(n)
    Returns:      s[v] = sum_u dist(v, u).
    Idea:         s[child] = s[parent] + n - 2 * size[child].
    Related:      subtree_sizes, tree_farthest.
    CSES:         Tree Distances II (1133).
    Example:
        >>> tree_distance_sums(5, [[1, 2], [0, 3, 4], [0], [1], [1]])
        [6, 5, 9, 8, 8]
    """
    order, parent = tree_parents_order(n, adj, 0)
    size = [1] * n
    down = [0] * n  # сумма расстояний внутри поддерева
    for v in reversed(order):
        p = parent[v]
        if p >= 0:
            size[p] += size[v]
            down[p] += down[v] + size[v]
    res = [0] * n
    res[0] = down[0]
    for v in order[1:]:  # сверху вниз: переносим корень в ребёнка
        res[v] = res[parent[v]] + n - 2 * size[v]
    return res


@algo(
    tags=["tree", "centroid"], cses=["Finding a Centroid (2079)"], requires=["tree_parents_order"]
)
def find_centroid(n: int, adj: list[list[int]]) -> int:
    """A centroid: removing it leaves components of size <= n / 2.   # Центроид дерева.

    When to use:  centroid decomposition, balanced splits.
    Complexity:   O(n)
    Returns:      a centroid vertex.
    Related:      centroid_decomposition, subtree_sizes.
    CSES:         Finding a Centroid (2079).
    Example:
        >>> find_centroid(5, [[1], [0, 2], [1, 3], [2, 4], [3]])
        2
    """
    order, parent = tree_parents_order(n, adj, 0)
    size = [1] * n
    for v in reversed(order):
        if parent[v] >= 0:
            size[parent[v]] += size[v]
    for v in order:
        biggest = n - size[v]  # часть «сверху»
        for u in adj[v]:
            if u != parent[v]:
                biggest = max(biggest, size[u])
        if 2 * biggest <= n:
            return v
    return 0


@algo(tags=["tree", "euler-tour", "subtree"], cses=["Subtree Queries (1137)"])
def euler_tour(n: int, adj: list[list[int]], root: int = 0) -> tuple[list[int], list[int]]:
    """DFS entry indices: subtree of v is [tin[v], tout[v]).   # Эйлеров обход (tin/tout).

    When to use:  turn subtree queries into range queries; ancestor checks.
    Complexity:   O(n)
    Returns:      (tin, tout), tin is a permutation of 0..n-1.
    Pitfalls:     u is an ancestor of v iff tin[u] <= tin[v] < tout[u].
    Related:      SubtreeQueries, PathSumQueries, distinct_colors.
    CSES:         Subtree Queries (1137).
    Example:
        >>> euler_tour(5, [[1, 2], [0, 3, 4], [0], [1], [1]])
        ([0, 1, 4, 2, 3], [5, 4, 5, 3, 4])
    """
    tin = [0] * n
    tout = [0] * n
    parent = [-1] * n
    timer = 0
    stack = [(root, False)]
    while stack:
        v, done = stack.pop()
        if done:
            tout[v] = timer  # всё поддерево уже пронумеровано
            continue
        tin[v] = timer
        timer += 1
        stack.append((v, True))
        for u in reversed(adj[v]):
            if u != parent[v]:
                parent[u] = v
                stack.append((u, False))
    return tin, tout


@algo(
    tags=["tree", "lca", "binary-lifting"],
    cses=["Company Queries I (1687)", "Company Queries II (1688)", "Distance Queries (1135)"],
    requires=["tree_parents_order"],
)
class LCA:
    """Lowest common ancestor by binary lifting.   # LCA двоичными подъёмами.

    When to use:  LCA, k-th ancestor, distances; n, q up to 2 * 10^5.
    Complexity:   O(n log n) build, O(log n) per query
    Methods:      lca(a, b); kth_ancestor(v, k) (-1 if too high); dist(a, b); depth[v];
                  parent[v]
    Python speed: build n = 2 * 10^5 ~ 0.5 s; 2 * 10^5 lca queries ~ 1.5 s.
    Related:      LCAEuler (O(1) query), HLD.
    CSES:         Company Queries I (1687), Company Queries II (1688), Distance Queries (1135).
    Example:
        >>> t = LCA(6, [[1, 2], [0, 3, 4], [0, 5], [1], [1], [2]])
        >>> t.lca(3, 4), t.lca(3, 5), t.kth_ancestor(3, 2), t.kth_ancestor(3, 3), t.dist(4, 5)
        (1, 0, 0, -1, 4)
    """

    def __init__(self, n: int, adj: list[list[int]], root: int = 0) -> None:
        order, parent = tree_parents_order(n, adj, root)
        depth = [0] * n
        for v in order[1:]:
            depth[v] = depth[parent[v]] + 1
        self.parent = parent
        self.depth = depth
        up0 = [p if p >= 0 else v for v, p in enumerate(parent)]  # корень ссылается на себя
        self.up = [up0]
        for _ in range(max(1, n.bit_length())):
            prev = self.up[-1]
            self.up.append([prev[x] for x in prev])

    def kth_ancestor(self, v: int, k: int) -> int:
        if k > self.depth[v]:
            return -1
        j = 0
        while k:
            if k & 1:
                v = self.up[j][v]
            k >>= 1
            j += 1
        return v

    def lca(self, a: int, b: int) -> int:
        if self.depth[a] < self.depth[b]:
            a, b = b, a
        a = self.kth_ancestor(a, self.depth[a] - self.depth[b])  # выравниваем глубины
        if a == b:
            return a
        for row in reversed(self.up):
            if row[a] != row[b]:  # прыгаем, пока предки различаются
                a, b = row[a], row[b]
        return self.up[0][a]

    def dist(self, a: int, b: int) -> int:
        return self.depth[a] + self.depth[b] - 2 * self.depth[self.lca(a, b)]


@algo(tags=["tree", "lca", "euler-tour", "sparse-table"], cses=["Distance Queries (1135)"])
class LCAEuler:
    """LCA via Euler tour + sparse table: O(1) per query.   # LCA через эйлеров обход.

    When to use:  very many LCA queries on a static tree.
    Complexity:   O(n log n) build, O(1) per query
    Methods:      lca(a, b); dist(a, b); depth[v]
    Related:      LCA.
    CSES:         Distance Queries (1135).
    Example:
        >>> t = LCAEuler(6, [[1, 2], [0, 3, 4], [0, 5], [1], [1], [2]])
        >>> t.lca(3, 4), t.lca(3, 5), t.dist(4, 5)
        (1, 0, 4)
    """

    def __init__(self, n: int, adj: list[list[int]], root: int = 0) -> None:
        depth = [0] * n
        first = [0] * n
        euler: list[int] = []
        parent = [-1] * n
        it = [0] * n
        stack = [root]
        first[root] = 0
        euler.append(root)
        while stack:  # эйлеров обход: вершина записывается при каждом возврате
            v = stack[-1]
            if it[v] < len(adj[v]):
                u = adj[v][it[v]]
                it[v] += 1
                if u != parent[v]:
                    parent[u] = v
                    depth[u] = depth[v] + 1
                    first[u] = len(euler)
                    euler.append(u)
                    stack.append(u)
            else:
                stack.pop()
                if stack:
                    euler.append(stack[-1])
        self.depth, self.first = depth, first
        table = [euler]
        k = 1
        m = len(euler)
        while 2 * k <= m:
            prev = table[-1]
            table.append(
                [a if depth[a] < depth[b] else b for a, b in zip(prev[: m - 2 * k + 1], prev[k:])]
            )
            k *= 2
        self.table = table

    def lca(self, a: int, b: int) -> int:
        l, r = self.first[a], self.first[b]
        if l > r:
            l, r = r, l
        r += 1
        k = (r - l).bit_length() - 1
        x, y = self.table[k][l], self.table[k][r - (1 << k)]
        return x if self.depth[x] < self.depth[y] else y  # самая мелкая вершина на отрезке

    def dist(self, a: int, b: int) -> int:
        return self.depth[a] + self.depth[b] - 2 * self.depth[self.lca(a, b)]


@algo(
    tags=["tree", "matching", "greedy"],
    cses=["Tree Matching (1130)"],
    requires=["tree_parents_order"],
)
def tree_matching(n: int, adj: list[list[int]]) -> int:
    """Maximum matching in a tree (greedy from the leaves).   # Паросочетание в дереве.

    When to use:  max number of disjoint edges in a tree.
    Complexity:   O(n)
    Returns:      matching size.
    Idea:         bottom-up: match a vertex with its parent if both are still free.
    Related:      graph.hopcroft_karp.
    CSES:         Tree Matching (1130).
    Example:
        >>> tree_matching(5, [[1, 2], [0, 3, 4], [0], [1], [1]])
        2
    """
    order, parent = tree_parents_order(n, adj, 0)
    used = [False] * n
    res = 0
    for v in reversed(order):
        p = parent[v]
        if p >= 0 and not used[v] and not used[p]:  # жадно берём ребро к родителю
            used[v] = used[p] = True
            res += 1
    return res


@algo(
    tags=["tree", "lca", "difference-array"],
    cses=["Counting Paths (1136)"],
    requires=["tree_parents_order", "LCA"],
)
def counting_paths(n: int, adj: list[list[int]], paths: list[tuple[int, int]]) -> list[int]:
    """For every vertex: how many of the given paths pass through it.   # Разности на дереве.

    When to use:  "add 1 on the path a-b" offline for many paths.
    Complexity:   O((n + q) log n)
    Returns:      cnt[v].
    Idea:         +1 at a and b, -1 at lca and at parent(lca), then subtree sums.
    Related:      LCA, PathSumQueries.
    CSES:         Counting Paths (1136).
    Example:
        >>> counting_paths(5, [[1, 2], [0, 3, 4], [0], [1], [1]], [(3, 4), (3, 2)])
        [1, 2, 1, 2, 1]
    """
    t = LCA(n, adj)
    d = [0] * n
    for a, b in paths:
        c = t.lca(a, b)
        d[a] += 1
        d[b] += 1
        d[c] -= 1
        if t.parent[c] >= 0:
            d[t.parent[c]] -= 1
    order, parent = tree_parents_order(n, adj, 0)
    for v in reversed(order):  # суммы по поддеревьям
        if parent[v] >= 0:
            d[parent[v]] += d[v]
    return d


@algo(
    tags=["tree", "euler-tour", "fenwick", "subtree"],
    cses=["Subtree Queries (1137)"],
    requires=["euler_tour"],
)
class SubtreeQueries:
    """Point update + subtree sum (Euler tour + Fenwick).   # Запросы на поддеревьях.

    When to use:  values on vertices, "change v", "sum of the subtree of v".
    Complexity:   O(n log n) build, O(log n) per operation
    Methods:      set_value(v, x); subtree_sum(v)
    Related:      euler_tour, PathSumQueries.
    CSES:         Subtree Queries (1137).
    Example:
        >>> sq = SubtreeQueries(5, [[1, 2], [0, 3, 4], [0], [1], [1]], [4, 2, 5, 2, 1])
        >>> sq.subtree_sum(1), sq.subtree_sum(0)
        (5, 14)
        >>> sq.set_value(3, 10); sq.subtree_sum(1)
        13
    """

    def __init__(self, n: int, adj: list[list[int]], values: list[int], root: int = 0) -> None:
        self.tin, self.tout = euler_tour(n, adj, root)
        self.n = n
        self.val = list(values)
        self.t = [0] * (n + 1)
        for v in range(n):
            self._add(self.tin[v], values[v])

    def _add(self, i: int, d: int) -> None:
        i += 1
        while i <= self.n:
            self.t[i] += d
            i += i & -i

    def _pref(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s

    def set_value(self, v: int, x: int) -> None:
        self._add(self.tin[v], x - self.val[v])
        self.val[v] = x

    def subtree_sum(self, v: int) -> int:
        return self._pref(self.tout[v]) - self._pref(self.tin[v])  # отрезок поддерева


@algo(
    tags=["tree", "euler-tour", "fenwick", "path"],
    cses=["Path Queries (1138)"],
    requires=["euler_tour"],
)
class PathSumQueries:
    """Point update + sum on the root -> v path.   # Суммы на пути от корня.

    When to use:  "change value of v", "sum of values from the root to v".
    Complexity:   O(n log n) build, O(log n) per operation
    Methods:      set_value(v, x); path_sum(v)
    Idea:         value of v contributes to every vertex of its subtree -> range add on
                  [tin, tout), point query at tin.
    Related:      SubtreeQueries, HLD (arbitrary paths).
    CSES:         Path Queries (1138).
    Example:
        >>> pq = PathSumQueries(5, [[1, 2], [0, 3, 4], [0], [1], [1]], [4, 2, 5, 2, 1])
        >>> pq.path_sum(3), pq.path_sum(2)
        (8, 9)
        >>> pq.set_value(1, 5); pq.path_sum(4)
        10
    """

    def __init__(self, n: int, adj: list[list[int]], values: list[int], root: int = 0) -> None:
        self.tin, self.tout = euler_tour(n, adj, root)
        self.n = n
        self.val = list(values)
        self.t = [0] * (n + 1)
        for v in range(n):
            self._range_add(self.tin[v], self.tout[v], values[v])

    def _add(self, i: int, d: int) -> None:
        i += 1
        while i <= self.n:
            self.t[i] += d
            i += i & -i

    def _range_add(self, l: int, r: int, d: int) -> None:
        self._add(l, d)  # разностный массив
        if r < self.n:
            self._add(r, -d)

    def set_value(self, v: int, x: int) -> None:
        self._range_add(self.tin[v], self.tout[v], x - self.val[v])
        self.val[v] = x

    def path_sum(self, v: int) -> int:
        i, s = self.tin[v] + 1, 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s


@algo(
    tags=["tree", "hld", "segment-tree", "path"],
    cses=["Path Queries II (2134)"],
    requires=["NEG_INF", "tree_parents_order"],
)
class HLD:
    """Heavy-light decomposition with a max segment tree on paths.   # Тяжёлые пути (HLD).

    When to use:  point update + query on ARBITRARY paths (max, sum, ...).
    Complexity:   O(n) build, O(log^2 n) per path query
    Methods:      set_value(v, x); path_max(a, b); lca(a, b)
    Pitfalls:     for sums replace max by + and NEG_INF by 0 in the segment tree.
    Python speed: build n = 2 * 10^5 + 2 * 10^5 path queries ~ 2.5 s in CPython.
    Related:      LCA, PathSumQueries.
    CSES:         Path Queries II (2134).
    Example:
        >>> h = HLD(5, [[1, 2], [0, 3, 4], [0], [1], [1]], [2, 4, 1, 3, 3])
        >>> h.path_max(3, 2), h.path_max(3, 4), h.lca(3, 4)
        (4, 4, 1)
        >>> h.set_value(1, 0); h.path_max(3, 4)
        3
    """

    def __init__(self, n: int, adj: list[list[int]], values: list[int], root: int = 0) -> None:
        order, parent = tree_parents_order(n, adj, root)
        size = [1] * n
        heavy = [-1] * n
        depth = [0] * n
        for v in order[1:]:
            depth[v] = depth[parent[v]] + 1
        for v in reversed(order):
            p = parent[v]
            if p >= 0:
                size[p] += size[v]
                if heavy[p] == -1 or size[v] > size[heavy[p]]:
                    heavy[p] = v  # самый тяжёлый ребёнок
        head = [0] * n
        pos = [0] * n
        cur = 0
        for v in order:
            if parent[v] == -1 or heavy[parent[v]] != v:  # начало новой цепочки
                u = v
                while u != -1:
                    head[u] = v
                    pos[u] = cur
                    cur += 1
                    u = heavy[u]
        self.parent, self.depth, self.head, self.pos = parent, depth, head, pos
        size2 = 1
        while size2 < n:
            size2 <<= 1
        self.size = size2
        self.t = [NEG_INF] * (2 * size2)
        for v in range(n):
            self.t[size2 + pos[v]] = values[v]
        for i in range(size2 - 1, 0, -1):
            self.t[i] = max(self.t[2 * i], self.t[2 * i + 1])

    def set_value(self, v: int, x: int) -> None:
        i = self.size + self.pos[v]
        self.t[i] = x
        i >>= 1
        while i:
            self.t[i] = max(self.t[2 * i], self.t[2 * i + 1])
            i >>= 1

    def _query(self, l: int, r: int) -> int:
        res = NEG_INF
        l += self.size
        r += self.size
        t = self.t
        while l < r:
            if l & 1:
                res = max(res, t[l])
                l += 1
            if r & 1:
                r -= 1
                res = max(res, t[r])
            l >>= 1
            r >>= 1
        return res

    def path_max(self, a: int, b: int) -> int:
        head, pos, depth, parent = self.head, self.pos, self.depth, self.parent
        res = NEG_INF
        while head[a] != head[b]:  # поднимаемся по цепочкам
            if depth[head[a]] < depth[head[b]]:
                a, b = b, a
            res = max(res, self._query(pos[head[a]], pos[a] + 1))
            a = parent[head[a]]
        if depth[a] > depth[b]:
            a, b = b, a
        return max(res, self._query(pos[a], pos[b] + 1))  # общая цепочка

    def lca(self, a: int, b: int) -> int:
        head, depth, parent = self.head, self.depth, self.parent
        while head[a] != head[b]:
            if depth[head[a]] < depth[head[b]]:
                a, b = b, a
            a = parent[head[a]]
        return a if depth[a] < depth[b] else b


@algo(tags=["tree", "centroid", "decomposition"], cses=["Finding a Centroid (2079)"])
def centroid_decomposition(n: int, adj: list[list[int]]) -> list[int]:
    """Centroid tree: parent of every vertex in it.   # Центроидная декомпозиция.

    When to use:  path counting / nearest marked vertex / distance queries on trees.
    Complexity:   O(n log n)
    Returns:      cpar[v] (-1 for the top centroid); depth in this tree is O(log n).
    Related:      fixed_length_paths, fixed_length_paths_range, find_centroid.
    CSES:         Finding a Centroid (2079) (top centroid), Fixed-Length Paths I/II.
    Example:
        >>> centroid_decomposition(5, [[1], [0, 2], [1, 3], [2, 4], [3]])
        [1, 2, -1, 2, 3]
    """
    removed = [False] * n
    cpar = [-1] * n
    size = [0] * n
    par = [-1] * n
    stack = [(0, -1)] if n else []
    while stack:
        s, pc = stack.pop()
        order = [s]  # BFS по текущей компоненте
        par[s] = -1
        for u in order:
            for v in adj[u]:
                if v != par[u] and not removed[v]:
                    par[v] = u
                    order.append(v)
        for u in reversed(order):
            size[u] = 1
            for v in adj[u]:
                if v != par[u] and not removed[v]:
                    size[u] += size[v]
        total = len(order)
        c = s
        for u in order:
            biggest = total - size[u]
            for v in adj[u]:
                if v != par[u] and not removed[v]:
                    biggest = max(biggest, size[v])
            if 2 * biggest <= total:
                c = u
                break
        removed[c] = True
        cpar[c] = pc
        for v in adj[c]:
            if not removed[v]:
                stack.append((v, c))  # рекурсия заменена стеком компонент
    return cpar


def _centroid_levels(n: int, cpar: list[int]) -> list[int]:
    """Depth of every vertex in the centroid tree."""
    level = [-1] * n
    for v in range(n):
        path = []
        u = v
        while u != -1 and level[u] == -1:
            path.append(u)
            u = cpar[u]
        base = level[u] if u != -1 else -1
        for x in reversed(path):
            base += 1
            level[x] = base
    return level


@algo(
    tags=["tree", "centroid", "paths", "counting"],
    cses=["Fixed-Length Paths I (2080)"],
    requires=["centroid_decomposition", "_centroid_levels"],
)
def fixed_length_paths(n: int, adj: list[list[int]], k: int) -> int:
    """Number of paths with exactly k edges.   # Пути длины ровно k.

    When to use:  count vertex pairs at distance k.
    Complexity:   O(n log n)
    Returns:      number of unordered pairs (u, v) with dist(u, v) = k.
    Python speed: n = 2 * 10^5 ~ 1.5-3 s in CPython (depends on the tree shape).
    Idea:         for every centroid c, count paths through c: depths of each child subtree
                  against the counts of previously processed subtrees (cnt[0] = 1 for c).
    Related:      centroid_decomposition, fixed_length_paths_range.
    CSES:         Fixed-Length Paths I (2080).
    Example:
        >>> fixed_length_paths(5, [[1, 2], [0, 3, 4], [0], [1], [1]], 2)
        4
    """
    cpar = centroid_decomposition(n, adj)
    level = _centroid_levels(n, cpar)
    total = 0
    for c in range(n):
        lc = level[c]
        cnt = [1]  # cnt[d] - вершин на глубине d в уже обработанных поддеревьях
        for start in adj[c]:
            if level[start] <= lc:
                continue  # вершина вне компоненты центроида
            depths = []
            q = [(start, c, 1)]
            for v, p, d in q:  # BFS с ограничением глубины k
                depths.append(d)
                if d < k:
                    for w in adj[v]:
                        if w != p and level[w] > lc:
                            q.append((w, v, d + 1))
            for d in depths:
                if k - d < len(cnt):
                    total += cnt[k - d]
            for d in depths:
                while len(cnt) <= d:
                    cnt.append(0)
                cnt[d] += 1
    return total


@algo(
    tags=["tree", "centroid", "paths", "counting"],
    cses=["Fixed-Length Paths II (2081)"],
    requires=["centroid_decomposition", "_centroid_levels"],
)
def fixed_length_paths_range(n: int, adj: list[list[int]], k1: int, k2: int) -> int:
    """Number of paths whose length is in [k1, k2].   # Пути длины от k1 до k2.

    When to use:  count pairs with distance in a range.
    Complexity:   O(n log n) (subtrees merged by increasing depth, prefix sums rebuilt)
    Returns:      number of unordered pairs with k1 <= dist <= k2.
    Python speed: n = 2 * 10^5 ~ 2 s in CPython.
    Related:      fixed_length_paths.
    CSES:         Fixed-Length Paths II (2081).
    Example:
        >>> fixed_length_paths_range(5, [[1, 2], [0, 3, 4], [0], [1], [1]], 1, 2)
        8
    """
    cpar = centroid_decomposition(n, adj)
    level = _centroid_levels(n, cpar)
    total = 0
    for c in range(n):
        lc = level[c]
        subs = []
        for start in adj[c]:
            if level[start] <= lc:
                continue
            hist = [0]
            q = [(start, c, 1)]
            for v, p, d in q:
                while len(hist) <= d:
                    hist.append(0)
                hist[d] += 1
                if d < k2:
                    for w in adj[v]:
                        if w != p and level[w] > lc:
                            q.append((w, v, d + 1))
            subs.append(hist)
        subs.sort(key=len)  # по возрастанию глубины - суммарно O(размер компоненты)
        acc = [1]
        pre = [0, 1]
        for hist in subs:
            for d in range(1, len(hist)):
                if hist[d]:
                    lo, hi = max(0, k1 - d), min(len(acc) - 1, k2 - d)
                    if lo <= hi:
                        total += hist[d] * (pre[hi + 1] - pre[lo])
            while len(acc) < len(hist):
                acc.append(0)
            for d in range(1, len(hist)):
                acc[d] += hist[d]
            pre = [0] * (len(acc) + 1)
            for i, x in enumerate(acc):
                pre[i + 1] = pre[i] + x
    return total


@algo(
    tags=["tree", "small-to-large", "sets"],
    cses=["Distinct Colors (1139)"],
    requires=["tree_parents_order"],
)
def distinct_colors(n: int, adj: list[list[int]], colors: list[int]) -> list[int]:
    """Number of distinct colours in every subtree.   # Различные цвета в поддеревьях.

    When to use:  subtree statistics that merge as sets / maps.
    Complexity:   O(n log n) set insertions
    Returns:      ans[v].
    Idea:         keep the biggest child's set, pour the smaller ones into it.
    Related:      euler_tour (+ offline distinct_values_queries).
    CSES:         Distinct Colors (1139).
    Example:
        >>> distinct_colors(5, [[1, 2], [0, 3, 4], [0], [1], [1]], [2, 3, 2, 2, 1])
        [3, 3, 1, 1, 1]
    """
    order, parent = tree_parents_order(n, adj, 0)
    sets: list[set[int] | None] = [None] * n
    ans = [0] * n
    for v in reversed(order):
        best: set[int] | None = None
        for u in adj[v]:
            if u != parent[v]:
                su = sets[u]
                if su is not None and (best is None or len(su) > len(best)):
                    best = su
        if best is None:
            best = set()
        for u in adj[v]:
            if u != parent[v]:
                su = sets[u]
                if su is not None and su is not best:
                    best |= su  # меньшее вливаем в большее
                sets[u] = None
        best.add(colors[v])
        sets[v] = best
        ans[v] = len(best)
    return ans


def _canon_ids(n: int, adj: list[list[int]], root: int, table: dict[tuple[int, ...], int]) -> int:
    """AHU canonical id of the tree rooted at root (shared table across trees)."""
    parent = [-1] * n
    order = [root]
    for u in order:
        for v in adj[u]:
            if v != parent[u]:
                parent[v] = u
                order.append(v)
    ident = [0] * n
    kids: list[list[int]] = [[] for _ in range(n)]
    for v in reversed(order):
        key = tuple(sorted(kids[v]))
        ident[v] = table.setdefault(key, len(table))
        if parent[v] >= 0:
            kids[parent[v]].append(ident[v])
    return ident[root]


def _centers(n: int, adj: list[list[int]]) -> list[int]:
    """One or two centers of a tree (leaf peeling)."""
    if n <= 2:
        return list(range(n))
    deg = [len(a) for a in adj]
    layer = [v for v in range(n) if deg[v] == 1]
    left = n
    while left > 2:
        left -= len(layer)
        nxt = []
        for v in layer:
            for u in adj[v]:
                deg[u] -= 1
                if deg[u] == 1:
                    nxt.append(u)
        layer = nxt
    return layer


@algo(
    tags=["tree", "isomorphism", "hashing", "ahu"],
    cses=["Tree Isomorphism I (1700)", "Tree Isomorphism II (1701)"],
    requires=["_canon_ids", "_centers"],
)
def tree_isomorphic(
    n: int, adj1: list[list[int]], adj2: list[list[int]], rooted: bool = True
) -> bool:
    """Are two trees isomorphic? (AHU canonical forms).   # Изоморфизм деревьев.

    When to use:  compare tree shapes; rooted at 0, or unrooted (via centers).
    Complexity:   O(n log n)
    Returns:      True iff isomorphic.
    Idea:         id(v) = index of the sorted tuple of children ids in a shared dictionary;
                  unrooted trees are compared rooted at their centers.
    Related:      tree_diameter.
    CSES:         Tree Isomorphism I (1700) (rooted), Tree Isomorphism II (1701) (unrooted).
    Example:
        >>> a = [[1, 2], [0], [0, 3], [2]]  # путь 1-0-2-3, корень 0 в середине
        >>> b = [[1], [0, 2], [1, 3], [2]]  # путь 0-1-2-3, корень 0 на конце
        >>> star = [[1], [0, 2, 3], [1], [1]]
        >>> tree_isomorphic(4, a, b), tree_isomorphic(4, a, b, rooted=False)
        (False, True)
        >>> tree_isomorphic(4, a, star, rooted=False)
        False
    """
    table: dict[tuple[int, ...], int] = {}
    if rooted:
        return _canon_ids(n, adj1, 0, table) == _canon_ids(n, adj2, 0, table)
    c1 = _centers(n, adj1)
    c2 = _centers(n, adj2)
    if len(c1) != len(c2):
        return False
    first = _canon_ids(n, adj1, c1[0], table)  # корень в центре первого дерева
    return any(_canon_ids(n, adj2, c, table) == first for c in c2)


@algo(tags=["tree", "greedy", "leaves"], icpc=["2025 F"], verified=False, stub=True)
def fix_the_leak(n: int, parent: list[int], k: int) -> int:
    """ICPC-UZ 2025 F "Fix the Leak": remove exactly k agents, minimise leaves.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return the minimal number of leaves.
    Idea:         tree given by parents p_i < i (so vertices are already in topological order:
                  process i = n-1..1 for bottom-up DP). What an "agent" and a "chain" are is
                  unknown - NOT VERIFIED until the statement is checked.
    ICPC-UZ:      2025 F.
    Example:
        >>> fix_the_leak(1, [-1], 0)
        Traceback (most recent call last):
        NotImplementedError: ICPC-UZ 2025 F: statement not verified yet
    """
    # NOT VERIFIED: заглушка до сверки условия (этап 5)
    raise NotImplementedError("ICPC-UZ 2025 F: statement not verified yet")
