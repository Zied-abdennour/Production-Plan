import streamlit as st

from gui.style import apply_style, page_header

apply_style()

page_header(
    "Orders",
    "Define production orders, quantities, products, and deadlines."
)

if "orders" not in st.session_state:
    st.session_state.orders = {}

if "product_operations" not in st.session_state:
    st.session_state.product_operations = {}

st.subheader("Add Order")

with st.container(border=True):

    order_name = st.text_input(
        "Order name",
        placeholder="Example: Order1",
        key="add_order_name"
    )

    products = list(st.session_state.product_operations.keys())

    if products:
        product = st.selectbox(
            "Product",
            products,
            key="add_order_product"
        )
    else:
        product = st.text_input(
            "Product",
            placeholder="Example: A",
            key="add_order_product_text"
        )

    c1, c2 = st.columns(2)

    with c1:
        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1,
            step=1,
            key="add_order_quantity"
        )

    with c2:
        deadline = st.number_input(
            "Deadline (minutes)",
            min_value=0,
            value=0,
            step=1,
            key="add_order_deadline"
        )

    if st.button(
        "Add Order",
        type="primary",
        key="add_order_button"
    ):

        name = order_name.strip()

        if not name:
            st.error("Order name cannot be empty.")

        elif name in st.session_state.orders:
            st.error(f"Order '{name}' already exists.")

        elif not product:
            st.error("Product cannot be empty.")

        else:
            st.session_state.orders[name] = {
                "product": product,
                "quantity": quantity,
                "deadline": deadline
            }

            st.success(f"Order '{name}' added.")
            st.rerun()

st.divider()

st.subheader("Current Orders")

if not st.session_state.orders:

    st.info("No orders have been added yet.")

else:

    c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 1])

    c1.markdown("**Order**")
    c2.markdown("**Product**")
    c3.markdown("**Quantity**")
    c4.markdown("**Deadline**")
    c5.markdown("**Action**")

    for order_name in list(st.session_state.orders):

        order = st.session_state.orders[order_name]

        c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 1])

        c1.write(order_name)
        c2.write(order["product"])
        c3.write(order["quantity"])
        c4.write(order["deadline"])

        if c5.button(
            "Edit",
            key=f"edit_order_{order_name}"
        ):
            st.session_state[
                f"editing_order_{order_name}"
            ] = True

        if st.session_state.get(
            f"editing_order_{order_name}",
            False
        ):

            st.markdown("---")
            st.markdown(f"**Edit Order: {order_name}**")

            new_name = st.text_input(
                "Order name",
                value=order_name,
                key=f"edit_order_name_{order_name}"
            )

            products = list(
                st.session_state.product_operations.keys()
            )

            if products:

                current_product = order["product"]

                if current_product in products:
                    product_index = products.index(current_product)
                else:
                    product_index = 0

                new_product = st.selectbox(
                    "Product",
                    products,
                    index=product_index,
                    key=f"edit_order_product_{order_name}"
                )

            else:

                new_product = st.text_input(
                    "Product",
                    value=order["product"],
                    key=f"edit_order_product_text_{order_name}"
                )

            c1, c2 = st.columns(2)

            with c1:

                new_quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    value=int(order["quantity"]),
                    step=1,
                    key=f"edit_order_quantity_{order_name}"
                )

            with c2:

                new_deadline = st.number_input(
                    "Deadline (minutes)",
                    min_value=0,
                    value=int(order["deadline"]),
                    step=1,
                    key=f"edit_order_deadline_{order_name}"
                )

            save_col, cancel_col, delete_col = st.columns(3)

            with save_col:

                if st.button(
                    "Save Changes",
                    type="primary",
                    key=f"save_order_{order_name}"
                ):

                    new_name = new_name.strip()

                    if not new_name:
                        st.error(
                            "Order name cannot be empty."
                        )

                    elif (
                        new_name != order_name
                        and new_name in st.session_state.orders
                    ):
                        st.error(
                            f"Order '{new_name}' already exists."
                        )

                    elif not new_product:
                        st.error(
                            "Product cannot be empty."
                        )

                    else:

                        del st.session_state.orders[
                            order_name
                        ]

                        st.session_state.orders[
                            new_name
                        ] = {
                            "product": new_product,
                            "quantity": new_quantity,
                            "deadline": new_deadline
                        }

                        st.session_state[
                            f"editing_order_{order_name}"
                        ] = False

                        st.success(
                            f"Order '{new_name}' updated."
                        )

                        st.rerun()

            with cancel_col:

                if st.button(
                    "Cancel",
                    key=f"cancel_order_{order_name}"
                ):

                    st.session_state[
                        f"editing_order_{order_name}"
                    ] = False

                    st.rerun()

            with delete_col:

                if st.button(
                    "Delete",
                    key=f"delete_order_{order_name}"
                ):

                    del st.session_state.orders[
                        order_name
                    ]

                    st.session_state.pop(
                        f"editing_order_{order_name}",
                        None
                    )

                    st.success(
                        f"Order '{order_name}' deleted."
                    )

                    st.rerun()