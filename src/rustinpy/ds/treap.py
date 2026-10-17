"""Treaps: ordered multiset and implicit treap with range reversal (iterative split/merge).

Декартовы деревья. Split и merge без рекурсии. Отрезки [l, r), позиции 0-based.
"""

from __future__ import annotations

import random

from rustinpy._registry import algo

INF = 1 << 60


@algo(tags=["treap", "ordered-set", "order-statistics"], cses=["- (ordered multiset)"])
class Treap:
    """Ordered multiset on a treap: insert, erase, k-th, rank.   # Декартово дерево по ключу.

    When to use:  order statistics with insertions and deletions (SortedList is usually
                  faster in Python; the treap is the TRD template for C++ ports).
    Complexity:   O(log n) expected per operation
    Methods:      insert(x); erase(x) -> bool (one copy); kth(k) (0-based); rank(x) = #(< x);
                  len(t); x in t; to_list()
    Related:      SortedList, ImplicitTreap, Fenwick.kth.
    CSES:         - (ordered multiset)
    Example:
        >>> t = Treap()
        >>> for x in [5, 1, 4, 1, 3]: t.insert(x)
        >>> t.to_list(), t.kth(2), t.rank(4), len(t)
        ([1, 1, 3, 4, 5], 3, 3, 5)
        >>> t.erase(1), t.erase(7), t.to_list()
        (True, False, [1, 3, 4, 5])
    """

    def __init__(self) -> None:
        self.key = [0]
        self.pri = [0.0]
        self.L = [0]
        self.R = [0]
        self.sz = [0]  # узел 0 - пустой
        self.root = 0

    def _new(self, k: int) -> int:
        self.key.append(k)
        self.pri.append(random.random())
        self.L.append(0)
        self.R.append(0)
        self.sz.append(1)
        return len(self.key) - 1

    def _split(self, t: int, x: int, strict: bool) -> tuple[int, int]:
        """Left part: keys < x (strict) or keys <= x."""
        L, R, key, sz = self.L, self.R, self.key, self.sz
        lroot = rroot = lt = rt = 0
        path = []
        while t:
            path.append(t)
            if key[t] < x or (not strict and key[t] == x):
                if lt:
                    R[lt] = t  # t уходит в левую часть
                else:
                    lroot = t
                lt, t = t, R[t]
            else:
                if rt:
                    L[rt] = t  # t уходит в правую часть
                else:
                    rroot = t
                rt, t = t, L[t]
        if lt:
            R[lt] = 0
        if rt:
            L[rt] = 0
        for v in reversed(path):  # размеры снизу вверх
            sz[v] = 1 + sz[L[v]] + sz[R[v]]
        return lroot, rroot

    def _merge(self, a: int, b: int) -> int:
        L, R, pri, sz = self.L, self.R, self.pri, self.sz
        root = parent = 0
        right_side = False
        path = []
        while a and b:
            if pri[a] > pri[b]:
                node, nxt_a, nxt_b, go_right = a, R[a], b, True
            else:
                node, nxt_a, nxt_b, go_right = b, a, L[b], False
            if not parent:
                root = node
            elif right_side:
                R[parent] = node
            else:
                L[parent] = node
            path.append(node)
            parent, right_side = node, go_right
            a, b = nxt_a, nxt_b
        rest = a or b
        if not parent:
            root = rest
        elif right_side:
            R[parent] = rest
        else:
            L[parent] = rest
        for v in reversed(path):
            sz[v] = 1 + sz[L[v]] + sz[R[v]]
        return root

    def insert(self, x: int) -> None:
        l, r = self._split(self.root, x, True)
        self.root = self._merge(self._merge(l, self._new(x)), r)

    def erase(self, x: int) -> bool:
        l, r = self._split(self.root, x, True)
        m, r = self._split(r, x, False)  # m - все ключи, равные x
        found = m != 0
        if m:
            m = self._merge(self.L[m], self.R[m])  # выбрасываем один узел
        self.root = self._merge(self._merge(l, m), r)
        return found

    def kth(self, k: int) -> int:
        t = self.root
        while t:
            ls = self.sz[self.L[t]]
            if k < ls:
                t = self.L[t]
            elif k == ls:
                return self.key[t]
            else:
                k -= ls + 1
                t = self.R[t]
        raise IndexError("kth out of range")

    def rank(self, x: int) -> int:
        t, res = self.root, 0
        while t:
            if self.key[t] < x:
                res += self.sz[self.L[t]] + 1  # t и его левое поддерево меньше x
                t = self.R[t]
            else:
                t = self.L[t]
        return res

    def __len__(self) -> int:
        return self.sz[self.root]

    def __contains__(self, x: int) -> bool:
        t = self.root
        while t:
            if self.key[t] == x:
                return True
            t = self.R[t] if self.key[t] < x else self.L[t]
        return False

    def to_list(self) -> list[int]:
        res: list[int] = []
        st: list[int] = []
        t = self.root
        while st or t:
            while t:
                st.append(t)
                t = self.L[t]
            t = st.pop()
            res.append(self.key[t])
            t = self.R[t]
        return res


