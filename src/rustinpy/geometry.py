"""Computational geometry on integer points: orientation, segments, polygons, convex hull,
closest pair, Manhattan tricks, sweep lines, Li Chao (max), 3D determinants.

Геометрия. Точки - кортежи (x, y) целых чисел: точная арифметика без float.
"""

from __future__ import annotations

import math
from bisect import bisect_left, bisect_right
from fractions import Fraction
from typing import NamedTuple

from rustinpy._registry import algo

Pt = tuple[int, int]


@algo(tags=["geometry", "point", "vector"], cses=["- (vector helper)"])
class Point(NamedTuple):
    """2D integer point / vector with the usual operations.   # Точка / вектор.

    When to use:  readable vector code; for speed use plain tuples and cross() below.
    Complexity:   O(1) per operation
    Methods:      p + q, p - q, p.cross(q), p.dot(q), p.norm2()
    Related:      cross, dot, orientation.
    CSES:         - (vector helper)
    Example:
        >>> a, b = Point(1, 2), Point(3, -1)
        >>> a + b, b - a, a.cross(b), a.dot(b), a.norm2()
        (Point(x=4, y=1), Point(x=2, y=-3), -7, 1, 5)
    """

    x: int
    y: int

    def __add__(self, o: object) -> Point:
        assert isinstance(o, Point)
        return Point(self.x + o.x, self.y + o.y)

    def __sub__(self, o: Point) -> Point:
        return Point(self.x - o.x, self.y - o.y)

    def cross(self, o: Point) -> int:
        return self.x * o.y - self.y * o.x  # > 0: o левее self

    def dot(self, o: Point) -> int:
        return self.x * o.x + self.y * o.y

    def norm2(self) -> int:
        return self.x * self.x + self.y * self.y


