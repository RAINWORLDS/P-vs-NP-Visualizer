import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.p_problems.sorting import SortingAlgorithms
from src.p_problems.searching import SearchingAlgorithms
from src.np_problems.traveling_salesman import TravelingSalesman
from src.np_problems.knapsack import KnapsackSolver
from src.simulations.p_equals_np import PEqualsNPSimulation
from src.visualization.charts import ComplexityVisualizer

def demo_p_problems():
    print("=== DEMO: P PROBLEMS ===")
    
    sorter = SortingAlgorithms()
    searcher = SearchingAlgorithms()
    
    arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original array: {arr}")
    
    sorted_arr, steps = sorter.quick_sort(arr.copy())
    print(f"Quick sorted: {sorted_arr}")
    print(f"Steps taken: {steps}")
    
    target = 22
    index, search_steps = searcher.binary_search(sorted(arr), target)
    print(f"Binary search for {target}: index={index}")
    print(f"Search steps: {search_steps}")

def demo_np_problems():
    print("\n=== DEMO: NP PROBLEMS ===")
    
    tsp = TravelingSalesman()
    tsp.create_random_cities(5, 100)
    
    path, distance, steps = tsp.nearest_neighbor()
    print(f"TSP Nearest Neighbor:")
    print(f"  Path: {path}")
    print(f"  Distance: {distance:.2f}")
    print(f"  Steps: {steps}")
    
    knapsack = KnapsackSolver()
    knapsack.create_random_items(5, 50, 100)
    
    items, value, weight, ksteps = knapsack.greedy_by_value_density(30)
    print(f"\nKnapsack Greedy Solution:")
    print(f"  Value: {value}")
    print(f"  Weight: {weight}")
    print(f"  Steps: {ksteps}")

def demo_complexity_visualization():
    print("\n=== DEMO: COMPLEXITY VISUALIZATION ===")
    
    visualizer = ComplexityVisualizer()
    
    fig = visualizer.plot_complexity_growth()
    fig.savefig('complexity_growth.png', dpi=300, bbox_inches='tight')
    print("Saved complexity_growth.png")
    
    p_data = [
        {'size': 100, 'time': 0.001},
        {'size': 1000, 'time': 0.01},
        {'size': 10000, 'time': 0.1}
    ]
    
    np_data = [
        {'size': 5, 'time': 0.001},
        {'size': 10, 'time': 0.1},
        {'size': 15, 'time': 10.0}
    ]
    
    fig2 = visualizer.plot_p_vs_np_comparison(p_data, np_data)
    fig2.savefig('p_vs_np_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved p_vs_np_comparison.png")

def demo_p_equals_np_simulation():
    print("\n=== DEMO: P = NP SIMULATION ===")
    
    simulator = PEqualsNPSimulation()
    results = simulator.run_comparison(20)
    
    print("Problem Size | Current NP Time | If P=NP Time | Speedup")
    print("-" * 60)
    for result in results:
        print(f"{result['problem_size']:12} | {result['current_np_time']:15.6f} | "
              f"{result['if_p_equals_np_time']:12.6f} | {result['speedup_factor']:8.1f}x")

def interactive_demo():
    print("\n=== INTERACTIVE DEMO ===")
    print("This demonstrates the contrast between P and NP problems")
    
    from src.simulations.interactive_demo import InteractiveSimulation
    sim = InteractiveSimulation()
    
    print("\n1. Demonstrating P problem (sorting 10,000 numbers)...")
    arr = list(range(10000))
    import random
    random.shuffle(arr)
    
    import time
    start = time.time()
    sorted_arr = sorted(arr)
    p_time = time.time() - start
    print(f"   Time: {p_time:.6f} seconds")
    
    print("\n2. Demonstrating NP problem (subset sum with n=20)...")
    numbers = [random.randint(1, 100) for _ in range(20)]
    target = sum(random.sample(numbers, 5))
    
    start = time.time()
    found = False
    for i in range(1 << 10):
        current_sum = 0
        for j in range(10):
            if i & (1 << j):
                current_sum += numbers[j]
        if current_sum == target:
            found = True
            break
    np_time = time.time() - start
    
    print(f"   Time: {np_time:.6f} seconds")
    print(f"   Ratio NP/P: {np_time/p_time:.0f}x slower")
    
    print("\n3. Complexity implications:")
    print(f"   P problem scales polynomially: O(n log n)")
    print(f"   NP problem scales exponentially: O(2^n)")
    print(f"   For n=30: P ~ 0.001s, NP ~ 1,000s")

if __name__ == "__main__":
    print("P vs NP Visualizer - Basic Usage Examples")
    print("=" * 50)
    
    demo_p_problems()
    demo_np_problems()
    demo_complexity_visualization()
    demo_p_equals_np_simulation()
    interactive_demo()
    
    print("\n" + "=" * 50)
    print("All demonstrations completed successfully!")
    print("Check the generated PNG files for visualizations.")