@algo(
    tags=["treap", "implicit-treap", "reverse"],
    cses=["Cut and Paste (2072)", "Substring Reversals (2073)", "Reversal Sorting (2074)"],
    requires=["INF"],
)
class ImplicitTreap:
    """Implicit treap (array by position) with reversal and range min.   # Неявное декартово дерево.

    When to use:  cut/paste pieces of an array, reverse subarrays, keep min of the sequence.
    Complexity:   O(n) build, O(log n) expected per operation
    Methods:      split(t, k) -> (first k, rest); merge(a, b); reverse(l, r);
                  move_to_end(l, r); argmin(t) (position of the minimum); to_list(); len()
    Python speed: 2 * 10^5 operations take ~5 s in CPython.
    Related:      cut_and_paste, substring_reversals, reversal_sorting, Treap.
    CSES:         Cut and Paste (2072), Substring Reversals (2073), Reversal Sorting (2074).
    Example:
        >>> it = ImplicitTreap([1, 2, 3, 4, 5])
        >>> it.reverse(1, 4); it.to_list()
        [1, 4, 3, 2, 5]
        >>> it.move_to_end(0, 2); it.to_list()
        [3, 2, 5, 1, 4]
    """

    def __init__(self, values: list[int]) -> None:
        n = len(values)
        self.val = [INF, *values]
        self.mn = [INF, *values]
        self.pri = [0.0] + [random.random() for _ in range(n)]
        self.L = [0] * (n + 1)
        self.R = [0] * (n + 1)
        self.sz = [0] + [1] * n
        self.rev = [False] * (n + 1)
        # построение за O(n): правая ветка декартова дерева на стеке
        stack: list[int] = []
        for x in range(1, n + 1):
            last = 0
            while stack and self.pri[stack[-1]] < self.pri[x]:
                last = stack.pop()
            self.L[x] = last
            if stack:
                self.R[stack[-1]] = x
            stack.append(x)
        self.root = stack[0] if stack else 0
        order: list[int] = []
        st = [self.root]
        while st:
            t = st.pop()
            if t:
                order.append(t)
                st.append(self.L[t])
                st.append(self.R[t])
        for t in reversed(order):  # дети раньше родителей
            self._upd(t)

    def _upd(self, t: int) -> None:
        L, R = self.L[t], self.R[t]
        self.sz[t] = 1 + self.sz[L] + self.sz[R]
        self.mn[t] = min(self.val[t], self.mn[L], self.mn[R])

    def _push(self, t: int) -> None:
        if self.rev[t]:
            self.L[t], self.R[t] = self.R[t], self.L[t]  # разворот: меняем детей
            self.rev[self.L[t]] ^= True
            self.rev[self.R[t]] ^= True
            self.rev[t] = False
            self.rev[0] = False

    def split(self, t: int, k: int) -> tuple[int, int]:
        L, R, sz = self.L, self.R, self.sz
        lroot = rroot = lt = rt = 0
        path = []
        while t:
            self._push(t)
            path.append(t)
            ls = sz[L[t]]
            if ls < k:  # t и левое поддерево - в первые k
                k -= ls + 1
                if lt:
                    R[lt] = t
                else:
                    lroot = t
                lt, t = t, R[t]
            else:
                if rt:
                    L[rt] = t
                else:
                    rroot = t
                rt, t = t, L[t]
        if lt:
            R[lt] = 0
        if rt:
            L[rt] = 0
        for v in reversed(path):
            self._upd(v)
        return lroot, rroot

    def merge(self, a: int, b: int) -> int:
        L, R, pri = self.L, self.R, self.pri
        root = parent = 0
        right_side = False
        path = []
        while a and b:
            if pri[a] > pri[b]:
                self._push(a)
                node, nxt_a, nxt_b, go_right = a, R[a], b, True
            else:
                self._push(b)
                node, nxt_a, nxt_b, go_right = b, a, L[b], False
            if not parent:
                root = node
            elif right_side:
                R[parent] = node
            else:
                L[parent] = node
            path.append(node)
            parent, right_side = node, go_right
            a, b = nxt_a, nxt_b
        rest = a or b
        if not parent:
            root = rest
        elif right_side:
            R[parent] = rest
        else:
            L[parent] = rest
        for v in reversed(path):
            self._upd(v)
        return root

    def reverse(self, l: int, r: int) -> None:
        a, bc = self.split(self.root, l)
        b, c = self.split(bc, r - l)
        self.rev[b] ^= True  # ленивая метка разворота
        self.rev[0] = False
        self.root = self.merge(self.merge(a, b), c)

    def move_to_end(self, l: int, r: int) -> None:
        a, bc = self.split(self.root, l)
        b, c = self.split(bc, r - l)
        self.root = self.merge(self.merge(a, c), b)  # вырезали b и вставили в конец

    def argmin(self, t: int) -> int:
        pos = 0
        while True:
            self._push(t)
            left = self.L[t]
            if left and self.mn[left] == self.mn[t]:
                t = left
            elif self.val[t] == self.mn[t]:
                return pos + self.sz[left]
            else:
                pos += self.sz[left] + 1
                t = self.R[t]

    def to_list(self) -> list[int]:
        res: list[int] = []
        st: list[int] = []
        t = self.root
        while st or t:
            while t:
                self._push(t)
                st.append(t)
                t = self.L[t]
            t = st.pop()
            res.append(self.val[t])
            t = self.R[t]
        return res

    def __len__(self) -> int:
        return self.sz[self.root]


