import random
import math
import numpy as np
from typing import List, Dict, Any

class QuantumPvsNPSimulation:
    
    def __init__(self):
        self.results = []
    
    def grovers_algorithm_simulation(self, n_qubits):
        if n_qubits > 10:
            n_qubits = 10
        
        classical_steps = 2 ** n_qubits
        quantum_steps = int(math.sqrt(2 ** n_qubits))
        
        speedup = classical_steps / quantum_steps
        
        return {
            'n_qubits': n_qubits,
            'classical_steps': classical_steps,
            'quantum_steps': quantum_steps,
            'speedup': speedup,
            'search_space': 2 ** n_qubits
        }
    
    def simulate_quantum_annealing(self, problem_size, temperature=1.0, steps=100):
        current_state = [random.choice([-1, 1]) for _ in range(problem_size)]
        current_energy = self.calculate_energy(current_state)
        
        best_state = current_state.copy()
        best_energy = current_energy
        
        energies = [current_energy]
        
        for step in range(steps):
            new_state = current_state.copy()
            flip_index = random.randint(0, problem_size - 1)
            new_state[flip_index] *= -1
            
            new_energy = self.calculate_energy(new_state)
            
            delta_energy = new_energy - current_energy
            
            if delta_energy < 0:
                current_state = new_state
                current_energy = new_energy
                
                if new_energy < best_energy:
                    best_state = new_state.copy()
                    best_energy = new_energy
            else:
                probability = math.exp(-delta_energy / temperature)
                if random.random() < probability:
                    current_state = new_state
                    current_energy = new_energy
            
            temperature *= 0.99
            energies.append(current_energy)
        
        return {
            'problem_size': problem_size,
            'best_energy': best_energy,
            'steps': steps,
            'energies': energies,
            'final_state': best_state
        }
    
    def calculate_energy(self, state):
        energy = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                interaction = random.uniform(-1, 1)
                energy += -interaction * state[i] * state[j]
        return energy
    
    def quantum_fourier_sim(self, n_bits):
        size = 2 ** n_bits
        
        input_state = [complex(random.random(), random.random()) for _ in range(size)]
        norm = math.sqrt(sum(abs(x) ** 2 for x in input_state))
        input_state = [x / norm for x in input_state]
        
        output_state = self.qft_simulate(input_state)
        
        return {
            'n_bits': n_bits,
            'input_state_magnitude': [abs(x) for x in input_state],
            'output_state_magnitude': [abs(x) for x in output_state],
            'size': size
        }
    
    def qft_simulate(self, state):
        n = len(state)
        output = [0] * n
        
        for k in range(n):
            total = 0
            for j in range(n):
                angle = 2 * math.pi * j * k / n
                total += state[j] * complex(math.cos(angle), -math.sin(angle))
            output[k] = total / math.sqrt(n)
        
        return output
    
    def simulate_shors_algorithm(self, n_to_factor):
        if n_to_factor < 2:
            return {'error': 'Number too small'}
        
        factors = []
        temp_n = n_to_factor
        
        for i in range(2, int(math.sqrt(temp_n)) + 1):
            while temp_n % i == 0:
                factors.append(i)
                temp_n //= i
        
        if temp_n > 1:
            factors.append(temp_n)
        
        classical_time = n_to_factor ** 0.5
        quantum_time = (math.log(n_to_factor)) ** 3
        
        return {
            'number': n_to_factor,
            'factors': factors,
            'classical_time_estimate': classical_time,
            'quantum_time_estimate': quantum_time,
            'speedup': classical_time / quantum_time if quantum_time > 0 else float('inf')
        }
    
    def compare_quantum_classical(self, max_problem_size=10):
        comparisons = []
        
        for n in range(2, max_problem_size + 1):
            grover = self.grovers_algorithm_simulation(n)
            shor = self.simulate_shors_algorithm(2 ** n)
            
            comparison = {
                'problem_size': n,
                'grovers_speedup': grover['speedup'],
                'shors_speedup': shor['speedup'],
                'quantum_advantage': max(grover['speedup'], shor.get('speedup', 1)),
                'search_space': 2 ** n
            }
            
            comparisons.append(comparison)
        
        return comparisons
    
    def create_quantum_report(self):
        grover_data = self.grovers_algorithm_simulation(8)
        annealing_data = self.simulate_quantum_annealing(20)
        shor_data = self.simulate_shors_algorithm(15)
        comparisons = self.compare_quantum_classical(8)
        
        report = {
            'grovers_algorithm': grover_data,
            'quantum_annealing': annealing_data,
            'shors_algorithm': shor_data,
            'comparisons': comparisons,
            'insights': [
                'Quantum provides quadratic speedup for unstructured search',
                'Exponential speedup possible for specific problems',
                'Quantum annealing useful for optimization',
                'P vs NP question changes in quantum context'
            ]
        }
        
        return report
