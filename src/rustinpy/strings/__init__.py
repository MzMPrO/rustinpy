"""Strings: Z / prefix function, hashing, trie, Aho-Corasick, suffix array and automaton,
palindromes, Burrows-Wheeler, subsequences.

Строковые алгоритмы: ``from rustinpy.strings import z_function, SuffixAutomaton``.
Римские числа - отдельный модуль ``rustinpy.roman``.
"""

from __future__ import annotations

from rustinpy.strings.hashing import PalindromeQueries, StringHash, StringHashDouble
from rustinpy.strings.misc import (
    apostrophe_number,
    brands,
    distinct_subsequences,
    shortest_non_subsequence,
    string_functions,
)
from rustinpy.strings.palindromes import longest_palindrome, longest_palindrome_ending_at, manacher
from rustinpy.strings.prefix import (
    borders,
    kmp_find_all,
    lyndon_factorization,
    min_rotation,
    periods,
    prefix_function,
    required_substring,
    z_function,
)
from rustinpy.strings.suffix import (
    SuffixAutomaton,
    bwt,
    distinct_substrings_count,
    inverse_bwt,
    inverse_suffix_array,
    lcp_kasai,
    suffix_array,
)
from rustinpy.strings.trie import AhoCorasick, Trie, word_combinations

__all__ = [
    "AhoCorasick",
    "PalindromeQueries",
    "StringHash",
    "StringHashDouble",
    "SuffixAutomaton",
    "Trie",
    "apostrophe_number",
    "borders",
    "brands",
    "bwt",
    "distinct_subsequences",
    "distinct_substrings_count",
    "inverse_bwt",
    "inverse_suffix_array",
    "kmp_find_all",
    "lcp_kasai",
    "longest_palindrome",
    "longest_palindrome_ending_at",
    "lyndon_factorization",
    "manacher",
    "min_rotation",
    "periods",
    "prefix_function",
    "required_substring",
    "shortest_non_subsequence",
    "string_functions",
    "suffix_array",
    "word_combinations",
    "z_function",
]
