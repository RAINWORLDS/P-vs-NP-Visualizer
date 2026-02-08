import matplotlib.pyplot as plt
import numpy as np
import ipywidgets as widgets
from IPython.display import display, clear_output
import time
from typing import Dict, Any

class InteractiveVisualizer:
    
    def __init__(self):
        self.fig = None
        self.ax = None
    
    def create_complexity_slider(self):
        n_slider = widgets.IntSlider(
            value=10,
            min=1,
            max=20,
            step=1,
            description='n:',
            continuous_update=False
        )
        
        complexity_dropdown = widgets.Dropdown(
            options=['O(1)', 'O(log n)', 'O(n)', 'O(n²)', 'O(2ⁿ)', 'O(n!)'],
            value='O(n)',
            description='Complexity:'
        )
        
        output = widgets.Output()
        
        def update_plot(change):
            with output:
                clear_output(wait=True)
                n = n_slider.value
                complexity = complexity_dropdown.value
                
                self.fig, self.ax = plt.subplots(figsize=(10, 6))
                
                x = np.arange(1, n + 1)
                
                if complexity == 'O(1)':
                    y = np.ones_like(x)
                elif complexity == 'O(log n)':
                    y = np.log2(x)
                elif complexity == 'O(n)':
                    y = x
                elif complexity == 'O(n²)':
                    y = x ** 2
                elif complexity == 'O(2ⁿ)':
                    y = 2 ** x
                elif complexity == 'O(n!)':
                    y = [np.math.factorial(i) for i in x]
                
                self.ax.plot(x, y, 'b-o', linewidth=2, markersize=6)
                self.ax.fill_between(x, 0, y, alpha=0.3)
                
                self.ax.set_xlabel('Input Size (n)', fontsize=12)
                self.ax.set_ylabel('Operations', fontsize=12)
                self.ax.set_title(f'{complexity} Complexity Growth', fontsize=14, fontweight='bold')
                self.ax.grid(True, alpha=0.3)
                
                total_ops = y[-1]
                self.ax.text(0.02, 0.98, f'Total operations for n={n}: {total_ops:,.0f}',
                           transform=self.ax.transAxes, fontsize=11,
                           verticalalignment='top',
                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
                
                plt.tight_layout()
                plt.show()
        
        n_slider.observe(update_plot, 'value')
        complexity_dropdown.observe(update_plot, 'value')
        
        ui = widgets.VBox([n_slider, complexity_dropdown])
        display(ui, output)
        update_plot(None)
    
    def create_algorithm_comparison(self):
        algorithms = {
            'Bubble Sort': lambda n: n**2,
            'Quick Sort': lambda n: n * np.log2(n),
            'Merge Sort': lambda n: n * np.log2(n),
            'Linear Search': lambda n: n,
            'Binary Search': lambda n: np.log2(n)
        }
        
        algorithm_checkboxes = []
        for algo in algorithms.keys():
            cb = widgets.Checkbox(
                value=True,
                description=algo,
                disabled=False
            )
            algorithm_checkboxes.append((algo, cb))
        
        max_n_slider = widgets.IntSlider(
            value=100,
            min=10,
            max=1000,
            step=10,
            description='Max n:',
            continuous_update=False
        )
        
        output = widgets.Output()
        
        def update_comparison(change):
            with output:
                clear_output(wait=True)
                max_n = max_n_slider.value
                
                selected_algorithms = []
                for algo_name, checkbox in algorithm_checkboxes:
                    if checkbox.value:
                        selected_algorithms.append(algo_name)
                
                if not selected_algorithms:
                    print("Please select at least one algorithm")
                    return
                
                self.fig, self.ax = plt.subplots(figsize=(12, 7))
                
                n_values = np.linspace(1, max_n, 100)
                
                colors = plt.cm.tab10(np.linspace(0, 1, len(selected_algorithms)))
                
                for algo_name, color in zip(selected_algorithms, colors):
                    y = algorithms[algo_name](n_values)
                    self.ax.plot(n_values, y, label=algo_name, color=color, linewidth=3)
                
                self.ax.set_xlabel('Input Size (n)', fontsize=12)
                self.ax.set_ylabel('Operations', fontsize=12)
                self.ax.set_title('Algorithm Complexity Comparison', fontsize=14, fontweight='bold')
                self.ax.legend(fontsize=11)
                self.ax.grid(True, alpha=0.3)
                
                if max_n > 100:
                    self.ax.set_yscale('log')
                
                plt.tight_layout()
                plt.show()
        
        checkboxes_ui = widgets.VBox([cb for _, cb in algorithm_checkboxes])
        
        for _, cb in algorithm_checkboxes:
            cb.observe(update_comparison, 'value')
        
        max_n_slider.observe(update_comparison, 'value')
        
        ui = widgets.VBox([
            widgets.Label('Select Algorithms:'),
            checkboxes_ui,
            max_n_slider
        ])
        
        display(ui, output)
        update_comparison(None)
    
    def create_p_np_decision_explorer(self):
        problem_types = ['Sorting', 'Searching', 'Graph Path', 'TSP', 'SAT', 'Knapsack']
        
        problem_dropdown = widgets.Dropdown(
            options=problem_types,
            value='Sorting',
            description='Problem:'
        )
        
        size_slider = widgets.IntSlider(
            value=10,
            min=1,
            max=50,
            step=1,
            description='Size:'
        )
        
        output = widgets.Output()
        
        def simulate_problem(problem_type, size):
            if problem_type in ['Sorting', 'Searching', 'Graph Path']:
                time_needed = size * np.log2(size + 1) / 1000
                complexity_class = 'P'
                color = 'green'
            else:
                time_needed = (2 ** (size / 5)) / 1000
                complexity_class = 'NP'
                color = 'red'
            
            return {
                'time': time_needed,
                'class': complexity_class,
                'color': color,
                'message': f'{problem_type} with n={size}'
            }
        
        def update_explorer(change):
            with output:
                clear_output(wait=True)
                
                problem = problem_dropdown.value
                size = size_slider.value
                
                result = simulate_problem(problem, size)
                
                self.fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
                
                sizes = np.arange(1, 51)
                p_times = sizes * np.log2(sizes + 1) / 1000
                np_times = (2 ** (sizes / 5)) / 1000
                
                ax1.plot(sizes, p_times, 'g-', label='P Problems', linewidth=2, alpha=0.7)
                ax1.plot(sizes, np_times, 'r-', label='NP Problems', linewidth=2, alpha=0.7)
                ax1.scatter([size], [result['time']], color=result['color'], s=200, zorder=5,
                          edgecolor='black', linewidth=2)
                ax1.set_xlabel('Problem Size (n)', fontsize=12)
                ax1.set_ylabel('Time (seconds)', fontsize=12)
                ax1.set_title('P vs NP Time Complexity', fontsize=14, fontweight='bold')
                ax1.legend()
                ax1.grid(True, alpha=0.3)
                
                ax2.text(0.5, 0.7, f'Problem: {problem}\nn = {size}',
                        fontsize=14, ha='center', transform=ax2.transAxes)
                ax2.text(0.5, 0.6, f'Complexity Class: {result["class"]}',
                        fontsize=16, ha='center', fontweight='bold',
                        color=result['color'], transform=ax2.transAxes)
                
                if result['class'] == 'P':
                    explanation = '✓ Solvable in polynomial time\n✓ Efficient algorithms exist\n✓ Scales reasonably'
                else:
                    explanation = '✗ No known polynomial solution\n✓ Verifiable in polynomial time\n✗ Becomes impractical quickly'
                
                ax2.text(0.5, 0.4, explanation, fontsize=12, ha='center',
                        transform=ax2.transAxes, va='top',
                        bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))
                
                ax2.text(0.5, 0.1, f'Estimated time: {result["time"]:.6f} seconds',
                        fontsize=11, ha='center', transform=ax2.transAxes)
                
                ax2.set_xlim(0, 1)
                ax2.set_ylim(0, 1)
                ax2.axis('off')
                ax2.set_title('Problem Analysis', fontsize=14, fontweight='bold')
                
                plt.tight_layout()
                plt.show()
        
        problem_dropdown.observe(update_explorer, 'value')
        size_slider.observe(update_explorer, 'value')
        
        ui = widgets.VBox([problem_dropdown, size_slider])
        display(ui, output)
        update_explorer(None)
    
    def create_what_if_p_equals_np(self):
        scenario_slider = widgets.FloatSlider(
            value=0.0,
            min=0.0,
            max=1.0,
            step=0.1,
            description='P=NP Probability:',
            continuous_update=False
        )
        
        years_slider = widgets.IntSlider(
            value=10,
            min=0,
            max=50,
            step=5,
            description='Years from now:'
        )
        
        output = widgets.Output()
        
        def update_scenario(change):
            with output:
                clear_output(wait=True)
                
                probability = scenario_slider.value
                years = years_slider.value
                
                self.fig, axes = plt.subplots(2, 2, figsize=(14, 10))
                axes = axes.flatten()
                
                areas = ['Cryptography', 'Optimization', 'AI', 'Medicine']
                current_status = ['Secure', 'Heuristic', 'Narrow', 'Limited']
                future_status = ['Broken', 'Optimal', 'General', 'Precise']
                
                for idx, (area, curr, future) in enumerate(zip(areas, current_status, future_status)):
                    if idx >= 4:
                        break
                    
                    ax = axes[idx]
                    
                    current_val = 100 - (probability * 100)
                    future_val = probability * 100
                    
                    bars = ax.bar(['Current', 'If P=NP'], [current_val, future_val],
                                 color=['lightblue', 'lightcoral'])
                    
                    ax.set_ylim(0, 100)
                    ax.set_ylabel('Capability (%)', fontsize=10)
                    ax.set_title(f'{area}', fontsize=12, fontweight='bold')
                    ax.grid(True, alpha=0.3, axis='y')
                    
                    for bar, label in zip(bars, [curr, future]):
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                               label, ha='center', va='bottom', fontsize=9)
                
                plt.suptitle(f'P=NP Scenario (Probability: {probability:.0%}, Years: {years})',
                           fontsize=16, fontweight='bold')
                plt.tight_layout()
                plt.show()
                
                print("\n" + "="*60)
                print("SCENARIO ANALYSIS")
                print("="*60)
                
                if probability < 0.3:
                    print("Most likely: P ≠ NP")
                    print("Status quo maintained")
                    print("Cryptography remains secure")
                elif probability < 0.7:
                    print("Uncertain outcome")
                    print("Active research continues")
                    print("Prepare for both possibilities")
                else:
                    print("P = NP likely")
                    print("Revolution in computing")
                    print("Complete paradigm shift needed")
                
                print(f"\nIn {years} years:")
                print(f"• Crypto security: {100 - probability*100:.0f}%")
                print(f"• Optimization improvement: {probability*100:.0f}%")
                print(f"• AI capability increase: {probability*80:.0f}%")
        
        scenario_slider.observe(update_scenario, 'value')
        years_slider.observe(update_scenario, 'value')
        
        ui = widgets.VBox([scenario_slider, years_slider])
        display(ui, output)
        update_scenario(None)
