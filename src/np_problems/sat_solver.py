import itertools
import random
import time
from typing import List, Tuple, Dict, Set

class SATSolver:
    
    def __init__(self):
        self.variables = set()
        self.clauses = []
    
    def add_clause(self, clause):
        self.clauses.append(clause)
        for literal in clause:
            var = literal.strip('-')
            self.variables.add(var)
    
    def create_random_sat(self, n_vars=10, n_clauses=20, clause_size=3):
        self.variables = {f'x{i}' for i in range(n_vars)}
        self.clauses = []
        
        for _ in range(n_clauses):
            clause = []
            vars_sample = random.sample(list(self.variables), min(clause_size, n_vars))
            
            for var in vars_sample:
                if random.random() < 0.5:
                    clause.append(f'-{var}')
                else:
                    clause.append(var)
            
            self.clauses.append(clause)
        
        return self.clauses
    
    def brute_force_solve(self):
        if not self.variables:
            return False, {}, 0
        
        variables_list = list(self.variables)
        n = len(variables_list)
        steps = 0
        
        for i in range(2 ** n):
            steps += 1
            assignment = {}
            
            for j, var in enumerate(variables_list):
                assignment[var] = bool((i >> j) & 1)
            
            all_clauses_satisfied = True
            
            for clause in self.clauses:
                clause_satisfied = False
                
                for literal in clause:
                    var = literal.strip('-')
                    
                    if literal.startswith('-'):
                        if not assignment[var]:
                            clause_satisfied = True
                            break
                    else:
                        if assignment[var]:
                            clause_satisfied = True
                            break
                
                if not clause_satisfied:
                    all_clauses_satisfied = False
                    break
            
            if all_clauses_satisfied:
                return True, assignment, steps
        
        return False, {}, steps
    
    def dpll_solve(self):
        if not self.clauses:
            return True, {}, 0
        
        steps = [0]
        
        def simplify(clauses, var, value):
            new_clauses = []
            for clause in clauses:
                new_clause = []
                satisfied = False
                
                for literal in clause:
                    lit_var = literal.strip('-')
                    
                    if lit_var == var:
                        if (value and not literal.startswith('-')) or (not value and literal.startswith('-')):
                            satisfied = True
                            break
                        else:
                            continue
                    
                    new_clause.append(literal)
                
                if not satisfied:
                    new_clauses.append(new_clause)
            
            return new_clauses
        
        def dpll_recursive(clauses, assignment):
            steps[0] += 1
            
            if not clauses:
                return True, assignment
            
            for clause in clauses:
                if not clause:
                    return False, None
            
            unit_clauses = [c for c in clauses if len(c) == 1]
            for unit in unit_clauses:
                literal = unit[0]
                var = literal.strip('-')
                value = not literal.startswith('-')
                
                if var in assignment:
                    if assignment[var] != value:
                        return False, None
                    continue
                
                assignment[var] = value
                new_clauses = simplify(clauses, var, value)
                result, new_assignment = dpll_recursive(new_clauses, assignment.copy())
                
                if result:
                    assignment.update(new_assignment)
                    return True, assignment
            
            pure_literals = {}
            for clause in clauses:
                for literal in clause:
                    var = literal.strip('-')
                    is_positive = not literal.startswith('-')
                    
                    if var not in pure_literals:
                        pure_literals[var] = is_positive
                    elif pure_literals[var] != is_positive:
                        pure_literals[var] = None
            
            for var, value in pure_literals.items():
                if value is not None and var not in assignment:
                    assignment[var] = value
                    new_clauses = simplify(clauses, var, value)
                    result, new_assignment = dpll_recursive(new_clauses, assignment.copy())
                    
                    if result:
                        assignment.update(new_assignment)
                        return True, assignment
            
            var_to_assign = None
            for clause in clauses:
                for literal in clause:
                    var = literal.strip('-')
                    if var not in assignment:
                        var_to_assign = var
                        break
                if var_to_assign:
                    break
            
            if not var_to_assign:
                return True, assignment
            
            for value in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[var_to_assign] = value
                new_clauses = simplify(clauses, var_to_assign, value)
                result, final_assignment = dpll_recursive(new_clauses, new_assignment)
                
                if result:
                    new_assignment.update(final_assignment)
                    return True, new_assignment
            
            return False, None
        
        initial_assignment = {}
        result, assignment = dpll_recursive(self.clauses, initial_assignment)
        
        return result, assignment, steps[0]
    
    def measure_performance(self, n_vars_range=(3, 12)):
        results = []
        
        for n_vars in range(n_vars_range[0], n_vars_range[1] + 1):
            self.create_random_sat(n_vars, n_vars * 2, 3)
            
            start_time = time.time()
            found_bf, assignment_bf, steps_bf = self.brute_force_solve()
            end_time = time.time()
            
            start_time_dpll = time.time()
            found_dpll, assignment_dpll, steps_dpll = self.dpll_solve()
            end_time_dpll = time.time()
            
            results.append({
                'n_vars': n_vars,
                'n_clauses': len(self.clauses),
                'brute_force_time': end_time - start_time,
                'brute_force_steps': steps_bf,
                'brute_force_found': found_bf,
                'dpll_time': end_time_dpll - start_time_dpll,
                'dpll_steps': steps_dpll,
                'dpll_found': found_dpll,
                'possible_assignments': 2 ** n_vars
            })
        
        return results
    
    def generate_3sat_instance(self, n_vars, n_clauses):
        self.create_random_sat(n_vars, n_clauses, 3)
        return {
            'variables': list(self.variables),
            'clauses': self.clauses,
            'is_3sat': all(len(clause) == 3 for clause in self.clauses)
        }
