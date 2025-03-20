import networkx as nx
import matplotlib.pyplot as plt

# Correct edges/weights (matching your figure)
edges = [
    ('a', 'b', 5),  # vertical (left)
    ('a', 'c', 6),  # top horizontal
    ('b', 'c', 1),  # diagonal
    ('c', 'd', 2),  # vertical
    ('a', 'd', 4),  # diagonal
    ('b', 'd', 3),  # bottom horizontal
    ('c', 'e', 7),  # top horizontal
    ('d', 'e', 6),  # diagonal
    ('e', 'f', 4),  # vertical
    ('c', 'f', 8),  # diagonal
    ('d', 'f', 7),  # diagonal
    ('e', 'g', 8),  # top horizontal
    ('f', 'h', 9),  # bottom horizontal
    ('g', 'h', 1),  # vertical (right)
]

G = nx.Graph()
G.add_weighted_edges_from(edges)

# Adjust positions to spread things out a bit more vertically
# so the diagonals are less likely to overlap labels:
pos = {
    'a': (0, 1.5),
    'b': (0, 0),
    'c': (2, 1.5),
    'd': (2, 0),
    'e': (4, 1.5),
    'f': (4, 0),
    'g': (6, 1.5),
    'h': (6, 0),
}

plt.figure(figsize=(10, 5))
nx.draw(
    G, pos, with_labels=True,
    node_color='lightblue', node_size=800,
    font_size=12, edge_color='gray'
)

# Create the edge-label dictionary
edge_labels = {(u, v): w for u, v, w in edges}

# Draw edge labels with a small offset (label_pos) so they don’t
# sit exactly on the middle of crossing lines:
nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=edge_labels,
    font_color='red',
    label_pos=0.25  # tweak between 0.2 and 0.5 to move labels
)

plt.title("Undirected Graph with Correct Weights & Adjusted Layout")
plt.axis('off')
plt.show()
