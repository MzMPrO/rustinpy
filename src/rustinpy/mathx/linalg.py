"""Linear algebra: Gaussian elimination modulo a prime and over floats, determinant.

Метод Гаусса.
"""

from __future__ import annotations

from rustinpy._registry import algo

MOD = 998244353
MOD7 = 10**9 + 7


@algo(
    tags=["gauss", "linear-system", "modular"],
    cses=["System of Linear Equations (3154)"],
    requires=["MOD7"],
)
def gauss_mod(a: list[list[int]], b: list[int], mod: int = MOD7) -> list[int] | None:
    """Solve A x = b modulo a prime (Gauss-Jordan).   # Система уравнений по модулю.

    When to use:  linear systems over Z_p; any solution if there are free variables.
    Complexity:   O(n * m * min(n, m))
    Input:        a is n x m, b has length n; mod prime.
    Returns:      one solution x (free variables = 0), or None if inconsistent.
    Python speed: 500 x 500 ~ 5-10 s in CPython (rows are processed by list comprehensions).
    Related:      gauss_float, det_mod, bits.XorBasis (mod 2).
    CSES:         System of Linear Equations (3154).
    Example:
        >>> gauss_mod([[1, 1], [1, 2]], [3, 5], 7)
        [1, 2]
        >>> gauss_mod([[1, 1], [2, 2]], [1, 3], 7) is None
        True
    """
    n = len(a)
    m = len(a[0]) if n else 0
    rows = [[x % mod for x in a[i]] + [b[i] % mod] for i in range(n)]
    where = [-1] * m
    r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if rows[i][c]), -1)
        if piv == -1:
            continue  # свободная переменная
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][c], mod - 2, mod)
        pr = [x * inv % mod for x in rows[r]]  # нормируем ведущую строку
        rows[r] = pr
        for i in range(n):
            if i != r and rows[i][c]:
                f = rows[i][c]
                rows[i] = [(x - f * y) % mod for x, y in zip(rows[i], pr)]  # зануляем столбец
        where[c] = r
        r += 1
        if r == n:
            break
    for i in range(r, n):
        if rows[i][m]:
            return None  # 0 = ненулевое: решений нет
    return [rows[where[c]][m] if where[c] != -1 else 0 for c in range(m)]


@algo(tags=["gauss", "linear-system", "float"], cses=["- (real linear systems)"])
def gauss_float(a: list[list[float]], b: list[float], eps: float = 1e-9) -> list[float] | None:
    """Solve A x = b over reals with partial pivoting.   # Метод Гаусса с плавающей точкой.

    When to use:  small real systems (probabilities, geometry), n <= ~300.
    Complexity:   O(n * m * min(n, m))
    Returns:      one solution (free variables = 0), or None if inconsistent (within eps).
    Pitfalls:     choose the pivot with the largest |value| - otherwise errors explode.
    Related:      gauss_mod.
    CSES:         - (real linear systems)
    Example:
        >>> [round(v, 9) for v in gauss_float([[2.0, 1.0], [1.0, 3.0]], [3.0, 5.0])]
        [0.8, 1.4]
    """
    n = len(a)
    m = len(a[0]) if n else 0
    rows = [[*map(float, a[i]), float(b[i])] for i in range(n)]
    where = [-1] * m
    r = 0
    for c in range(m):
        piv = max(range(r, n), key=lambda i: abs(rows[i][c]), default=-1)  # частичный выбор
        if piv == -1 or abs(rows[piv][c]) < eps:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        pv = rows[r][c]
        pr = [x / pv for x in rows[r]]  # нормируем строку
        rows[r] = pr
        for i in range(n):
            if i != r and abs(rows[i][c]) > eps:
                f = rows[i][c]
                rows[i] = [x - f * y for x, y in zip(rows[i], pr)]  # зануляем столбец
        where[c] = r
        r += 1
        if r == n:
            break
    for i in range(r, n):
        if abs(rows[i][m]) > eps:
            return None
    return [rows[where[c]][m] if where[c] != -1 else 0.0 for c in range(m)]


@algo(tags=["gauss", "determinant", "modular"], cses=["- (determinant mod p)"], requires=["MOD"])
def det_mod(a: list[list[int]], mod: int = MOD) -> int:
    """Determinant of a square matrix modulo a prime.   # Определитель по модулю.

    When to use:  Kirchhoff matrix-tree theorem, counting perfect matchings mod p.
    Complexity:   O(n^3)
    Returns:      det(A) mod prime.
    Related:      gauss_mod.
    CSES:         - (determinant mod p)
    Example:
        >>> det_mod([[2, 1], [7, 4]], 1000000007)
        1
    """
    n = len(a)
    rows = [[x % mod for x in row] for row in a]
    det = 1
    for c in range(n):
        piv = next((i for i in range(c, n) if rows[i][c]), -1)
        if piv == -1:
            return 0
        if piv != c:
            rows[c], rows[piv] = rows[piv], rows[c]
            det = -det  # перестановка строк меняет знак
        det = det * rows[c][c] % mod
        inv = pow(rows[c][c], mod - 2, mod)
        for i in range(c + 1, n):
            if rows[i][c]:
                f = rows[i][c] * inv % mod
                rows[i] = [(x - f * y) % mod for x, y in zip(rows[i], rows[c])]
    return det % mod
