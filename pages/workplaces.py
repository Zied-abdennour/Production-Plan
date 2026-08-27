import streamlit as st

from gui.style import apply_style, page_header

apply_style()

page_header(
    "Workplaces",
    "Define the production workplaces available for scheduling."
)

if "workplaces" not in st.session_state:
    st.session_state.workplaces = []

if "operation_workplaces" not in st.session_state:
    st.session_state.operation_workplaces = {}

st.subheader("Add Workplace")

with st.container(border=True):

    workplace_name = st.text_input(
        "Workplace name",
        placeholder="Example: WP1",
        key="add_workplace_name"
    )

    if st.button(
        "Add Workplace",
        type="primary",
        key="add_workplace_button"
    ):

        name = workplace_name.strip()

        if not name:
            st.error(
                "Workplace name cannot be empty."
            )

        elif name in st.session_state.workplaces:
            st.error(
                f"Workplace '{name}' already exists."
            )

        else:

            st.session_state.workplaces.append(
                name
            )

            st.success(
                f"Workplace '{name}' added."
            )

            st.rerun()

st.divider()

st.subheader("Current Workplaces")

if not st.session_state.workplaces:

    st.info("No workplaces have been added yet.")

else:

    c1, c2, c3 = st.columns([2, 5, 1])

    c1.markdown("**Workplace**")
    c2.markdown("**Used By**")
    c3.markdown("**Action**")

    for workplace in list(
        st.session_state.workplaces
    ):

        used_by = []

        for operation, available_workplaces in st.session_state.operation_workplaces.items():

            if workplace in available_workplaces:
                used_by.append(operation)

        c1, c2, c3 = st.columns([2, 5, 1])

        c1.write(workplace)

        if used_by:
            c2.write(", ".join(used_by))
        else:
            c2.write("Not assigned")

        if c3.button(
            "Edit",
            key=f"edit_workplace_{workplace}"
        ):
            st.session_state[
                f"editing_workplace_{workplace}"
            ] = True

        if st.session_state.get(
            f"editing_workplace_{workplace}",
            False
        ):

            st.markdown("---")
            st.markdown(
                f"**Edit Workplace: {workplace}**"
            )

            new_name = st.text_input(
                "Workplace name",
                value=workplace,
                key=f"edit_workplace_name_{workplace}"
            )

            save_col, cancel_col, delete_col = st.columns(3)

            with save_col:

                if st.button(
                    "Save Changes",
                    type="primary",
                    key=f"save_workplace_{workplace}"
                ):

                    new_name = new_name.strip()

                    if not new_name:
                        st.error(
                            "Workplace name cannot be empty."
                        )

                    elif (
                        new_name != workplace
                        and new_name in st.session_state.workplaces
                    ):
                        st.error(
                            f"Workplace '{new_name}' already exists."
                        )

                    else:

                        index = (
                            st.session_state.workplaces.index(
                                workplace
                            )
                        )

                        st.session_state.workplaces[
                            index
                        ] = new_name

                        for operation in st.session_state.operation_workplaces:

                            st.session_state.operation_workplaces[
                                operation
                            ] = [
                                new_name
                                if wp == workplace
                                else wp
                                for wp in st.session_state.operation_workplaces[
                                    operation
                                ]
                            ]

                        st.session_state[
                            f"editing_workplace_{workplace}"
                        ] = False

                        st.success(
                            f"Workplace '{new_name}' updated."
                        )

                        st.rerun()

            with cancel_col:

                if st.button(
                    "Cancel",
                    key=f"cancel_workplace_{workplace}"
                ):

                    st.session_state[
                        f"editing_workplace_{workplace}"
                    ] = False

                    st.rerun()

            with delete_col:

                if st.button(
                    "Delete",
                    key=f"delete_workplace_{workplace}"
                ):

                    st.session_state.workplaces.remove(
                        workplace
                    )

                    for operation in st.session_state.operation_workplaces:

                        st.session_state.operation_workplaces[
                            operation
                        ] = [
                            wp
                            for wp in st.session_state.operation_workplaces[
                                operation
                            ]
                            if wp != workplace
                        ]

                    st.session_state.pop(
                        f"editing_workplace_{workplace}",
                        None
                    )

                    st.success(
                        f"Workplace '{workplace}' deleted."
                    )

                    st.rerun()