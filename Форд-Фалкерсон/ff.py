from collections import deque

# Функция для поиска пути с использованием BFS
def bfs(residual_graph, source, sink, parent):
    visited = set()
    queue = deque([source])
    visited.add(source)

    while queue:
        current = queue.popleft()

        for neighbor, capacity in enumerate(residual_graph[current]):
            if neighbor not in visited and capacity > 0:  # Проверяем, что ребро пригодно для прохода
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current
                if neighbor == sink:
                    return True

    return False

# Алгоритм Форда-Фалкерсона
def ford_fulkerson(graph, source, sink):
    n = len(graph)
    residual_graph = [row[:] for row in graph]  # Копируем исходный граф для резидуальной сети
    parent = [-1] * n  # Массив для хранения пути
    max_flow = 0

    # Пока существует путь из истока в сток в резидуальной сети
    while bfs(residual_graph, source, sink, parent):
        # Находим минимальную пропускную способность в найденном пути
        path_flow = float('Inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, residual_graph[parent[s]][s])
            s = parent[s]

        # Обновляем пропускные способности рёбер и обратных рёбер вдоль пути
        v = sink
        while v != source:
            u = parent[v]
            residual_graph[u][v] -= path_flow
            residual_graph[v][u] += path_flow
            v = parent[v]

        max_flow += path_flow

    return max_flow

# Пример использования
graph = [
    [0, 16, 13, 0, 0, 0],
    [0, 0, 10, 12, 0, 0],
    [0, 4, 0, 0, 14, 0],
    [0, 0, 9, 0, 0, 20],
    [0, 0, 0, 7, 0, 4],
    [0, 0, 0, 0, 0, 0]
]
source = 0
sink = 5

print("Максимальный поток:", ford_fulkerson(graph, source, sink))

# Тесты
def test_ford_fulkerson():
    # Тест 1: Простой случай
    graph1 = [
        [0, 8, 0, 0],
        [0, 0, 9, 0],
        [0, 0, 0, 7],
        [0, 0, 0, 0]
    ]
    assert ford_fulkerson(graph1, 0, 3) == 7

    # Тест 2: Граф с несколькими путями
    graph2 = [
        [0, 10, 10, 0, 0, 0],
        [0, 0, 2, 4, 8, 0],
        [0, 0, 0, 0, 9, 0],
        [0, 0, 0, 0, 0, 10],
        [0, 0, 0, 6, 0, 10],
        [0, 0, 0, 0, 0, 0]
    ]
    assert ford_fulkerson(graph2, 0, 5) == 19

    # Тест 3: Граф без пути из истока в сток
    graph3 = [
        [0, 5, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    assert ford_fulkerson(graph3, 0, 3) == 0

    # Тест 4: Петли и избыточные рёбра
    graph4 = [
        [0, 15, 0, 0, 0],
        [0, 0, 12, 0, 0],
        [0, 4, 0, 10, 0],
        [0, 0, 0, 0, 7],
        [0, 0, 0, 0, 0]
    ]
    assert ford_fulkerson(graph4, 0, 4) == 7

    print("Все тесты пройдены успешно!")

test_ford_fulkerson()