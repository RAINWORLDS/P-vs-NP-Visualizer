import sys
import os
import time
import random
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.np_problems.sat_solver import SATSolver
from src.np_problems.graph_coloring import GraphColoring
from src.np_problems.subset_sum import SubsetSum
from src.simulations.quantum_simulation import QuantumPvsNPSimulation
from src.visualization.interactive import InteractiveVisualizer

def advanced_sat_solving():
    print("=== ADVANCED SAT SOLVING ===")
    
    sat_solver = SATSolver()
    
    print("1. Creating random 3-SAT instance with 10 variables, 20 clauses...")
    clauses = sat_solver.create_random_sat(10, 20, 3)
    
    print(f"   Variables: {len(sat_solver.variables)}")
    print(f"   Clauses: {len(clauses)}")
    print(f"   Sample clauses: {clauses[:3]}")
    
    print("\n2. Solving with brute force...")
    start = time.time()
    found_bf, assignment_bf, steps_bf = sat_solver.brute_force_solve()
    bf_time = time.time() - start
    
    print(f"   Satisfiable: {found_bf}")
    print(f"   Steps: {steps_bf:,}")
    print(f"   Time: {bf_time:.4f} seconds")
    
    print("\n3. Solving with DPLL algorithm...")
    start = time.time()
    found_dpll, assignment_dpll, steps_dpll = sat_solver.dpll_solve()
    dpll_time = time.time() - start
    
    print(f"   Satisfiable: {found_dpll}")
    print(f"   Steps: {steps_dpll:,}")
    print(f"   Time: {dpll_time:.4f} seconds")
    
    if found_bf and found_dpll:
        print("\n4. Verification:")
        print(f"   Both algorithms found solutions")
        print(f"   Speedup: {bf_time/dpll_time:.1f}x")
        print(f"   Steps reduction: {steps_bf/steps_dpll:.1f}x")

def advanced_graph_coloring():
    print("\n=== ADVANCED GRAPH COLORING ===")
    
    coloring = GraphColoring()
    
    print("1. Creating random graph with 8 nodes...")
    graph = coloring.create_random_graph(8, 0.4)
    
    print(f"   Nodes: {len(graph)}")
    print(f"   Edges: {sum(len(neighbors) for neighbors in graph.values())//2}")
    
    k = 3
    print(f"\n2. Testing if graph is {k}-colorable...")
    
    print("   Using brute force:")
    start = time.time()
    possible_bf, coloring_bf, steps_bf = coloring.brute_force_coloring(k)
    bf_time = time.time() - start
    print(f"   Possible: {possible_bf}")
    print(f"   Steps: {steps_bf:,}")
    print(f"   Time: {bf_time:.4f}s")
    
    print("\n   Using backtracking:")
    start = time.time()
    coloring_bt, steps_bt = coloring.backtracking_coloring(k)
    bt_time = time.time() - start
    print(f"   Found coloring: {len(coloring_bt) > 0}")
    print(f"   Steps: {steps_bt:,}")
    print(f"   Time: {bt_time:.4f}s")
    
    print("\n   Using greedy algorithm:")
    start = time.time()
    coloring_greedy, steps_greedy = coloring.greedy_coloring()
    greedy_time = time.time() - start
    colors_used = len(set(coloring_greedy.values()))
    print(f"   Colors used: {colors_used}")
    print(f"   Steps: {steps_greedy:,}")
    print(f"   Time: {greedy_time:.4f}s")
    
    if coloring_bf:
        print(f"\n3. Optimal coloring uses {k} colors")
        print(f"   Greedy used {colors_used} colors")
        print(f"   Ratio: {colors_used/k:.2f}")

def quantum_computing_simulation():
    print("\n=== QUANTUM COMPUTING SIMULATION ===")
    
    quantum_sim = QuantumPvsNPSimulation()
    
    print("1. Grover's Algorithm Search Speedup:")
    for n_qubits in [4, 6, 8, 10]:
        result = quantum_sim.grovers_algorithm_simulation(n_qubits)
        print(f"   {n_qubits} qubits: Classical {result['classical_steps']:,} steps, "
              f"Quantum {result['quantum_steps']:,} steps, "
              f"Speedup: {result['speedup']:.0f}x")
    
    print("\n2. Quantum Annealing for Optimization:")
    result = quantum_sim.simulate_quantum_annealing(15, temperature=2.0, steps=500)
    print(f"   Problem size: {result['problem_size']}")
    print(f"   Initial energy: {result['energies'][0]:.2f}")
    print(f"   Final energy: {result['best_energy']:.2f}")
    print(f"   Improvement: {result['energies'][0] - result['best_energy']:.2f}")
    
    print("\n3. Shor's Algorithm Factorization:")
    numbers_to_factor = [15, 21, 35]
    for num in numbers_to_factor:
        result = quantum_sim.simulate_shors_algorithm(num)
        print(f"   {num} = {' × '.join(map(str, result['factors']))}")
        if 'speedup' in result:
            print(f"     Speedup vs classical: {result['speedup']:.0f}x")

