from src.p_problems.sorting import SortingAlgorithms
from src.np_problems.traveling_salesman import TravelingSalesman
import random

# 测试P问题
print("Testing P Problem: Sorting")
sorter = SortingAlgorithms()
arr = [random.randint(1, 100) for _ in range(10)]
sorted_arr, steps = sorter.quick_sort(arr.copy())
print(f"Original: {arr}")
print(f"Sorted: {sorted_arr}")
print(f"Steps: {steps}")

# 测试NP问题
print("\nTesting NP Problem: Traveling Salesman")
tsp = TravelingSalesman()
tsp.create_random_cities(5, 100)
path, distance, steps = tsp.nearest_neighbor()
print(f"Path: {path}")
print(f"Distance: {distance:.2f}")
print(f"Steps: {steps}")
