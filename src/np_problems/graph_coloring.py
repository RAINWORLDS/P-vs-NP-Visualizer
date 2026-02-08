import itertools
import random
import time
from typing import List, Tuple, Dict, Set

class GraphColoring:
    
    def __init__(self):
        self.graph = {}
    
    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = set()
        if v not in self.graph:
            self.graph[v] = set()
        
        self.graph[u].add(v)
        self.graph[v].add(u)
    
    def create_random_graph(self, n_nodes=10, edge_prob=0.5):
        self.graph = {i: set() for i in range(n_nodes)}
        
        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                if random.random() < edge_prob:
                    self.graph[i].add(j)
                    self.graph[j].add(i)
        
        return self.graph
    
    def brute_force_coloring(self, k):
        if not self.graph:
            return False, {}, 0
        
        nodes = list(self.graph.keys())
        n = len(nodes)
        steps = 0
        
        for coloring in itertools.product(range(k), repeat=n):
            steps += 1
            valid = True
            
            for i, node in enumerate(nodes):
                for neighbor in self.graph[node]:
                    neighbor_idx = nodes.index(neighbor)
                    if coloring[i] == coloring[neighbor_idx]:
                        valid = False
                        break
                if not valid:
                    break
            
            if valid:
                coloring_dict = {node: coloring[i] for i, node in enumerate(nodes)}
                return True, coloring_dict, steps
        
        return False, {}, steps
    
    def greedy_coloring(self):
        if not self.graph:
            return {}, 0
        
        nodes = list(self.graph.keys())
        coloring = {}
        steps = 0
        
        for node in nodes:
            steps += 1
            used_colors = set()
            
            for neighbor in self.graph[node]:
                if neighbor in coloring:
                    used_colors.add(coloring[neighbor])
            
            for color in range(len(nodes)):
                if color not in used_colors:
                    coloring[node] = color
                    break
        
        return coloring, steps
    
    def backtracking_coloring(self, k):
        if not self.graph:
            return {}, 0
        
        nodes = list(self.graph.keys())
        n = len(nodes)
        coloring = {}
        steps = [0]
        
        def is_safe(node, color):
            for neighbor in self.graph[node]:
                if neighbor in coloring and coloring[neighbor] == color:
                    return False
            return True
        
        def backtrack(idx):
            steps[0] += 1
            
            if idx == n:
                return True
            
            node = nodes[idx]
            for color in range(k):
                if is_safe(node, color):
                    coloring[node] = color
                    if backtrack(idx + 1):
                        return True
                    coloring.pop(node)
            
            return False
        
        result = backtrack(0)
        return coloring if result else {}, steps[0]
    
    def welsh_powell_coloring(self):
        if not self.graph:
            return {}, 0
        
        nodes = list(self.graph.keys())
        steps = 0
        
        degree = {node: len(self.graph[node]) for node in nodes}
        sorted_nodes = sorted(nodes, key=lambda x: degree[x], reverse=True)
        
        coloring = {}
        current_color = 0
        
        while sorted_nodes:
            steps += 1
            node = sorted_nodes.pop(0)
            
            if node not in coloring:
                coloring[node] = current_color
                
                independent_set = [node]
                for other in sorted_nodes:
                    steps += 1
                    if other not in coloring:
                        can_color = True
                        for colored_node in independent_set:
                            if other in self.graph[colored_node]:
                                can_color = False
                                break
                        
                        if can_color:
                            coloring[other] = current_color
                            independent_set.append(other)
                
                for colored_node in independent_set:
                    if colored_node in sorted_nodes:
                        sorted_nodes.remove(colored_node)
                
                current_color += 1
        
        return coloring, steps
    
    def measure_performance(self, k_range=(2, 5), n_nodes=8):
        results = []
        
        for k in range(k_range[0], k_range[1] + 1):
            self.create_random_graph(n_nodes, 0.4)
            
            results_item = {'k': k, 'n_nodes': n_nodes}
            
            start_time = time.time()
            possible_bf, coloring_bf, steps_bf = self.brute_force_coloring(k)
            end_time = time.time()
            results_item['brute_force'] = {
                'time': end_time - start_time,
                'steps': steps_bf,
                'possible': possible_bf,
                'colors_used': len(set(coloring_bf.values())) if possible_bf else 0
            }
            
            start_time = time.time()
            coloring_greedy, steps_greedy = self.greedy_coloring()
            end_time = time.time()
            results_item['greedy'] = {
                'time': end_time - start_time,
                'steps': steps_greedy,
                'colors_used': len(set(coloring_greedy.values())) if coloring_greedy else 0
            }
            
            start_time = time.time()
            coloring_backtrack, steps_backtrack = self.backtracking_coloring(k)
            end_time = time.time()
            results_item['backtracking'] = {
                'time': end_time - start_time,
                'steps': steps_backtrack,
                'possible': len(coloring_backtrack) > 0,
                'colors_used': len(set(coloring_backtrack.values())) if coloring_backtrack else 0
            }
            
            start_time = time.time()
            coloring_wp, steps_wp = self.welsh_powell_coloring()
            end_time = time.time()
            results_item['welsh_powell'] = {
                'time': end_time - start_time,
                'steps': steps_wp,
                'colors_used': len(set(coloring_wp.values())) if coloring_wp else 0
            }
            
            results.append(results_item)
        
        return results
    
    def generate_coloring_instance(self, n_nodes, edge_density=0.3):
        self.create_random_graph(n_nodes, edge_density)
        
        chromatic_number = None
        for k in range(1, n_nodes + 1):
            possible, coloring, _ = self.brute_force_coloring(k)
            if possible:
                chromatic_number = k
                break
        
        return {
            'graph': {k: list(v) for k, v in self.graph.items()},
            'n_nodes': n_nodes,
            'n_edges': sum(len(neighbors) for neighbors in self.graph.values()) // 2,
            'edge_density': edge_density,
            'chromatic_number': chromatic_number
        }
