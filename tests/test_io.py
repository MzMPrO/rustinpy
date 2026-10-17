"""AC-12: fast I/O on substituted streams."""

from __future__ import annotations

import io

from rustinpy.io import (
    FastReader,
    FastWriter,
    fast_io_template,
    read_all_ints,
    read_int,
    read_ints,
    read_str,
    set_input,
)


def test_ac_12_fast_reader_tokens() -> None:
    r = FastReader(io.BytesIO(b"  2\n-5 7\r\nhello 3.25\n9 8 7"))
    assert r.next_int() == 2
    assert r.next_ints(2) == [-5, 7]
    assert r.next_str() == "hello"
    assert r.next_float() == 3.25
    assert r.next_bytes() == b"9"
    assert r.rest_ints() == [8, 7]
    assert r.rest_ints() == []


def test_ac_12_module_level_readers() -> None:
    set_input(io.BytesIO(b"3 1 2 3 word 10 20"))
    n = read_int()
    assert read_ints(n) == [1, 2, 3]
    assert read_str() == "word"
    assert read_all_ints() == [10, 20]
    set_input(None)  # вернуть stdin


def test_ac_12_fast_writer_buffers_until_flush() -> None:
    buf = io.StringIO()
    w = FastWriter(buf)
    w.write("a", 1, sep="-", end="!")
    w.write_lines([1, 2])
    assert buf.getvalue() == ""
    w.flush()
    assert buf.getvalue() == "a-1!1\n2\n"


def test_ac_12_template_is_valid_python() -> None:
    src = fast_io_template()
    compile(src, "<template>", "exec")
    assert "sys.stdin.buffer.read" in src
