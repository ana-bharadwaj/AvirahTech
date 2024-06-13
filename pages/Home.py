import streamlit as st
from st_pages import Page, add_page_title, show_pages, hide_pages

"## Declaring the pages in your app:"
user_role = st.session_state.get('adminT', None)
st.write(user_role)

if(user_role == True):
    show_pages(
        [
            Page("pages/admin_entry.py", "Assembly Configuration"),
            # Can use :<icon-name>: or the actual icon
            Page("pages/measurement.py", "Measurement"),
            # The pages appear in the order you pass them
            Page("pages/reports.py", "Reports"),
            Page("pages/userconfig.py", "User Configuration"),
            Page("pages/passwords.py","Passwords"),
        ]
    )
else:
    show_pages(
        [
            Page("pages/measurement.py", "Measurement"),
            # The pages appear in the order you pass them
            Page("pages/reports.py", "Reports"),
        ]
    )
    hide_pages(
        [
            Page("pages/admin_entry.py", "Assembly Configuration"),
            Page("pages/userconfig.py", "User Configuration"),
            Page("pages/passwords.py","Passwords"),
        ]
    )


