"""rustinpy - ICPC / CSES algorithms cheat sheet.

Шпаргалка алгоритмов для ICPC: каждая функция самодостаточна, её можно скопировать в TRD.

    >>> import rustinpy
    >>> rustinpy.__version__
    '0.1.0'

Algorithms live in submodules (``from rustinpy.graph import dijkstra``);
only the helpers below are exported at the top level.
"""

from __future__ import annotations

from rustinpy._api import export, help, list_algos, search, show
from rustinpy._registry import AlgoInfo

__version__ = "0.1.0"

__all__ = ["AlgoInfo", "__version__", "export", "help", "list_algos", "search", "show"]
