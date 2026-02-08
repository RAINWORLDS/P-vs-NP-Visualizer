import time
import random
import sys
from typing import Dict, List, Any

class InteractiveSimulation:
    
    def __init__(self):
        self.state = {}
    
    def demonstrate_p_problem(self):
        print("Demonstrating P Problem: Sorting")
        print("=" * 50)
        
        sizes = [100, 1000, 10000]
        for size in sizes:
            arr = [random.randint(1, 10000) for _ in range(size)]
            
            start = time.time()
            sorted_arr = sorted(arr)
            elapsed = time.time() - start
            
            print(f"Array size: {size:,}")
            print(f"Time: {elapsed:.6f} seconds")
            print(f"Time per element: {elapsed/size:.8f} seconds")
            print("-" * 30)
        
        print("\nP Problems scale polynomially:")
        print("O(n log n) for sorting")
        print("Doubling input increases time by ~2.2x")
    
    def demonstrate_np_problem(self):
        print("\nDemonstrating NP Problem: Subset Sum")
        print("=" * 50)
        
        sizes = [10, 15, 20]
        for size in sizes:
            numbers = [random.randint(1, 100) for _ in range(size)]
            target = sum(random.sample(numbers, max(1, size//2)))
            
            start = time.time()
            found = False
            
            for i in range(1 << size):
                current_sum = 0
                for j in range(size):
                    if i & (1 << j):
                        current_sum += numbers[j]
                
                if current_sum == target:
                    found = True
                    break
            
            elapsed = time.time() - start
            
            print(f"Set size: {size}")
            print(f"Target: {target}")
            print(f"Found: {found}")
            print(f"Time: {elapsed:.6f} seconds")
            print(f"Possible subsets: {2**size:,}")
            print(f"Subsets checked per second: {2**size/max(elapsed, 0.001):,.0f}")
            print("-" * 30)
        
        print("\nNP Problems scale exponentially:")
        print("O(2^n) for subset sum")
        print("Adding one element doubles the time")
    
    def interactive_complexity_choice(self):
        print("\nChoose a complexity class to explore:")
        print("1. O(1) - Constant time")
        print("2. O(log n) - Logarithmic")
        print("3. O(n) - Linear")
        print("4. O(n log n) - Linearithmic")
        print("5. O(n^2) - Quadratic")
        print("6. O(2^n) - Exponential")
        print("7. O(n!) - Factorial")
        
        choice = input("\nEnter choice (1-7): ")
        
        complexities = {
            '1': ('O(1)', lambda n: 1),
            '2': ('O(log n)', lambda n: max(1, int(math.log2(n)))),
            '3': ('O(n)', lambda n: n),
            '4': ('O(n log n)', lambda n: int(n * max(1, math.log2(n)))),
            '5': ('O(n^2)', lambda n: n ** 2),
            '6': ('O(2^n)', lambda n: 2 ** n),
            '7': ('O(n!)', lambda n: math.factorial(min(n, 10)))
        }
        
        if choice in complexities:
            name, func = complexities[choice]
            print(f"\nExploring {name}:")
            
            for n in [1, 2, 5, 10, 20, 50, 100]:
                if n <= 100 or name not in ['O(2^n)', 'O(n!)']:
                    operations = func(n)
                    print(f"n={n}: {operations:,} operations")
        
        return choice
    
    def simulate_p_equals_np_scenario(self):
        print("\n" + "=" * 60)
        print("SIMULATING P = NP SCENARIO")
        print("=" * 60)
        
        print("\nCurrent World (P ≠ NP assumed):")
        print("-" * 40)
        print("✓ Encryption: Secure")
        print("✓ Optimization: Hard")
        print("✓ AI reasoning: Limited")
        print("✓ Protein folding: Approximate")
        
        print("\n\nIf P = NP:")
        print("-" * 40)
        print("🔓 Encryption: Broken instantly")
        print("⚡ Optimization: Perfect solutions")
        print("🧠 AI: Human-level reasoning")
        print("🧬 Biology: Exact protein folding")
        print("💰 Economics: Perfect markets")
        print("🚗 Logistics: Optimal routes")
        
        print("\nConsequences:")
        print("1. Cryptography needs complete redesign")
        print("2. Million-dollar prize awarded")
        print("3. Computational limits disappear")
        print("4. New era of technological advancement")
        
        response = input("\nWhat would you do in a P=NP world? ")
        print(f"\nInteresting! '{response}' could indeed change dramatically.")
    
    def run_tutorial_mode(self):
        print("\n📚 P vs NP TUTORIAL MODE")
        print("=" * 50)
        
        steps = [
            "Step 1: Understanding Complexity Classes",
            "   • P: Problems solvable quickly",
            "   • NP: Problems verifiable quickly",
            "   • NP-complete: Hardest NP problems",
            "",
            "Step 2: The Million Dollar Question",
            "   • P = NP? Are they the same?",
            "   • Clay Mathematics Institute prize",
            "   • Most experts believe P ≠ NP",
            "",
            "Step 3: Real-world Examples",
            "   • P: Sorting, searching, shortest path",
            "   • NP: Traveling salesman, scheduling",
            "   • Cryptography relies on P ≠ NP",
            "",
            "Step 4: Implications",
            "   • If P = NP: Revolution",
            "   • If P ≠ NP: Status quo",
            "   • Quantum computing adds new dimension"
        ]
        
        for step in steps:
            print(step)
            time.sleep(0.5 if step else 0.1)
    
    def create_interactive_session(self):
        print("🧠 INTERACTIVE P vs NP EXPLORER")
        print("=" * 50)
        
        while True:
            print("\nMain Menu:")
            print("1. Demonstrate P Problem")
            print("2. Demonstrate NP Problem")
            print("3. Explore Complexity Classes")
            print("4. Simulate P=NP Scenario")
            print("5. Run Tutorial")
            print("6. Exit")
            
            choice = input("\nEnter choice (1-6): ")
            
            if choice == '1':
                self.demonstrate_p_problem()
            elif choice == '2':
                self.demonstrate_np_problem()
            elif choice == '3':
                self.interactive_complexity_choice()
            elif choice == '4':
                self.simulate_p_equals_np_scenario()
            elif choice == '5':
                self.run_tutorial_mode()
            elif choice == '6':
                print("\nThank you for exploring P vs NP!")
                break
            else:
                print("Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
