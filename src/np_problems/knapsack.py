import itertools
import random
import time
from typing import List, Tuple, Dict

class KnapsackSolver:
    
    def __init__(self):
        self.items = []
    
    def add_item(self, name, weight, value):
        self.items.append({'name': name, 'weight': weight, 'value': value})
    
    def create_random_items(self, n_items=10, max_weight=50, max_value=100):
        self.items = []
        for i in range(n_items):
            weight = random.randint(1, max_weight)
            value = random.randint(1, max_value)
            self.items.append({
                'name': f'Item_{i}',
                'weight': weight,
                'value': value
            })
        return self.items
    
    def brute_force_knapsack(self, capacity):
        if not self.items:
            return [], 0, 0, 0
        
        n = len(self.items)
        best_value = 0
        best_combination = None
        steps = 0
        
        for i in range(1 << n):
            steps += 1
            total_weight = 0
            total_value = 0
            
            for j in range(n):
                if i & (1 << j):
                    total_weight += self.items[j]['weight']
                    total_value += self.items[j]['value']
            
            if total_weight <= capacity and total_value > best_value:
                best_value = total_value
                best_combination = i
        
        if best_combination is not None:
            selected_items = []
            for j in range(n):
                if best_combination & (1 << j):
                    selected_items.append(self.items[j])
            return selected_items, best_value, sum(item['weight'] for item in selected_items), steps
        
        return [], 0, 0, steps
    
    def greedy_by_value(self, capacity):
        sorted_items = sorted(self.items, key=lambda x: x['value'], reverse=True)
        
        total_weight = 0
        total_value = 0
        selected = []
        steps = 0
        
        for item in sorted_items:
            steps += 1
            if total_weight + item['weight'] <= capacity:
                selected.append(item)
                total_weight += item['weight']
                total_value += item['value']
        
        return selected, total_value, total_weight, steps
    
    def greedy_by_value_density(self, capacity):
        sorted_items = sorted(self.items, key=lambda x: x['value'] / x['weight'], reverse=True)
        
        total_weight = 0
        total_value = 0
        selected = []
        steps = 0
        
        for item in sorted_items:
            steps += 1
            if total_weight + item['weight'] <= capacity:
                selected.append(item)
                total_weight += item['weight']
                total_value += item['value']
        
        return selected, total_value, total_weight, steps
    
    def dynamic_programming_knapsack(self, capacity):
        n = len(self.items)
        weights = [item['weight'] for item in self.items]
        values = [item['value'] for item in self.items]
        
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        steps = 0
        
        for i in range(1, n + 1):
            for w in range(capacity + 1):
                steps += 1
                if weights[i-1] <= w:
                    dp[i][w] = max(dp[i-1][w], dp[i-1][w-weights[i-1]] + values[i-1])
                else:
                    dp[i][w] = dp[i-1][w]
        
        w = capacity
        selected = []
        for i in range(n, 0, -1):
            steps += 1
            if dp[i][w] != dp[i-1][w]:
                selected.append(self.items[i-1])
                w -= weights[i-1]
        
        selected.reverse()
        total_value = dp[n][capacity]
        total_weight = sum(item['weight'] for item in selected)
        
        return selected, total_value, total_weight, steps
    
    def measure_performance(self, n_items_range=(5, 20), capacity=50):
        results = []
        
        for n_items in range(n_items_range[0], n_items_range[1] + 1):
            self.create_random_items(n_items, 20, 100)
            
            results_item = {'n_items': n_items, 'capacity': capacity}
            
            start_time = time.time()
            selected_bf, value_bf, weight_bf, steps_bf = self.brute_force_knapsack(capacity)
            end_time = time.time()
            results_item['brute_force'] = {
                'time': end_time - start_time,
                'steps': steps_bf,
                'value': value_bf,
                'weight': weight_bf,
                'possible_combinations': 2 ** n_items
            }
            
            start_time = time.time()
            selected_g1, value_g1, weight_g1, steps_g1 = self.greedy_by_value(capacity)
            end_time = time.time()
            results_item['greedy_value'] = {
                'time': end_time - start_time,
                'steps': steps_g1,
                'value': value_g1,
                'weight': weight_g1
            }
            
            start_time = time.time()
            selected_g2, value_g2, weight_g2, steps_g2 = self.greedy_by_value_density(capacity)
            end_time = time.time()
            results_item['greedy_density'] = {
                'time': end_time - start_time,
                'steps': steps_g2,
                'value': value_g2,
                'weight': weight_g2
            }
            
            start_time = time.time()
            selected_dp, value_dp, weight_dp, steps_dp = self.dynamic_programming_knapsack(capacity)
            end_time = time.time()
            results_item['dynamic_programming'] = {
                'time': end_time - start_time,
                'steps': steps_dp,
                'value': value_dp,
                'weight': weight_dp
            }
            
            results.append(results_item)
        
        return results
    
    def generate_knapsack_instance(self, n_items, capacity_multiplier=2):
        total_weight = 0
        items = []
        
        for i in range(n_items):
            weight = random.randint(1, 30)
            value = random.randint(1, 100)
            total_weight += weight
            items.append({
                'name': f'Item_{i}',
                'weight': weight,
                'value': value
            })
        
        capacity = int(total_weight * capacity_multiplier / n_items)
        
        return {
            'items': items,
            'capacity': capacity,
            'total_possible_weight': total_weight
        }
