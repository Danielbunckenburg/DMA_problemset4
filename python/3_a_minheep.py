import random
import matplotlib.pyplot as plt
import networkx as nx


class MinHeap:
    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2

    def left(self, i):
        return 2 * i + 1

    def right(self, i):
        return 2 * i + 2

    def insert(self, key):
        # Append the new key at the end and sift it up to maintain the heap property
        self.heap.append(key)
        i = len(self.heap) - 1
        while i != 0 and self.heap[self.parent(i)] > self.heap[i]:
            self.heap[i], self.heap[self.parent(i)] = self.heap[self.parent(i)], self.heap[i]
            i = self.parent(i)

    def heapify(self, i):
        l = self.left(i)
        r = self.right(i)
        smallest = i

        if l < len(self.heap) and self.heap[l] < self.heap[smallest]:
            smallest = l
        if r < len(self.heap) and self.heap[r] < self.heap[smallest]:
            smallest = r

        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self.heapify(smallest)

    def extract_min(self):
        if not self.heap:
            return None  # or raise an exception if preferred
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify(0)
        return root

    def get_min(self):
        return self.heap[0] if self.heap else None

    def draw(self):
        """Visualizes the heap as a binary tree using networkx and matplotlib."""
        if not self.heap:
            print("Heap is empty. Nothing to draw.")
            return

        G = nx.DiGraph()
        # Add nodes and edges according to the heap list
        for i, val in enumerate(self.heap):
            G.add_node(i, label=str(val))
            left_index = self.left(i)
            right_index = self.right(i)
            if left_index < len(self.heap):
                G.add_edge(i, left_index)
            if right_index < len(self.heap):
                G.add_edge(i, right_index)

        # Compute positions for a binary tree layout
        pos = {}

        def assign_pos(index, depth, x_min, x_max):
            if index >= len(self.heap):
                return
            x = (x_min + x_max) / 2
            pos[index] = (x, -depth)  # Negative depth to have the root at the top
            assign_pos(self.left(index), depth + 1, x_min, x)
            assign_pos(self.right(index), depth + 1, x, x_max)

        assign_pos(0, 0, 0, 1)

        # Create labels dictionary for nodes
        labels = {i: self.heap[i] for i in range(len(self.heap))}
        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, labels=labels, node_size=800, node_color='lightblue', arrows=False)
        plt.title("Min Heap Visualization")
        plt.show()


# Example usage:
if __name__ == "__main__":
    # Ask the user for the number of random elements to generate
    n = int(input("Enter the number of elements to generate: "))
    # Generate n random integers between 1 and 100
    random_elements = [random.randint(1, 100) for _ in range(n)]
    print("Generated elements:", random_elements)

    # Create the min heap and insert each random element
    min_heap = MinHeap()
    for el in random_elements:
        min_heap.insert(el)
        print(f"Inserted {el}: Heap = {min_heap.heap}")

    # Draw the min heap as a binary tree
    print("\nHeap drawn as a binary tree:")
    min_heap.draw()

    # Extract and print elements in sorted order (heap sort)
    print("\nExtracting elements in sorted order:")
    sorted_elements = []
    while min_heap.heap:
        sorted_elements.append(min_heap.extract_min())
    print(sorted_elements)