def advanced_performance_analysis():
    print("\n=== ADVANCED PERFORMANCE ANALYSIS ===")
    
    subset_sum = SubsetSum()
    
    print("1. Subset Sum Problem Complexity Growth:")
    
    sizes = [10, 15, 20, 25]
    results = []
    
    for size in sizes:
        subset_sum.create_random_numbers(size, 100)
        target = sum(random.sample(subset_sum.numbers, max(1, size//3)))
        
        start = time.time()
        found_bf, subset_bf, steps_bf = subset_sum.brute_force_subset_sum(target)
        bf_time = time.time() - start
        
        start = time.time()
        found_dp, subset_dp, steps_dp = subset_sum.dynamic_programming_subset_sum(target)
        dp_time = time.time() - start
        
        results.append({
            'size': size,
            'bf_time': bf_time,
            'dp_time': dp_time,
            'bf_steps': steps_bf,
            'dp_steps': steps_dp,
            'speedup': bf_time / dp_time if dp_time > 0 else float('inf')
        })
    
    print("\n   Size | Brute Force Time | DP Time | Speedup")
    print("   " + "-" * 50)
    for r in results:
        print(f"   {r['size']:4} | {r['bf_time']:16.4f}s | {r['dp_time']:8.4f}s | {r['speedup']:8.1f}x")
    
    print("\n2. Exponential Growth Analysis:")
    print("   n  | 2^n      | n^2      | Ratio")
    print("   " + "-" * 35)
    for n in [5, 10, 15, 20, 25]:
        exp = 2 ** n
        poly = n ** 2
        ratio = exp / poly
        print(f"   {n:2} | {exp:8,} | {poly:8,} | {ratio:12,.0f}x")

def interactive_visualization_demo():
    print("\n=== INTERACTIVE VISUALIZATION DEMO ===")
    print("Note: This requires Jupyter notebook environment")
    print("The following visualizations would be available:")
    
    print("\n1. Complexity Class Explorer")
    print("   • Adjust n values with sliders")
    print("   • Compare different complexity classes")
    print("   • Visualize growth rates")
    
    print("\n2. Algorithm Performance Comparison")
    print("   • Select multiple algorithms")
    print("   • Compare time complexities")
    print("   • Interactive performance curves")
    
    print("\n3. P=NP Scenario Explorer")
    print("   • Adjust probability of P=NP")
    print("   • See impact on different fields")
    print("   • Future projections")
    
    try:
        visualizer = InteractiveVisualizer()
        print("\nInteractive widgets would load in Jupyter...")
    except:
        print("\n(Running in non-interactive mode)")

def generate_educational_content():
    print("\n=== EDUCATIONAL CONTENT GENERATION ===")
    
    print("1. Key Concepts Summary:")
    concepts = {
        'P Class': 'Problems solvable in polynomial time',
        'NP Class': 'Problems verifiable in polynomial time',
        'NP-Complete': 'Hardest problems in NP',
        'NP-Hard': 'At least as hard as NP-complete',
        'P vs NP': 'Are they equal? Unsolved!',
        'Reduction': 'Transforming one problem to another',
        'Cook-Levin': 'SAT is NP-complete',
        'Millennium Prize': '$1,000,000 for solution'
    }
    
    for concept, definition in concepts.items():
        print(f"   • {concept}: {definition}")
    
    print("\n2. Common P Problems:")
    p_problems = ['Sorting', 'Searching', 'Shortest Path', 'Minimum Spanning Tree']
    for prob in p_problems:
        print(f"   • {prob}")
    
    print("\n3. Common NP-Complete Problems:")
    np_problems = ['Traveling Salesman', 'Boolean SAT', 'Knapsack', 
                   'Graph Coloring', 'Subset Sum', 'Hamiltonian Path']
    for prob in np_problems:
        print(f"   • {prob}")
    
    print("\n4. If P = NP Consequences:")
    consequences = [
        'Cryptography breaks',
        'Perfect optimization',
        'AI reasoning solved',
        'Protein folding solved',
        'Mathematical proofs automated'
    ]
    for i, cons in enumerate(consequences, 1):
        print(f"   {i}. {cons}")

if __name__ == "__main__":
    print("P vs NP Visualizer - Advanced Demonstrations")
    print("=" * 60)
    
    advanced_sat_solving()
    advanced_graph_coloring()
    quantum_computing_simulation()
    advanced_performance_analysis()
    interactive_visualization_demo()
    generate_educational_content()
    
    print("\n" + "=" * 60)
    print("Advanced demonstrations completed!")
    print("\nNext steps:")
    print("1. Run in Jupyter for interactive visualizations")
    print("2. Modify parameters for deeper exploration")
    print("3. Extend with custom algorithms")
