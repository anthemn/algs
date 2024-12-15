from collections import deque, defaultdict

class Dinic:
    def __init__(self, n):
        self.n = n  # number of vertices
        self.graph = defaultdict(list)  # adjacency list for the graph
        self.capacity = {}  # residual capacities of edges

    def add_edge(self, u, v, cap):
        """Add an edge to the graph with capacity cap."""
        self.graph[u].append(v)
        self.graph[v].append(u)
        self.capacity[(u, v)] = cap
        self.capacity[(v, u)] = 0  # reverse edge with 0 initial capacity

    def bfs(self, source, sink):
        """Build level graph using BFS."""
        self.level = [-1] * self.n
        self.level[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in self.graph[u]:
                if self.level[v] == -1 and self.capacity[(u, v)] > 0:
                    self.level[v] = self.level[u] + 1
                    queue.append(v)
        return self.level[sink] != -1

    def dfs(self, u, sink, flow):
        """Send flow along augmenting paths using DFS."""
        if u == sink:
            return flow
        for v in self.graph[u]:
            if self.level[v] == self.level[u] + 1 and self.capacity[(u, v)] > 0:
                min_flow = min(flow, self.capacity[(u, v)])
                pushed = self.dfs(v, sink, min_flow)
                if pushed > 0:
                    self.capacity[(u, v)] -= pushed
                    self.capacity[(v, u)] += pushed
                    return pushed
        return 0

    def max_flow(self, source, sink):
        """Find the maximum flow from source to sink."""
        total_flow = 0
        while self.bfs(source, sink):
            flow = float('inf')
            while flow:
                flow = self.dfs(source, sink, float('inf'))
                total_flow += flow
        return total_flow

# Testing the implementation
def run_tests():
    # Test case 1
    n = 6
    dinic = Dinic(n)
    edges = [
        (0, 1, 10),
        (0, 2, 10),
        (1, 3, 4),
        (1, 4, 8),
        (1, 2, 2),
        (2, 4, 9),
        (3, 5, 10),
        (4, 3, 6),
        (4, 5, 10)
    ]
    for u, v, cap in edges:
        dinic.add_edge(u, v, cap)
    assert dinic.max_flow(0, 5) == 19, "Test case 1 failed"

    # Test case 2
    n = 4
    dinic = Dinic(n)
    edges = [
        (0, 1, 1000),
        (1, 2, 1),
        (2, 3, 1000)
    ]
    for u, v, cap in edges:
        dinic.add_edge(u, v, cap)
    assert dinic.max_flow(0, 3) == 1, "Test case 2 failed"

    # Test case 3
    n = 5
    dinic = Dinic(n)
    edges = [
        (0, 1, 10),
        (0, 2, 5),
        (1, 2, 15),
        (1, 3, 10),
        (2, 4, 10),
        (3, 4, 10)
    ]
    for u, v, cap in edges:
        dinic.add_edge(u, v, cap)
    assert dinic.max_flow(0, 4) == 15, "Test case 3 failed"

    print("All test cases passed!")

if __name__ == "__main__":
    run_tests()
