"""Fast input / output for contest solutions.

Быстрый ввод-вывод: читаем весь stdin одним вызовом, пишем одним sys.stdout.write.
"""

from __future__ import annotations

import sys
from collections.abc import Iterable
from typing import BinaryIO, TextIO

from rustinpy._registry import algo

__all__ = [
    "FastReader",
    "FastWriter",
    "fast_io_template",
    "read_all_ints",
    "read_int",
    "read_ints",
    "read_str",
    "set_input",
]


@algo(tags=["io", "template"], cses=["- (any problem with big input)"])
class FastReader:
    """Token reader over sys.stdin.buffer.   # Быстрое чтение токенов из stdin.

    When to use:  input bigger than ~10^4 numbers; input() is 5-10x slower.
    Complexity:   O(input size) once, O(1) per token
    Methods:      next_int(), next_ints(k), next_str(), next_bytes(), next_float(), rest_ints()
    Pitfalls:     reads ALL input at once -> not for interactive problems.   # не для интерактива
    Related:      FastWriter, interactive.make_ask.
    CSES:         - (any problem with big input)
    Example:
        >>> import io
        >>> r = FastReader(io.BytesIO(b"3 10 20 30 abc 2.5"))
        >>> n = r.next_int()
        >>> r.next_ints(n), r.next_str(), r.next_float()
        ([10, 20, 30], 'abc', 2.5)
    """

    def __init__(self, stream: BinaryIO | None = None) -> None:
        self._stream = stream
        self._data: list[bytes] | None = None
        self._pos = 0

    def _tokens(self) -> list[bytes]:
        if self._data is None:  # читаем всё один раз, лениво
            src = self._stream if self._stream is not None else sys.stdin.buffer
            self._data = src.read().split()
        return self._data

    def next_bytes(self) -> bytes:
        data = self._tokens()
        self._pos += 1
        return data[self._pos - 1]

    def next_int(self) -> int:
        return int(self.next_bytes())

    def next_ints(self, k: int) -> list[int]:
        data = self._tokens()
        start = self._pos
        self._pos += k
        return list(map(int, data[start : start + k]))

    def next_str(self) -> str:
        return self.next_bytes().decode()

    def next_float(self) -> float:
        return float(self.next_bytes())

    def rest_ints(self) -> list[int]:
        data = self._tokens()
        start, self._pos = self._pos, len(data)
        return list(map(int, data[start:]))


_READER: FastReader | None = None


def _reader() -> FastReader:
    global _READER
    if _READER is None:
        _READER = FastReader()
    return _READER


@algo(tags=["io"], cses=["- (tests and tools)"], requires=["FastReader", "_READER", "_reader"])
def set_input(stream: BinaryIO | None = None) -> None:
    """Replace the stream behind read_int/read_ints/read_str.   # Подменить источник ввода.

    When to use:  tests, or reading from a file instead of stdin.
    Complexity:   O(1)
    Returns:      None; next read_* call reads from the new stream.
    CSES:         - (tests and tools)
    Example:
        >>> import io
        >>> set_input(io.BytesIO(b"5"))
        >>> _reader().next_int()
        5
    """
    global _READER
    _READER = FastReader(stream)


@algo(tags=["io"], cses=["- (any)"], requires=["FastReader", "_READER", "_reader", "set_input"])
def read_int() -> int:
    """Next integer from stdin.   # Следующее целое из stdin.

    When to use:  quick scripts; for speed-critical loops keep a FastReader in a local variable.
    Complexity:   O(1) per call after the first one
    Returns:      int
    Related:      read_ints, read_str, FastReader.
    CSES:         - (any)
    Example:
        >>> import io
        >>> set_input(io.BytesIO(b"42 -7"))
        >>> read_int(), read_int()
        (42, -7)
    """
    return _reader().next_int()


