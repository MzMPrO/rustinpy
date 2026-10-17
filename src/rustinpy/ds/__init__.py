"""Data structures and range queries.

Структуры данных и запросы на отрезках. Отрезки везде полуоткрытые [l, r), индексы 0-based:
``from rustinpy.ds import Fenwick, SegTree, LazySegAddSum, SortedList``.
"""

from __future__ import annotations

from rustinpy.ds.connectivity import dynamic_connectivity_offline, new_roads_queries
from rustinpy.ds.fenwick import Fenwick, Fenwick2D, FenwickRangeAdd, FenwickRangeRange
from rustinpy.ds.icpc import SegTreeFlipRuns, exclusions, generic_strings, subarray_mex_offline
from rustinpy.ds.lazy import LazySegAddMin, LazySegAddSum, LazySegArithmetic, LazySegAssignAddSum
from rustinpy.ds.mo import SqrtDecomposition, mo_distinct_count, mo_order, mo_with_updates
from rustinpy.ds.offline import (
    distinct_values_queries,
    hotel_queries,
    list_removals,
    missing_coin_sum_queries,
    movie_festival_queries,
    pizzeria_queries,
    salary_queries,
)
from rustinpy.ds.pav import isotonic_sse_mod, pav
from rustinpy.ds.persistent import MergeSortTree, PersistentSegTree, range_kth_smallest
from rustinpy.ds.prefix import PrefixSum2D, prefix_sums
from rustinpy.ds.segtree import SegTree, SegTreeMaxPrefix, SegTreeMaxSubarray, SegTreeRuns
from rustinpy.ds.sliding import (
    MinStack,
    MonotonicQueue,
    TwoStackQueue,
    longest_window_no_repeats,
    sliding_window_distinct,
    sliding_window_inversions,
    sliding_window_mex,
    sliding_window_min,
    sliding_window_mode,
    sliding_window_or,
    sliding_window_sum,
    sliding_window_xor,
)
from rustinpy.ds.sortedlist import SortedList
from rustinpy.ds.sparse import SparseTable
from rustinpy.ds.treap import (
    ImplicitTreap,
    Treap,
    cut_and_paste,
    reversal_sorting,
    substring_reversals,
)

__all__ = [
    "Fenwick",
    "Fenwick2D",
    "FenwickRangeAdd",
    "FenwickRangeRange",
    "ImplicitTreap",
    "LazySegAddMin",
    "LazySegAddSum",
    "LazySegArithmetic",
    "LazySegAssignAddSum",
    "MergeSortTree",
    "MinStack",
    "MonotonicQueue",
    "PersistentSegTree",
    "PrefixSum2D",
    "SegTree",
    "SegTreeFlipRuns",
    "SegTreeMaxPrefix",
    "SegTreeMaxSubarray",
    "SegTreeRuns",
    "SortedList",
    "SparseTable",
    "SqrtDecomposition",
    "Treap",
    "TwoStackQueue",
    "cut_and_paste",
    "distinct_values_queries",
    "dynamic_connectivity_offline",
    "exclusions",
    "generic_strings",
    "hotel_queries",
    "isotonic_sse_mod",
    "list_removals",
    "longest_window_no_repeats",
    "missing_coin_sum_queries",
    "mo_distinct_count",
    "mo_order",
    "mo_with_updates",
    "movie_festival_queries",
    "new_roads_queries",
    "pav",
    "pizzeria_queries",
    "prefix_sums",
    "range_kth_smallest",
    "reversal_sorting",
    "salary_queries",
    "sliding_window_distinct",
    "sliding_window_inversions",
    "sliding_window_mex",
    "sliding_window_min",
    "sliding_window_mode",
    "sliding_window_or",
    "sliding_window_sum",
    "sliding_window_xor",
    "subarray_mex_offline",
    "substring_reversals",
]
