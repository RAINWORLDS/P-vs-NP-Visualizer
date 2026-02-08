import numpy as np
import math
import matplotlib.pyplot as plt
from typing import Dict, List, Any

class ComplexityGrowthSimulator:
    
    def __init__(self):
        self.complexity_classes = {}
    
    def calculate_growth(self, n_values):
        n = np.array(n_values)
        
        growth = {
            'O(1)': np.ones_like(n),
            'O(log n)': np.log2(n),
            'O(n)': n,
            'O(n log n)': n * np.log2(n),
            'O(n^2)': n ** 2,
            'O(n^3)': n ** 3,
            'O(2^n)': 2 ** n,
            'O(n!)': [math.factorial(i) if i <= 7 else math.factorial(7) * 2 ** (i - 7) for i in n]
        }
        
        return growth
    
    def generate_complexity_data(self, max_n=20):
        n_values = list(range(1, max_n + 1))
        growth = self.calculate_growth(n_values)
        
        complexity_data = []
        for n in n_values:
            row = {'n': n}
            for complexity, values in growth.items():
                row[complexity] = values[n-1]
            complexity_data.append(row)
        
        return complexity_data
    
    def find_crossover_points(self):
        n = np.array(range(1, 101))
        
        linear = n
        quadratic = n ** 2
        exponential = 2 ** n
        factorial_like = [math.factorial(i) if i <= 10 else math.factorial(10) * 2 ** (i - 10) for i in n]
        
        crossovers = {}
        
        idx = np.where(quadratic > linear * 10)[0]
        crossovers['linear_vs_quadratic'] = n[idx[0]] if len(idx) > 0 else None
        
        idx = np.where(exponential > quadratic * 10)[0]
        crossovers['quadratic_vs_exponential'] = n[idx[0]] if len(idx) > 0 else None
        
        idx = np.where(factorial_like > exponential * 10)[0]
        crossovers['exponential_vs_factorial'] = n[idx[0]] if len(idx) > 0 else None
        
        return crossovers
    
    def simulate_real_world_scenarios(self):
        scenarios = [
            {
                'name': 'Database Search',
                'n': 1000000,
                'complexities': {
                    'O(log n)': 'Binary search (instant)',
                    'O(n)': 'Linear search (seconds)',
                    'O(n^2)': 'Naive search (days)'
                }
            },
            {
                'name': 'Image Processing',
                'n': 1000,
                'complexities': {
                    'O(n)': 'Basic operations (milliseconds)',
                    'O(n^2)': 'Convolution (seconds)',
                    'O(n^3)': '3D processing (minutes)'
                }
            },
            {
                'name': 'Cryptography',
                'n': 256,
                'complexities': {
                    'O(2^n)': 'Brute force key (universe lifetime)',
                    'O(n^3)': 'Factoring (hours with quantum)'
                }
            },
            {
                'name': 'Traveling Salesman',
                'n': 15,
                'complexities': {
                    'O(n!)': 'Exact solution (seconds)',
                    'O(2^n)': 'Dynamic programming (milliseconds)',
                    'O(n^2)': 'Approximation (microseconds)'
                }
            }
        ]
        
        return scenarios
    
    def create_complexity_chart_data(self):
        n = list(range(1, 21))
        
        data = []
        for n_val in n:
            row = {'n': n_val}
            
            if n_val > 0:
                row['log_n'] = math.log2(n_val)
                row['n'] = n_val
                row['n_log_n'] = n_val * math.log2(n_val) if n_val > 0 else 0
                row['n_squared'] = n_val ** 2
                row['n_cubed'] = n_val ** 3
                row['two_pow_n'] = 2 ** n_val
                
                if n_val <= 10:
                    row['factorial'] = math.factorial(n_val)
                else:
                    row['factorial'] = math.factorial(10) * 2 ** (n_val - 10)
            
            data.append(row)
        
        return data
    
    def calculate_practical_limits(self):
        operations_per_second = 10 ** 9
        
        limits = {}
        
        for complexity, func in [
            ('O(n)', lambda n: n),
            ('O(n log n)', lambda n: n * math.log2(n) if n > 0 else 0),
            ('O(n^2)', lambda n: n ** 2),
            ('O(n^3)', lambda n: n ** 3),
            ('O(2^n)', lambda n: 2 ** n),
            ('O(n!)', lambda n: math.factorial(min(n, 20)))
        ]:
            max_n = 1
            for n in range(1, 100):
                if func(n) <= operations_per_second:
                    max_n = n
                else:
                    break
            limits[complexity] = max_n
        
        return limits
