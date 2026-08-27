import streamlit as st

from gui.style import apply_style, page_header

apply_style()

page_header(
    "Production Rates",
    "Define the production rate for each operation and product combination."
)

if "rates" not in st.session_state:
    st.session_state.rates = {}

if "products" not in st.session_state:
    st.session_state.products = {}

if "product_operations" not in st.session_state:
    st.session_state.product_operations = {}

products = list(
    st.session_state.product_operations.keys()
)

st.subheader("Add Rate")

with st.container(border=True):

    col1, col2, col3 = st.columns(3)

    with col1:

        product = st.selectbox(
            "Product",
            products if products else ["No products"],
            key="add_rate_product"
        )

    available_operations = (
        st.session_state.product_operations.get(
            product,
            []
        )
        if products
        else []
    )

    with col2:

        operation = st.selectbox(
            "Operation",
            available_operations
            if available_operations
            else ["No operations"],
            key="add_rate_operation"
        )

    with col3:

        rate = st.number_input(
            "Production rate",
            min_value=0.01,
            value=1.0,
            step=0.1,
            key="add_rate_value"
        )

    if st.button(
        "Add Rate",
        type="primary",
        key="add_rate_button"
    ):

        if not products:
            st.error("Add a product first.")

        elif not available_operations:
            st.error(
                f"No operations are assigned to product '{product}'."
            )

        else:

            rate_key = f"{operation}_{product}"

            if rate_key in st.session_state.rates:
                st.error(
                    f"A rate for {operation} + {product} already exists."
                )

            else:

                st.session_state.rates[rate_key] = float(rate)

                st.success(
                    f"Rate for {operation} / {product} added."
                )

                st.rerun()

st.divider()

st.subheader("Current Rates")

if not st.session_state.rates:

    st.info("No production rates have been added yet.")

else:

    c1, c2, c3, c4 = st.columns(
        [2, 2, 2, 1]
    )

    c1.markdown("**Operation**")
    c2.markdown("**Product**")
    c3.markdown("**Production Rate**")
    c4.markdown("**Action**")

    for rate_key in list(
        st.session_state.rates
    ):

        try:
            operation, product = rate_key.split("_", 1)
        except ValueError:
            continue

        rate_value = st.session_state.rates[rate_key]

        c1, c2, c3, c4 = st.columns(
            [2, 2, 2, 1]
        )

        c1.write(operation)
        c2.write(product)
        c3.write(rate_value)

        if c4.button(
            "Edit",
            key=f"edit_rate_{rate_key}"
        ):
            st.session_state[
                f"editing_rate_{rate_key}"
            ] = True

        if st.session_state.get(
            f"editing_rate_{rate_key}",
            False
        ):

            st.markdown("---")

            st.markdown(
                f"**Edit Rate: {operation} / {product}**"
            )

            new_rate = st.number_input(
                "Production rate",
                min_value=0.01,
                value=float(rate_value),
                step=0.1,
                key=f"edit_rate_value_{rate_key}"
            )

            save_col, cancel_col, delete_col = st.columns(3)

            with save_col:

                if st.button(
                    "Save Changes",
                    type="primary",
                    key=f"save_rate_{rate_key}"
                ):

                    st.session_state.rates[
                        rate_key
                    ] = float(new_rate)

                    st.session_state[
                        f"editing_rate_{rate_key}"
                    ] = False

                    st.success(
                        f"Rate for {operation} / {product} updated."
                    )

                    st.rerun()

            with cancel_col:

                if st.button(
                    "Cancel",
                    key=f"cancel_rate_{rate_key}"
                ):

                    st.session_state[
                        f"editing_rate_{rate_key}"
                    ] = False

                    st.rerun()

            with delete_col:

                if st.button(
                    "Delete",
                    key=f"delete_rate_{rate_key}"
                ):

                    del st.session_state.rates[
                        rate_key
                    ]

                    st.session_state.pop(
                        f"editing_rate_{rate_key}",
                        None
                    )

                    st.success(
                        f"Rate for {operation} / {product} deleted."
                    )

                    st.rerun()