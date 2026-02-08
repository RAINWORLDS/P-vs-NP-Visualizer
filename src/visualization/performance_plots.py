import matplotlib.pyplot as plt
import numpy as np
import time
import random
from typing import List, Dict, Any
from datetime import datetime

class PerformancePlotter:
    
    def __init__(self):
        plt.style.use('seaborn-v0_8')
        self.colors = plt.cm.tab10.colors
    
    def plot_runtime_comparison(self, algorithms_data):
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()
        
        for idx, (algo_name, data) in enumerate(algorithms_data.items()):
            if idx >= 6:
                break
            
            ax = axes[idx]
            
            sizes = data['sizes']
            times = data['times']
            
            ax.plot(sizes, times, 'o-', linewidth=2, markersize=6,
                   color=self.colors[idx % len(self.colors)])
            
            ax.set_xlabel('Input Size', fontsize=10)
            ax.set_ylabel('Time (seconds)', fontsize=10)
            ax.set_title(algo_name, fontsize=12, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            if max(times) / min(times) > 100:
                ax.set_yscale('log')
        
        plt.suptitle('Algorithm Runtime Comparison', fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig
    
    def plot_scalability_analysis(self, scalability_data):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        algorithms = list(scalability_data.keys())
        n_algorithms = len(algorithms)
        
        bar_width = 0.35
        index = np.arange(n_algorithms)
        
        efficiency_scores = [scalability_data[algo]['efficiency'] for algo in algorithms]
        scalability_scores = [scalability_data[algo]['scalability'] for algo in algorithms]
        
        bars1 = ax1.bar(index, efficiency_scores, bar_width, label='Efficiency', color='skyblue')
        bars2 = ax1.bar(index + bar_width, scalability_scores, bar_width, label='Scalability', color='lightcoral')
        
        ax1.set_xlabel('Algorithm', fontsize=12)
        ax1.set_ylabel('Score (0-100)', fontsize=12)
        ax1.set_title('Algorithm Efficiency & Scalability', fontsize=14, fontweight='bold')
        ax1.set_xticks(index + bar_width / 2)
        ax1.set_xticklabels(algorithms, rotation=45, ha='right')
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')
        
        for i, (eff, scal) in enumerate(zip(efficiency_scores, scalability_scores)):
            ax1.text(i, eff + 1, f'{eff:.0f}', ha='center', fontsize=9)
            ax1.text(i + bar_width, scal + 1, f'{scal:.0f}', ha='center', fontsize=9)
        
        sizes = scalability_data[algorithms[0]]['sizes']
        
        for i, algo in enumerate(algorithms):
            times = scalability_data[algo]['times']
            color = self.colors[i % len(self.colors)]
            ax2.plot(sizes, times, 'o-', linewidth=2, markersize=4, label=algo, color=color)
        
        ax2.set_xlabel('Input Size', fontsize=12)
        ax2.set_ylabel('Time (seconds, log scale)', fontsize=12)
        ax2.set_title('Scalability Curves', fontsize=14, fontweight='bold')
        ax2.set_yscale('log')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_memory_usage(self, memory_data):
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        algorithms = list(memory_data.keys())
        sizes = memory_data[algorithms[0]]['sizes']
        
        for i, algo in enumerate(algorithms):
            memory = memory_data[algo]['memory']
            color = self.colors[i % len(self.colors)]
            axes[0].plot(sizes, memory, 's-', linewidth=2, markersize=5, label=algo, color=color)
        
        axes[0].set_xlabel('Input Size', fontsize=12)
        axes[0].set_ylabel('Memory Usage (MB)', fontsize=12)
        axes[0].set_title('Memory Usage Comparison', fontsize=14, fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        last_size_index = -1
        last_memory = [memory_data[algo]['memory'][last_size_index] for algo in algorithms]
        
        bars = axes[1].bar(algorithms, last_memory, color=self.colors[:len(algorithms)])
        axes[1].set_xlabel('Algorithm', fontsize=12)
        axes[1].set_ylabel(f'Memory at n={sizes[last_size_index]} (MB)', fontsize=12)
        axes[1].set_title(f'Memory Usage (n={sizes[last_size_index]})', fontsize=14, fontweight='bold')
        axes[1].grid(True, alpha=0.3, axis='y')
        
        for bar, mem in zip(bars, last_memory):
            height = bar.get_height()
            axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{mem:.1f}', ha='center', va='bottom', fontsize=10)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
    
    def plot_benchmark_results(self, benchmark_results):
        fig = plt.figure(figsize=(16, 12))
        
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        ax1 = fig.add_subplot(gs[0, :])
        ax2 = fig.add_subplot(gs[1, 0])
        ax3 = fig.add_subplot(gs[1, 1])
        ax4 = fig.add_subplot(gs[1, 2])
        ax5 = fig.add_subplot(gs[2, :])
        
        algorithms = benchmark_results['algorithms']
        sizes = benchmark_results['sizes']
        
        times_matrix = benchmark_results['times']
        
        im = ax1.imshow(times_matrix, aspect='auto', cmap='viridis')
        ax1.set_xlabel('Input Size', fontsize=12)
        ax1.set_ylabel('Algorithm', fontsize=12)
        ax1.set_title('Performance Heatmap', fontsize=14, fontweight='bold')
        ax1.set_xticks(np.arange(len(sizes)))
        ax1.set_yticks(np.arange(len(algorithms)))
        ax1.set_xticklabels(sizes)
        ax1.set_yticklabels(algorithms)
        plt.colorbar(im, ax=ax1, label='Time (seconds)')
        
        avg_times = np.mean(times_matrix, axis=1)
        ax2.barh(algorithms, avg_times, color='steelblue')
        ax2.set_xlabel('Average Time (seconds)', fontsize=10)
        ax2.set_title('Average Performance', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')
        
        std_times = np.std(times_matrix, axis=1)
        ax3.bar(algorithms, std_times, color='coral')
        ax3.set_xlabel('Algorithm', fontsize=10)
        ax3.set_ylabel('Time Std Dev', fontsize=10)
        ax3.set_title('Performance Consistency', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')
        plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
        
        best_times = np.min(times_matrix, axis=1)
        worst_times = np.max(times_matrix, axis=1)
        
        x = np.arange(len(algorithms))
        ax4.bar(x - 0.2, best_times, 0.4, label='Best', color='lightgreen')
        ax4.bar(x + 0.2, worst_times, 0.4, label='Worst', color='lightcoral')
        ax4.set_xlabel('Algorithm', fontsize=10)
        ax4.set_ylabel('Time (seconds)', fontsize=10)
        ax4.set_title('Best vs Worst Case', fontsize=12, fontweight='bold')
        ax4.set_xticks(x)
        ax4.set_xticklabels(algorithms, rotation=45, ha='right')
        ax4.legend()
        ax4.grid(True, alpha=0.3, axis='y')
        
        for i, algo in enumerate(algorithms):
            ax5.plot(sizes, times_matrix[i], 'o-', linewidth=2, markersize=4,
                    label=algo, color=self.colors[i % len(self.colors)])
        
        ax5.set_xlabel('Input Size', fontsize=12)
        ax5.set_ylabel('Time (seconds)', fontsize=12)
        ax5.set_title('Detailed Performance Curves', fontsize=14, fontweight='bold')
        ax5.legend(fontsize=10)
        ax5.grid(True, alpha=0.3)
        
        if np.max(times_matrix) / np.min(times_matrix) > 100:
            ax5.set_yscale('log')
        
        plt.suptitle('Comprehensive Benchmark Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        return fig
    
    def create_performance_report(self, all_data):
        report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        fig = plt.figure(figsize=(18, 14))
        
        fig.suptitle(f'Performance Analysis Report\nGenerated: {report_time}',
                    fontsize=18, fontweight='bold')
        
        gs = fig.add_gridspec(4, 4, hspace=0.4, wspace=0.4)
        
        ax1 = fig.add_subplot(gs[0, :2])
        ax2 = fig.add_subplot(gs[0, 2:])
        ax3 = fig.add_subplot(gs[1, :2])
        ax4 = fig.add_subplot(gs[1, 2:])
        ax5 = fig.add_subplot(gs[2, :])
        ax6 = fig.add_subplot(gs[3, :])
        
        runtime_data = all_data.get('runtime', {})
        if runtime_data:
            for algo, data in runtime_data.items():
                ax1.plot(data['sizes'], data['times'], 'o-', linewidth=2, label=algo)
            ax1.set_title('Runtime Performance', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Input Size')
            ax1.set_ylabel('Time (seconds)')
            ax1.legend(fontsize=9)
            ax1.grid(True, alpha=0.3)
        
        memory_data = all_data.get('memory', {})
        if memory_data:
            for algo, data in memory_data.items():
                ax2.plot(data['sizes'], data['memory'], 's-', linewidth=2, label=algo)
            ax2.set_title('Memory Usage', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Input Size')
            ax2.set_ylabel('Memory (MB)')
            ax2.legend(fontsize=9)
            ax2.grid(True, alpha=0.3)
        
        if 'efficiency' in all_data:
            algorithms = list(all_data['efficiency'].keys())
            scores = [all_data['efficiency'][algo] for algo in algorithms]
            bars = ax3.bar(algorithms, scores, color='lightblue')
            ax3.set_title('Algorithm Efficiency Scores', fontsize=14, fontweight='bold')
            ax3.set_ylabel('Score (0-100)')
            ax3.grid(True, alpha=0.3, axis='y')
            for bar, score in zip(bars, scores):
                ax3.text(bar.get_x() + bar.get_width()/2., score + 1,
                        f'{score:.0f}', ha='center', fontsize=9)
            plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
        
        if 'complexity' in all_data:
            complexity_types = list(all_data['complexity'].keys())
            counts = list(all_data['complexity'].values())
            ax4.pie(counts, labels=complexity_types, autopct='%1.1f%%')
            ax4.set_title('Complexity Class Distribution', fontsize=14, fontweight='bold')
        
        if 'comparison' in all_data:
            comparison_data = all_data['comparison']
            x = np.arange(len(comparison_data['labels']))
            width = 0.35
            
            bars1 = ax5.bar(x - width/2, comparison_data['values1'], width, label='P Problems')
            bars2 = ax5.bar(x + width/2, comparison_data['values2'], width, label='NP Problems')
            
            ax5.set_title('P vs NP Comparison', fontsize=14, fontweight='bold')
            ax5.set_xticks(x)
            ax5.set_xticklabels(comparison_data['labels'], rotation=45, ha='right')
            ax5.legend()
            ax5.grid(True, alpha=0.3, axis='y')
        
        summary_text = "Performance Summary:\n\n"
        if 'summary' in all_data:
            for key, value in all_data['summary'].items():
                summary_text += f"{key}: {value}\n"
        
        ax6.text(0.02, 0.98, summary_text, fontsize=11,
                transform=ax6.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
        ax6.axis('off')
        ax6.set_title('Executive Summary', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        return fig
