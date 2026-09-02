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

    if result is None or not isinstance(result, tuple) or len(result) != 3:
        st.error("The genetic algorithm returned an invalid result.")
        st.session_state.pop("best_result", None)
        st.stop()

    st.session_state.best_result = result

    try:
        save_equal_score_plans(
            orders,
            product_operations,
            rates
        )

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

timeline_width = 900

html = f"""
<div style="
    width:100%;
    overflow-x:auto;
    border:1px solid #e2e8f0;
    border-radius:12px;
    background:#ffffff;
    padding:20px;
    box-sizing:border-box;
">
    <div style="
        min-width:{timeline_width}px;
        font-family:Arial,sans-serif;
    ">

        <div style="
            display:grid;
            grid-template-columns:80px 1fr;
            margin-bottom:12px;
        ">

            <div style="
                font-size:13px;
                font-weight:600;
                color:#64748b;
                padding-top:4px;
            ">
                Workplace
            </div>

            <div style="
                position:relative;
                height:40px;
                border-bottom:1px solid #cbd5e1;
            ">
"""

for i in range(11):
    percent = i * 10
    time_value = max_time * percent / 100

    html += f"""
                <div style="
                    position:absolute;
                    left:{percent}%;
                    top:0;
                    bottom:0;
                    width:1px;
                    background:#e2e8f0;
                "></div>

                <div style="
                    position:absolute;
                    left:{percent}%;
                    top:2px;
                    transform:translateX(-50%);
                    font-size:11px;
                    color:#64748b;
                    white-space:nowrap;
                ">
                    {time_value:.0f}
                </div>
"""

html += """
            </div>
        </div>
"""

for workplace in timeline_workplaces:

    html += f"""
        <div style="
            display:grid;
            grid-template-columns:80px 1fr;
            min-height:68px;
        ">

            <div style="
                display:flex;
                align-items:center;
                font-size:13px;
                font-weight:700;
                color:#1e293b;
                border-bottom:1px solid #f1f5f9;
            ">
                {workplace}
            </div>

            <div style="
                position:relative;
                height:68px;
                border-bottom:1px solid #f1f5f9;
                background:#ffffff;
            ">
"""

    for i in range(1, 10):
        percent = i * 10

        html += f"""
                <div style="
                    position:absolute;
                    left:{percent}%;
                    top:0;
                    bottom:0;
                    width:1px;
                    background:#eef2f7;
                "></div>
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

        html += f"""
                <div title="{title}" style="
                    position:absolute;
                    left:{left}%;
                    width:{width}%;
                    top:15px;
                    height:38px;
                    min-width:8px;
                    box-sizing:border-box;
                    background:#334155;
                    border:1px solid #273449;
                    border-radius:7px;
                    display:flex;
                    align-items:center;
                    overflow:hidden;
                    box-shadow:0 1px 2px rgba(15,23,42,0.12);
                ">
                    <span style="
                        color:#ffffff;
                        font-size:11px;
                        font-weight:600;
                        padding:0 9px;
                        white-space:nowrap;
                        overflow:hidden;
                        text-overflow:ellipsis;
                    ">
                        {label}
                    </span>
                </div>
"""

    html += """
            </div>
        </div>
"""

html += f"""
        <div style="
            display:grid;
            grid-template-columns:80px 1fr;
            margin-top:12px;
        ">
            <div></div>

            <div style="
                display:flex;
                justify-content:space-between;
                color:#64748b;
                font-size:11px;
            ">
                <span>0</span>
                <span>{max_time:.0f} minutes</span>
            </div>
        </div>

    </div>
</div>
"""

st.html(html)

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