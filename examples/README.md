# Examples

This directory contains example data files for testing UrbanFlow.

## edges_example.csv

A sample directed network with 7 nodes and multiple parallel edges:
- Nodes: 1, 2, 3, 4, 5, 6, 7
- Includes parallel edges (e.g., multiple edges between the same node pairs)
- Format: CSV with `from` and `to` columns

### Usage

```bash
python -m urbanflow.cli examples/edges_example.csv --output-dir examples_output
```

