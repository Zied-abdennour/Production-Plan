import json
import os

import algorithm.genetic_algorithm as ga
from algorithm.decoder import decode_all


def save_equal_score_plans(orders, product_operations, rates, output_path="data/plans.json"):
    if not ga.last_population:
        print("RAG: final population is empty")
        return False

    best_score = ga.last_population[0][2]

    equal_plans = [
        individual for individual in ga.last_population
        if abs(individual[2] - best_score) < 0.01
    ]

    plans = []

    for index, individual in enumerate(equal_plans, start=1):
        sequence = individual[0]
        workplace_choices = individual[1]
        score = individual[2]

        schedule = decode_all(sequence, workplace_choices, orders, product_operations, rates)

        sequence_data = [
            {
                "order": order_name,
                "operation": operation
            }
            for order_name, operation in sequence
        ]

        workplace_data = [
            {
                "order": order_name,
                "operation": operation,
                "workplace": workplace_choices[(order_name, operation)]
            }
            for order_name, operation in sequence
        ]

        schedule_data = [
            {
                "order": order_name,
                "operation": operation,
                "workplace": workplace,
                "start": start,
                "end": end
            }
            for order_name, operation, workplace, start, end in schedule
        ]

        plans.append({
            "plan_id": f"Plan_{index:02d}",
            "score": score,
            "sequence": sequence_data,
            "workplace_assignments": workplace_data,
            "schedule": schedule_data
        })

    data = {
        "best_score": best_score,
        "number_of_equal_plans": len(plans),
        "plans": plans
    }

    folder = os.path.dirname(output_path)

    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"RAG: saved {len(plans)} plans to {output_path}")

    return True