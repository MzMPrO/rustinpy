"""geometry: exact predicates and algorithms against brute force (AC-05, AC-06)."""

from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction

import pytest

from rustinpy.geometry import (
    LiChaoMax,
    Point,
    all_manhattan_distances_sum,
    area_of_rectangles,
    biathlon_route,
    closest_pair,
    closest_pair_sweep,
    convex_hull,
    coplanar_with_origin,
    cross,
    death_star_min_changes,
    det3,
    dot,
    intersection_points_count,
    line_segments_trace,
    max_manhattan_distances,
    on_segment,
    orientation,
    point_in_polygon,
    point_location,
    polygon_area2,
    polygon_lattice_points,
    robot_path,
    segment_intersection_point,
    segments_intersect,
    tetra_volume6,
)


def rp(rng: random.Random, c: int = 5) -> tuple[int, int]:
    return rng.randint(-c, c), rng.randint(-c, c)


def seg_points(
    a: tuple[int, int], b: tuple[int, int], steps: int = 60
) -> list[tuple[Fraction, Fraction]]:
    return [
        (a[0] + Fraction(t, steps) * (b[0] - a[0]), a[1] + Fraction(t, steps) * (b[1] - a[1]))
        for t in range(steps + 1)
    ]


def test_basic_predicates(rng: random.Random) -> None:
    for _ in range(500):
        o, a, b = rp(rng), rp(rng), rp(rng)
        c = cross(o, a, b)
        assert c == Point(a[0] - o[0], a[1] - o[1]).cross(Point(b[0] - o[0], b[1] - o[1]))
        assert dot(o, a, b) == Point(a[0] - o[0], a[1] - o[1]).dot(Point(b[0] - o[0], b[1] - o[1]))
        assert orientation(o, a, b) == (c > 0) - (c < 0)
        assert point_location(o, a, b) == ("LEFT" if c > 0 else "RIGHT" if c < 0 else "TOUCH")
        p = rp(rng)
        assert on_segment(p, a, b) == on_segment_param(p, a, b)
    q = Point(1, 2) + Point(3, 4)
    assert q == Point(4, 6) and (Point(3, 4) - Point(1, 1)).norm2() == 13


def on_segment_param(p: tuple[int, int], a: tuple[int, int], b: tuple[int, int]) -> bool:
    """Эталон: p = a + t (b - a) для некоторого t из [0, 1]."""
    if a == b:
        return p == a
    i = 0 if a[0] != b[0] else 1
    t = Fraction(p[i] - a[i], b[i] - a[i])
    return 0 <= t <= 1 and all(p[j] == a[j] + t * (b[j] - a[j]) for j in (0, 1))


def brute_intersection(p1, p2, p3, p4) -> set[tuple[Fraction, Fraction]]:  # type: ignore[no-untyped-def]
    # общие точки на целочисленной решётке масштаба 1/L - для коротких отрезков точно
    s1 = set(seg_points(p1, p2, 840))
    s2 = set(seg_points(p3, p4, 840))
    return s1 & s2


def test_segment_intersection_vs_dense_sampling(rng: random.Random) -> None:
    for _ in range(300):
        p1, p2, p3, p4 = (rp(rng, 3) for _ in range(4))
        common = brute_intersection(p1, p2, p3, p4)
        got = segments_intersect(p1, p2, p3, p4)
        if common:
            assert got
        pt = segment_intersection_point(p1, p2, p3, p4)
        if pt is not None:
            assert got and on_segment_exact(pt, p1, p2) and on_segment_exact(pt, p3, p4)
        if got and len(common) == 1 and p1 != p2 and p3 != p4:
            assert pt == next(iter(common))


def on_segment_exact(p: tuple[Fraction, Fraction], a: tuple[int, int], b: tuple[int, int]) -> bool:
    cr = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
    return (
        cr == 0
        and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
        and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
    )


