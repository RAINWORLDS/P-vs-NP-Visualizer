import itertools
import random
import time
import math
from typing import List, Tuple, Dict, Optional
import heapq

class TravelingSalesman:
    
    def __init__(self):
        self.cities = {}
    
    def add_city(self, name, x, y):
        self.cities[name] = (x, y)
    
    def distance(self, city1, city2):
        x1, y1 = self.cities[city1]
        x2, y2 = self.cities[city2]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def create_random_cities(self, n_cities=8, grid_size=100):
        self.cities = {}
        for i in range(n_cities):
            x = random.randint(0, grid_size)
            y = random.randint(0, grid_size)
            self.cities[f"City_{i}"] = (x, y)
        return self.cities
    
    def brute_force_tsp(self):
        if len(self.cities) < 2:
            return None, 0, 0
        
        cities_list = list(self.cities.keys())
        if len(cities_list) > 10:
            return None, 0, math.factorial(len(cities_list))
        
        min_distance = float('inf')
        best_path = None
        steps = 0
        
        for perm in itertools.permutations(cities_list):
            steps += 1
            distance = 0
            valid = True
            
            for i in range(len(perm)):
                if i == len(perm) - 1:
                    distance += self.distance(perm[i], perm[0])
                else:
                    distance += self.distance(perm[i], perm[i + 1])
                
            if distance < min_distance:
                min_distance = distance
                best_path = perm
        
        return best_path, min_distance, steps
    
    def nearest_neighbor(self):
        if not self.cities:
            return None, 0, 0
        
        cities_list = list(self.cities.keys())
        start = cities_list[0]
        unvisited = set(cities_list)
        unvisited.remove(start)
        
        path = [start]
        total_distance = 0
        steps = 0
        
        current = start
        
        while unvisited:
            steps += 1
            nearest = None
            min_dist = float('inf')
            
            for city in unvisited:
                dist = self.distance(current, city)
                if dist < min_dist:
                    min_dist = dist
                    nearest = city
            
            total_distance += min_dist
            path.append(nearest)
            unvisited.remove(nearest)
            current = nearest
        
        total_distance += self.distance(path[-1], path[0])
        steps += len(self.cities) * len(self.cities)
        
        return path, total_distance, steps
    
    def simulated_annealing(self, initial_temp=1000, cooling_rate=0.995, iterations=1000):
        if len(self.cities) < 2:
            return None, 0, 0
        
        cities_list = list(self.cities.keys())
        current_path = cities_list.copy()
        random.shuffle(current_path)
        
        def path_distance(path):
            dist = 0
            for i in range(len(path)):
                if i == len(path) - 1:
                    dist += self.distance(path[i], path[0])
                else:
                    dist += self.distance(path[i], path[i + 1])
            return dist
        
        current_distance = path_distance(current_path)
        best_path = current_path.copy()
        best_distance = current_distance
        steps = 0
        
        temperature = initial_temp
        
        for _ in range(iterations):
            steps += 1
            
            new_path = current_path.copy()
            i, j = random.sample(range(len(new_path)), 2)
            new_path[i], new_path[j] = new_path[j], new_path[i]
            
            new_distance = path_distance(new_path)
            
            if new_distance < current_distance:
                current_path = new_path
                current_distance = new_distance
                
                if new_distance < best_distance:
                    best_path = new_path.copy()
                    best_distance = new_distance
            else:
                probability = math.exp((current_distance - new_distance) / temperature)
                if random.random() < probability:
                    current_path = new_path
                    current_distance = new_distance
            
            temperature *= cooling_rate
        
        return best_path, best_distance, steps
    
    def measure_complexity(self, max_cities=10):
        results = []
        
        for n in range(2, max_cities + 1):
            self.create_random_cities(n)
            
            start_time = time.time()
            path, distance, steps = self.brute_force_tsp()
            end_time = time.time()
            
            if path:
                results.append({
                    'n_cities': n,
                    'brute_force_time': end_time - start_time,
                    'brute_force_steps': steps,
                    'brute_force_distance': distance,
                    'factorial': math.factorial(n),
                    'possible_paths': math.factorial(n - 1)
                })
            
            start_time = time.time()
            path_nn, distance_nn, steps_nn = self.nearest_neighbor()
            end_time = time.time()
            
            results[-1]['nearest_neighbor_time'] = end_time - start_time
            results[-1]['nearest_neighbor_steps'] = steps_nn
            results[-1]['nearest_neighbor_distance'] = distance_nn
        
        return results
    
    def generate_tsp_instance(self, n_cities, difficulty='medium'):
        self.create_random_cities(n_cities)
        
        distances = {}
        for city1 in self.cities:
            distances[city1] = {}
            for city2 in self.cities:
                if city1 != city2:
                    distances[city1][city2] = self.distance(city1, city2)
        
        return {
            'cities': self.cities,
            'distances': distances,
            'n_cities': n_cities,
            'difficulty': difficulty
        }
