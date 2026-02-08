import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import math
from src.simulations.p_equals_np import PEqualsNPSimulation
from src.simulations.complexity_growth import ComplexityGrowthSimulator
from src.simulations.quantum_simulation import QuantumPvsNPSimulation

class TestPEqualsNPSimulation(unittest.TestCase):
    
    def setUp(self):
        self.simulator = PEqualsNPSimulation()
    
    def test_simulate_p_time(self):
        for size in [10, 100, 1000]:
            time_taken = self.simulator.simulate_p_time(size)
            self.assertGreaterEqual(time_taken, 0)
            self.assertLess(time_taken, 10)
    
    def test_simulate_np_time(self):
        for size in [5, 10, 15]:
            time_taken = self.simulator.simulate_np_time(size, 'bruteforce')
            self.assertGreaterEqual(time_taken, 0)
    
    def test_simulate_if_p_equals_np(self):
        result = self.simulator.simulate_if_p_equals_np(10)
        
        self.assertIn('problem_size', result)
        self.assertIn('current_np_time', result)
        self.assertIn('if_p_equals_np_time', result)
        self.assertIn('current_p_time', result)
        self.assertIn('speedup_factor', result)
        
        self.assertGreaterEqual(result['current_np_time'], 0)
        self.assertGreaterEqual(result['if_p_equals_np_time'], 0)
        self.assertGreaterEqual(result['current_p_time'], 0)
        self.assertGreaterEqual(result['speedup_factor'], 0)
    
    def test_run_comparison(self):
        results = self.simulator.run_comparison(10)
        
        self.assertGreater(len(results), 0)
        for result in results:
            self.assertIn('problem_size', result)
            self.assertGreater(result['problem_size'], 0)
    
    def test_calculate_impact_areas(self):
        impact_areas = self.simulator.calculate_impact_areas()
        
        self.assertIn('cryptography', impact_areas)
        self.assertIn('optimization', impact_areas)
        self.assertIn('artificial_intelligence', impact_areas)
        
        for area, info in impact_areas.items():
            self.assertIn('current', info)
            self.assertIn('if_p_equals_np', info)
            self.assertIn('impact', info)

class TestComplexityGrowthSimulator(unittest.TestCase):
    
    def