def random_simple_polygon(rng: random.Random) -> list[tuple[int, int]]:
    # звёздный многоугольник: точки отсортированы по углу вокруг центра
    n = rng.randint(3, 8)
    pts = set()
    while len(pts) < n:
        ang = rng.random() * 2 * math.pi
        r = rng.randint(2, 8)
        pts.add((round(r * math.cos(ang)), round(r * math.sin(ang))))
    poly = sorted(pts, key=lambda p: (math.atan2(p[1], p[0]), p[0] ** 2 + p[1] ** 2))
    return poly


def test_polygons_vs_grid_counting(rng: random.Random) -> None:
    for _ in range(150):
        poly = random_simple_polygon(rng)
        if polygon_area2(poly) <= 0 or len(set(poly)) < 3:
            continue
        # простота: никакие два несмежных ребра не пересекаются
        n = len(poly)
        edges = [(poly[i], poly[(i + 1) % n]) for i in range(n)]
        simple = all(
            not segments_intersect(*edges[i], *edges[j])
            for i in range(n)
            for j in range(i + 1, n)
            if j != i + 1 and not (i == 0 and j == n - 1)
        )
        if not simple:
            continue
        inside = boundary = 0
        for x in range(-9, 10):
            for y in range(-9, 10):
                r = point_in_polygon(poly, (x, y))
                on_edge = any(on_segment((x, y), a, b) for a, b in edges)
                assert (r == "BOUNDARY") == on_edge
                if r == "INSIDE":
                    inside += 1
                elif r == "BOUNDARY":
                    boundary += 1
        assert polygon_lattice_points(poly) == (inside, boundary)
        assert polygon_area2(poly) == 2 * inside + boundary - 2  # Пик


def test_convex_hull_vs_brute(rng: random.Random) -> None:
    for _ in range(200):
        pts = [rp(rng, 4) for _ in range(rng.randint(1, 12))]
        hull = convex_hull(pts)
        hull_c = convex_hull(pts, keep_collinear=True)
        uniq = set(pts)
        assert set(hull) <= uniq and set(hull_c) <= uniq
        collinear = all(cross(a, b, c) == 0 for a, b, c in itertools.combinations(uniq, 3))
        if collinear:  # вырожденный случай: концы отрезка / все точки
            ends = [min(uniq), max(uniq)] if len(uniq) > 1 else [min(uniq)]
            assert hull == ends and sorted(hull_c) == sorted(uniq)
            continue
        m = len(hull)
        for i in range(m):
            a, b, c = hull[i], hull[(i + 1) % m], hull[(i + 2) % m]
            assert cross(a, b, c) > 0  # строго выпуклые вершины, против часовой
            assert all(cross(a, b, p) >= 0 for p in uniq)  # все точки слева от ребра
        on_hull = {p for p in uniq if point_in_polygon(hull, p) == "BOUNDARY"}
        assert set(hull_c) == on_hull and len(hull_c) == len(on_hull)


