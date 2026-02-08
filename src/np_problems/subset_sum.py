import itertools
import random
import time
from typing import List, Tuple

class SubsetSum:
    
    def __init__(self):
        self.numbers = []
    
    def set_numbers(self, numbers):
        self.numbers = numbers
    
    def create_random_numbers(self, n=10, max_val=100):
        self.numbers = [random.randint(1, max_val) for _ in range(n)]
        return self.numbers
    
    def brute_force_subset_sum(self, target):
        n = len(self.numbers)
        steps = 0
        
        for i in range(1 << n):
            steps += 1
            current_sum = 0
            subset = []
            
            for j in range(n):
                if i & (1 << j):
                    current_sum += self.numbers[j]
                    subset.append(self.numbers[j])
            
            if current_sum == target:
                return True, subset, steps
        
        return False, [], steps
    
    def meet_in_the_middle(self, target):
        n = len(self.numbers)
        if n == 0:
            return False, [], 0
        
        steps = 0
        
        left = self.numbers[:n//2]
        right = self.numbers[n//2:]
        
        left_sums = {0: []}
        for i in range(len(left)):
            new_sums = {}
            steps += 1
            for s, subset in left_sums.items():
                new_sum = s + left[i]
                new_subsets = subset + [left[i]]
                new_sums[new_sum] = new_subsets
            
            left_sums.update(new_sums)
        
        right_sums = {0: []}
        for i in range(len(right)):
            new_sums = {}
            steps += 1
            for s, subset in right_sums.items():
                new_sum = s + right[i]
                new_subsets = subset + [right[i]]
                new_sums[new_sum] = new_subsets
            
            right_sums.update(new_sums)
        
        for left_sum, left_subset in left_sums.items():
            steps += 1
            needed = target - left_sum
            if needed in right_sums:
                full_subset = left_subset + right_sums[needed]
                return True, full_subset, steps
        
        return False, [], steps
    
    def dynamic_programming_subset_sum(self, target):
        n = len(self.numbers)
        dp = [False] * (target + 1)
        dp[0] = True
        steps = 0
        
        for num in self.numbers:
            steps += 1
            for i in range(target, num - 1, -1):
                steps += 1
                if dp[i - num]:
                    dp[i] = True
        
        if not dp[target]:
            return False, [], steps
        
        subset = []
        remaining = target
        for i in range(n - 1, -1, -1):
            steps += 1
            if remaining >= self.numbers[i] and dp[remaining - self.numbers[i]]:
                subset.append(self.numbers[i])
                remaining -= self.numbers[i]
        
        return True, subset, steps
    
    def measure_performance(self, n_range=(5, 20)):
        results = []
        
        for n in range(n_range[0], n_range[1] + 1):
            self.create_random_numbers(n, 100)
            target = sum(random.sample(self.numbers, max(1, n//3)))
            
            results_item = {'n': n, 'target': target}
            
            start_time = time.time()
            found_bf, subset_bf, steps_bf = self.brute_force_subset_sum(target)
            end_time = time.time()
            results_item['brute_force'] = {
                'time': end_time - start_time,
                'steps': steps_bf,
                'found': found_bf,
                'possible_subsets': 2 ** n
            }
            
            start_time = time.time()
            found_mitm, subset_mitm, steps_mitm = self.meet_in_the_middle(target)
            end_time = time.time()
            results_item['meet_in_middle'] = {
                'time': end_time - start_time,
                'steps': steps_mitm,
                'found': found_mitm
            }
            
            start_time = time.time()
            found_dp, subset_dp, steps_dp = self.dynamic_programming_subset_sum(target)
            end_time = time.time()
            results_item['dynamic_programming'] = {
                'time': end_time - start_time,
                'steps': steps_dp,
                'found': found_dp
            }
            
            results.append(results_item)
        
        return results
    
    def generate_subset_sum_instance(self, n, difficulty='medium'):
        if difficulty == 'easy':
            max_val = 20
            numbers = [random.randint(1, max_val) for _ in range(n)]
            subset = random.sample(numbers, max(1, n//2))
            target = sum(subset)
        elif difficulty == 'hard':
            max_val = 1000
            numbers = [random.randint(1, max_val) for _ in range(n)]
            target = sum(numbers) + 1
        else:
            max_val = 100
            numbers = [random.randint(1, max_val) for _ in range(n)]
            subset = random.sample(numbers, max(1, n//3))
            target = sum(subset)
        
        return {
            'numbers': numbers,
            'target': target,
            'n': n,
            'difficulty': difficulty,
            'has_solution': difficulty != 'hard'
        }
