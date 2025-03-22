import networkx as nx
import matplotlib.pyplot as plt
import math


def shift_label(u, v, pos, shift=0.15):
    """
    Compute a shifted position for an edge label between nodes u and v.
    The label is shifted perpendicular to the edge by the specified amount.
    """
    x1, y1 = pos[u]
    x2, y2 = pos[v]
    # Midpoint of the edge
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx ** 2 + dy ** 2)
    if length == 0:
        return (mx, my)
    # Perpendicular vector (normalized)
    px = -dy / length
    py = dx / length
    # Shift the midpoint
    sx = mx + shift * px
    sy = my + shift * py
    return (sx, sy)


def main():
    G = nx.Graph()
    # Define node positions for the desired layout
    pos = {
        'a': (0, 2),
        'b': (0, 0),
        'c': (2, 2),
        'd': (2, 0),
        'e': (4, 2),
        'f': (4, 0),
        'g': (6, 2),
        'h': (6, 0)
    }
    for node, p in pos.items():
        G.add_node(node, pos=p)

    # Add edges with weights (including (a,d)=4 and (b,c)=1)
    edges = [
        ('a', 'b', 5),
        ('a', 'c', 6),
        ('a', 'd', 4),
        ('b', 'c', 1),
        ('b', 'd', 3),
        ('c', 'd', 2),
        ('c', 'e', 7),
        ('c', 'f', 8),
        ('d', 'e', 6),
        ('d', 'f', 7),
        ('e', 'f', 4),
        ('e', 'g', 8),
        ('f', 'h', 9),
        ('g', 'h', 1)
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    # Verify stored weights (optional)
    print("Edges with weights:")
    for e in G.edges(data=True):
        print(e)

    # Draw the graph's nodes, edges, and labels
    plt.figure(figsize=(8, 4))
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color='white', edgecolors='black')
    nx.draw_networkx_edges(G, pos, width=1.5, edge_color='black')
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')

    # Get the edge weights from the graph
    edge_labels = nx.get_edge_attributes(G, 'weight')

    # Define the crossing edges that need label shifting:
    # Here, (a,d) and (b,c) are one crossing pair,
    # while (c,f) and (d,e) are another.
    crossing_edges = [('a', 'd'), ('b', 'c'), ('c', 'f'), ('d', 'e')]

    # Build a dictionary for label positions for all edges
    label_pos = {}
    for u, v in G.edges():
        # Check if this edge is one of the crossing edges (in either order)
        if (u, v) in crossing_edges or (v, u) in crossing_edges:
            # For clarity, alternate the shift direction
            shift = 0.15 if (u, v) in crossing_edges else -0.15
            label_pos[(u, v)] = shift_label(u, v, pos, shift)
        else:
            # For non-crossing edges, no shift (or you can adjust if needed)
            label_pos[(u, v)] = shift_label(u, v, pos, 0)

    # Manually draw edge labels using plt.text
    for edge, (x, y) in label_pos.items():
        # Retrieve the label for the edge; check both (u,v) and (v,u)
        label = edge_labels.get(edge)
        if label is None:
            label = edge_labels.get((edge[1], edge[0]), "")
        plt.text(x, y, str(label), color='red', fontsize=10,
                 horizontalalignment='center', verticalalignment='center')

    plt.axis('equal')
    plt.axis('off')
    plt.title("Undirected Weighted Graph with Adjusted Edge Label Positions")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
