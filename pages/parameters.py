import streamlit as st

from gui.style import apply_style, page_header

apply_style()

page_header(
    "Genetic Algorithm",
    "Configure the optimization parameters before running the scheduler."
)

if "parameters" not in st.session_state:
    st.session_state.parameters = {
        "generations": 20,
        "population_size": 30,
        "selection_percent": 0.2,
        "mutation_rate": 0.1
    }

with st.form("parameters_form"):
    st.markdown("### Evolution Parameters")

    col1, col2 = st.columns(2)

    with col1:
        generations = st.number_input(
            "Generations",
            min_value=1,
            value=st.session_state.parameters["generations"],
            step=10
        )

        population_size = st.number_input(
            "Population size",
            min_value=2,
            value=st.session_state.parameters["population_size"],
            step=5
        )

    with col2:
        selection_percent = st.number_input(
            "Selection percentage",
            min_value=0.01,
            max_value=1.0,
            value=st.session_state.parameters["selection_percent"],
            step=0.05
        )

        mutation_rate = st.number_input(
            "Mutation rate",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.parameters["mutation_rate"],
            step=0.05
        )

    submitted = st.form_submit_button(
        "Save Parameters",
        type="primary"
    )

    if submitted:
        st.session_state.parameters = {
            "generations": int(generations),
            "population_size": int(population_size),
            "selection_percent": selection_percent,
            "mutation_rate": mutation_rate
        }

        st.success("Parameters saved.")