@algo(tags=["geometry", "cross-product"], cses=["Point Location Test (2189)"])
def cross(o: Pt, a: Pt, b: Pt) -> int:
    """Cross product (a - o) x (b - o).   # Векторное произведение.

    When to use:  orientation tests, areas, convex hulls - everything in 2D.
    Complexity:   O(1)
    Returns:      > 0 if o -> a -> b turns left (counter-clockwise), < 0 right, 0 collinear.
    Related:      orientation, dot, polygon_area2.
    CSES:         Point Location Test (2189).
    Example:
        >>> cross((0, 0), (1, 0), (0, 1)), cross((0, 0), (1, 1), (2, 2))
        (1, 0)
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


@algo(tags=["geometry", "dot-product"], cses=["- (angles, projections)"])
def dot(o: Pt, a: Pt, b: Pt) -> int:
    """Dot product (a - o) . (b - o).   # Скалярное произведение.

    When to use:  angle sign (acute / obtuse), projections, "is the point inside the segment".
    Complexity:   O(1)
    Returns:      integer dot product.
    Related:      cross.
    CSES:         - (angles, projections)
    Example:
        >>> dot((0, 0), (1, 0), (0, 1)), dot((0, 0), (2, 1), (3, 1))
        (0, 7)
    """
    return (a[0] - o[0]) * (b[0] - o[0]) + (a[1] - o[1]) * (b[1] - o[1])


@algo(tags=["geometry", "orientation"], cses=["Point Location Test (2189)"], requires=["cross"])
def orientation(a: Pt, b: Pt, c: Pt) -> int:
    """Sign of the turn a -> b -> c: 1 left, -1 right, 0 collinear.   # Ориентация тройки точек.

    When to use:  predicates for segment intersection and hulls.
    Complexity:   O(1)
    Returns:      -1, 0 or 1.
    Related:      cross, point_location.
    CSES:         Point Location Test (2189).
    Example:
        >>> orientation((0, 0), (2, 0), (1, 1)), orientation((0, 0), (2, 0), (1, -1))
        (1, -1)
    """
    v = cross(a, b, c)
    return (v > 0) - (v < 0)


@algo(tags=["geometry", "orientation"], cses=["Point Location Test (2189)"], requires=["cross"])
def point_location(p1: Pt, p2: Pt, p3: Pt) -> str:
    """Where is p3 relative to the directed line p1 -> p2.   # Положение точки относительно прямой.

    When to use:  CSES Point Location Test.
    Complexity:   O(1)
    Returns:      "LEFT", "RIGHT" or "TOUCH".
    Related:      orientation.
    CSES:         Point Location Test (2189).
    Example:
        >>> [point_location((1, 1), (5, 3), p) for p in [(2, 3), (4, 1), (3, 2)]]
        ['LEFT', 'RIGHT', 'TOUCH']
    """
    v = cross(p1, p2, p3)
    return "LEFT" if v > 0 else ("RIGHT" if v < 0 else "TOUCH")


@algo(tags=["geometry", "segment"], cses=["Line Segment Intersection (2190)"], requires=["cross"])
def on_segment(p: Pt, a: Pt, b: Pt) -> bool:
    """Does p lie on the closed segment [a, b]?   # Точка на отрезке.

    When to use:  boundary checks, degenerate intersections.
    Complexity:   O(1)
    Returns:      True / False.
    Related:      segments_intersect, point_in_polygon.
    CSES:         Line Segment Intersection (2190).
    Example:
        >>> on_segment((1, 1), (0, 0), (2, 2)), on_segment((3, 3), (0, 0), (2, 2))
        (True, False)
    """
    return (
        cross(a, b, p) == 0
        and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
        and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])  # коллинеарна и внутри рамки
    )


@algo(
    tags=["geometry", "segment", "intersection"],
    cses=["Line Segment Intersection (2190)"],
    requires=["cross", "on_segment"],
)
def segments_intersect(p1: Pt, p2: Pt, p3: Pt, p4: Pt) -> bool:
    """Do closed segments [p1, p2] and [p3, p4] share at least one point?   # Пересечение отрезков.

    When to use:  exact intersection test with all degenerate cases (touching, overlapping).
    Complexity:   O(1)
    Returns:      True / False.
    Pitfalls:     collinear segments need the bounding-box check (handled by on_segment).
    Related:      segment_intersection_point, on_segment.
    CSES:         Line Segment Intersection (2190).
    Example:
        >>> segments_intersect((1, 1), (5, 3), (1, 2), (4, 3))
        False
        >>> segments_intersect((1, 1), (5, 3), (1, 1), (4, 3))  # общий конец
        True
        >>> segments_intersect((0, 0), (2, 2), (1, 1), (3, 3))  # наложение
        True
    """
    d1 = cross(p3, p4, p1)
    d2 = cross(p3, p4, p2)
    d3 = cross(p1, p2, p3)
    d4 = cross(p1, p2, p4)
    if ((d1 > 0) != (d2 > 0) and d1 and d2) and ((d3 > 0) != (d4 > 0) and d3 and d4):
        return True  # собственное пересечение
    return (
        on_segment(p1, p3, p4)
        or on_segment(p2, p3, p4)
        or on_segment(p3, p1, p2)
        or on_segment(p4, p1, p2)
    )


@algo(
    tags=["geometry", "segment", "intersection"],
    cses=["- (intersection point)"],
    requires=["cross", "on_segment", "segments_intersect"],
)
def segment_intersection_point(p1: Pt, p2: Pt, p3: Pt, p4: Pt) -> tuple[Fraction, Fraction] | None:
    """The unique common point of two segments (exact fractions).   # Точка пересечения отрезков.

    When to use:  the coordinates of the intersection are needed.
    Complexity:   O(1)
    Returns:      (x, y) as Fractions if the segments meet in exactly one point, else None
                  (disjoint or overlapping on a piece).
    Related:      segments_intersect.
    CSES:         - (intersection point)
    Example:
        >>> segment_intersection_point((0, 0), (2, 2), (0, 2), (2, 0))
        (Fraction(1, 1), Fraction(1, 1))
        >>> segment_intersection_point((0, 0), (2, 2), (1, 1), (3, 3)) is None
        True
    """
    if not segments_intersect(p1, p2, p3, p4):
        return None
    dx1, dy1 = p2[0] - p1[0], p2[1] - p1[1]
    dx2, dy2 = p4[0] - p3[0], p4[1] - p3[1]
    den = dx1 * dy2 - dy1 * dx2
    if den == 0:  # параллельны: общая точка единственна, только если касаются концами
        common = {p for p in (p1, p2) if on_segment(p, p3, p4)} | {
            p for p in (p3, p4) if on_segment(p, p1, p2)
        }
        if len(common) == 1:
            x, y = common.pop()
            return Fraction(x), Fraction(y)
        return None
    t = Fraction((p3[0] - p1[0]) * dy2 - (p3[1] - p1[1]) * dx2, den)
    return p1[0] + t * dx1, p1[1] + t * dy1


@algo(tags=["geometry", "polygon", "area", "shoelace"], cses=["Polygon Area (2191)"])
def polygon_area2(poly: list[Pt]) -> int:
    """Twice the signed area of a polygon (shoelace formula).   # Удвоенная площадь многоугольника.

    When to use:  polygon area, orientation of a polygon (sign), Pick's theorem.
    Complexity:   O(n)
    Returns:      2 * area, positive for counter-clockwise order.
    Related:      polygon_lattice_points, point_in_polygon.
    CSES:         Polygon Area (2191) (print abs value).
    Example:
        >>> polygon_area2([(1, 1), (4, 2), (3, 5), (1, 4)])
        16
    """
    s = 0
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1  # формула шнурования
    return s


@algo(
    tags=["geometry", "polygon", "point-in-polygon"],
    cses=["Point in Polygon (2192)"],
    requires=["cross", "on_segment"],
)
def point_in_polygon(poly: list[Pt], p: Pt) -> str:
    """Point inside / outside / on the boundary of a simple polygon.   # Точка в многоугольнике.

    When to use:  any simple polygon (not necessarily convex).
    Complexity:   O(n)
    Returns:      "INSIDE", "OUTSIDE" or "BOUNDARY".
    Idea:         ray to the right; count edges crossing it with the half-open rule
                  (one endpoint strictly above, the other not) - no float, no vertex trouble.
    Related:      on_segment, polygon_area2.
    CSES:         Point in Polygon (2192).
    Example:
        >>> poly = [(1, 1), (4, 1), (3, 3), (1, 4)]
        >>> [point_in_polygon(poly, q) for q in [(2, 2), (4, 4), (2, 1)]]
        ['INSIDE', 'OUTSIDE', 'BOUNDARY']
    """
    n = len(poly)
    inside = False
    y = p[1]
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if on_segment(p, a, b):
            return "BOUNDARY"
        if (a[1] > y) != (b[1] > y):  # ребро пересекает горизонталь y
            # точка пересечения правее p? знак проверяем без деления
            c = cross(a, b, p)
            if (c > 0) == (b[1] > a[1]):
                inside = not inside
    return "INSIDE" if inside else "OUTSIDE"


@algo(
    tags=["geometry", "polygon", "pick"],
    cses=["Polygon Lattice Points (2193)"],
    requires=["polygon_area2"],
)
def polygon_lattice_points(poly: list[Pt]) -> tuple[int, int]:
    """Lattice points inside and on the boundary (Pick).   # Целые точки многоугольника.

    When to use:  count integer points of a lattice polygon.
    Complexity:   O(n log C)
    Returns:      (interior, boundary).
    Idea:         boundary = sum gcd(|dx|, |dy|) over edges; Pick: A = I + B/2 - 1.
    Related:      polygon_area2.
    CSES:         Polygon Lattice Points (2193).
    Example:
        >>> polygon_lattice_points([(1, 1), (5, 3), (3, 5), (1, 4)])
        (6, 8)
    """
    n = len(poly)
    b = 0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        b += math.gcd(abs(x2 - x1), abs(y2 - y1))  # целые точки на ребре (без начала)
    a2 = abs(polygon_area2(poly))
    interior = (a2 - b + 2) // 2  # 2A = 2I + B - 2
    return interior, b


@algo(tags=["geometry", "convex-hull", "andrew"], cses=["Convex Hull (2195)"], requires=["cross"])
def convex_hull(points: list[Pt], keep_collinear: bool = False) -> list[Pt]:
    """Convex hull by Andrew's monotone chain, counter-clockwise.   # Выпуклая оболочка.

    When to use:  hull of up to 2 * 10^5 points.
    Complexity:   O(n log n)
    Returns:      hull vertices CCW starting from the lowest-leftmost point; with
                  keep_collinear=True also the points lying on hull edges (CSES).
    Pitfalls:     duplicates are removed; all-collinear input returns the sorted points
                  (keep_collinear) or the two extremes.
    Related:      cross, polygon_area2.
    CSES:         Convex Hull (2195) (keep_collinear=True).
    Example:
        >>> pts = [(0, 0), (2, 0), (1, 1), (2, 2), (0, 2), (1, 0)]
        >>> convex_hull(pts), len(convex_hull(pts, keep_collinear=True))
        ([(0, 0), (2, 0), (2, 2), (0, 2)], 5)
    """
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def build(seq: list[Pt]) -> list[Pt]:
        h: list[Pt] = []
        for p in seq:
            while len(h) >= 2:
                c = cross(h[-2], h[-1], p)
                if c < 0 or (c == 0 and not keep_collinear):
                    h.pop()  # правый поворот (или прямая) - точка не на оболочке
                else:
                    break
            h.append(p)
        return h

    lower = build(pts)
    upper = build(pts[::-1])
    hull = lower[:-1] + upper[:-1]
    return list(dict.fromkeys(hull))  # убираем повторы при полностью коллинеарном входе


@algo(
    tags=["geometry", "closest-pair", "divide-and-conquer"],
    cses=["Minimum Euclidean Distance (2194)"],
)
def closest_pair(points: list[Pt]) -> int:
    """Squared distance of the closest pair (bottom-up divide & conquer).   # Ближайшая пара точек.

    When to use:  n up to 2 * 10^5 points.
    Complexity:   O(n log n)
    Returns:      minimal squared Euclidean distance (needs >= 2 points).
    Idea:         merge sort by y over x-sorted blocks of size 1, 2, 4, ...; while merging
                  two blocks check only points within d of the dividing x in y-order.
    Related:      closest_pair_sweep.
    CSES:         Minimum Euclidean Distance (2194) (prints the squared distance).
    Example:
        >>> closest_pair([(2, 1), (4, 4), (1, 2), (6, 3)])
        2
    """
    pts = sorted(points)
    n = len(pts)
    best = 1 << 62
    for i in range(n - 1):  # повтор точки - сразу 0
        if pts[i] == pts[i + 1]:
            return 0
    ys = [[p] for p in pts]  # блоки, отсортированные по y
    width = 1
    while width < n:
        merged = []
        for start in range(0, n, 2 * width):
            left = ys[start // width]
            right = ys[start // width + 1] if start // width + 1 < len(ys) else []
            if not right:
                merged.append(left)
                continue
            mid_x = pts[start + width][0]  # разделяющая вертикаль
            block = sorted(left + right, key=lambda p: p[1])  # Timsort сливает за O(n)
            strip = [p for p in block if (p[0] - mid_x) ** 2 < best]
            for i, p in enumerate(strip):
                for q in strip[i + 1 :]:
                    dy = q[1] - p[1]
                    if dy * dy >= best:
                        break
                    d = (q[0] - p[0]) ** 2 + dy * dy
                    if d < best:
                        best = d
            merged.append(block)
        ys = merged
        width *= 2
    return best


@algo(tags=["geometry", "closest-pair", "sweep-line"], cses=["Minimum Euclidean Distance (2194)"])
def closest_pair_sweep(points: list[Pt]) -> int:
    """Closest pair by a sweep over x with a y-ordered window.   # Ближайшая пара (сканирование).

    When to use:  same as closest_pair; shorter to write.
    Complexity:   O(n log n) comparisons (+ list insertions, C-fast memmove)
    Returns:      minimal squared distance.
    Python speed: 2 * 10^5 random points ~ 0.3 s; adversarial (all on one vertical) is slower.
    Related:      closest_pair.
    CSES:         Minimum Euclidean Distance (2194).
    Example:
        >>> closest_pair_sweep([(2, 1), (4, 4), (1, 2), (6, 3)])
        2
    """
    pts = sorted(points)
    best = 1 << 62
    window: list[tuple[int, int]] = []  # (y, x) точек с x > текущий - d
    left = 0
    for x, y in pts:
        d = math.isqrt(best) + 1
        while pts[left][0] < x - d:  # выкидываем далёкие по x
            lx, ly = pts[left]
            window.pop(bisect_left(window, (ly, lx)))
            left += 1
        lo = bisect_left(window, (y - d, -(1 << 62)))
        hi = bisect_right(window, (y + d, 1 << 62))
        for wy, wx in window[lo:hi]:
            dd = (wx - x) ** 2 + (wy - y) ** 2
            if dd < best:
                best = dd
        window.insert(bisect_left(window, (y, x)), (y, x))
    return best


@algo(tags=["geometry", "manhattan", "rotation"], cses=["Maximum Manhattan Distances (3410)"])
def max_manhattan_distances(points: list[Pt]) -> list[int]:
    """Max Manhattan distance after adding each point.   # Максимальное манхэттенское расстояние.

    When to use:  |dx| + |dy| = max(|du|, |dv|) with u = x + y, v = x - y (45 degree turn).
    Complexity:   O(n)
    Returns:      list of answers, 0 for the first point.
    Related:      all_manhattan_distances_sum.
    CSES:         Maximum Manhattan Distances (3410).
    Example:
        >>> max_manhattan_distances([(1, 1), (3, 2), (2, 4), (0, 0)])
        [0, 3, 4, 6]
    """
    res = []
    umin = vmin = 1 << 62
    umax = vmax = -(1 << 62)
    for x, y in points:
        u, v = x + y, x - y  # поворот на 45 градусов
        umin, umax = min(umin, u), max(umax, u)
        vmin, vmax = min(vmin, v), max(vmax, v)
        res.append(max(umax - umin, vmax - vmin))
    return res


@algo(tags=["geometry", "manhattan", "prefix-sums"], cses=["All Manhattan Distances (3411)"])
def all_manhattan_distances_sum(points: list[Pt]) -> int:
    """Sum of Manhattan distances over all unordered pairs.   # Сумма всех манхэттенских расстояний.

    When to use:  coordinates separate: sum |x_i - x_j| + sum |y_i - y_j|.
    Complexity:   O(n log n)
    Returns:      the total.
    Related:      max_manhattan_distances.
    CSES:         All Manhattan Distances (3411).
    Example:
        >>> all_manhattan_distances_sum([(1, 1), (3, 2), (2, 4)])  # 3 + 4 + 3
        10
    """
    total = 0
    for coord in (0, 1):
        vals = sorted(p[coord] for p in points)
        pref = 0
        for i, v in enumerate(vals):
            total += v * i - pref  # вклад v со всеми меньшими
            pref += v
    return total


@algo(tags=["geometry", "sweep-line", "fenwick"], cses=["Intersection Points (1740)"])
def intersection_points_count(segments: list[tuple[int, int, int, int]]) -> int:
    """Intersections of horizontal and vertical segments.   # Точки пересечения.

    When to use:  axis-parallel segments; horizontal-horizontal / vertical-vertical never meet.
    Complexity:   O(n log n)
    Input:        segments (x1, y1, x2, y2), each horizontal or vertical.
    Returns:      number of (horizontal, vertical) pairs that intersect (endpoints included).
    Idea:         sweep x; a horizontal segment is active on [x1, x2]; a vertical one counts
                  active y in [y1, y2] with a Fenwick tree over compressed y.
    Related:      area_of_rectangles.
    CSES:         Intersection Points (1740).
    Example:
        >>> intersection_points_count([(2, 3, 7, 3), (3, 1, 3, 5), (6, 2, 6, 6), (1, 4, 4, 4)])
        3
    """
    ys = sorted({s[1] for s in segments} | {s[3] for s in segments})
    idx = {y: i for i, y in enumerate(ys)}
    m = len(ys)
    t = [0] * (m + 1)

    def add(i: int, d: int) -> None:
        i += 1
        while i <= m:
            t[i] += d
            i += i & -i

    def pref(i: int) -> int:
        s = 0
        while i > 0:
            s += t[i]
            i -= i & -i
        return s

    events = []  # (x, тип, ...): 0 - начало горизонтали, 1 - вертикаль, 2 - конец горизонтали
    for x1, y1, x2, y2 in segments:
        if y1 == y2:
            a, b = min(x1, x2), max(x1, x2)
            events.append((a, 0, y1, 0))
            events.append((b, 2, y1, 0))
        else:
            events.append((x1, 1, min(y1, y2), max(y1, y2)))
    events.sort()
    total = 0
    for _, kind, ya, yb in events:
        if kind == 0:
            add(idx[ya], 1)
        elif kind == 2:
            add(idx[ya], -1)
        else:
            total += pref(idx[yb] + 1) - pref(idx[ya])  # активные горизонтали в [ya, yb]
    return total


@algo(
    tags=["geometry", "sweep-line", "segment-tree", "union-area"],
    cses=["Area of Rectangles (1741)"],
)
def area_of_rectangles(rects: list[tuple[int, int, int, int]]) -> int:
    """Area of the union of axis-parallel rectangles.   # Площадь объединения прямоугольников.

    When to use:  union area / perimeter-like sweeps.
    Complexity:   O(n log n)
    Input:        rectangles (x1, y1, x2, y2) with x1 < x2, y1 < y2.
    Returns:      union area.
    Python speed: n = 10^5 ~ 2-3 s.
    Idea:         sweep x; segment tree over compressed y stores cover count and covered
                  length (node fully covered -> its whole length, else children's sum).
    Related:      intersection_points_count.
    CSES:         Area of Rectangles (1741).
    Example:
        >>> area_of_rectangles([(0, 0, 2, 2), (1, 1, 3, 3)])
        7
    """
    ys = sorted({r[1] for r in rects} | {r[3] for r in rects})
    m = len(ys) - 1  # элементарных отрезков по y
    if m <= 0:
        return 0
    idx = {y: i for i, y in enumerate(ys)}
    size = 1
    while size < m:
        size <<= 1
    cnt = [0] * (2 * size)
    covered = [0] * (2 * size)
    full = [0] * (2 * size)  # полная длина узла
    for i in range(m):
        full[size + i] = ys[i + 1] - ys[i]
    for k in range(size - 1, 0, -1):
        full[k] = full[2 * k] + full[2 * k + 1]

    def pull(k: int) -> None:
        if cnt[k]:
            covered[k] = full[k]
        elif k >= size:
            covered[k] = 0
        else:
            covered[k] = covered[2 * k] + covered[2 * k + 1]

    def update(l: int, r: int, d: int) -> None:
        l += size
        r += size
        l0, r0 = l, r
        while l < r:  # покрытие канонических узлов снизу вверх
            if l & 1:
                cnt[l] += d
                pull(l)
                l += 1
            if r & 1:
                r -= 1
                cnt[r] += d
                pull(r)
            l >>= 1
            r >>= 1
        for k in (l0, r0 - 1):  # пересчитываем предков границ
            k >>= 1
            while k:
                pull(k)
                k >>= 1

    events = []
    for x1, y1, x2, y2 in rects:
        events.append((x1, 1, idx[y1], idx[y2]))
        events.append((x2, -1, idx[y1], idx[y2]))
    events.sort()
    area = 0
    prev_x = events[0][0]
    for x, d, a, b in events:
        area += covered[1] * (x - prev_x)  # полоса между событиями
        prev_x = x
        update(a, b, d)
    return area


@algo(tags=["geometry", "simulation", "segments"], cses=["Robot Path (1742)"], verified=False)
def robot_path(moves: list[tuple[str, int]]) -> int:
    """Steps until the robot first visits a point twice.   # Путь робота.

    When to use:  axis-parallel walk; find the first self-intersection.
    Complexity:   O(n^2)
    Returns:      number of unit steps until a point is visited the second time
                  (the whole length if it never happens).
    Python speed: n <= ~3000 in CPython; the full CSES limits need a sweep (not implemented).
    Idea:         for each new segment find the earliest point where it touches any earlier
                  segment (overlap or crossing); reversing direction hits at once.
    CSES:         Robot Path (1742) (exact statement NOT VERIFIED).
    Example:
        >>> robot_path([("U", 2), ("R", 2), ("D", 1), ("L", 4)])
        7
    """
    # NOT VERIFIED: условие CSES Robot Path не сверено, решение O(n^2)
    dirs = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}
    segs: list[tuple[int, int, int, int]] = []  # пройденные отрезки
    x = y = 0
    total = 0
    for ch, length in moves:
        dx, dy = dirs[ch]
        best = length + 1  # первый шаг t (1..length), на котором точка уже была
        for ax, ay, bx, by in segs:
            # точки отрезка j в координате t вдоль текущего движения: P + t * dir
            if dx:  # горизонтальное движение: нужна общая y
                if not min(ay, by) <= y <= max(ay, by):
                    continue
                ta, tb = (ax - x) * dx, (bx - x) * dx
            else:
                if not min(ax, bx) <= x <= max(ax, bx):
                    continue
                ta, tb = (ay - y) * dy, (by - y) * dy
            lo, hi = min(ta, tb), max(ta, tb)  # для перпендикулярного отрезка lo == hi
            t = max(1, lo)
            if t <= min(length, hi):
                best = min(best, t)  # самое раннее попадание на старый отрезок
        if best <= length:
            return total + best
        segs.append((x, y, x + length * dx, y + length * dy))
        x, y = x + length * dx, y + length * dy
        total += length
    return total


@algo(tags=["geometry", "li-chao", "lines", "max"], cses=["Lines and Queries I (3204)"])
class LiChaoMax:
    """Li Chao tree for MAXIMUM of lines at integer x (self-contained copy).   # Ли Чао на максимум.

    When to use:  "add line y = kx + b", "max at x" (Lines and Queries).
    Complexity:   O(log C) per operation
    Methods:      add_line(k, b); query(x) (-(1 << 60) if empty)
    Related:      dp.LiChaoTree (minimum).
    CSES:         Lines and Queries I (3204).
    Example:
        >>> t = LiChaoMax(0, 100)
        >>> t.add_line(1, 0); t.add_line(-1, 50)
        >>> t.query(10), t.query(40)
        (40, 40)
    """

    NONE = -(1 << 62)

    def __init__(self, lo: int, hi: int) -> None:
        self.lo, self.hi = lo, hi
        self.k = [0]
        self.b = [self.NONE]
        self.left = [-1]
        self.right = [-1]

    def _new(self) -> int:
        self.k.append(0)
        self.b.append(self.NONE)
        self.left.append(-1)
        self.right.append(-1)
        return len(self.k) - 1

    def add_line(self, k: int, b: int) -> None:
        node, lo, hi = 0, self.lo, self.hi
        while True:
            mid = (lo + hi) // 2
            if k * mid + b > self.k[node] * mid + self.b[node]:  # лучше в середине - меняем
                self.k[node], k = k, self.k[node]
                self.b[node], b = b, self.b[node]
            if hi - lo == 1 or b == self.NONE:
                return
            if k * lo + b > self.k[node] * lo + self.b[node]:
                if self.left[node] == -1:
                    self.left[node] = self._new()
                node, hi = self.left[node], mid
            elif k * (hi - 1) + b > self.k[node] * (hi - 1) + self.b[node]:
                if self.right[node] == -1:
                    self.right[node] = self._new()
                node, lo = self.right[node], mid
            else:
                return

    def query(self, x: int) -> int:
        node, lo, hi = 0, self.lo, self.hi
        res = -(1 << 60)
        while node != -1:
            if self.b[node] != self.NONE:
                res = max(res, self.k[node] * x + self.b[node])
            if hi - lo == 1:
                break
            mid = (lo + hi) // 2
            if x < mid:
                node, hi = self.left[node], mid
            else:
                node, lo = self.right[node], mid
        return res


@algo(
    tags=["geometry", "li-chao", "segments"],
    cses=["Line Segments Trace I"],
    verified=False,
    stub=True,
)
def line_segments_trace(segments: list[tuple[int, int, int, int]], x_max: int) -> list[int]:
    """CSES Line Segments Trace - not implemented yet.   # Заглушка.

    When to use:  -
    Complexity:   -
    Returns:      would return the upper envelope values at integer x.
    Idea:         Li Chao tree with segment insertion (insert a line only into the O(log C)
                  nodes covering [x1, x2]). NOT VERIFIED: exact statement (integer / real
                  output, ranges) unknown.
    CSES:         Line Segments Trace I / II.
    Example:
        >>> line_segments_trace([], 1)
        Traceback (most recent call last):
        NotImplementedError: CSES Line Segments Trace: statement not verified yet
    """
    # NOT VERIFIED: заглушка, условие задачи не сверено
    raise NotImplementedError("CSES Line Segments Trace: statement not verified yet")


@algo(tags=["geometry", "3d", "determinant"], icpc=["2025 D"])
def det3(a: tuple[int, int, int], b: tuple[int, int, int], c: tuple[int, int, int]) -> int:
    """Determinant of the 3 x 3 matrix with rows a, b, c (triple product).   # Определитель 3 x 3.

    When to use:  volumes, coplanarity, orientation in 3D.
    Complexity:   O(1)
    Returns:      a . (b x c).
    Related:      tetra_volume6, coplanar_with_origin.
    ICPC-UZ:      2025 D "Death Star N" (det == 0 test).
    Example:
        >>> det3((1, 0, 0), (0, 1, 0), (0, 0, 1)), det3((1, 2, 3), (2, 4, 6), (0, 1, 5))
        (1, 0)
    """
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])  # разложение по первой строке
    )


@algo(tags=["geometry", "3d", "volume"], cses=["- (3D volumes)"], requires=["det3"])
def tetra_volume6(
    a: tuple[int, int, int],
    b: tuple[int, int, int],
    c: tuple[int, int, int],
    d: tuple[int, int, int],
) -> int:
    """Six times the signed volume of tetrahedron abcd.   # Удвоенный (x6) объём тетраэдра.

    When to use:  coplanarity of 4 points (0), orientation of a point against a plane.
    Complexity:   O(1)
    Returns:      det(b - a, c - a, d - a).
    Related:      det3.
    CSES:         - (3D volumes)
    Example:
        >>> tetra_volume6((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
        1
    """
    return det3(
        (b[0] - a[0], b[1] - a[1], b[2] - a[2]),
        (c[0] - a[0], c[1] - a[1], c[2] - a[2]),
        (d[0] - a[0], d[1] - a[1], d[2] - a[2]),
    )


@algo(tags=["geometry", "3d", "coplanar", "rank"], icpc=["2025 D"], requires=["det3"])
def coplanar_with_origin(points: list[tuple[int, int, int]]) -> bool:
    """Do all points lie in one plane through the origin?   # Плоскость через начало координат.

    When to use:  rank of the set of vectors <= 2.
    Complexity:   O(n) after finding two independent vectors
    Returns:      True iff some plane through (0, 0, 0) contains every point.
    Related:      det3.
    ICPC-UZ:      2025 D "Death Star N" (building block).
    Example:
        >>> coplanar_with_origin([(1, 0, 0), (0, 1, 0), (1, 1, 0)])
        True
        >>> coplanar_with_origin([(1, 0, 0), (0, 1, 0), (0, 0, 1)])
        False
    """
    nz = [p for p in points if p != (0, 0, 0)]
    if not nz:
        return True
    a = nz[0]
    b = None
    for p in nz[1:]:
        cr = (a[1] * p[2] - a[2] * p[1], a[2] * p[0] - a[0] * p[2], a[0] * p[1] - a[1] * p[0])
        if cr != (0, 0, 0):
            b = p  # первый вектор, не коллинеарный a
            break
    if b is None:
        return True  # все на одной прямой через 0
    return all(det3(a, b, p) == 0 for p in nz)


@algo(
    tags=["geometry", "3d", "determinant", "bitmask"],
    icpc=["2025 D"],
    requires=["det3"],
    verified=False,
)
def death_star_min_changes(points: list[tuple[int, int, int]]) -> tuple[int, int] | None:
    """Fewest coordinates to raise by [0, 1) so that O, A, B, C are coplanar.   # Звезда смерти.

    When to use:  ICPC-UZ 2025 D as described by the official tutorial.
    Complexity:   O(2^9) determinants
    Input:        three integer points A, B, C (the fourth point is the origin).
    Returns:      (minimal number of changed coordinates, number of such coordinate sets);
                  (0, 1) if already coplanar; None if impossible.
    Idea:         det is linear in every coordinate: if some shift in (0, 1)^S flips the
                  sign, pushing each coordinate to the better end 0 or 1 gives a corner that
                  flips too. So for the smallest S a root exists iff adding 1 to all of S makes
                  the sign strictly opposite. Try the 511 sets, count the smallest flipping.
                  NOT VERIFIED: statement not found (input format, what is "distorted").
    ICPC-UZ:      2025 D "Death Star N".
    Example:
        >>> death_star_min_changes([(1, 0, 0), (0, 1, 0), (0, 0, 1)])
        (4, 3)
        >>> death_star_min_changes([(1, 2, 3), (2, 4, 6), (5, 0, 1)])
        (0, 1)
    """
    # NOT VERIFIED: по разбору жюри, условие не найдено
    base = det3(points[0], points[1], points[2])
    if base == 0:
        return 0, 1
    best = 10
    ways = 0
    for mask in range(1, 1 << 9):
        k = bin(mask).count("1")
        if k > best:
            continue
        m = [list(p) for p in points]
        for b in range(9):
            if mask >> b & 1:
                m[b // 3][b % 3] += 1  # координата сдвинута на 1 вместо дроби
        d = det3(
            (m[0][0], m[0][1], m[0][2]), (m[1][0], m[1][1], m[1][2]), (m[2][0], m[2][1], m[2][2])
        )
        if d != 0 and (d > 0) != (base > 0):
            if k < best:
                best = k
                ways = 0
            ways += 1
    return (best, ways) if ways else None


@algo(tags=["geometry", "tsp", "bitmask-dp"], icpc=["2023 K"], verified=False)
def biathlon_route(points: list[Pt]) -> float:
    """Shortest closed route through all points (base version).   # Маршрут биатлониста.

    When to use:  ICPC-UZ 2023 K base version: n <= ~15 points.
    Complexity:   O(2^n * n^2)
    Returns:      minimal tour length (Euclidean), 0.0 for one point.
    Pitfalls:     float answer; print with enough digits.
    Idea:         Held-Karp DP over subsets. An optimal Euclidean tour never crosses itself
                  (uncrossing two edges shortens it), so "no self-intersections" holds for
                  free. The real problem (pairs of shooting ranges) is harder - NOT VERIFIED.
    ICPC-UZ:      2023 K (statement NOT VERIFIED, this is only the base version).
    Example:
        >>> round(biathlon_route([(0, 0), (0, 1), (1, 1), (1, 0)]), 6)
        4.0
    """
    # NOT VERIFIED: базовая версия (TSP); условие 2023 K с парами стрельбищ не сверено
    n = len(points)
    if n <= 1:
        return 0.0
    d = [[math.dist(p, q) for q in points] for p in points]
    full = 1 << n
    INF_F = float("inf")
    dp = [[INF_F] * n for _ in range(full)]
    dp[1][0] = 0.0
    for mask in range(1, full, 2):  # маршрут всегда начинается в точке 0
        row = dp[mask]
        for v in range(n):
            cur = row[v]
            if cur == INF_F:
                continue
            for u in range(n):
                if not mask >> u & 1:
                    nm = mask | 1 << u
                    nd = cur + d[v][u]
                    if nd < dp[nm][u]:
                        dp[nm][u] = nd
    return min(dp[full - 1][v] + d[v][0] for v in range(1, n))