def test_closest_pair_vs_brute(rng: random.Random) -> None:
    for _ in range(200):
        pts = [rp(rng, 30) for _ in range(rng.randint(2, 40))]
        exp = min(
            (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 for a, b in itertools.combinations(pts, 2)
        )
        assert closest_pair(pts) == exp == closest_pair_sweep(pts)


def test_manhattan(rng: random.Random) -> None:
    for _ in range(100):
        pts = [rp(rng, 20) for _ in range(rng.randint(1, 15))]
        exp = []
        for i in range(len(pts)):
            exp.append(
                max(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a in pts[: i + 1] for b in pts[: i + 1])
            )
        assert max_manhattan_distances(pts) == exp
        assert all_manhattan_distances_sum(pts) == sum(
            abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in itertools.combinations(pts, 2)
        )


def test_sweeps_vs_grid(rng: random.Random) -> None:
    for _ in range(100):
        segs = []
        hs, vs = [], []
        used_y, used_x = set(), set()
        for _ in range(rng.randint(0, 8)):
            if rng.random() < 0.5:
                y = rng.randint(0, 10)
                if y in used_y:
                    continue
                used_y.add(y)
                a, b = sorted(rng.sample(range(0, 11), 2))
                segs.append((a, y, b, y))
                hs.append((a, b, y))
            else:
                x = rng.randint(0, 10)
                if x in used_x:
                    continue
                used_x.add(x)
                a, b = sorted(rng.sample(range(0, 11), 2))
                segs.append((x, a, x, b))
                vs.append((x, a, b))
        exp = sum(1 for a, b, y in hs for x, c, d in vs if a <= x <= b and c <= y <= d)
        assert intersection_points_count(segs) == exp
        rects = []
        for _ in range(rng.randint(1, 5)):
            x1, x2 = sorted(rng.sample(range(0, 9), 2))
            y1, y2 = sorted(rng.sample(range(0, 9), 2))
            rects.append((x1, y1, x2, y2))
        cells = {(x, y) for x1, y1, x2, y2 in rects for x in range(x1, x2) for y in range(y1, y2)}
        assert area_of_rectangles(rects) == len(cells)


def brute_robot(moves: list[tuple[str, int]]) -> int:
    dirs = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}
    seen = {(0, 0)}
    x = y = steps = 0
    for ch, length in moves:
        dx, dy = dirs[ch]
        for _ in range(length):
            x, y = x + dx, y + dy
            steps += 1
            if (x, y) in seen:
                return steps
            seen.add((x, y))
    return steps


def test_robot_path_vs_simulation(rng: random.Random) -> None:
    for _ in range(300):
        moves = [(rng.choice("UDLR"), rng.randint(1, 4)) for _ in range(rng.randint(1, 8))]
        assert robot_path(moves) == brute_robot(moves)


def test_li_chao_max(rng: random.Random) -> None:
    t = LiChaoMax(-50, 50)
    lines: list[tuple[int, int]] = []
    for _ in range(300):
        if rng.random() < 0.5:
            k, b = rng.randint(-9, 9), rng.randint(-50, 50)
            t.add_line(k, b)
            lines.append((k, b))
        else:
            x = rng.randint(-50, 49)
            assert t.query(x) == max((k * x + b for k, b in lines), default=-(1 << 60))


def test_3d(rng: random.Random) -> None:
    for _ in range(300):
        a, b, c, d = (tuple(rng.randint(-4, 4) for _ in range(3)) for _ in range(4))
        m = [list(a), list(b), list(c)]
        exp = (
            m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
        )
        assert det3(a, b, c) == exp  # type: ignore[arg-type]
        assert tetra_volume6(d, a, b, c) == det3(  # type: ignore[arg-type]
            tuple(x - y for x, y in zip(a, d)),
            tuple(x - y for x, y in zip(b, d)),  # type: ignore[arg-type]
            tuple(x - y for x, y in zip(c, d)),  # type: ignore[arg-type]
        )
        pts = [tuple(rng.randint(-2, 2) for _ in range(3)) for _ in range(rng.randint(0, 5))]
        exp_c = all(det3(p, q, r) == 0 for p, q, r in itertools.combinations(pts, 3))  # type: ignore[arg-type]
        assert coplanar_with_origin(pts) == exp_c  # type: ignore[arg-type]


def test_biathlon_tsp_vs_permutations(rng: random.Random) -> None:
    for _ in range(40):
        pts = [rp(rng, 6) for _ in range(rng.randint(1, 6))]
        if len(pts) == 1:
            assert biathlon_route(pts) == 0.0
            continue
        best = min(
            sum(math.dist(a, b) for a, b in zip((pts[0], *p), (*p, pts[0])))
            for p in itertools.permutations(pts[1:])
        )
        assert abs(biathlon_route(pts) - best) < 1e-9


def test_geometry_stubs_raise() -> None:
    with pytest.raises(NotImplementedError):
        line_segments_trace([], 1)
    with pytest.raises(NotImplementedError):
        death_star_min_changes([])
