import time
import random
from typing import List, Tuple
import heapq

class SortingAlgorithms:
    
    def bubble_sort(self, arr):
        n = len(arr)
        steps = 0
        for i in range(n):
            for j in range(0, n-i-1):
                steps += 1
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr, steps
    
    def quick_sort(self, arr):
        steps = [0]
        
        def partition(low, high):
            pivot = arr[high]
            i = low - 1
            
            for j in range(low, high):
                steps[0] += 1
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            
            arr[i+1], arr[high] = arr[high], arr[i+1]
            return i + 1
        
        def quick_sort_recursive(low, high):
            if low < high:
                pi = partition(low, high)
                quick_sort_recursive(low, pi-1)
                quick_sort_recursive(pi+1, high)
        
        quick_sort_recursive(0, len(arr)-1)
        return arr, steps[0]
    
    def merge_sort(self, arr):
        steps = [0]
        
        def merge(left, right):
            result = []
            i = j = 0
            
            while i < len(left) and j < len(right):
                steps[0] += 1
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            
            result.extend(left[i:])
            result.extend(right[j:])
            return result
        
        def merge_sort_recursive(arr):
            if len(arr) <= 1:
                return arr
            
            mid = len(arr) // 2
            left = merge_sort_recursive(arr[:mid])
            right = merge_sort_recursive(arr[mid:])
            
            return merge(left, right)
        
        sorted_arr = merge_sort_recursive(arr)
        return sorted_arr, steps[0]
    
    def heap_sort(self, arr):
        steps = 0
        heapq.heapify(arr)
        steps += len(arr)
        
        result = []
        while arr:
            steps += 1
            result.append(heapq.heappop(arr))
        
        return result, steps
    
    def measure_performance(self, algorithm, arr_size=1000):
        arr = [random.randint(1, 10000) for _ in range(arr_size)]
        
        algorithms = {
            'bubble_sort': self.bubble_sort,
            'quick_sort': self.quick_sort,
            'merge_sort': self.merge_sort,
            'heap_sort': self.heap_sort
        }
        
        if algorithm not in algorithms:
            return None
        
        arr_copy = arr.copy()
        start_time = time.time()
        sorted_arr, steps = algorithms[algorithm](arr_copy)
        end_time = time.time()
        
        is_sorted = all(sorted_arr[i] <= sorted_arr[i+1] for i in range(len(sorted_arr)-1))
        
        return {
            'algorithm': algorithm,
            'size': arr_size,
            'time': end_time - start_time,
            'steps': steps,
            'sorted': is_sorted
        }
