import heapq
import time
from typing import Dict, List, Tuple, Set, Any
import random

class GraphAlgorithms:
    
    def __init__(self):
        self.adjacency_list = {}
    
    def add_edge(self, u, v, weight=1):
        if u not in self.adjacency_list:
            self.adjacency_list[u] = {}
        if v not in self.adjacency_list:
            self.adjacency_list[v] = {}
        
        self.adjacency_list[u][v] = weight
        self.adjacency_list[v][u] = weight
    
    def create_random_graph(self, nodes=10, edge_probability=0.5):
        self.adjacency_list = {}
        
        for i in range(nodes):
            self.adjacency_list[i] = {}
            for j in range(i+1, nodes):
                if random.random() < edge_probability:
                    weight = random.randint(1, 20)
                    self.adjacency_list[i][j] = weight
                    self.adjacency_list[j][i] = weight
        
        return self.adjacency_list
    
    def dijkstra(self, start):
        if start not in self.adjacency_list:
            return {}, 0
        
        distances = {node: float('inf') for node in self.adjacency_list}
        distances[start] = 0
        priority_queue = [(0, start)]
        steps = 0
        
        while priority_queue:
            steps += 1
            current_distance, current_node = heapq.heappop(priority_queue)
            
            if current_distance > distances[current_node]:
                continue
            
            for neighbor, weight in self.adjacency_list[current_node].items():
                steps += 1
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
        
        return distances, steps
    
    def bellman_ford(self, start):
        if start not in self.adjacency_list:
            return {}, 0
        
        nodes = list(self.adjacency_list.keys())
        edges = []
        
        for u in self.adjacency_list:
            for v, weight in self.adjacency_list[u].items():
                edges.append((u, v, weight))
        
        distances = {node: float('inf') for node in nodes}
        distances[start] = 0
        steps = 0
        
        for _ in range(len(nodes) - 1):
            for u, v, weight in edges:
                steps += 1
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
        
        for u, v, weight in edges:
            steps += 1
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                return None, steps
        
        return distances, steps
    
    def floyd_warshall(self):
        nodes = list(self.adjacency_list.keys())
        n = len(nodes)
        node_index = {node: i for i, node in enumerate(nodes)}
        
        dist = [[float('inf')] * n for _ in range(n)]
        
        for i in range(n):
            dist[i][i] = 0
        
        for u in self.adjacency_list:
            for v, weight in self.adjacency_list[u].items():
                i, j = node_index[u], node_index[v]
                dist[i][j] = weight
        
        steps = 0
        
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    steps += 1
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        
        result = {}
        for i, node_i in enumerate(nodes):
            result[node_i] = {}
            for j, node_j in enumerate(nodes):
                result[node_i][node_j] = dist[i][j]
        
        return result, steps
    
    def prim_mst(self):
        if not self.adjacency_list:
            return {}, 0
        
        start_node = list(self.adjacency_list.keys())[0]
        mst = {}
        visited = {start_node}
        edges = []
        steps = 0
        
        for neighbor, weight in self.adjacency_list[start_node].items():
            heapq.heappush(edges, (weight, start_node, neighbor))
        
        while edges and len(visited) < len(self.adjacency_list):
            steps += 1
            weight, u, v = heapq.heappop(edges)
            
            if v not in visited:
                visited.add(v)
                if u not in mst:
                    mst[u] = {}
                mst[u][v] = weight
                if v not in mst:
                    mst[v] = {}
                mst[v][u] = weight
                
                for neighbor, w in self.adjacency_list[v].items():
                    if neighbor not in visited:
                        heapq.heappush(edges, (w, v, neighbor))
        
        return mst, steps
    
    def kruskal_mst(self):
        if not self.adjacency_list:
            return {}, 0
        
        edges = []
        for u in self.adjacency_list:
            for v, weight in self.adjacency_list[u].items():
                if u < v:
                    edges.append((weight, u, v))
        
        edges.sort()
        
        parent = {}
        rank = {}
        
        def find(node):
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]
        
        def union(u, v):
            root_u = find(u)
            root_v = find(v)
            
            if root_u != root_v:
                if rank[root_u] > rank[root_v]:
                    parent[root_v] = root_u
                elif rank[root_u] < rank[root_v]:
                    parent[root_u] = root_v
                else:
                    parent[root_v] = root_u
                    rank[root_u] += 1
                return True
            return False
        
        for node in self.adjacency_list:
            parent[node] = node
            rank[node] = 0
        
        mst = {}
        steps = 0
        
        for weight, u, v in edges:
            steps += 1
            if union(u, v):
                if u not in mst:
                    mst[u] = {}
                if v not in mst:
                    mst[v] = {}
                mst[u][v] = weight
                mst[v][u] = weight
        
        return mst, steps
    
    def bfs_shortest_path(self, start, end):
        if start not in self.adjacency_list or end not in self.adjacency_list:
            return None, 0
        
        visited = {start}
        queue = [(start, [start])]
        steps = 0
        
        while queue:
            steps += 1
            current, path = queue.pop(0)
            
            if current == end:
                return path, steps
            
            for neighbor in self.adjacency_list[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None, steps
    
    def dfs_path(self, start, end):
        if start not in self.adjacency_list or end not in self.adjacency_list:
            return None, 0
        
        visited = set()
        steps = [0]
        
        def dfs_recursive(current, path):
            steps[0] += 1
            visited.add(current)
            
            if current == end:
                return path
            
            for neighbor in self.adjacency_list[current]:
                if neighbor not in visited:
                    result = dfs_recursive(neighbor, path + [neighbor])
                    if result:
                        return result
            
            return None
        
        result = dfs_recursive(start, [start])
        return result, steps[0]
    
    def measure_performance(self, algorithm_name, graph_size=50):
        self.create_random_graph(graph_size, 0.3)
        
        algorithms = {
            'dijkstra': lambda: self.dijkstra(0),
            'bellman_ford': lambda: self.bellman_ford(0),
            'floyd_warshall': self.floyd_warshall,
            'prim_mst': self.prim_mst,
            'kruskal_mst': self.kruskal_mst
        }
        
        if algorithm_name not in algorithms:
            return None
        
        start_time = time.time()
        result, steps = algorithms[algorithm_name]()
        end_time = time.time()
        
        return {
            'algorithm': algorithm_name,
            'graph_size': graph_size,
            'time': end_time - start_time,
            'steps': steps,
            'result_size': len(str(result))
        }
