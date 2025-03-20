import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation

# Create the original directed graph
G = nx.DiGraph()
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
    ('c', 'a'),
    ('a', 'd')
]
G.add_edges_from(edges)

# Compute the reversed graph (G^R)
G_rev = G.reverse(copy=True)

# Use the same fixed positions for nodes
pos = {
    'a': (0, 1),
    'b': (0, 0),
    'c': (1, 1),
    'd': (1, 0),
    'e': (2, 1),
    'f': (2, 0),
    'g': (3, 1),
    'h': (3, 0)
}

# Manually define the DFS steps for the second pass on the reversed graph.
# This follows the order (from the first pass finishing times): a, b, c, e, d, f, g, h.
# And it produces three SCCs:
#   - SCC1 (starting at a): {a, b, c}
#   - SCC2 (starting at e): {e, d}
#   - SCC3 (starting at f): {f, h, g}
steps = [
    # SCC1: DFS starting at 'a'
    {
        "visited": {"a"},
        "stack": ["a"],
        "finished": set(),
        "current": "a",
        "desc": "Step 1 (SCC1): Start DFS at node a."
    },
    {
        "visited": {"a", "b"},
        "stack": ["a", "b"],
        "finished": set(),
        "current": "b",
        "desc": "Step 2 (SCC1): From a, explore neighbor b."
    },
    {
        "visited": {"a", "b"},
        "stack": ["a"],
        "finished": {"b"},
        "current": None,
        "desc": "Step 3 (SCC1): Finished exploring b; backtrack to a."
    },
    {
        "visited": {"a", "b", "c"},
        "stack": ["a", "c"],
        "finished": {"b"},
        "current": "c",
        "desc": "Step 4 (SCC1): From a, explore neighbor c."
    },
    {
        "visited": {"a", "b", "c"},
        "stack": ["a"],
        "finished": {"b", "c"},
        "current": None,
        "desc": "Step 5 (SCC1): Finished exploring c; backtrack to a."
    },
    {
        "visited": {"a", "b", "c"},
        "stack": [],
        "finished": {"a", "b", "c"},
        "current": None,
        "desc": "Step 6 (SCC1): Finished DFS from a. SCC1 = {a, b, c}."
    },
    # SCC2: DFS starting at 'e'
    {
        "visited": {"a", "b", "c", "e"},
        "stack": ["e"],
        "finished": {"a", "b", "c"},
        "current": "e",
        "desc": "Step 7 (SCC2): Start new DFS at node e."
    },
    {
        "visited": {"a", "b", "c", "d", "e"},
        "stack": ["e", "d"],
        "finished": {"a", "b", "c"},
        "current": "d",
        "desc": "Step 8 (SCC2): From e, explore neighbor d."
    },
    {
        "visited": {"a", "b", "c", "d", "e"},
        "stack": ["e"],
        "finished": {"a", "b", "c", "d"},
        "current": None,
        "desc": "Step 9 (SCC2): Finished exploring d; backtrack to e."
    },
    {
        "visited": {"a", "b", "c", "d", "e"},
        "stack": [],
        "finished": {"a", "b", "c", "d", "e"},
        "current": None,
        "desc": "Step 10 (SCC2): Finished DFS from e. SCC2 = {e, d}."
    },
    # SCC3: DFS starting at 'f'
    {
        "visited": {"a", "b", "c", "d", "e", "f"},
        "stack": ["f"],
        "finished": {"a", "b", "c", "d", "e"},
        "current": "f",
        "desc": "Step 11 (SCC3): Start new DFS at node f."
    },
    {
        "visited": {"a", "b", "c", "d", "e", "f", "h"},
        "stack": ["f", "h"],
        "finished": {"a", "b", "c", "d", "e"},
        "current": "h",
        "desc": "Step 12 (SCC3): From f, explore neighbor h."
    },
    {
        "visited": {"a", "b", "c", "d", "e", "f", "g", "h"},
        "stack": ["f", "h", "g"],
        "finished": {"a", "b", "c", "d", "e"},
        "current": "g",
        "desc": "Step 13 (SCC3): From h, explore neighbor g."
    },
    {
        "visited": {"a", "b", "c", "d", "e", "f", "g", "h"},
        "stack": ["f", "h"],
        "finished": {"a", "b", "c", "d", "e", "g"},
        "current": None,
        "desc": "Step 14 (SCC3): Finished exploring g; backtrack to h."
    },
    {
        "visited": {"a", "b", "c", "d", "e", "f", "g", "h"},
        "stack": ["f"],
        "finished": {"a", "b", "c", "d", "e", "g", "h"},
        "current": None,
        "desc": "Step 15 (SCC3): Finished exploring h; backtrack to f."
    },
    {
        "visited": {"a", "b", "c", "d", "e", "f", "g", "h"},
        "stack": [],
        "finished": {"a", "b", "c", "d", "e", "g", "h", "f"},
        "current": None,
        "desc": "Step 16 (SCC3): Finished DFS from f. SCC3 = {f, h, g}."
    },
]

# Create a figure for the animation
fig, ax = plt.subplots(figsize=(6, 4))


def update(frame):
    ax.clear()
    step = steps[frame]
    # Assign colors based on DFS status:
    # - Gray for finished nodes,
    # - Red for the current node,
    # - Yellow for nodes in the recursion stack,
    # - Light blue for visited nodes,
    # - White for unvisited nodes.
    colors = {}
    for node in G_rev.nodes():
        if node in step["finished"]:
            colors[node] = "gray"
        elif node == step["current"]:
            colors[node] = "red"
        elif node in step["stack"]:
            colors[node] = "yellow"
        elif node in step["visited"]:
            colors[node] = "lightblue"
        else:
            colors[node] = "white"
    node_colors = [colors[node] for node in G_rev.nodes()]

    # Draw the reversed graph with arrows (using a slight curvature)
    nx.draw_networkx(
        G_rev,
        pos,
        node_color=node_colors,
        with_labels=True,
        arrows=True,
        arrowstyle='-|>',
        arrowsize=20,
        connectionstyle='arc3,rad=0.1',
        edge_color='black',
        ax=ax
    )
    ax.set_title(step["desc"])
    ax.axis("off")


# Create the animation with a 1-second interval between frames
ani = animation.FuncAnimation(fig, update, frames=len(steps), interval=1000, repeat=False)

plt.show()
