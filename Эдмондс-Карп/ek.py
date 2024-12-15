from collections import deque

def bfs(residual_graph, source, sink, parent):
    """Поиск пути увеличения с использованием BFS."""
    n = len(residual_graph)
    visited = [False] * n
    queue = deque([source])
    visited[source] = True

    while queue:
        current = queue.popleft()
        for neighbor, capacity in enumerate(residual_graph[current]):
            if not visited[neighbor] and capacity > 0:  # Ребро пригодно для прохода
                parent[neighbor] = current
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)

    return False

def edmonds_karp(graph, source, sink):
    """Алгоритм Эдмондса-Карпа для нахождения максимального потока."""
    n = len(graph)
    residual_graph = [row[:] for row in graph]  # Копия исходного графа
    parent = [-1] * n  # Массив для восстановления пути
    max_flow = 0

    while bfs(residual_graph, source, sink, parent):
        # Определяем минимальную пропускную способность вдоль пути
        path_flow = float('Inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, residual_graph[u][v])
            v = parent[v]

        # Обновляем пропускные способности в резидуальном графе
        v = sink
        while v != source:
            u = parent[v]
            residual_graph[u][v] -= path_flow
            residual_graph[v][u] += path_flow
            v = parent[v]

        max_flow += path_flow

    return max_flow

# Тесты
if __name__ == "__main__":
    def run_tests():
        """Тестирование алгоритма Эдмондса-Карпа."""
        test_cases = [
            {
                "graph": [
                    [0, 16, 13, 0, 0, 0],
                    [0, 0, 10, 12, 0, 0],
                    [0, 4, 0, 0, 14, 0],
                    [0, 0, 9, 0, 0, 20],
                    [0, 0, 0, 7, 0, 4],
                    [0, 0, 0, 0, 0, 0],
                ],
                "source": 0,
                "sink": 5,
                "expected": 23,
            },
            {
                "graph": [
                    [0, 10, 10, 0, 0, 0],
                    [0, 0, 2, 4, 8, 0],
                    [0, 0, 0, 0, 9, 0],
                    [0, 0, 0, 0, 0, 10],
                    [0, 0, 0, 6, 0, 10],
                    [0, 0, 0, 0, 0, 0],
                ],
                "source": 0,
                "sink": 5,
                "expected": 19,
            },
        ]

        for i, test in enumerate(test_cases):
            graph = test["graph"]
            source = test["source"]
            sink = test["sink"]
            expected = test["expected"]
            result = edmonds_karp(graph, source, sink)
            assert result == expected, f"Test case {i+1} failed: expected {expected}, got {result}"

        print("All test cases passed!")

    run_tests()
