import networkx as nx
import matplotlib.pyplot as plt
import random


def generate_weighted_graph(num_nodes, edge_probability, min_weight, max_weight):
    """
    Generates a random weighted graph.

    Parameters:
      num_nodes (int): Number of nodes in the graph.
      edge_probability (float): Probability that an edge exists between any two nodes.
      min_weight (int): Minimum edge weight.
      max_weight (int): Maximum edge weight.

    Returns:
      NetworkX Graph: The generated weighted graph.
    """
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < edge_probability:
                weight = random.randint(min_weight, max_weight)
                G.add_edge(i, j, weight=weight)
    return G


def kruskal_mst(G):
    """
    Computes the Minimum Spanning Tree (MST) of a graph using Kruskal's algorithm.

    Parameters:
      G (NetworkX Graph): A weighted graph.

    Returns:
      NetworkX Graph: A graph representing the MST.
    """
    # Initialize union-find structure
    parent = {node: node for node in G.nodes()}
    rank = {node: 0 for node in G.nodes()}

    def find(u):
        # Path compression
        if parent[u] != u:
            parent[u] = find(parent[u])
        return parent[u]

    def union(u, v):
        ru = find(u)
        rv = find(v)
        if ru == rv:
            return False
        if rank[ru] < rank[rv]:
            parent[ru] = rv
        elif rank[ru] > rank[rv]:
            parent[rv] = ru
        else:
            parent[rv] = ru
            rank[ru] += 1
        return True

    # Get all edges and sort them by weight
    edges = list(G.edges(data=True))
    edges.sort(key=lambda edge: edge[2]['weight'])

    # Create MST graph and add nodes
    T = nx.Graph()
    T.add_nodes_from(G.nodes())

    # Iterate over sorted edges and add them if they don't form a cycle
    for u, v, data in edges:
        if union(u, v):
            T.add_edge(u, v, weight=data['weight'])

    return T


def draw_graphs_side_by_side(G, T):
    """
    Draws the original graph and its MST side by side.

    Parameters:
      G (NetworkX Graph): The original weighted graph.
      T (NetworkX Graph): The minimum spanning tree of G.
    """
    # Compute a layout that will be shared by both graphs
    pos = nx.spring_layout(G)

    # Create side-by-side subplots
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Draw original graph
    ax = axes[0]
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, ax=ax)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    ax.set_title("Original Graph")

    # Draw MST
    ax = axes[1]
    nx.draw(T, pos, with_labels=True, node_color='lightgreen', node_size=500, ax=ax)
    mst_edge_labels = nx.get_edge_attributes(T, 'weight')
    nx.draw_networkx_edge_labels(T, pos, edge_labels=mst_edge_labels, ax=ax)
    ax.set_title("Minimum Spanning Tree (Kruskal)")

    plt.tight_layout()
    plt.show()


# Example usage:
if __name__ == '__main__':
    num_nodes = 20  # Number of nodes in the graph
    edge_probability = 0.3  # Probability for creating an edge between any two nodes
    min_weight = 1  # Minimum weight of an edge
    max_weight = 10  # Maximum weight of an edge

    # Generate the weighted graph
    G = generate_weighted_graph(num_nodes, edge_probability, min_weight, max_weight)

    # Compute its MST using Kruskal's algorithm
    T = kruskal_mst(G)

    # Draw both graphs side by side
    draw_graphs_side_by_side(G, T)
