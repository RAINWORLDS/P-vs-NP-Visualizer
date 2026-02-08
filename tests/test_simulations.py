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
    
    def setUp(self):
        self.simulator = ComplexityGrowthSimulator()
    
    def test_calculate_growth(self):
        n_values = [1, 2, 5, 10]
        growth = self.simulator.calculate_growth(n_values)
        
        expected_classes = ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)', 
                           'O(n^2)', 'O(n^3)', 'O(2^n)', 'O(n!)']
        
        for cls in expected_classes:
            self.assertIn(cls, growth)
            self.assertEqual(len(growth[cls]), len(n_values))
    
    def test_generate_complexity_data(self):
        data = self.simulator.generate_complexity_data(5)
        
        self.assertEqual(len(data), 5)
        for row in data:
            self.assertIn('n', row)
            self.assertIn('O(1)', row)
            self.assertIn('O(2^n)', row)
    
    def test_find_crossover_points(self):
        crossovers = self.simulator.find_crossover_points()
        
        self.assertIsInstance(crossovers, dict)
        for key in ['linear_vs_quadratic', 'quadratic_vs_exponential', 
                   'exponential_vs_factorial']:
            self.assertIn(key, crossovers)
    
    def test_simulate_real_world_scenarios(self):
        scenarios = self.simulator.simulate_real_world_scenarios()
        
        self.assertGreater(len(scenarios), 0)
        for scenario in scenarios:
            self.assertIn('name', scenario)
            self.assertIn('n', scenario)
            self.assertIn('complexities', scenario)
    
    def test_calculate_practical_limits(self):
        limits = self.simulator.calculate_practical_limits()
        
        expected_classes = ['O(n)', 'O(n log n)', 'O(n^2)', 
                           'O(n^3)', 'O(2^n)', 'O(n!)']
        
        for cls in expected_classes:
            self.assertIn(cls, limits)
            self.assertGreater(limits[cls], 0)

class TestQuantumPvsNPSimulation(unittest.TestCase):
    
    def setUp(self):
        self.quantum_sim = QuantumPvsNPSimulation()
    
    def test_grovers_algorithm_simulation(self):
        for n_qubits in [2, 4, 6]:
            result = self.quantum_sim.grovers_algorithm_simulation(n_qubits)
            
            self.assertIn('n_qubits', result)
            self.assertIn('classical_steps', result)
            self.assertIn('quantum_steps', result)
            self.assertIn('speedup', result)
            self.assertIn('search_space', result)
            
            self.assertEqual(result['n_qubits'], n_qubits)
            self.assertEqual(result['search_space'], 2 ** n_qubits)
            self.assertGreater(result['speedup'], 1)
    
    def test_simulate_quantum_annealing(self):
        result = self.quantum_sim.simulate_quantum_annealing(10)
        
        self.assertIn('problem_size', result)
        self.assertIn('best_energy', result)
        self.assertIn('steps', result)
        self.assertIn('energies', result)
        self.assertIn('final_state', result)
        
        self.assertEqual(result['problem_size'], 10)
        self.assertGreater(len(result['energies']), 0)
        self.assertEqual(len(result['final_state']), 10)
    
    def test_quantum_fourier_sim(self):
        for n_bits in [2, 3, 4]:
            result = self.quantum_sim.quantum_fourier_sim(n_bits)
            
            self.assertIn('n_bits', result)
            self.assertIn('input_state_magnitude', result)
            self.assertIn('output_state_magnitude', result)
            self.assertIn('size', result)
            
            self.assertEqual(result['n_bits'], n_bits)
            self.assertEqual(result['size'], 2 ** n_bits)
            self.assertEqual(len(result['input_state_magnitude']), 2 ** n_bits)
    
    def test_simulate_shors_algorithm(self):
        test_cases = [6, 15, 21]
        
        for num in test_cases:
            result = self.quantum_sim.simulate_shors_algorithm(num)
            
            self.assertIn('number', result)
            self.assertIn('factors', result)
            
            product = 1
            for factor in result['factors']:
                product *= factor
            
            self.assertEqual(product, num)
            
            if num > 2:
                self.assertIn('classical_time_estimate', result)
                self.assertIn('quantum_time_estimate', result)
                self.assertIn('speedup', result)
    
    def test_compare_quantum_classical(self):
        comparisons = self.quantum_sim.compare_quantum_classical(5)
        
        self.assertGreater(len(comparisons), 0)
        for comp in comparisons:
            self.assertIn('problem_size', comp)
            self.assertIn('grovers_speedup', comp)
            self.assertIn('shors_speedup', comp)
            self.assertIn('quantum_advantage', comp)
            self.assertIn('search_space', comp)

if __name__ == '__main__':
    unittest.main()
