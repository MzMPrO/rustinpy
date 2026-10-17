"""Graphs: traversals, shortest paths, DAGs, DSU / MST, SCC / 2-SAT, Euler, functional graphs,
flows, matchings, Hamiltonian paths and advanced CSES problems.

Графы. Вершины 0..n-1; adj[u] = [v, ...] или [(v, w), ...]; рёбра (u, v[, w]). Без рекурсии:
``from rustinpy.graph import dijkstra, Dinic, scc_tarjan``.
"""

from __future__ import annotations

from rustinpy.graph.advanced import (
    bus_companies,
    critical_cities,
    even_outdegree_edges,
    flight_route_requests,
    network_renovation,
    strongly_connected_edges,
)
from rustinpy.graph.dag import (
    count_paths_dag,
    longest_path_dag,
    reachable_counts,
    toposort_kahn,
    toposort_lex_min,
    toposort_smallest_first,
)
from rustinpy.graph.dsu import DSU, RollbackDSU, kruskal, prim, road_construction
from rustinpy.graph.euler import euler_path_directed, euler_path_undirected
from rustinpy.graph.flow import Dinic, MinCostFlow, edge_disjoint_paths, edmonds_karp, min_cut_edges
from rustinpy.graph.functional import (
    build_lifting,
    cycle_steps,
    escalators,
    functional_distance,
    kth_successor,
)
from rustinpy.graph.matching import hopcroft_karp, hungarian, kuhn_matching
from rustinpy.graph.paths import hamiltonian_path, knights_tour
from rustinpy.graph.scc import (
    articulation_points,
    bridges,
    coin_collector,
    condensation,
    reachability_queries,
    scc_kosaraju,
    scc_tarjan,
    two_sat,
)
from rustinpy.graph.shortest import (
    INF,
    bellman_ford,
    dijkstra,
    dijkstra_coupon,
    dijkstra_path,
    dijkstra_states,
    dijkstra_stats,
    find_negative_cycle,
    floyd_warshall,
    k_shortest_walks,
    max_score_path,
    zero_one_bfs,
)
from rustinpy.graph.traversal import (
    bfs,
    bfs_path,
    bipartite_coloring,
    connected_components,
    dfs_order,
    find_cycle_directed,
    find_cycle_undirected,
    girth,
    grid_bfs,
    multi_source_bfs,
)

__all__ = [
    "DSU",
    "INF",
    "Dinic",
    "MinCostFlow",
    "RollbackDSU",
    "articulation_points",
    "bellman_ford",
    "bfs",
    "bfs_path",
    "bipartite_coloring",
    "bridges",
    "build_lifting",
    "bus_companies",
    "coin_collector",
    "condensation",
    "connected_components",
    "count_paths_dag",
    "critical_cities",
    "cycle_steps",
    "dfs_order",
    "dijkstra",
    "dijkstra_coupon",
    "dijkstra_path",
    "dijkstra_states",
    "dijkstra_stats",
    "edge_disjoint_paths",
    "edmonds_karp",
    "escalators",
    "euler_path_directed",
    "euler_path_undirected",
    "even_outdegree_edges",
    "find_cycle_directed",
    "find_cycle_undirected",
    "find_negative_cycle",
    "flight_route_requests",
    "floyd_warshall",
    "functional_distance",
    "girth",
    "grid_bfs",
    "hamiltonian_path",
    "hopcroft_karp",
    "hungarian",
    "k_shortest_walks",
    "knights_tour",
    "kruskal",
    "kth_successor",
    "kuhn_matching",
    "longest_path_dag",
    "max_score_path",
    "min_cut_edges",
    "multi_source_bfs",
    "network_renovation",
    "prim",
    "reachability_queries",
    "reachable_counts",
    "road_construction",
    "scc_kosaraju",
    "scc_tarjan",
    "strongly_connected_edges",
    "toposort_kahn",
    "toposort_lex_min",
    "toposort_smallest_first",
    "two_sat",
    "zero_one_bfs",
]
