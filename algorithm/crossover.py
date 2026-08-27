import random 

def precedence_crossover(parent1_seq, parent2_seq): 
    child = [] 
    p1 = parent1_seq.copy() 
    p2 = parent2_seq.copy() 
     
    while p1 or p2: 
        if p1 and p2: 
            chosen_parent = random.choice([p1, p2]) 
        elif p1: 
            chosen_parent = p1 
        else: 
            chosen_parent = p2 
         
        gene = chosen_parent.pop(0) 
        child.append(gene) 
         
        if gene in p1: 
            p1.remove(gene) 
        if gene in p2: 
            p2.remove(gene) 
     
    return child 
 
def crossover_workplaces(child_sequence, parent1_choices, parent2_choices): 
    child_choices = {} 
    for order_name, op in child_sequence: 
        key = (order_name, op) 
        child_choices[key] = random.choice([parent1_choices[key], parent2_choices[key]]) 
 
    return child_choices