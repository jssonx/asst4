from igraph import Graph
import struct

# Parameters
n = 2000000  # Number of nodes
mu = 5       # Average degree
p = 0.25     # Probability of forming a triangle

# Create a power-law cluster graph
# Step 1: Generate a graph with a power-law degree distribution using the Barabasi method
G = Graph.Barabasi(n, mu)

# Step 2: Rewire a portion of the edges to increase clustering
G.rewire(int(G.ecount() * p))

# Code for writing the graph data to a binary file
GRAPH_HEADER_TOKEN = 0xDEADBEEF
outgoing_starts = [0] * n
outgoing_edges = []
current_outgoing_edge_count = 0

# Collect edges and their starting points
for node in range(n):
    neighbors = G.neighbors(node, mode="out")
    outgoing_starts[node] = current_outgoing_edge_count
    outgoing_edges.extend(neighbors)
    current_outgoing_edge_count += len(neighbors)

# Write graph data to a binary file
with open("random_graph.graph", "wb") as f:
    # Header: token, number of nodes, number of edges
    header = struct.pack('III', GRAPH_HEADER_TOKEN, n, len(outgoing_edges))
    f.write(header)

    # Outgoing starts and edges
    outgoing_starts_bytes = struct.pack(f'{len(outgoing_starts)}i', *outgoing_starts)
    f.write(outgoing_starts_bytes)
    outgoing_edges_bytes = struct.pack(f'{len(outgoing_edges)}i', *outgoing_edges)
    f.write(outgoing_edges_bytes)
