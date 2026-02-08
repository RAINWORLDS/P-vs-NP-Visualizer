import time
import random
from typing import List, Tuple, Optional
import bisect

class SearchingAlgorithms:
    
    def linear_search(self, arr, target):
        steps = 0
        for i, element in enumerate(arr):
            steps += 1
            if element == target:
                return i, steps
        return -1, steps
    
    def binary_search(self, arr, target):
        steps = 0
        left, right = 0, len(arr) - 1
        
        while left <= right:
            steps += 1
            mid = (left + right) // 2
            
            if arr[mid] == target:
                return mid, steps
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return -1, steps
    
    def binary_search_recursive(self, arr, target, left=0, right=None, steps=[0]):
        if right is None:
            right = len(arr) - 1
        
        steps[0] += 1
        
        if left > right:
            return -1, steps[0]
        
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid, steps[0]
        elif arr[mid] < target:
            return self.binary_search_recursive(arr, target, mid + 1, right, steps)
        else:
            return self.binary_search_recursive(arr, target, left, mid - 1, steps)
    
    def interpolation_search(self, arr, target):
        steps = 0
        left, right = 0, len(arr) - 1
        
        while left <= right and target >= arr[left] and target <= arr[right]:
            steps += 1
            
            if left == right:
                if arr[left] == target:
                    return left, steps
                return -1, steps
            
            pos = left + ((target - arr[left]) * (right - left)) // (arr[right] - arr[left])
            
            if arr[pos] == target:
                return pos, steps
            elif arr[pos] < target:
                left = pos + 1
            else:
                right = pos - 1
        
        return -1, steps
    
    def jump_search(self, arr, target):
        steps = 0
        n = len(arr)
        step = int(n ** 0.5)
        prev = 0
        
        while arr[min(step, n) - 1] < target:
            steps += 1
            prev = step
            step += int(n ** 0.5)
            if prev >= n:
                return -1, steps
        
        while arr[prev] < target:
            steps += 1
            prev += 1
            if prev == min(step, n):
                return -1, steps
        
        steps += 1
        if arr[prev] == target:
            return prev, steps
        return -1, steps
    
    def exponential_search(self, arr, target):
        steps = 0
        
        if arr[0] == target:
            steps += 1
            return 0, steps
        
        n = len(arr)
        i = 1
        while i < n and arr[i] <= target:
            steps += 1
            i *= 2
        
        left = i // 2
        right = min(i, n - 1)
        
        result, sub_steps = self.binary_search(arr[left:right+1], target)
        steps += sub_steps
        
        if result != -1:
            return left + result, steps
        return -1, steps
    
    def create_search_performance_data(self, size=1000):
        arr = sorted([random.randint(1, 10000) for _ in range(size)])
        target = random.choice(arr)
        
        results = {}
        
        search_methods = {
            'linear_search': self.linear_search,
            'binary_search': self.binary_search,
            'interpolation_search': self.interpolation_search,
            'jump_search': self.jump_search,
            'exponential_search': self.exponential_search
        }
        
        for name, method in search_methods.items():
            start_time = time.time()
            index, steps = method(arr.copy(), target)
            end_time = time.time()
            
            results[name] = {
                'found': index != -1,
                'index': index,
                'steps': steps,
                'time': end_time - start_time,
                'target': target
            }
        
        return results
