import streamlit as st
import pandas as pd
import request_edit

DATA_FILE = "Data.xlsx"


def load_excel_data():
    """Load required sheets from Data.xlsx for My Requests list."""
    request_df = pd.read_excel(DATA_FILE, sheet_name="Request", engine="openpyxl")
    workflow_df = pd.read_excel(DATA_FILE, sheet_name="Workflow", engine="openpyxl")
    return request_df, workflow_df


def open_edit_form(request_id):
    """Store selected request and open edit form."""
    st.session_state.selected_req = request_id
    st.session_state.show_request_edit_form = True


def show_my_requests_list():
    st.title("My Requests")

    request_df, workflow_df = load_excel_data()

    df = request_df.merge(
        workflow_df,
        left_on="WorkFlowLevel",
        right_on="WorkFlowLevel",
        how="left",
    )

    # Existing filter kept: show Shilpa's requests only
    shilpa_df = df[df["RequesterName"] == "Shilpa"].copy()

    display_cols = [
        "Request ID",
        "Department",
        "Req_JobTitle",
        "Business Unit",
        "WorkFlowLevel_Description",
    ]

    existing_cols = [col for col in display_cols if col in shilpa_df.columns]
    st.dataframe(shilpa_df[existing_cols], use_container_width=True)

    st.subheader("Actions")

    # Existing requirement: editable requests at WF Level 3
    shilpa_df_edit = shilpa_df[shilpa_df["WorkFlowLevel"] == 3].copy()

    if shilpa_df_edit.empty:
        st.info("No editable requests found at WF Level 3.")
        return

    for _, row in shilpa_df_edit.iterrows():
        c1, c2 = st.columns([5, 1])

        with c1:
            st.write(
                f"{row['Request ID']} | {row['Req_JobTitle']} | WF Level {int(row['WorkFlowLevel'])}"
            )

        with c2:
            if st.button("Edit", key=f"edit_{row['Request ID']}"):
                open_edit_form(row["Request ID"])
                st.rerun()


def show():
    if "selected_req" not in st.session_state:
        st.session_state.selected_req = None

    if "show_request_edit_form" not in st.session_state:
        st.session_state.show_request_edit_form = False

    if st.session_state.show_request_edit_form and st.session_state.selected_req:
        request_edit.show(st.session_state.selected_req)
    else:
        show_my_requests_list()
