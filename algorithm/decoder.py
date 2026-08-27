import random 

def random_valid_sequence(orders, product_operations): 
    sequence = [] 
    progress = {} 
     
    for order_name in orders: 
        progress[order_name] = 0 
     
    remaining_orders = list(orders.keys()) 
     
    while remaining_orders: 
        order_name = random.choice(remaining_orders) 
        product = orders[order_name]["product"] 
        operations = product_operations[product] 
         
        next_op_index = progress[order_name] 
        next_op = operations[next_op_index] 
         
        sequence.append((order_name, next_op)) 
        progress[order_name] += 1 
         
        if progress[order_name] == len(operations): 
            remaining_orders.remove(order_name) 
     
    return sequence 
 
def random_workplace_choices(sequence, operation_workplaces): 
    choices = {} 
    for order_name, op in sequence: 
        eligible = operation_workplaces[op] 
        choices[(order_name, op)] = random.choice(eligible) 
 
    return choices 
 
def decode_all(sequence, workplace_choices, orders, product_operations, rates): 
    workplace_free = {} 
    schedule = [] 
    order_progress_time = {} 
 
    for order_name, op in sequence: 
        order = orders[order_name] 
        product = order["product"] 
        operations = product_operations[product] 
        rate_key = op + "_" + product 
        rate = rates[rate_key] 
        duration = order["quantity"] / rate 
        current_time = order_progress_time.get(order_name, 0) 
        workplace = workplace_choices[(order_name, op)] 
        wp_free = workplace_free.get(workplace, 0) 
 
        start = max(current_time, wp_free) 
        end = start + duration 
 
        schedule.append((order_name, op, workplace, round(start, 2), round(end, 2))) 
 
        order_progress_time[order_name] = end 
        workplace_free[workplace] = end 
 
    return schedule