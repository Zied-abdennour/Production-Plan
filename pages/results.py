import streamlit as st

from gui.style import apply_style, page_header
from algorithm.genetic_algorithm import genetic_algorithm
from algorithm.decoder import decode_all

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
        st.error(
            "The genetic algorithm did not return a valid result. "
            "Check the production data and parameters."
        )
        st.session_state.pop("best_result", None)
        st.stop()

    if not isinstance(result, tuple) or len(result) != 3:
        st.error("The genetic algorithm returned an invalid result.")
        st.session_state.pop("best_result", None)
        st.stop()

    st.session_state.best_result = result
    st.success("Optimization completed.")

if "best_result" not in st.session_state:
    st.info("Click Run Genetic Algorithm to generate a production schedule.")
    st.stop()

result = st.session_state.best_result

if result is None or not isinstance(result, tuple) or len(result) != 3:
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
    workplace = item[2]

    if workplace not in timeline_workplaces:
        timeline_workplaces.append(workplace)

timeline_workplaces = list(dict.fromkeys(timeline_workplaces))

timeline_html = """
<style>

.production-timeline {
    width: 100%;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    background: #ffffff;
    overflow-x: auto;
    padding: 22px 20px 20px 20px;
    box-sizing: border-box;
}

.timeline-inner {
    min-width: 850px;
}

.timeline-axis-row {
    display: grid;
    grid-template-columns: 70px 1fr;
    margin-bottom: 16px;
}

.timeline-axis-label {
    font-size: 12px;
    font-weight: 600;
    color: #64748b;
}

.timeline-axis {
    position: relative;
    height: 38px;
    border-bottom: 1px solid #cbd5e1;
}

.timeline-axis-line {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 1px;
    background: #e2e8f0;
}

.timeline-axis-value {
    position: absolute;
    top: -2px;
    transform: translateX(-50%);
    font-size: 11px;
    color: #64748b;
    white-space: nowrap;
}

.timeline-row {
    display: grid;
    grid-template-columns: 70px 1fr;
    min-height: 68px;
    margin-bottom: 8px;
}

.timeline-workplace {
    display: flex;
    align-items: center;
    font-size: 13px;
    font-weight: 700;
    color: #1e293b;
}

.timeline-track {
    position: relative;
    min-height: 58px;
    background:
        linear-gradient(
            to right,
            transparent calc(10% - 1px),
            #eef2f7 10%,
            transparent calc(10% + 1px)
        );
    border-bottom: 1px solid #f1f5f9;
}

.timeline-grid-line {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 1px;
    background: #eef2f7;
}

.timeline-block {
    position: absolute;
    top: 10px;
    height: 38px;
    min-width: 8px;
    box-sizing: border-box;
    background: #334155;
    border-radius: 7px;
    border: 1px solid #273449;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.12);
    display: flex;
    align-items: center;
    overflow: hidden;
    transition: transform 0.12s ease, box-shadow 0.12s ease;
}

.timeline-block:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 10px rgba(15, 23, 42, 0.18);
    z-index: 20;
}

.timeline-block-label {
    color: #ffffff;
    font-size: 11px;
    font-weight: 600;
    padding: 0 9px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.timeline-footer {
    display: flex;
    justify-content: space-between;
    margin-top: 14px;
    padding-left: 70px;
    color: #64748b;
    font-size: 11px;
}

</style>

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

    for i in range(11):
        percent = i * 10

        if percent not in (0, 100):
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

    for order_name, op, wp, start, end in workplace_operations:

        left = (start / max_time) * 100
        width = ((end - start) / max_time) * 100

        left = max(0, min(left, 100))
        width = max(0.3, min(width, 100 - left))

        short_order = str(order_name).replace("Order", "O")

        label = f"{short_order} • {op}"

        title = (
            f"{order_name} → {op} | "
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

for order_name, op, workplace, start, end in schedule:
    table_rows.append(
        {
            "Order": order_name,
            "Operation": op,
            "Workplace": workplace,
            "Start": f"{start:.2f}",
            "End": f"{end:.2f}"
        }
    )

st.dataframe(
    table_rows,
    width="stretch",
    hide_index=True,
    column_config={
        "Order": st.column_config.TextColumn(
            "Order",
            width="medium"
        ),
        "Operation": st.column_config.TextColumn(
            "Operation",
            width="medium"
        ),
        "Workplace": st.column_config.TextColumn(
            "Workplace",
            width="medium"
        ),
        "Start": st.column_config.TextColumn(
            "Start",
            width="medium"
        ),
        "End": st.column_config.TextColumn(
            "End",
            width="medium"
        )
    }
)