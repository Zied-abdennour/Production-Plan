import json
import os


PLANS_FILE = "data/plans.json"


def load_plans():
    if not os.path.exists(PLANS_FILE):
        return []

    with open(PLANS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def retrieve_equal_score_plans(score, plans):
    return [
        plan
        for plan in plans
        if plan.get("score") == score
    ]


def retrieve_plan_by_score(score):
    plans = load_plans()

    return retrieve_equal_score_plans(
        score,
        plans
    )


def format_plan(plan):
    sequence = plan.get("sequence", [])
    assignments = plan.get("workplace_assignment", {})
    schedule = plan.get("schedule", [])

    text = []

    text.append(f"Score: {plan.get('score')}")

    text.append("\nProduction sequence:")

    for order, operation in sequence:
        text.append(
            f"{order} -> {operation}"
        )

    text.append("\nWorkplace assignments:")

    for key, workplace in assignments.items():
        text.append(
            f"{key} -> {workplace}"
        )

    text.append("\nSchedule:")

    for item in schedule:
        text.append(
            f"{item['order']} -> "
            f"{item['operation']} -> "
            f"{item['workplace']} | "
            f"{item['start']} -> {item['end']}"
        )

    return "\n".join(text)


def build_context(plans):
    if not plans:
        return "No relevant production plans were found."

    context = []

    for i, plan in enumerate(plans, 1):
        context.append(
            f"--- Plan {i} ---\n"
            f"{format_plan(plan)}"
        )

    return "\n\n".join(context)