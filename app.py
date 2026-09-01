import streamlit as st

from data.example_data import (
    orders as example_orders,
    product_operations as example_product_operations,
    operation_workplaces as example_operation_workplaces,
    rates as example_rates,
    workplaces as example_workplaces
)

st.set_page_config(
    page_title="Production Planner",
    page_icon="⚙️",
    layout="wide"
)

if "orders" not in st.session_state:
    st.session_state.orders = {}

if "product_operations" not in st.session_state:
    st.session_state.product_operations = {}

if "operation_workplaces" not in st.session_state:
    st.session_state.operation_workplaces = {}

if "rates" not in st.session_state:
    st.session_state.rates = {}

if "workplaces" not in st.session_state:
    st.session_state.workplaces = []

if "parameters" not in st.session_state:
    st.session_state.parameters = {
        "generations": 100,
        "population_size": 50,
        "selection_percent": 0.2,
        "mutation_rate": 0.1
    }

if "best_result" not in st.session_state:
    st.session_state.best_result = None

def load_example_data():
    st.session_state.orders = example_orders.copy()
    st.session_state.product_operations = example_product_operations.copy()
    st.session_state.operation_workplaces = example_operation_workplaces.copy()
    st.session_state.rates = example_rates.copy()
    st.session_state.workplaces = example_workplaces.copy()
    st.session_state.best_result = None

def clear_all_data():
    st.session_state.orders = {}
    st.session_state.product_operations = {}
    st.session_state.operation_workplaces = {}
    st.session_state.rates = {}
    st.session_state.workplaces = []
    st.session_state.best_result = None

pg = st.navigation(
    [
        st.Page(
            "pages/dashboard.py",
            title="Dashboard",
            icon=":material/dashboard:"
        ),
        st.Page(
            "pages/workplaces.py",
            title="Workplaces",
            icon=":material/factory:"
        ),
        st.Page(
            "pages/operations.py",
            title="Operations",
            icon=":material/handyman:"
        ),
        st.Page(
            "pages/products.py",
            title="Products",
            icon=":material/inventory_2:"
        ),
        st.Page(
            "pages/rates.py",
            title="Rates",
            icon=":material/monitoring:"
        ),
        st.Page(
            "pages/orders.py",
            title="Orders",
            icon=":material/receipt_long:"
        ),
        st.Page(
            "pages/parameters.py",
            title="Parameters",
            icon=":material/tune:"
        ),
        st.Page(
            "pages/results.py",
            title="Results",
            icon=":material/analytics:"
        ),
        st.Page(
            "pages/chatbot.py",
            title="AI Assistant",
            icon=":material/smart_toy:"
        )
    ]
)

with st.sidebar:
    st.markdown("### Data")

    if st.button(
        "Load Example Data",
        use_container_width=True
    ):
        load_example_data()
        st.success("Example data loaded.")
        st.rerun()

    if st.button(
        "Clear All Data",
        use_container_width=True
    ):
        clear_all_data()
        st.success("All data cleared.")
        st.rerun()

pg.run()