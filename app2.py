import streamlit as st


def hide_streamlit_toolbar():
    st.markdown("""
    """, unsafe_allow_html=True)


import streamlit as st


def maximize_page_space():
    st.markdown("""
    """, unsafe_allow_html=True)


st.set_page_config(layout="wide")
hide_streamlit_toolbar()
maximize_page_space()

# Initialize page
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Header
col1, col2 = st.columns([8, 1])

# with col1:
#     st.image("ETS_Digital_RGB_Ink.jpeg", width=100)

with col1:
    st.markdown(
        """

## Headcount Planning Workspace
        """,
        unsafe_allow_html=True,
    )

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

if "selected_req" not in st.session_state:
    st.session_state.selected_req = None

# Required for request_edit.py form flow from my_requests.py
if "show_request_edit_form" not in st.session_state:
    st.session_state.show_request_edit_form = False

# st.divider()

# Sidebar Menu
with st.sidebar:
    # IMPORTANT:
    # st.set_page_config should be called only once and before other Streamlit commands.
    # It is already called above, so the old duplicate call is intentionally not used here.
    # st.set_page_config(initial_sidebar_state="expanded")

    # st.image("ETS_Digital_RGB_Ink.jpeg", width=100)
    st.markdown("### Navigation")

    pages = {
        "🏠 Home": "Home",
        "📝 Submit a Request": "Submit",
        "📋 My Requests": "My Requests",
        "👥 BU SLT Review": "SLT Review",
        "📖 People Process Review": "People Process Review",
        "📖 HRBP Review": "HRBP Review",
        "📖 Division Finance Review": "Comp Review",
        "📖 HRTA Review": "HRTA Review",
        "📖 Senior Leadership Review": "Senior Leadership Review",
        "📊 Session Analytics": "Session Analytics",
        "⚙️ BU Settings": "BU Settings",
    }

    # =====================================================
    # Sidebar navigation with active page highlight
    # =====================================================
    #0078D4
    st.markdown("""
    """, unsafe_allow_html=True)

    for label, page in pages.items():
        # If this is the currently selected page, show highlighted block
        if st.session_state.page == page:
            st.markdown(
                f"""
 {label}
                """,
                unsafe_allow_html=True,
            )
        # Otherwise show normal clickable button
        else:
            if st.button(
                label,
                use_container_width=True,
                key=f"nav_{page}",
            ):
                st.session_state.page = page
                st.session_state.current_page = "home"

                # Reset request edit state when user manually navigates to another page
                st.session_state.show_request_edit_form = False
                st.session_state.selected_req = None

                st.rerun()

    # st.markdown(
    #     """
    #     """,
    #     unsafe_allow_html=True
    # )

    # for label, page in pages.items():
    #     if st.button(label, use_container_width=True):
    #         st.session_state.page = page

# Main Content
page = st.session_state.page

if st.session_state.current_page == "jd_edit":
    import jd_edit
    jd_edit.show()
    st.stop()

# Optional compatibility route for request_edit.py.
# Your current my_requests.py directly imports request_edit and calls request_edit.show(...).
# This block is added only so app2 also supports request_edit page routing if needed later.
if st.session_state.current_page == "request_edit":
    import request_edit
    request_edit.show(st.session_state.selected_req)
    st.stop()

if page == "Home":
    # st.header("Home")
    import home_page
    home_page.show()

elif page == "Submit":
    import jd2
    jd2.show()

elif page == "My Requests":
    import my_requests
    my_requests.show()

elif page == "SLT Review":
    st.header("SLT Review")

elif page == "People Process Review":
    st.header("People Process Review")

elif page == "HRBP Review":
    st.header("HRBP Review")

elif page == "Comp Review":
    st.header("Division Finance Review")

elif page == "HRTA Review":
    st.header("HRTA Review")

elif page == "Senior Leadership Review":
    st.header("Senior Leadership Review")

elif page == "Session Analytics":
    st.header("Session Analytics")

elif page == "BU Settings":
    st.header("BU Settings")
