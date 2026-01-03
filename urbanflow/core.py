from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import networkx as nx
import pandas as pd


Node = str
Edge = Tuple[Node, Node]
PathType = List[Node]


@dataclass
class UrbanFlowResult:
    graph: nx.MultiDiGraph
    all_paths: List[PathType]
    path_repetitions: Dict[str, int]
    edge_repetitions: Dict[Edge, int]
    od_incidence: pd.DataFrame


def load_graph_from_edges(
    edges: pd.DataFrame,
    source_col: str = "from",
    target_col: str = "to",
) -> Dict[Node, List[Node]]:
    """
    Load a graph definition from an edge list DataFrame.

    Expected columns: at least `source_col` and `target_col`.
    """
    if source_col not in edges.columns or target_col not in edges.columns:
        raise ValueError(
            f"Edges DataFrame must contain '{source_col}' and '{target_col}' columns."
        )

    graph: Dict[Node, List[Node]] = {}
    for _, row in edges.iterrows():
        src = str(row[source_col])
        dst = str(row[target_col])
        graph.setdefault(src, []).append(dst)
        graph.setdefault(dst, graph.get(dst, []))
    return graph


def build_digraph(graph: Dict[Node, Sequence[Node]]) -> nx.MultiDiGraph:
    """Build a NetworkX MultiDiGraph to preserve parallel edges."""
    G = nx.MultiDiGraph()
    for node in graph:
        G.add_node(node)
    for src, targets in graph.items():
        for dst in targets:
            G.add_edge(src, dst)
    return G


def find_paths(graph: Dict[Node, Sequence[Node]], start: Node, end: Node, path: PathType | None = None) -> List[PathType]:
    """Find all simple paths from `start` to `end` using DFS."""
    if path is None:
        path = []
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths: List[PathType] = []
    for node in graph[start]:
        if node not in path:
            new_paths = find_paths(graph, node, end, path)
            for new_path in new_paths:
                paths.append(new_path)
    return paths


def find_all_paths_between_all_pairs(graph: Dict[Node, Sequence[Node]]) -> List[PathType]:
    """Compute all simple paths between all ordered node pairs in the graph."""
    all_paths: List[PathType] = []
    nodes = list(graph.keys())
    for start_node in nodes:
        for end_node in nodes:
            if start_node != end_node:
                paths = find_paths(graph, start_node, end_node)
                all_paths.extend(paths)
    return all_paths


def count_path_repetitions(all_paths: Iterable[PathType]) -> Dict[str, int]:
    """Count how many times each unique path appears."""
    path_repetitions: Dict[str, int] = {}
    for path in all_paths:
        path_str = " -> ".join(path)
        path_repetitions[path_str] = path_repetitions.get(path_str, 0) + 1
    return path_repetitions


def count_edge_repetitions(path_repetitions: Dict[str, int]) -> Dict[Edge, int]:
    """Count edge usage based on path repetitions."""
    edge_repetitions: Dict[Edge, int] = {}
    for path_str, repetitions in path_repetitions.items():
        nodes = path_str.split(" -> ")
        edges = [(nodes[i], nodes[i + 1]) for i in range(len(nodes) - 1)]
        for edge in edges:
            edge_repetitions[edge] = edge_repetitions.get(edge, 0) + repetitions
    return edge_repetitions


def _format_path_as_edges(path: PathType) -> List[Edge]:
    return [(path[i], path[i + 1]) for i in range(len(path) - 1)]


def build_od_incidence_matrix(
    graph: Dict[Node, Sequence[Node]],
    all_paths: Iterable[PathType] | None = None,
) -> pd.DataFrame:
    """
    Build an OD-labeled incidence matrix where:
    - index: directed edges (from_node, to_node)
    - columns: OD pairs (origin, destination)
    - values: 1 if edge participates in at least one path for that OD, 0 otherwise
    """
    if all_paths is None:
        all_paths = find_all_paths_between_all_pairs(graph)

    # Collect OD -> set(edges)
    od_to_edges: Dict[Tuple[Node, Node], set[Edge]] = {}
    for path in all_paths:
        if len(path) < 2:
            continue
        od = (path[0], path[-1])
        edges = _format_path_as_edges(path)
        od_to_edges.setdefault(od, set()).update(edges)

    # Build simple string keys for edges and OD pairs to keep the table easy to index/export
    edge_keys: set[str] = set()
    od_keys: set[str] = set()
    for od, edges in od_to_edges.items():
        od_key = f"{od[0]}->{od[1]}"
        od_keys.add(od_key)
        for edge in edges:
            edge_key = f"{edge[0]}->{edge[1]}"
            edge_keys.add(edge_key)

    edge_list = sorted(edge_keys)
    od_list = sorted(od_keys)

    incidence = pd.DataFrame(0, index=edge_list, columns=od_list, dtype=int)
    for od, edges in od_to_edges.items():
        od_key = f"{od[0]}->{od[1]}"
        for edge in edges:
            edge_key = f"{edge[0]}->{edge[1]}"
            incidence.loc[edge_key, od_key] = 1

    incidence["SUM"] = incidence.sum(axis=1)
    incidence.index.name = "edge"
    return incidence


def analyze_network(
    graph: Dict[Node, Sequence[Node]],
) -> UrbanFlowResult:
    """
    High-level one-shot analysis for a given graph.
    Returns the NetworkX graph, all paths, repetition stats, and OD incidence matrix.
    """
    all_paths = find_all_paths_between_all_pairs(graph)
    path_reps = count_path_repetitions(all_paths)
    edge_reps = count_edge_repetitions(path_reps)
    incidence = build_od_incidence_matrix(graph, all_paths=all_paths)
    di_graph = build_digraph(graph)
    return UrbanFlowResult(
        graph=di_graph,
        all_paths=all_paths,
        path_repetitions=path_reps,
        edge_repetitions=edge_reps,
        od_incidence=incidence,
    )


def save_analysis_results(
    result: UrbanFlowResult,
    output_dir: str | Path,
    base_name: str = "urbanflow",
) -> None:
    """
    Save core analysis outputs to CSV/Excel in the given directory.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Edge usage table
    edge_usage_df = (
        pd.DataFrame(
            [
                {"from": edge[0], "to": edge[1], "count": count}
                for edge, count in result.edge_repetitions.items()
            ]
        )
        .sort_values(by="count", ascending=False)
        .reset_index(drop=True)
    )

    edge_usage_df.to_csv(output_dir / f"{base_name}_edge_usage.csv", index=False)

    # OD incidence
    result.od_incidence.to_csv(output_dir / f"{base_name}_od_incidence.csv")
    with pd.ExcelWriter(output_dir / f"{base_name}_results.xlsx") as writer:
        edge_usage_df.to_excel(writer, sheet_name="edge_usage", index=False)
        result.od_incidence.to_excel(writer, sheet_name="od_incidence")


