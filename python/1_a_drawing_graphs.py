import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation

# Define the directed graph with all edges
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

# Manually set positions for clarity
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

# Define the DFS steps manually.
# Each dictionary represents a DFS step with the following keys:
#   visited: nodes that have been discovered
#   stack: nodes currently in the DFS recursion stack
#   finished: nodes that have been completely processed
#   current: the node being explored at this step
#   desc: description of the current step
steps = [
    {
        "visited": {"a"},
        "stack": ["a"],
        "finished": set(),
        "current": "a",
        "desc": "Step 1: Start DFS at node a."
    },
    {
        "visited": {"a", "b"},
        "stack": ["a", "b"],
        "finished": set(),
        "current": "b",
        "desc": "Step 2: From a, explore to b."
    },
    {
        "visited": {"a", "b", "c"},
        "stack": ["a", "b", "c"],
        "finished": set(),
        "current": "c",
        "desc": "Step 3: From b, explore to c."
    },
    {
        "visited": {"a", "b", "c", "e"},
        "stack": ["a", "b", "c", "e"],
        "finished": set(),
        "current": "e",
        "desc": "Step 4: From c, explore to e."
    },
    {
        "visited": {"a", "b", "c", "e", "f"},
        "stack": ["a", "b", "c", "e", "f"],
        "finished": set(),
        "current": "f",
        "desc": "Step 5: From e, explore to f."
    },
    {
        "visited": {"a", "b", "c", "e", "f", "g"},
        "stack": ["a", "b", "c", "e", "f", "g"],
        "finished": set(),
        "current": "g",
        "desc": "Step 6: From f, explore to g."
    },
    {
        "visited": {"a", "b", "c", "e", "f", "g", "h"},
        "stack": ["a", "b", "c", "e", "f", "g", "h"],
        "finished": set(),
        "current": "h",
        "desc": "Step 7: From g, explore to h."
    },
    {
        "visited": {"a", "b", "c", "e", "f", "g", "h"},
        "stack": ["a", "b", "c", "e", "f", "g"],
        "finished": {"h"},
        "current": None,
        "desc": "Step 8: h finished. Backtrack to g."
    },
    {
        "visited": {"a", "b", "c", "e", "f", "g", "h"},
        "stack": ["a", "b", "c", "e", "f"],
        "finished": {"h", "g"},
        "current": None,
        "desc": "Step 9: g finished. Backtrack to f."
    },
    {
        "visited": {"a", "b", "c", "e", "f", "g", "h"},
        "stack": ["a", "b", "c", "e"],
        "finished": {"h", "g", "f"},
        "current": None,
        "desc": "Step 10: f finished. Backtrack to e."
    },
    {
        "visited": {"a", "b", "c", "d", "e", "f", "g", "h"},
        "stack": ["a", "b", "c", "e", "d"],
        "finished": {"h", "g", "f"},
        "current": "d",
        "desc": "Step 11: From e, explore to d."
    },
    {
        "visited": {"a", "b", "c", "d", "e", "f", "g", "h"},
        "stack": ["a", "b", "c", "e"],
        "finished": {"h", "g", "f", "d"},
        "current": None,
        "desc": "Step 12: d finished. Backtrack to e."
    },
    {
        "visited": {"a", "b", "c", "d", "e", "f", "g", "h"},
        "stack": ["a", "b", "c"],
        "finished": {"h", "g", "f", "d", "e"},
        "current": None,
        "desc": "Step 13: e finished. Backtrack to c."
    },
    {
        "visited": {"a", "b", "c", "d", "e", "f", "g", "h"},
        "stack": ["a", "b"],
        "finished": {"h", "g", "f", "d", "e", "c"},
        "current": None,
        "desc": "Step 14: c finished. Backtrack to b."
    },
    {
        "visited": {"a", "b", "c", "d", "e", "f", "g", "h"},
        "stack": ["a"],
        "finished": {"h", "g", "f", "d", "e", "c", "b"},
        "current": None,
        "desc": "Step 15: b finished. Backtrack to a."
    },
    {
        "visited": {"a", "b", "c", "d", "e", "f", "g", "h"},
        "stack": [],
        "finished": {"h", "g", "f", "d", "e", "c", "b", "a"},
        "current": None,
        "desc": "Step 16: a finished. DFS complete."
    },
]

# Create a figure and axis for the animation
fig, ax = plt.subplots(figsize=(6, 4))


def update(frame):
    ax.clear()
    step = steps[frame]
    # Determine node colors based on DFS status
    colors = {}
    for node in G.nodes():
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
    node_colors = [colors[node] for node in G.nodes()]

    # Draw the graph with the current DFS state
    nx.draw_networkx(
        G,
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


# Create the animation: interval=1000ms (1 second) per frame
ani = animation.FuncAnimation(fig, update, frames=len(steps), interval=1000, repeat=False)

plt.show()
