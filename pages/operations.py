import streamlit as st

from gui.style import apply_style, page_header

apply_style()

page_header(
    "Operations",
    "Define production operations and the workplaces that can perform them."
)

if "operation_workplaces" not in st.session_state:
    st.session_state.operation_workplaces = {}

if "workplaces" not in st.session_state:
    st.session_state.workplaces = []

st.subheader("Add Operation")

with st.container(border=True):

    operation_name = st.text_input(
        "Operation name",
        placeholder="Example: Op1",
        key="add_operation_name"
    )

    selected_workplaces = st.multiselect(
        "Available workplaces",
        st.session_state.workplaces,
        key="add_operation_workplaces"
    )

    if st.button(
        "Add Operation",
        type="primary",
        key="add_operation_button"
    ):

        name = operation_name.strip()

        if not name:
            st.error("Operation name cannot be empty.")

        elif name in st.session_state.operation_workplaces:
            st.error(f"Operation '{name}' already exists.")

        elif not selected_workplaces:
            st.error("Select at least one workplace.")

        else:
            st.session_state.operation_workplaces[name] = selected_workplaces
            st.success(f"Operation '{name}' added.")
            st.rerun()

st.divider()

st.subheader("Current Operations")

if not st.session_state.operation_workplaces:

    st.info("No operations have been added yet.")

else:

    c1, c2, c3 = st.columns([2, 5, 1])

    c1.markdown("**Operation**")
    c2.markdown("**Available Workplaces**")
    c3.markdown("**Action**")

    for operation in list(st.session_state.operation_workplaces):

        workplaces_for_operation = st.session_state.operation_workplaces[
            operation
        ]

        c1, c2, c3 = st.columns([2, 5, 1])

        c1.write(operation)
        c2.write(", ".join(workplaces_for_operation))

        if c3.button(
            "Edit",
            key=f"edit_operation_{operation}"
        ):
            st.session_state[f"editing_operation_{operation}"] = True

        if st.session_state.get(
            f"editing_operation_{operation}",
            False
        ):

            st.markdown("---")
            st.markdown(f"**Edit Operation: {operation}**")

            new_name = st.text_input(
                "Operation name",
                value=operation,
                key=f"edit_operation_name_{operation}"
            )

            new_workplaces = st.multiselect(
                "Available workplaces",
                st.session_state.workplaces,
                default=[
                    wp for wp in workplaces_for_operation
                    if wp in st.session_state.workplaces
                ],
                key=f"edit_operation_workplaces_{operation}"
            )

            save_col, cancel_col, delete_col = st.columns(3)

            with save_col:
                if st.button(
                    "Save Changes",
                    type="primary",
                    key=f"save_operation_{operation}"
                ):

                    new_name = new_name.strip()

                    if not new_name:
                        st.error("Operation name cannot be empty.")

                    elif (
                        new_name != operation
                        and new_name in st.session_state.operation_workplaces
                    ):
                        st.error(
                            f"Operation '{new_name}' already exists."
                        )

                    elif not new_workplaces:
                        st.error("Select at least one workplace.")

                    else:

                        del st.session_state.operation_workplaces[operation]

                        st.session_state.operation_workplaces[
                            new_name
                        ] = new_workplaces

                        st.session_state[
                            f"editing_operation_{operation}"
                        ] = False

                        st.success(
                            f"Operation '{new_name}' updated."
                        )

                        st.rerun()

            with cancel_col:
                if st.button(
                    "Cancel",
                    key=f"cancel_operation_{operation}"
                ):
                    st.session_state[
                        f"editing_operation_{operation}"
                    ] = False
                    st.rerun()

            with delete_col:
                if st.button(
                    "Delete",
                    key=f"delete_operation_{operation}"
                ):

                    del st.session_state.operation_workplaces[
                        operation
                    ]

                    for product in st.session_state.get(
                        "product_operations",
                        {}
                    ):

                        st.session_state.product_operations[
                            product
                        ] = [
                            op for op in
                            st.session_state.product_operations[product]
                            if op != operation
                        ]

                    st.session_state.pop(
                        f"editing_operation_{operation}",
                        None
                    )

                    st.success(
                        f"Operation '{operation}' deleted."
                    )

                    st.rerun()
                        
#python3 -m streamlit run app.py