from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from .core import UrbanFlowResult, analyze_network, load_graph_from_edges, save_analysis_results


def _visualize_network(
    result: UrbanFlowResult,
    output_dir: Path,
    title: str | None = None,
) -> None:
    """
    Visualize the network with edge thickness and color
    proportional to edge usage count.
    """
    G = result.graph
    edge_counts = result.edge_repetitions

    # Basic layout
    pos = nx.spring_layout(G, seed=42)

    # Slightly larger figure; we'll hide axes to keep focus on the graph.
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis("off")

    # draw nodes and labels
    nx.draw_networkx_nodes(
        G,
        pos,
        node_color="#ffd54f",
        node_size=900,
        ax=ax,
    )
    nx.draw_networkx_labels(
        G,
        pos,
        font_size=12,
        font_weight="bold",
        ax=ax,
    )

    # Normalize edge weights for visualization (colors / base width)
    counts = list(edge_counts.values()) or [1]
    min_c, max_c = min(counts), max(counts)
    span = max(max_c - min_c, 1)

    # Collect unique (u, v) pairs from the MultiDiGraph, preserving multiplicity info.
    unique_pairs: list[tuple[str, str]] = []
    seen_pairs: set[tuple[str, str]] = set()
    for u, v, _key in G.edges(keys=True):
        pair = (u, v)
        if pair not in seen_pairs:
            unique_pairs.append(pair)
            seen_pairs.add(pair)

    # Draw thinner edges first so thicker links stay visible on top.
    unique_pairs.sort(key=lambda pair: edge_counts.get(pair, 0))

    for u, v in unique_pairs:

        base_count = edge_counts.get((u, v), 0)
        color_val = base_count
        # Keep widths in a reasonable range so the plot doesn't get flooded.
        base_width = 1 + 2 * (base_count - min_c) / span if span else 1

        m = max(1, G.number_of_edges(u, v))

        # draw m parallel arcs with small different radii
        if m == 1:
            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=[(u, v)],
                width=base_width,
                edge_color=[color_val],
                edge_cmap=plt.cm.plasma,
                arrows=True,
                arrowstyle="-|>",
                arrowsize=22,
                ax=ax,
            )
        else:
            # spread arcs around zero radius with a noticeable separation
            start = -(m - 1) / 2
            rad_step = 0.25
            for i in range(m):
                rad = rad_step * (start + i)
                nx.draw_networkx_edges(
                    G,
                    pos,
                    edgelist=[(u, v)],
                    width=base_width,
                    edge_color=[color_val],
                    edge_cmap=plt.cm.plasma,
                    arrows=True,
                    arrowstyle="-|>",
                    arrowsize=22,
                    connectionstyle=f"arc3,rad={rad}",
                    ax=ax,
                )

    sm = plt.cm.ScalarMappable(
        cmap=plt.cm.plasma,
        norm=plt.Normalize(vmin=min_c, vmax=max_c),
    )
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label("Edge usage count")

    if title:
        plt.title(title)

    output_dir.mkdir(parents=True, exist_ok=True)
    image_path = output_dir / "urbanflow_network.png"
    plt.tight_layout()
    plt.savefig(image_path, dpi=200)
    plt.close()


def run_cli(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="UrbanFlow: Analyze directed transport networks from an edge list.",
    )
    parser.add_argument(
        "edges_csv",
        type=str,
        help="Path to CSV file containing edges with at least 'from' and 'to' columns.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="urbanflow_output",
        help="Directory to store analysis outputs (default: %(default)s).",
    )
    parser.add_argument(
        "--source-col",
        type=str,
        default="from",
        help="Name of the source column in the CSV (default: %(default)s).",
    )
    parser.add_argument(
        "--target-col",
        type=str,
        default="to",
        help="Name of the target column in the CSV (default: %(default)s).",
    )
    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="Skip generating the network visualization PNG.",
    )

    args = parser.parse_args(argv)

    edges_path = Path(args.edges_csv)
    output_dir = Path(args.output_dir)

    if not edges_path.is_file():
        raise SystemExit(f"Edge CSV file not found: {edges_path}")

    # allow commented lines starting with '#' in the CSV
    edges_df = pd.read_csv(edges_path, comment="#")
    graph_dict = load_graph_from_edges(
        edges_df,
        source_col=args.source_col,
        target_col=args.target_col,
    )
    result = analyze_network(graph_dict)

    save_analysis_results(result, output_dir=output_dir, base_name="urbanflow")

    if not args.no_plot:
        _visualize_network(
            result,
            output_dir=output_dir,
            title="UrbanFlow Network (edge usage)",
        )


if __name__ == "__main__":
    run_cli()


