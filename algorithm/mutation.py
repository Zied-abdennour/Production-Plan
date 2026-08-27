import random 

def mutate_sequence(sequence, mutation_rate): 
    seq = sequence.copy() 
    if random.random() < mutation_rate: 
        i, j = random.sample(range(len(seq)), 2) 
        if seq[i][0] != seq[j][0]: 
            seq[i], seq[j] = seq[j], seq[i] 
    return seq 
 
def mutate_workplaces(choices, operation_workplaces, mutation_rate): 
    new_choices = choices.copy() 
    if random.random() < mutation_rate: 
        all_keys = list(new_choices.keys()) 
        chosen_key = random.choice(all_keys) 
        op = chosen_key[1] 
        eligible = operation_workplaces[op] 
        new_workplace = random.choice(eligible) 
        new_choices[chosen_key] = new_workplace 
    return new_choices