@algo(
    tags=["io"],
    cses=["- (any)"],
    requires=["FastReader", "_READER", "_reader", "set_input", "read_int"],
)
def read_ints(k: int) -> list[int]:
    """Next k integers from stdin.   # Следующие k целых.

    When to use:  reading an array of known length.
    Complexity:   O(k)
    Returns:      list of k ints
    CSES:         - (any)
    Example:
        >>> import io
        >>> set_input(io.BytesIO(b"3 1 2 3"))
        >>> read_ints(read_int())
        [1, 2, 3]
    """
    return _reader().next_ints(k)


@algo(tags=["io"], cses=["- (any)"], requires=["FastReader", "_READER", "_reader", "set_input"])
def read_str() -> str:
    """Next whitespace-separated token as str.   # Следующий токен строкой.

    When to use:  words, grids given row by row.
    Complexity:   O(len)
    Returns:      str (no spaces inside)
    Pitfalls:     a line with spaces is several tokens -> read the raw buffer instead.
    CSES:         - (any)
    Example:
        >>> import io
        >>> set_input(io.BytesIO(b"abc #.#"))
        >>> read_str(), read_str()
        ('abc', '#.#')
    """
    return _reader().next_str()


@algo(tags=["io"], cses=["- (any)"], requires=["FastReader", "_READER", "_reader", "set_input"])
def read_all_ints() -> list[int]:
    """All remaining integers from stdin.   # Все оставшиеся числа.

    When to use:  input is only numbers; then index the list yourself (fastest way).
    Complexity:   O(input size)
    Returns:      list[int]
    CSES:         - (any)
    Example:
        >>> import io
        >>> set_input(io.BytesIO(b"2 3 4"))
        >>> read_all_ints()
        [2, 3, 4]
    """
    return _reader().rest_ints()


@algo(tags=["io", "template"], cses=["- (any problem with big output)"])
class FastWriter:
    """Buffered writer: collect pieces, one write at the end.   # Буферизованный вывод.

    When to use:  more than ~10^4 output lines; print() per line is slow.
    Complexity:   O(total output)
    Methods:      write(*items, sep=" ", end="\\n"), write_lines(items), flush()
    Pitfalls:     call flush() at the end, otherwise nothing is printed.   # не забыть flush
    Related:      FastReader, fast_io_template.
    CSES:         - (any problem with big output)
    Example:
        >>> import io
        >>> buf = io.StringIO()
        >>> w = FastWriter(buf)
        >>> w.write(1, 2, 3)
        >>> w.write_lines(["a", "b"])
        >>> w.flush()
        >>> buf.getvalue().split()
        ['1', '2', '3', 'a', 'b']
    """

    def __init__(self, stream: TextIO | None = None) -> None:
        self._out = stream if stream is not None else sys.stdout
        self._buf: list[str] = []

    def write(self, *items: object, sep: str = " ", end: str = "\n") -> None:
        self._buf.append(sep.join(map(str, items)) + end)

    def write_lines(self, items: Iterable[object]) -> None:
        self._buf.append("".join(f"{x}\n" for x in items))

    def flush(self) -> None:
        self._out.write("".join(self._buf))  # одна системная запись
        self._buf.clear()
        self._out.flush()


_TEMPLATE = """import sys

data = sys.stdin.buffer.read().split()
ptr = 0


def nxt() -> int:
    global ptr
    ptr += 1
    return int(data[ptr - 1])


def main() -> None:
    n = nxt()
    a = [nxt() for _ in range(n)]
    out = [str(sum(a))]
    sys.stdout.write("\\n".join(out) + "\\n")


main()
"""


@algo(tags=["io", "template"], cses=["- (copy into every solution)"], requires=["_TEMPLATE"])
def fast_io_template() -> str:
    """Minimal fast I/O skeleton to paste into a solution.   # Шаблон решения с быстрым вводом.

    When to use:  start of every contest solution in Python.
    Complexity:   O(1)
    Returns:      source text of the template (read all tokens, solve inside main()).
    Pitfalls:     code inside main() runs faster than at module level (local variables).
    CSES:         - (copy into every solution)
    Example:
        >>> fast_io_template().splitlines()[2]
        'data = sys.stdin.buffer.read().split()'
    """
    return _TEMPLATE
