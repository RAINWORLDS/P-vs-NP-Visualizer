import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import random
from src.p_problems.sorting import SortingAlgorithms
from src.p_problems.searching import SearchingAlgorithms
from src.p_problems.graph_algorithms import GraphAlgorithms

class TestSortingAlgorithms(unittest.TestCase):
    
    def setUp(self):
        self.sorter = SortingAlgorithms()
        self.test_arrays = [
            [],
            [1],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        ]
    
    def test_bubble_sort(self):
        for arr in self.test_arrays:
            with self.subTest(arr=arr):
                sorted_arr, steps = self.sorter.bubble_sort(arr.copy())
                self.assertEqual(sorted(sorted_arr), sorted_arr)
                self.assertGreaterEqual(steps, 0)
    
    def test_quick_sort(self):
        for arr in self.test_arrays:
            with self.subTest(arr=arr):
                sorted_arr, steps = self.sorter.quick_sort(arr.copy())
                self.assertEqual(sorted(arr), sorted_arr)
                self.assertGreaterEqual(steps, 0)
    
    def test_merge_sort(self):
        for arr in self.test_arrays:
            with self.subTest(arr=arr):
                sorted_arr, steps = self.sorter.merge_sort(arr.copy())
                self.assertEqual(sorted(arr), sorted_arr)
                self.assertGreaterEqual(steps, 0)
    
    def test_heap_sort(self):
        for arr in self.test_arrays:
            with self.subTest(arr=arr):
                sorted_arr, steps = self.sorter.heap_sort(arr.copy())
                self.assertEqual(sorted(arr), sorted_arr)
                self.assertGreaterEqual(steps, 0)
    
    def test_sorting_correctness(self):
        arr = [random.randint(1, 100) for _ in range(100)]
        
        methods = [
            self.sorter.bubble_sort,
            self.sorter.quick_sort,
            self.sorter.merge_sort,
            self.sorter.heap_sort
        ]
        
        results = []
        for method in methods:
            sorted_arr, _ = method(arr.copy())
            results.append(sorted_arr)
        
        for i in range(1, len(results)):
            self.assertEqual(results[0], results[i])

class TestSearchingAlgorithms(unittest.TestCase):
    
    def setUp(self):
        self.searcher = SearchingAlgorithms()
        self.sorted_arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        self.unsorted_arr = [19, 3, 15, 7, 11, 1, 17, 9, 13, 5]
    
    def test_linear_search_found(self):
        target = 7
        index, steps = self.searcher.linear_search(self.unsorted_arr, target)
        self.assertEqual(self.unsorted_arr[index], target)
        self.assertGreater(steps, 0)
    
    def test_linear_search_not_found(self):
        target = 100
        index, steps = self.searcher.linear_search(self.unsorted_arr, target)
        self.assertEqual(index, -1)
        self.assertEqual(steps, len(self.unsorted_arr))
    
    def test_binary_search_found(self):
        target = 11
        index, steps = self.searcher.binary_search(self.sorted_arr, target)
        self.assertEqual(self.sorted_arr[index], target)
        self.assertGreater(steps, 0)
    
    def test_binary_search_not_found(self):
        target = 10
        index, steps = self.searcher.binary_search(self.sorted_arr, target)
        self.assertEqual(index, -1)
        self.assertGreater(steps, 0)
    
    def test_binary_search_recursive(self):
        target = 13
        index, steps = self.searcher.binary_search_recursive(self.sorted_arr, target)
        self.assertEqual(self.sorted_arr[index], target)
        self.assertGreater(steps, 0)
    
    def test_interpolation_search(self):
        arr = list(range(0, 100, 2))
        target = 50
        index, steps = self.searcher.interpolation_search(arr, target)
        self.assertEqual(arr[index], target)
        self.assertGreater(steps, 0)
    
    def test_all_search_algorithms(self):
        arr = sorted([random.randint(1, 1000) for _ in range(1000)])
        target = random.choice(arr)
        
        methods = [
            ('linear', lambda: self.searcher.linear_search(arr, target)),
            ('binary', lambda: self.searcher.binary_search(arr, target)),
            ('interpolation', lambda: self.searcher.interpolation_search(arr, target)),
            ('jump', lambda: self.searcher.jump_search(arr, target)),
            ('exponential', lambda: self.searcher.exponential_search(arr, target))
        ]
        
        results = []
        for name, method in methods:
            index, steps = method()
            self.assertEqual(arr[index], target)
            results.append((name, steps))
        
        self.assertLess(results[1][1], results[0][1])

class TestGraphAlgorithms(unittest.TestCase):
    
    def setUp(self):
        self.graph = GraphAlgorithms()
        self.graph.add_edge('A', 'B', 4)
        self.graph.add_edge('A', 'C', 2)
        self.graph.add_edge('B', 'C', 1)
        self.graph.add_edge('B', 'D', 5)
        self.graph.add_edge('C', 'D', 8)
        self.graph.add_edge('C', 'E', 10)
        self.graph.add_edge('D', 'E', 2)
    
    def test_dijkstra(self):
        distances, steps = self.graph.dijkstra('A')
        expected = {
            'A': 0, 'B': 3, 'C': 2, 'D': 8, 'E': 10
        }
        for node in expected:
            self.assertAlmostEqual(distances[node], expected[node])
        self.assertGreater(steps, 0)
    
    def test_bfs_shortest_path(self):
        path, steps = self.graph.bfs_shortest_path('A', 'E')
        self.assertIn('E', path)
        self.assertIn('A', path)
        self.assertGreater(steps, 0)
    
    def test_dfs_path(self):
        path, steps = self.graph.dfs_path('A', 'E')
        self.assertIn('E', path)
        self.assertIn('A', path)
        self.assertGreater(steps, 0)
    
    def test_prim_mst(self):
        mst, steps = self.graph.prim_mst()
        self.assertEqual(len(mst), 5)
        total_weight = sum(weight for neighbors in mst.values() for weight in neighbors.values()) // 2
        self.assertGreater(total_weight, 0)
        self.assertGreater(steps, 0)
    
    def test_kruskal_mst(self):
        mst, steps = self.graph.kruskal_mst()
        self.assertEqual(len(mst), 5)
        total_weight = sum(weight for neighbors in mst.values() for weight in neighbors.values()) // 2
        self.assertGreater(total_weight, 0)
        self.assertGreater(steps, 0)
    
    def test_graph_creation(self):
        self.graph.create_random_graph(10, 0.5)
        self.assertEqual(len(self.graph.adjacency_list), 10)
        
        edge_count = 0
        for neighbors in self.graph.adjacency_list.values():
            edge_count += len(neighbors)
        edge_count //= 2
        
        self.assertGreaterEqual(edge_count, 0)
        self.assertLessEqual(edge_count, 45)

if __name__ == '__main__':
    unittest.main()
