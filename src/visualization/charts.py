import matplotlib.pyplot as plt
import numpy as np
import math
from typing import List, Dict, Any
import matplotlib

class ComplexityVisualizer:
    
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')
        self.figsize = (12, 8)
    
    def plot_complexity_growth(self):
        n = np.arange(1, 21)
        
        complexities = {
            'O(1)': np.ones_like(n),
            'O(log n)': np.log2(n),
            'O(n)': n,
            'O(n log n)': n * np.log2(n),
            'O(n²)': n**2,
            'O(n³)': n**3,
            'O(2ⁿ)': 2**n,
            'O(n!)': [math.factorial(i) if i <= 7 else math.factorial(7) * 2**(i-7) for i in n]
        }
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        colors = plt.cm.Set2(np.linspace(0, 1, len(complexities)))
        
        for (name, values), color in zip(complexities.items(), colors):
            if name in ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)', 'O(n²)', 'O(n³)']:
                ax1.plot(n, values, label=name, linewidth=3, color=color, marker='o')
            else:
                ax2.plot(n, values, label=name, linewidth=3, color=color, marker='s')
        
        ax1.set_xlabel('Input Size (n)', fontsize=12)
        ax1.set_ylabel('Operations', fontsize=12)
        ax1.set_title('Polynomial Complexities (P Class)', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        ax2.set_xlabel('Input Size (n)', fontsize=12)
        ax2.set_ylabel('Operations (log scale)', fontsize=12)
        ax2.set_title('Exponential Complexities (NP Class)', fontsize=14, fontweight='bold')
        ax2.set_yscale('log')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_p_vs_np_comparison(self, p_data, np_data):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        sizes = [d['size'] for d in p_data]
        p_times = [d['time'] for d in p_data]
        np_times = [d['time'] for d in np_data[:len(p_data)]]
        
        ax1.plot(sizes, p_times, 'b-o', label='P Problems', linewidth=2, markersize=8)
        ax1.plot(sizes, np_times, 'r-s', label='NP Problems', linewidth=2, markersize=8)
        ax1.set_xlabel('Problem Size', fontsize=12)
        ax1.set_ylabel('Execution Time (seconds)', fontsize=12)
        ax1.set_title('P vs NP: Time Complexity', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(sizes, np.array(p_times) * 1000, 'b-o', label='P (ms)', linewidth=2, markersize=8)
        ax2.plot(sizes, np.array(np_times) * 1000, 'r-s', label='NP (ms)', linewidth=2, markersize=8)
        ax2.set_xlabel('Problem Size', fontsize=12)
        ax2.set_ylabel('Execution Time (ms, log scale)', fontsize=12)
        ax2.set_title('P vs NP: Logarithmic Scale', fontsize=14, fontweight='bold')
        ax2.set_yscale('log')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_algorithm_performance(self, algorithms_data):
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()
        
        for idx, (algo_name, data) in enumerate(algorithms_data.items()):
            if idx >= 4:
                break
            
            sizes = data['sizes']
            times = data['times']
            steps = data['steps']
            
            ax1 = axes[idx]
            ax2 = ax1.twinx()
            
            line1 = ax1.plot(sizes, times, 'b-o', label='Time (s)', linewidth=2)
            line2 = ax2.plot(sizes, steps, 'r-s', label='Steps', linewidth=2, alpha=0.7)
            
            ax1.set_xlabel('Input Size', fontsize=10)
            ax1.set_ylabel('Time (seconds)', color='b', fontsize=10)
            ax2.set_ylabel('Operations', color='r', fontsize=10)
            ax1.set_title(f'{algo_name} Performance', fontsize=12, fontweight='bold')
            
            lines = line1 + line2
            labels = [l.get_label() for l in lines]
            ax1.legend(lines, labels, loc='upper left')
            
            ax1.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_complexity_heatmap(self):
        n = np.arange(1, 11)
        complexities = ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)', 'O(n²)', 'O(2ⁿ)']
        
        data = np.zeros((len(complexities), len(n)))
        
        for i, comp in enumerate(complexities):
            for j, size in enumerate(n):
                if comp == 'O(1)':
                    data[i, j] = 1
                elif comp == 'O(log n)':
                    data[i, j] = max(1, np.log2(size))
                elif comp == 'O(n)':
                    data[i, j] = size
                elif comp == 'O(n log n)':
                    data[i, j] = size * max(1, np.log2(size))
                elif comp == 'O(n²)':
                    data[i, j] = size ** 2
                elif comp == 'O(2ⁿ)':
                    data[i, j] = min(2 ** size, 10000)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        im = ax.imshow(data, cmap='YlOrRd', aspect='auto')
        
        ax.set_xticks(np.arange(len(n)))
        ax.set_yticks(np.arange(len(complexities)))
        ax.set_xticklabels([f'n={x}' for x in n])
        ax.set_yticklabels(complexities)
        
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
        
        for i in range(len(complexities)):
            for j in range(len(n)):
                text = ax.text(j, i, f'{data[i, j]:.0f}',
                             ha="center", va="center", color="black", fontsize=9)
        
        ax.set_title("Complexity Class Operations Heatmap", fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel("Input Size (n)", fontsize=12)
        ax.set_ylabel("Complexity Class", fontsize=12)
        
        plt.colorbar(im, ax=ax, label='Operations')
        plt.tight_layout()
        
        return fig
    
    def plot_practical_limits(self):
        ops_per_second = 10 ** 9
        
        complexities = ['O(n)', 'O(n log n)', 'O(n²)', 'O(n³)', 'O(2ⁿ)', 'O(n!)']
        max_sizes = []
        
        for comp in complexities:
            max_size = 0
            for n in range(1, 1000):
                if comp == 'O(n)':
                    ops = n
                elif comp == 'O(n log n)':
                    ops = n * max(1, np.log2(n))
                elif comp == 'O(n²)':
                    ops = n ** 2
                elif comp == 'O(n³)':
                    ops = n ** 3
                elif comp == 'O(2ⁿ)':
                    ops = 2 ** n
                elif comp == 'O(n!)':
                    ops = math.factorial(min(n, 20))
                
                if ops <= ops_per_second:
                    max_size = n
                else:
                    break
            max_sizes.append(max_size)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        bars = ax.bar(complexities, max_sizes, color=plt.cm.viridis(np.linspace(0, 1, len(complexities))))
        
        ax.set_xlabel('Complexity Class', fontsize=12)
        ax.set_ylabel('Maximum Practical Input Size', fontsize=12)
        ax.set_title('Practical Limits (1 billion ops/second)', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        for bar, size in zip(bars, max_sizes):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                   f'{size:,}', ha='center', va='bottom', fontsize=10)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
    
    def create_visualization_dashboard(self):
        fig = plt.figure(figsize=(16, 12))
        
        gs = fig.add_gridspec(3, 3)
        
        ax1 = fig.add_subplot(gs[0, :])
        ax2 = fig.add_subplot(gs[1, 0])
        ax3 = fig.add_subplot(gs[1, 1])
        ax4 = fig.add_subplot(gs[1, 2])
        ax5 = fig.add_subplot(gs[2, :])
        
        n = np.arange(1, 21)
        
        ax1.plot(n, n, 'b-', label='O(n)', linewidth=2)
        ax1.plot(n, n**2, 'r-', label='O(n²)', linewidth=2)
        ax1.plot(n, 2**n, 'g-', label='O(2ⁿ)', linewidth=2)
        ax1.set_title('Complexity Growth Comparison', fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        sizes = [100, 1000, 10000, 100000]
        p_times = [0.001, 0.01, 0.1, 1.0]
        np_times = [0.1, 10, 1000, 100000]
        ax2.bar(['P', 'NP'], [p_times[-1], np_times[-1]], color=['blue', 'red'])
        ax2.set_title('P vs NP Time (n=100k)', fontsize=12, fontweight
