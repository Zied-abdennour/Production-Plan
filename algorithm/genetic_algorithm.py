import random

from algorithm.decoder import random_valid_sequence, random_workplace_choices, decode_all
from algorithm.score import calculate_score
from algorithm.crossover import precedence_crossover, crossover_workplaces
from algorithm.mutation import mutate_sequence, mutate_workplaces

 
def generate_population(size, orders, product_operations, operation_workplaces, rates): 
    population = [] 
    for i in range(size): 
        sequence = random_valid_sequence(orders, product_operations) 
        workplace_choices = random_workplace_choices(sequence, operation_workplaces) 
        schedule = decode_all(sequence, workplace_choices, orders, product_operations, rates) 
        score = calculate_score(schedule, orders) 
        population.append((sequence, workplace_choices, score)) 
 
    return population 
 
def genetic_algorithm(generations, population_size, selection_percent, mutation_rate, orders, product_operations, operation_workplaces, rates): 
    population = generate_population(population_size, orders, product_operations, operation_workplaces, rates) 
     
    top_n = int(population_size * selection_percent) 
     
    for gen in range(generations): 
        population.sort(key=lambda ind: ind[2]) 
        best_score = population[0][2] 
        print(f"Generation {gen}: best score = {best_score}") 
         
        new_population = [] 
        new_population.append(population[0]) 
         
        while len(new_population) < population_size: 
            parent1 = random.choice(population[:top_n]) 
            parent2 = random.choice(population[:top_n]) 
             
            child_seq = precedence_crossover(parent1[0], parent2[0]) 
            child_seq = mutate_sequence(child_seq, mutation_rate) 
             
            child_choices = crossover_workplaces(child_seq, parent1[1], parent2[1]) 
            child_choices = mutate_workplaces(child_choices, operation_workplaces, mutation_rate) 
             
            child_schedule = decode_all(child_seq, child_choices, orders, product_operations, rates) 
            child_score = calculate_score(child_schedule, orders) 
             
            new_population.append((child_seq, child_choices, child_score)) 
         
        population = new_population 
     
    population.sort(key=lambda ind: ind[2])
    global last_population
    last_population = population.copy()
    return population[0]