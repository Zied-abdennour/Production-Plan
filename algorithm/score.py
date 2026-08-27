def calculate_score(schedule, orders): 
    score = 0 
    order_final_end = {} 
    for order_name, op, workplace, start, end in schedule: 
        if order_name not in order_final_end or end > order_final_end[order_name]: 
            order_final_end[order_name] = end 
 
    for order_name, final_end in order_final_end.items(): 
        deadline = orders[order_name]["deadline"] 
        lateness = max(0, final_end - deadline) 
        score += lateness 
 
    for i in range(len(schedule)): 
        for j in range(i + 1, len(schedule)): 
            order1, op1, wp1, start1, end1 = schedule[i] 
            order2, op2, wp2, start2, end2 = schedule[j] 
            if op1 == op2 and wp1 != wp2: 
                overlap = min(end1, end2) - max(start1, start2) 
                if overlap > 0: 
                    score += overlap  
    return score