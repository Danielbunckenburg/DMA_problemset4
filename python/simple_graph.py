import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Add edges, including the newly added (c->a) and (a->d)
edges = [
    ('a', 'b'),
    ('b', 'a'),
    ('a', 'e'),
    ('b', 'c'),
    ('b', 'd'),
    ('c', 'e'),
    ('c', 'f'),
    ('d', 'f'),
    ('d', 'e'),
    ('e', 'f'),
    ('e', 'h'),
    ('e', 'd'),
    ('f', 'g'),
    ('g', 'h'),
    ('h', 'f'),
    ('c', 'a'),  # newly added
    ('a', 'd')   # newly added
]
G.add_edges_from(edges)

# Manually assign positions to avoid confusing overlaps
pos = {
    'a': (0, 1),
    'b': (0, 0),
    'c': (1, 1),
    'd': (1, 0),
    'e': (2, 1),
    'f': (2, 0),
    # Shift g and h slightly so g->h doesn't overlap with h->f
    'g': (3, 1.2),
    'h': (3, -0.2)
}

# Create the figure
plt.figure(figsize=(8, 4))

# Draw nodes: white circles with black borders
nx.draw_networkx_nodes(
    G, pos,
    node_size=1200,
    node_color='white',
    edgecolors='black',
    linewidths=1.5
)

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=12, font_color='black')

# Draw edges with arrows
nx.draw_networkx_edges(
    G,
    pos,
    arrows=True,
    arrowstyle='-|>',
    arrowsize=20,
    edge_color='black',
    # Slight curvature to differentiate edges
    connectionstyle='arc3,rad=0.15',
    # Margins help keep arrows from getting hidden behind the nodes
    min_source_margin=15,
    min_target_margin=15
)

plt.axis('off')
plt.tight_layout()
plt.show()
