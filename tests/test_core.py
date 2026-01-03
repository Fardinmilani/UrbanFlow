"""Tests for urbanflow.core module."""

import warnings

import pytest

from urbanflow.core import (
    analyze_network,
    build_digraph,
    build_od_incidence_matrix,
    count_edge_repetitions,
    count_path_repetitions,
    find_all_paths_between_all_pairs,
    find_paths,
    load_graph_from_edges,
)


class TestGraphLoading:
    """Test graph loading from edge lists."""

    def test_load_graph_from_edges_simple(self):
        import pandas as pd

        edges = pd.DataFrame({"from": ["1", "2"], "to": ["2", "3"]})
        graph = load_graph_from_edges(edges)
        assert graph == {"1": ["2"], "2": ["3"], "3": []}

    def test_load_graph_from_edges_parallel(self):
        import pandas as pd

        edges = pd.DataFrame({"from": ["1", "1"], "to": ["2", "2"]})
        graph = load_graph_from_edges(edges)
        assert graph == {"1": ["2", "2"], "2": []}

    def test_load_graph_from_edges_missing_columns(self):
        import pandas as pd

        edges = pd.DataFrame({"source": ["1"], "target": ["2"]})
        with pytest.raises(ValueError, match="must contain"):
            load_graph_from_edges(edges, source_col="from", target_col="to")


class TestPathFinding:
    """Test path enumeration functions."""

    def test_find_paths_simple(self):
        graph = {"1": ["2"], "2": ["3"], "3": []}
        paths = find_paths(graph, "1", "3")
        assert paths == [["1", "2", "3"]]

    def test_find_paths_no_path(self):
        graph = {"1": ["2"], "2": [], "3": []}
        paths = find_paths(graph, "1", "3")
        assert paths == []

    def test_find_paths_self_loop(self):
        graph = {"1": ["1"], "2": []}
        paths = find_paths(graph, "1", "1")
        assert paths == [["1"]]

    def test_find_paths_max_length(self):
        graph = {"1": ["2"], "2": ["3"], "3": ["4"], "4": ["5"], "5": []}
        paths = find_paths(graph, "1", "5", max_path_length=3)
        assert paths == []  # Path length 5 exceeds max 3

    def test_find_paths_max_paths_limit(self):
        # Create a graph that would generate many paths
        graph = {}
        for i in range(10):
            graph[str(i)] = [str(i + 1)] if i < 9 else []
        # Add multiple paths
        graph["0"].extend(["1", "1"])

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            paths = find_paths(graph, "0", "9", max_paths=5)
            assert len(paths) <= 5
            if len(w) > 0:
                assert "limit reached" in str(w[0].message).lower()

    def test_find_all_paths_between_all_pairs(self):
        graph = {"1": ["2"], "2": ["3"], "3": []}
        all_paths = find_all_paths_between_all_pairs(graph)
        # Should find: 1->2, 1->3, 2->3
        assert len(all_paths) == 3
        assert ["1", "2"] in all_paths
        assert ["1", "2", "3"] in all_paths
        assert ["2", "3"] in all_paths


class TestCounting:
    """Test path and edge counting functions."""

    def test_count_path_repetitions(self):
        paths = [["1", "2"], ["1", "2"], ["2", "3"]]
        reps = count_path_repetitions(paths)
        assert reps["1 -> 2"] == 2
        assert reps["2 -> 3"] == 1

    def test_count_edge_repetitions(self):
        path_reps = {"1 -> 2 -> 3": 2, "2 -> 3": 1}
        edge_reps = count_edge_repetitions(path_reps)
        assert edge_reps[("1", "2")] == 2
        assert edge_reps[("2", "3")] == 3  # 2 from first path + 1 from second


class TestODIncidenceMatrix:
    """Test OD-incidence matrix construction."""

    def test_build_od_incidence_matrix_simple(self):
        graph = {"1": ["2"], "2": ["3"], "3": []}
        incidence = build_od_incidence_matrix(graph)
        assert "1->2" in incidence.index
        assert "2->3" in incidence.index
        assert "1->3" in incidence.columns
        assert "SUM" in incidence.columns

    def test_build_od_incidence_matrix_with_paths(self):
        graph = {"1": ["2"], "2": ["3"], "3": []}
        all_paths = [["1", "2"], ["1", "2", "3"], ["2", "3"]]
        incidence = build_od_incidence_matrix(graph, all_paths=all_paths)
        # Edge 1->2 should be in OD 1->2 and 1->3
        assert incidence.loc["1->2", "1->2"] == 1
        assert incidence.loc["1->2", "1->3"] == 1


class TestAnalyzeNetwork:
    """Test high-level analyze_network function."""

    def test_analyze_network_simple(self):
        graph = {"1": ["2"], "2": ["3"], "3": []}
        result = analyze_network(graph)
        assert len(result.all_paths) > 0
        assert len(result.edge_repetitions) > 0
        assert "SUM" in result.od_incidence.columns

    def test_analyze_network_parallel_edges(self):
        graph = {"1": ["2", "2"], "2": ["3"], "3": []}
        result = analyze_network(graph)
        # Should handle parallel edges correctly
        assert ("1", "2") in result.edge_repetitions

    def test_analyze_network_empty_graph(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            analyze_network({})

    def test_analyze_network_invalid_type(self):
        with pytest.raises(ValueError, match="must be a dict"):
            analyze_network("not a dict")

    def test_analyze_network_with_limits(self):
        # Create a larger graph
        graph = {}
        for i in range(5):
            graph[str(i)] = [str(i + 1)] if i < 4 else []
        # Add some branching
        graph["0"].append("2")

        result = analyze_network(graph, max_path_length=3, max_paths_per_od=10)
        # Should complete without crashing
        assert result is not None
        assert len(result.all_paths) > 0


class TestBuildDigraph:
    """Test MultiDiGraph construction."""

    def test_build_digraph_simple(self):
        graph = {"1": ["2"], "2": ["3"], "3": []}
        G = build_digraph(graph)
        assert G.has_edge("1", "2")
        assert G.has_edge("2", "3")
        assert not G.has_edge("1", "3")

    def test_build_digraph_parallel_edges(self):
        graph = {"1": ["2", "2"], "2": []}
        G = build_digraph(graph)
        assert G.number_of_edges("1", "2") == 2

