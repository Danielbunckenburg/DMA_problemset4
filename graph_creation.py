import networkx as nx
import matplotlib.pyplot as plt
import random


def generate_weighted_graph(num_nodes, edge_probability, min_weight, max_weight):
    # Create an empty graph and add nodes
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))

    # Iterate over each possible pair of nodes
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            # Add an edge with given probability
            if random.random() < edge_probability:
                weight = random.randint(min_weight, max_weight)
                G.add_edge(i, j, weight=weight)
    return G


def draw_weighted_graph(G):
    # Use a spring layout for better visualization
    pos = nx.spring_layout(G)

    # Extract edge labels (weights)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    # Draw nodes and edges
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)

    # Draw the weight labels on the edges
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Random Weighted Graph")
    plt.show()


# Example usage:
if __name__ == '__main__':
    num_nodes = 10  # Number of nodes in the graph
    edge_probability = 0.3  # Probability for edge creation between any two nodes
    min_weight = 1  # Minimum weight for an edge
    max_weight = 10  # Maximum weight for an edge

    # Generate the graph and draw it
    G = generate_weighted_graph(num_nodes, edge_probability, min_weight, max_weight)
    draw_weighted_graph(G)
