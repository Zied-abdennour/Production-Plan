import json
import requests
import chromadb

import algorithm.genetic_algorithm as ga
from algorithm.decoder import decode_all

PLANS_FILE = "data/plans.json"
OLLAMA_URL = "http://localhost:11434/api/embed"
EMBEDDING_MODEL = "nomic-embed-text"


def save_equal_score_plans(orders, product_operations, rates):
    population = ga.last_population

    if not population:
        print("No population available.")
        return

    score_groups = {}

    for sequence, workplace_choices, score in population:
        score_key = round(score, 6)

        if score_key not in score_groups:
            score_groups[score_key] = []

        score_groups[score_key].append(
            (sequence, workplace_choices, score)
        )

    equal_score_groups = [
        group
        for group in score_groups.values()
        if len(group) >= 2
    ]

    plans = []
    plan_number = 1

    for group in equal_score_groups:
        for sequence, workplace_choices, score in group:

            schedule = decode_all(
                sequence,
                workplace_choices,
                orders,
                product_operations,
                rates
            )

            workplace_assignment = {}

            for key, workplace in workplace_choices.items():
                order_name, operation = key
                assignment_key = f"{order_name}_{operation}"
                workplace_assignment[assignment_key] = workplace

            plan = {
                "plan_id": f"Plan_{plan_number:02d}",
                "score": score,
                "sequence": [
                    {
                        "order": item[0],
                        "operation": item[1]
                    }
                    for item in sequence
                ],
                "workplace_assignment": workplace_assignment,
                "schedule": [
                    {
                        "order": item[0],
                        "operation": item[1],
                        "workplace": item[2],
                        "start": item[3],
                        "end": item[4]
                    }
                    for item in schedule
                ]
            }

            plans.append(plan)
            plan_number += 1

    data = {
        "best_score": min(
            plan["score"] for plan in plans
        ) if plans else None,
        "number_of_equal_plans": len(plans),
        "plans": plans
    }

    with open(
        PLANS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=2
        )

    print(
        f"Saved {len(plans)} equal-score plans."
    )


def load_plans():
    with open(
        PLANS_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    return data["plans"]


def plan_to_text(plan):
    text = []

    text.append(
        f"Production plan {plan['plan_id']}."
    )

    text.append(
        f"Score: {plan['score']}."
    )

    text.append(
        "Production sequence:"
    )

    for item in plan["sequence"]:
        text.append(
            f"{item['order']} -> {item['operation']}"
        )

    text.append(
        "Workplace assignments:"
    )

    for key, workplace in plan[
        "workplace_assignment"
    ].items():
        text.append(
            f"{key} -> {workplace}"
        )

    text.append(
        "Schedule:"
    )

    for item in plan["schedule"]:
        text.append(
            f"{item['order']} -> "
            f"{item['operation']} -> "
            f"{item['workplace']} "
            f"from {item['start']} "
            f"to {item['end']}"
        )

    return "\n".join(text)


def create_embeddings(texts):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": EMBEDDING_MODEL,
            "input": texts
        }
    )

    response.raise_for_status()

    return response.json()["embeddings"]


def store_plans():
    plans = load_plans()

    if not plans:
        print("No plans found in plans.json.")
        return

    documents = []
    ids = []
    metadatas = []

    for plan in plans:
        documents.append(
            plan_to_text(plan)
        )

        ids.append(
            plan["plan_id"]
        )

        metadatas.append(
            {
                "plan_id": plan["plan_id"],
                "score": plan["score"]
            }
        )

    embeddings = create_embeddings(
        documents
    )

    client = chromadb.PersistentClient(
        path="data/chroma"
    )

    collection = client.get_or_create_collection(
        name="production_plans"
    )

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(
        f"Stored {len(plans)} production plans."
    )


if __name__ == "__main__":
    store_plans()