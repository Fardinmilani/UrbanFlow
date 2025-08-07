# UrbanFlow 🚦

![Project Banner](images/transport_network_banner.png)

Dive into the **UrbanFlow** project! This tool, built with Python, explores city transportation networks using directed graphs—nodes as locations and edges as paths (one-way or two-way). It tracks every possible route between points and counts how often each connection is used, pinpointing the most critical links. 📊

## Quick Guide
- [What’s Inside](#whats-inside)
- [What It Does](#what-it-does)
- [Getting Started](#getting-started)
- [How to Use](#how-to-use)
- [Sample Results](#sample-results)
- [Join In](#join-in)
- [Terms of Use](#terms-of-use)
- [Get in Touch](#get-in-touch)

## What’s Inside

This project comes with a Jupyter Notebook (`Transport project v2.ipynb`) to map and study transportation networks as directed graphs. Locations are nodes, and paths are edges—some one-way, some two-way. The code:
- Draws the network with `networkx` and `matplotlib`.
- Figures out all routes between any two points.
- Tallies up how often each link appears to spot key connections.
- Saves results as a DataFrame and exports them to CSV, Excel, and text files.

It’s powered by Python and uses libraries like `pandas`, `networkx`, `matplotlib`, and `numpy`.

## What It Does

- 📈 **Network View**: Shows the transport map with labeled spots and directed lines.
- 🛤️ **Route Tracking**: Lists every possible path between locations.
- 🔍 **Link Priority**: Highlights which connections get used the most.
- 💾 **File Output**: Dumps results into CSV, Excel, and text files.
- 🚀 **User-Friendly**: Runs in a Jupyter Notebook for easy tinkering.

## Getting Started

To run this on your machine, try these steps:

1. **Grab the Code**:
   ```bash
   git clone https://github.com/Fardinmilani/UrbanFlow.git
   cd UrbanFlow
   ```

2. **Install What You Need**:
   Make sure Python 3.11+ is ready. Then, get the libraries:
   ```bash
   pip install pandas networkx matplotlib numpy
   ```

3. **Set Up Jupyter**:
   If you don’t have Jupyter, add it:
   ```bash
   pip install jupyter
   ```

4. **Launch It**:
   Start Jupyter Notebook and open `Transport project v2.ipynb`:
   ```bash
   jupyter notebook
   ```

## How to Use

1. Load `Transport project v2.ipynb` in Jupyter Notebook.
2. Run the cells one by one to:
   - Load the tools.
   - Set up the graph (tweak the `graph` dictionary for your network).
   - See the graph.
   - Compute paths and link counts.
   - Save outputs to `incidence_matrix.csv`, `incidence_matrix.xlsx`, `incidence_matrix.txt`.
3. Adjust the `graph` dictionary to match your network. Example:
   ```python
   graph = {
       '1': ['3'],
       '2': ['3'],
       '3': ['4', '4'],  # Two paths from 3 to 4
       '4': []
   }
   ```

## Sample Results

Here’s a peek at the network visualization:

![Graph Visualization](images/graph_visualization.png)

You’ll get:
- A full list of paths between nodes.
- A table of link usage, saved as:
  - `incidence_matrix.csv`
  - `incidence_matrix.xlsx`
  - `incidence_matrix.txt`

Sample link count:
```
Link repetitions:
('1', '3'): 3 times
('3', '4'): 6 times
('2', '3'): 3 times
```

## Join In

Love to contribute? 🌟 Here’s how:
1. Fork this repo.
2. Start a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push it (`git push origin feature/your-feature`).
5. Send a pull request.

Keep the code tidy and add comments where needed.

## Terms of Use

This work is under the MIT License. Check the [LICENSE](LICENSE) file for the full story.

## Get in Touch

Got ideas or questions? Drop a line! 📬
- GitHub: [Fardinmilani](https://github.com/Fardinmilani)
- Email: fardin.milani.user@gmail.com

---

Give it a ⭐ if it helps!  
Enjoy exploring urban routes! 🚍