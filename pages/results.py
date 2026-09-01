import streamlit as st

from gui.style import apply_style, page_header
from algorithm.genetic_algorithm import genetic_algorithm
from algorithm.decoder import decode_all
from rag.plan_store import save_equal_score_plans, store_plans

apply_style()

page_header(
    "Optimization Results",
    "Run the genetic algorithm and inspect the optimized production schedule."
)

orders = st.session_state.get("orders", {})
product_operations = st.session_state.get("product_operations", {})
operation_workplaces = st.session_state.get("operation_workplaces", {})
rates = st.session_state.get("rates", {})
workplaces = st.session_state.get("workplaces", [])
parameters = st.session_state.get("parameters", {})

if not orders or not product_operations or not operation_workplaces or not rates:
    st.warning("Complete the production data before running the algorithm.")
    st.stop()

if not parameters:
    parameters = {
        "generations": 100,
        "population_size": 50,
        "selection_percent": 0.2,
        "mutation_rate": 0.1
    }

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Orders", len(orders))

with col2:
    st.metric("Operations", len(product_operations))

with col3:
    st.metric("Workplaces", len(workplaces))

st.markdown("<br>", unsafe_allow_html=True)

if st.button(
    "Run Genetic Algorithm",
    type="primary",
    width="stretch"
):
    result = genetic_algorithm(
        parameters["generations"],
        parameters["population_size"],
        parameters["selection_percent"],
        parameters["mutation_rate"],
        orders,
        product_operations,
        operation_workplaces,
        rates
    )

    if result is None:
        st.error("The genetic algorithm did not return a valid result.")
        st.session_state.pop("best_result", None)
        st.stop()

    if not isinstance(result, tuple) or len(result) != 3:
        st.error("The genetic algorithm returned an invalid result.")
        st.session_state.pop("best_result", None)
        st.stop()

    st.session_state.best_result = result

    save_equal_score_plans(
        orders,
        product_operations,
        rates
    )

    try:
        store_plans()
        st.success("Optimization completed.")
        st.success("Equal-score plans stored in the RAG database.")
    except Exception as e:
        st.success("Optimization completed.")
        st.warning(f"RAG storage failed: {e}")

if "best_result" not in st.session_state:
    st.info("Click Run Genetic Algorithm to generate a production schedule.")
    st.stop()

result = st.session_state.best_result

if not isinstance(result, tuple) or len(result) != 3:
    st.error("The stored optimization result is invalid. Run the algorithm again.")
    st.session_state.pop("best_result", None)
    st.stop()

best_sequence, best_choices, best_score = result

schedule = decode_all(
    best_sequence,
    best_choices,
    orders,
    product_operations,
    rates
)

if not schedule:
    st.warning("No schedule was generated.")
    st.stop()

st.markdown(
    f"""
    <div class="result-score">
        <div class="result-score-label">Best Score</div>
        <div class="result-score-value">{best_score:.2f}</div>
        <div class="result-score-description">
            Lower score = better schedule
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("Production Timeline")

max_time = max(item[4] for item in schedule)

if max_time <= 0:
    max_time = 1

timeline_workplaces = list(workplaces)

for item in schedule:
    if item[2] not in timeline_workplaces:
        timeline_workplaces.append(item[2])

timeline_workplaces = list(dict.fromkeys(timeline_workplaces))

timeline_html = """
<div class="production-timeline">
<div class="timeline-inner">
<div class="timeline-axis-row">
<div class="timeline-axis-label">Time</div>
<div class="timeline-axis">
"""

for i in range(11):
    percent = i * 10
    time_value = max_time * percent / 100

    timeline_html += f"""
    <div
        class="timeline-axis-line"
        style="left:{percent}%"
    ></div>

    <div
        class="timeline-axis-value"
        style="left:{percent}%"
    >
        {time_value:.0f}
    </div>
    """

timeline_html += """
</div>
</div>
"""

for workplace in timeline_workplaces:

    timeline_html += f"""
    <div class="timeline-row">
        <div class="timeline-workplace">
            {workplace}
        </div>
        <div class="timeline-track">
    """

    for i in range(1, 10):
        percent = i * 10

        timeline_html += f"""
        <div
            class="timeline-grid-line"
            style="left:{percent}%"
        ></div>
        """

    workplace_operations = [
        item for item in schedule
        if item[2] == workplace
    ]

    workplace_operations.sort(key=lambda x: x[3])

    for order, operation, wp, start, end in workplace_operations:

        left = (start / max_time) * 100
        width = ((end - start) / max_time) * 100

        left = max(0, min(left, 100))
        width = max(0.3, min(width, 100 - left))

        short_order = str(order).replace("Order", "O")
        label = f"{short_order} • {operation}"

        title = (
            f"{order} → {operation} | "
            f"{workplace} | "
            f"{start:.2f} → {end:.2f}"
        )

        timeline_html += f"""
        <div
            class="timeline-block"
            style="left:{left}%; width:{width}%"
            title="{title}"
        >
            <span class="timeline-block-label">
                {label}
            </span>
        </div>
        """

    timeline_html += """
        </div>
    </div>
    """

timeline_html += """
<div class="timeline-footer">
    <span>Production time</span>
    <span>Minutes</span>
</div>
</div>
</div>
"""

st.html(timeline_html)

st.subheader("Detailed Schedule")

table_rows = []

for order, operation, workplace, start, end in schedule:
    table_rows.append(
        {
            "Order": order,
            "Operation": operation,
            "Workplace": workplace,
            "Start": f"{start:.2f}",
            "End": f"{end:.2f}"
        }
    )

st.dataframe(
    table_rows,
    width="stretch",
    hide_index=True
)