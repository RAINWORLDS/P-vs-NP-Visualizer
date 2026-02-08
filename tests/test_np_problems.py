import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import random
from src.np_problems.traveling_salesman import TravelingSalesman
from src.np_problems.sat_solver import SATSolver
from src.np_problems.knapsack import KnapsackSolver
from src.np_problems.subset_sum import SubsetSum
from src.np_problems.graph_coloring import GraphColoring

class TestTravelingSalesman(unittest.TestCase):
    
    def setUp(self):
        self.tsp = TravelingSalesman()
        self.tsp.add_city('A', 0, 0)
        self.tsp.add_city('B', 1, 0)
        self.tsp.add_city('C', 0, 1)
        self.tsp.add_city('D', 1, 1)
    
    def test_distance_calculation(self):
        dist = self.tsp.distance('A', 'B')
        self.assertAlmostEqual(dist, 1.0)
        
        dist = self.tsp.distance('A', 'D')
        self.assertAlmostEqual(dist, 2**0.5)
    
    def test_nearest_neighbor(self):
        path, distance, steps = self.tsp.nearest_neighbor()
        
        self.assertEqual(len(path), 4)
        self.assertGreater(distance, 0)
        self.assertGreater(steps, 0)
        
        all_cities = set(self.tsp.cities.keys())
        path_set = set(path)
        self.assertEqual(all_cities, path_set)
    
    def test_small_tsp_bruteforce(self):
        path, distance, steps = self.tsp.brute_force_tsp()
        
        self.assertIsNotNone(path)
        self.assertGreater(distance, 0)
        self.assertGreater(steps, 0)
    
    def test_random_cities(self):
        self.tsp.create_random_cities(5, 100)
        self.assertEqual(len(self.tsp.cities), 5)
        
        path, distance, steps = self.tsp.nearest_neighbor()
        self.assertEqual(len(path), 5)

class TestSATSolver(unittest.TestCase):
    
    def setUp(self):
        self.sat = SATSolver()
    
    def test_simple_sat(self):
        self.sat.add_clause(['x1'])
        self.sat.add_clause(['x2'])
        
        satisfiable, assignment, steps = self.sat.brute_force_solve()
        
        self.assertTrue(satisfiable)
        self.assertIn('x1', assignment)
        self.assertIn('x2', assignment)
        self.assertGreater(steps, 0)
    
    def test_contradiction(self):
        self.sat.add_clause(['x1'])
        self.sat.add_clause(['-x1'])
        
        satisfiable, assignment, steps = self.sat.brute_force_solve()
        
        self.assertFalse(satisfiable)
        self.assertEqual(steps, 2)
    
    def test_dpll_simple(self):
        self.sat.add_clause(['x1', 'x2'])
        self.sat.add_clause(['-x1', 'x3'])
        
        satisfiable, assignment, steps = self.sat.dpll_solve()
        
        self.assertTrue(satisfiable)
        self.assertGreater(steps, 0)
    
    def test_random_sat_creation(self):
        clauses = self.sat.create_random_sat(5, 10, 3)
        
        self.assertEqual(len(clauses), 10)
        for clause in clauses:
            self.assertLessEqual(len(clause), 3)
            self.assertGreater(len(clause), 0)

class TestKnapsackSolver(unittest.TestCase):
    
    def setUp(self):
        self.knapsack = KnapsackSolver()
        self.knapsack.add_item('A', 10, 60)
        self.knapsack.add_item('B', 20, 100)
        self.knapsack.add_item('C', 30, 120)
    
    def test_bruteforce_knapsack(self):
        capacity = 50
        items, value, weight, steps = self.knapsack.brute_force_knapsack(capacity)
        
        self.assertLessEqual(weight, capacity)
        self.assertGreater(value, 0)
        self.assertGreater(steps, 0)
    
    def test_greedy_value_density(self):
        capacity = 50
        items, value, weight, steps = self.knapsack.greedy_by_value_density(capacity)
        
        self.assertLessEqual(weight, capacity)
        self.assertGreater(value, 0)
        self.assertGreater(steps, 0)
    
    def test_dynamic_programming(self):
        capacity = 50
        items, value, weight, steps = self.knapsack.dynamic_programming_knapsack(capacity)
        
        self.assertLessEqual(weight, capacity)
        self.assertGreater(value, 0)
        self.assertGreater(steps, 0)
    
    def test_random_items(self):
        items = self.knapsack.create_random_items(10, 50, 100)
        self.assertEqual(len(items), 10)
        
        for item in items:
            self.assertIn('name', item)
            self.assertIn('weight', item)
            self.assertIn('value', item)
            self.assertGreater(item['weight'], 0)
            self.assertGreater(item['value'], 0)

class TestSubsetSum(unittest.TestCase):
    
    def setUp(self):
        self.subset_sum = SubsetSum()
        self.numbers = [3, 34, 4, 12, 5, 2]
    
    def test_bruteforce_subset_sum(self):
        target = 9
        self.subset_sum.set_numbers(self.numbers)
        
        found, subset, steps = self.subset_sum.brute_force_subset_sum(target)
        
        self.assertTrue(found)
        self.assertEqual(sum(subset), target)
        self.assertGreater(steps, 0)
    
    def test_no_solution(self):
        target = 1000
        self.subset_sum.set_numbers(self.numbers)
        
        found, subset, steps = self.subset_sum.brute_force_subset_sum(target)
        
        self.assertFalse(found)
        self.assertEqual(len(subset), 0)
    
    def test_dynamic_programming(self):
        target = 9
        self.subset_sum.set_numbers(self.numbers)
        
        found, subset, steps = self.subset_sum.dynamic_programming_subset_sum(target)
        
        self.assertTrue(found)
        self.assertEqual(sum(subset), target)
    
    def test_random_numbers(self):
        numbers = self.subset_sum.create_random_numbers(10, 100)
        self.assertEqual(len(numbers), 10)
        
        for num in numbers:
            self.assertGreater(num, 0)
            self.assertLessEqual(num, 100)

class TestGraphColoring(unittest.TestCase):
    
    def setUp(self):
        self.coloring = GraphColoring()
        self.coloring.add_edge(0, 1)
        self.coloring.add_edge(0, 2)
        self.coloring.add_edge(1, 2)
        self.coloring.add_edge(1, 3)
    
    def test_bruteforce_coloring(self):
        k = 3
        possible, coloring, steps = self.coloring.brute_force_coloring(k)
        
        self.assertTrue(possible)
        self.assertEqual(len(coloring), 4)
        self.assertGreater(steps, 0)
        
        for node in coloring:
            for neighbor in self.coloring.graph[node]:
                self.assertNotEqual(coloring[node], coloring[neighbor])
    
    def test_greedy_coloring(self):
        coloring, steps = self.coloring.greedy_coloring()
        
        self.assertEqual(len(coloring), 4)
        self.assertGreater(steps, 0)
        
        for node in coloring:
            for neighbor in self.coloring.graph[node]:
                self.assertNotEqual(coloring[node], coloring[neighbor])
    
    def test_backtracking_coloring(self):
        k = 3
        coloring, steps = self.coloring.backtracking_coloring(k)
        
        self.assertEqual(len(coloring), 4)
        self.assertGreater(steps, 0)
    
    def test_random_graph(self):
        graph = self.coloring.create_random_graph(10, 0.3)
        self.assertEqual(len(graph), 10)

if __name__ == '__main__':
    unittest.main()
