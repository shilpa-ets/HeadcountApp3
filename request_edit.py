import streamlit as st
import pandas as pd

DATA_FILE = "Data.xlsx"


def _clean(value):
    """Convert NaN/None values to blank strings for form fields."""
    if pd.isna(value):
        return ""
    return value


def load_excel_data():
    """Load all required sheets from Data.xlsx."""
    request_df = pd.read_excel(DATA_FILE, sheet_name="Request", engine="openpyxl")
    workflow_df = pd.read_excel(DATA_FILE, sheet_name="Workflow", engine="openpyxl")
    wf_details_df = pd.read_excel(DATA_FILE, sheet_name="WFDetails", engine="openpyxl")
    return request_df, workflow_df, wf_details_df


def save_excel_data(request_df, workflow_df, wf_details_df):
    """Save all sheets back so Workflow and WFDetails are not lost."""
    with pd.ExcelWriter(DATA_FILE, engine="openpyxl", mode="w") as writer:
        request_df.to_excel(writer, sheet_name="Request", index=False)
        workflow_df.to_excel(writer, sheet_name="Workflow", index=False)
        wf_details_df.to_excel(writer, sheet_name="WFDetails", index=False)


def close_edit_form():
    """Close edit form and return to My Requests list."""
    st.session_state.selected_req = None
    st.session_state.show_request_edit_form = False
    st.session_state.current_page = "home"


def show(request_id=None):
    """Show request edit form for selected Request ID."""
    request_df, workflow_df, wf_details_df = load_excel_data()

    selected_req = request_id or st.session_state.get("selected_req")

    selected_rows = request_df[request_df["Request ID"].astype(str) == str(selected_req)]

    if selected_rows.empty:
        st.error(f"No request found for {selected_req}")
        if st.button("Back to My Requests"):
            close_edit_form()
            st.rerun()
        return

    row_index = selected_rows.index[0]
    row = selected_rows.iloc[0].copy()

    st.title(f"Edit Request - {selected_req}")

    with st.form(key=f"edit_request_form_{selected_req}"):
        col1, col2 = st.columns(2)

        with col1:
            row["Department"] = st.text_input(
                "Department",
                value=str(_clean(row.get("Department", ""))),
            )
            row["Req_JobTitle"] = st.text_input(
                "Requested Job Title",
                value=str(_clean(row.get("Req_JobTitle", ""))),
            )
            row["Req_JobCode"] = st.text_input(
                "Requested Job Code",
                value=str(_clean(row.get("Req_JobCode", ""))),
            )
            row["Job Family"] = st.text_input(
                "Job Family",
                value=str(_clean(row.get("Job Family", ""))),
            )
            row["Level"] = st.text_input(
                "Level",
                value=str(_clean(row.get("Level", ""))),
            )
            row["Business Unit"] = st.text_input(
                "Business Unit",
                value=str(_clean(row.get("Business Unit", ""))),
            )
            row["Quarter"] = st.text_input(
                "Quarter",
                value=str(_clean(row.get("Quarter", ""))),
            )

        with col2:
            row["RequestedForName"] = st.text_input(
                "Requested For Name",
                value=str(_clean(row.get("RequestedForName", ""))),
            )
            row["RequestedForEmpID"] = st.text_input(
                "Requested For Emp ID",
                value=str(_clean(row.get("RequestedForEmpID", ""))),
            )

            current_location = str(_clean(row.get("Onshore_Offshore", "Onshore")))
            row["Onshore_Offshore"] = st.selectbox(
                "Onshore / Offshore",
                ["Onshore", "Offshore"],
                index=1 if current_location == "Offshore" else 0,
            )

            current_direct_reports = str(_clean(row.get("DirectReportsFlag", "No")))
            row["DirectReportsFlag"] = st.selectbox(
                "Direct Reports?",
                ["No", "Yes"],
                index=1 if current_direct_reports == "Yes" else 0,
            )

            row["PostingScope"] = st.text_input(
                "Posting Scope",
                value=str(_clean(row.get("PostingScope", ""))),
            )
            row["Hire Dates"] = st.text_input(
                "Hire Date",
                value=str(_clean(row.get("Hire Dates", ""))),
            )

        row["Hiring Need"] = st.text_area(
            "Hiring Need",
            value=str(_clean(row.get("Hiring Need", ""))),
            height=90,
        )
        row["Business Justification"] = st.text_area(
            "Business Justification",
            value=str(_clean(row.get("Business Justification", ""))),
            height=120,
        )

        save_col, cancel_col = st.columns(2)

        with save_col:
            save_clicked = st.form_submit_button(
                "Save Changes",
                type="primary",
                use_container_width=True,
            )

        with cancel_col:
            cancel_clicked = st.form_submit_button(
                "Cancel",
                use_container_width=True,
            )

    if save_clicked:
        request_df.loc[row_index, row.index] = row
        save_excel_data(request_df, workflow_df, wf_details_df)
        st.success(f"{selected_req} updated successfully.")
        close_edit_form()
        st.rerun()

    if cancel_clicked:
        close_edit_form()
        st.rerun()
