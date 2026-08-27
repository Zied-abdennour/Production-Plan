import streamlit as st

from gui.style import apply_style, page_header, metric_card

apply_style()

page_header(
    "Production Planner",
    "Production scheduling and optimization workspace."
)

workplaces = st.session_state.get("workplaces", {})
operations = st.session_state.get("operation_workplaces", {})
products = st.session_state.get("product_operations", {})
rates = st.session_state.get("rates", {})
orders = st.session_state.get("orders", {})

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    metric_card("Workplaces", len(workplaces))

with col2:
    metric_card("Operations", len(operations))

with col3:
    metric_card("Products", len(products))

with col4:
    metric_card("Rates", len(rates))

with col5:
    metric_card("Orders", len(orders))

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">Production Configuration</div>',
    unsafe_allow_html=True
)

configuration = [
    ("Workplaces", workplaces),
    ("Operations", operations),
    ("Products", products),
    ("Rates", rates),
    ("Orders", orders)
]

for name, data in configuration:
    col1, col2 = st.columns([5, 1])

    with col1:
        st.write(name)

        if data:
            st.progress(1)
        else:
            st.progress(0)

    with col2:
        if data:
            st.success("Ready")
        else:
            st.warning("Empty")

st.markdown("<br>", unsafe_allow_html=True)

if all(data for _, data in configuration):
    st.success("✓ Production data is ready for optimization.")
else:
    st.info(
        "Configure all production data or use 'Load Data' "
        "to load the example dataset."
    )

if st.session_state.get("last_result") is not None:

    st.markdown("---")

    result = st.session_state.last_result

    st.markdown(
        f"""
        <div class="card">
            <div class="section-title">Latest Optimization</div>
            <div class="result-score">{result[2]}</div>
            <div class="item-info">
                Best score from the latest genetic algorithm run.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )