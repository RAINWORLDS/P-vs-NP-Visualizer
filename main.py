import sys
import os
from src.simulations.interactive_demo import InteractiveSimulation

def main():
    print("=" * 60)
    print("P vs NP VISUALIZER")
    print("=" * 60)
    print("\nInteractive tool for understanding computational complexity")
    
    sim = InteractiveSimulation()
    sim.create_interactive_session()

if __name__ == "__main__":
    main()
