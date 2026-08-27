import streamlit as st

from gui.style import apply_style, page_header

apply_style()

page_header(
    "Products",
    "Define product routings by assigning operations to each product."
)

if "product_operations" not in st.session_state:
    st.session_state.product_operations = {}

if "operation_workplaces" not in st.session_state:
    st.session_state.operation_workplaces = {}

operations = list(
    st.session_state.operation_workplaces.keys()
)

st.subheader("Add Product")

with st.container(border=True):

    product_name = st.text_input(
        "Product name",
        placeholder="Example: A",
        key="add_product_name"
    )

    routing = st.multiselect(
        "Production routing",
        operations,
        key="add_product_routing"
    )

    if st.button(
        "Add Product",
        type="primary",
        key="add_product_button"
    ):

        name = product_name.strip()

        if not name:
            st.error("Product name cannot be empty.")

        elif name in st.session_state.product_operations:
            st.error(f"Product '{name}' already exists.")

        elif not routing:
            st.error("Select at least one operation.")

        else:
            st.session_state.product_operations[name] = routing
            st.success(f"Product '{name}' added.")
            st.rerun()

st.divider()

st.subheader("Current Products")

if not st.session_state.product_operations:

    st.info("No products have been added yet.")

else:

    c1, c2, c3 = st.columns([2, 5, 1])

    c1.markdown("**Product**")
    c2.markdown("**Production Routing**")
    c3.markdown("**Action**")

    for product in list(
        st.session_state.product_operations
    ):

        product_routing = st.session_state.product_operations[
            product
        ]

        c1, c2, c3 = st.columns([2, 5, 1])

        c1.write(product)
        c2.write(" → ".join(product_routing))

        if c3.button(
            "Edit",
            key=f"edit_product_{product}"
        ):
            st.session_state[
                f"editing_product_{product}"
            ] = True

        if st.session_state.get(
            f"editing_product_{product}",
            False
        ):

            st.markdown("---")
            st.markdown(f"**Edit Product: {product}**")

            new_name = st.text_input(
                "Product name",
                value=product,
                key=f"edit_product_name_{product}"
            )

            new_routing = st.multiselect(
                "Production routing",
                operations,
                default=[
                    op for op in product_routing
                    if op in operations
                ],
                key=f"edit_product_routing_{product}"
            )

            save_col, cancel_col, delete_col = st.columns(3)

            with save_col:

                if st.button(
                    "Save Changes",
                    type="primary",
                    key=f"save_product_{product}"
                ):

                    new_name = new_name.strip()

                    if not new_name:
                        st.error("Product name cannot be empty.")

                    elif (
                        new_name != product
                        and new_name in st.session_state.product_operations
                    ):
                        st.error(
                            f"Product '{new_name}' already exists."
                        )

                    elif not new_routing:
                        st.error(
                            "Select at least one operation."
                        )

                    else:

                        del st.session_state.product_operations[
                            product
                        ]

                        st.session_state.product_operations[
                            new_name
                        ] = new_routing

                        for order_name, order in (
                            st.session_state.get(
                                "orders",
                                {}
                            ).items()
                        ):

                            if order["product"] == product:
                                order["product"] = new_name

                        st.session_state[
                            f"editing_product_{product}"
                        ] = False

                        st.success(
                            f"Product '{new_name}' updated."
                        )

                        st.rerun()

            with cancel_col:

                if st.button(
                    "Cancel",
                    key=f"cancel_product_{product}"
                ):

                    st.session_state[
                        f"editing_product_{product}"
                    ] = False

                    st.rerun()

            with delete_col:

                if st.button(
                    "Delete",
                    key=f"delete_product_{product}"
                ):

                    used_by_orders = [
                        order_name
                        for order_name, order in
                        st.session_state.get(
                            "orders",
                            {}
                        ).items()
                        if order["product"] == product
                    ]

                    if used_by_orders:

                        st.error(
                            "Cannot delete this product. "
                            "It is used by: "
                            + ", ".join(used_by_orders)
                        )

                    else:

                        del st.session_state.product_operations[
                            product
                        ]

                        st.session_state.pop(
                            f"editing_product_{product}",
                            None
                        )

                        st.success(
                            f"Product '{product}' deleted."
                        )

                        st.rerun()