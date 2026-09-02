import requests

from rag.retrieve import retrieve_plans

OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "qwen3:0.6b"


def build_context(results):
    documents = results["documents"][0]

    context = []

    for document in documents:
        context.append(document)

    return "\n\n---\n\n".join(context)


def ask_ollama(question, context):
    prompt = f"""
You are an AI assistant for a production planning optimization system.

Your job is to analyze production plans retrieved from the system and answer the user's question using only the provided information.

SCORING MECHANISM:

The score is calculated as follows:

1. For each order:
   lateness = max(0, final_end_time - deadline)

2. The score adds the lateness of all orders.

3. If two operations of the same operation type run at the same time on different workplaces, the overlapping time is added to the score.

Therefore:

- Lower score is better.
- A score of 0 means there is no lateness and no detected overlap penalty.
- Two different plans can have the same score.
- Equal scores do NOT necessarily mean the plans are identical.
- Do not invent other scoring criteria.

-Only use information contained in the retrieved plans and project context.
-Do not invent reasons for a score.
-If the retrieved information does not explain something, explicitly say that it is not available.

RETRIEVED PRODUCTION PLANS:

{context}

USER QUESTION:

{question}

RULES FOR YOUR ANSWER:

- Use only the retrieved plans and the scoring mechanism above.
- Never mention a plan that is not present in the retrieved plans.
- If the user asks you to compare plans, compare the actual sequence, workplace assignments, and schedules.
- If two plans have the same score, explain that they have the same numerical score according to the scoring function, even if their schedules or workplace assignments differ.
- Do not invent values, operations, workplaces, times, or scores.
- If the retrieved plans do not contain enough information to answer, say that the available retrieved plans are insufficient.
- When making a comparison, explicitly name the plans being compared.
- Give concrete reasoning based on the actual data.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    return response.json()["response"]

def ask_question(question):
    results = retrieve_plans(question)

    context = build_context(results)

    answer = ask_ollama(
        question,
        context
    )

    return answer


if __name__ == "__main__":
    question = input(
        "Ask about the production plans: "
    )

    answer = ask_question(question)

    print("\n--- Answer ---")
    print(answer)