@algo(
    tags=["treap", "implicit-treap", "strings"],
    cses=["Cut and Paste (2072)"],
    requires=["INF", "ImplicitTreap"],
)
def cut_and_paste(s: str, ops: list[tuple[int, int]]) -> str:
    """Repeatedly cut s[l:r] and append it to the end.   # Вырезать и вставить в конец.

    When to use:  many cut-and-move operations on a long string.
    Complexity:   O((n + q) log n) expected
    Input:        ops (l, r), 0-based half-open (CSES gives 1-based a, b -> (a - 1, b)).
    Returns:      the final string.
    Related:      ImplicitTreap, substring_reversals.
    CSES:         Cut and Paste (2072).
    Example:
        >>> cut_and_paste("AYBABTU", [(2, 5), (0, 3)])
        'UBABAYT'
    """
    it = ImplicitTreap([ord(c) for c in s])
    for l, r in ops:
        it.move_to_end(l, r)
    return "".join(map(chr, it.to_list()))


@algo(
    tags=["treap", "implicit-treap", "strings", "reverse"],
    cses=["Substring Reversals (2073)"],
    requires=["INF", "ImplicitTreap"],
)
def substring_reversals(s: str, ops: list[tuple[int, int]]) -> str:
    """Repeatedly reverse s[l:r].   # Развороты подстрок.

    When to use:  many substring reversals.
    Complexity:   O((n + q) log n) expected
    Input:        ops (l, r), 0-based half-open.
    Returns:      the final string.
    Related:      ImplicitTreap, cut_and_paste.
    CSES:         Substring Reversals (2073).
    Example:
        >>> substring_reversals("ABCDE", [(1, 4), (0, 2)])
        'DACBE'
    """
    it = ImplicitTreap([ord(c) for c in s])
    for l, r in ops:
        it.reverse(l, r)
    return "".join(map(chr, it.to_list()))


@algo(
    tags=["treap", "implicit-treap", "sorting", "construction"],
    cses=["Reversal Sorting (2074)"],
    requires=["INF", "ImplicitTreap"],
)
def reversal_sorting(p: list[int]) -> list[tuple[int, int]]:
    """Sort an array with at most n reversals; return them.   # Сортировка разворотами.

    When to use:  constructive "sort by reversals" with output of the operations.
    Complexity:   O(n log n) expected
    Returns:      list of (l, r) half-open reversals; applying them in order sorts p.
    Python speed: n = 2 * 10^5 takes ~5 s in CPython.
    Idea:         step i: find the minimum of the suffix (argmin in the treap) at position j,
                  reverse [i, j] so it lands at position i.
    Related:      ImplicitTreap.
    CSES:         Reversal Sorting (2074).
    Example:
        >>> ops = reversal_sorting([3, 1, 2])
        >>> a = [3, 1, 2]
        >>> for l, r in ops: a[l:r] = a[l:r][::-1]
        >>> a, len(ops) <= 3
        ([1, 2, 3], True)
    """
    it = ImplicitTreap(list(p))
    res: list[tuple[int, int]] = []
    for i in range(len(p)):
        a, b = it.split(it.root, i)
        j = it.argmin(b)  # где минимум оставшейся части
        if j:
            x, y = it.split(b, j + 1)
            it.rev[x] ^= True
            it.rev[0] = False
            b = it.merge(x, y)
            res.append((i, i + j + 1))
        it.root = it.merge(a, b)
    return res
