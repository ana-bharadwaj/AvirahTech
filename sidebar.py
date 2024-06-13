import streamlit as st

def create_sidebar():
    user_role = st.session_state.get('adminT', None)

    if user_role == True:
        st.sidebar.header("Admin Pages")
        if st.sidebar.button("Measurements"):
            st.write("Admin: Measurements page")
        if st.sidebar.button("Assembly Configuration"):
            st.switch_page("pages/admin_entry.py")
        if st.sidebar.button("User Configuration"):
            st.write("Admin: User Configuration page")
        if st.sidebar.button("Passwords"):
            st.write("Admin: Passwords page")
        if st.sidebar.button("Reports"):
            st.write("Admin: Reports page")
    else:
        st.sidebar.header("User Pages")
        if st.sidebar.button("Measurements"):
            st.write("User: Measurements page")
        if st.sidebar.button("Reports"):
            st.write("User: Reports page")
