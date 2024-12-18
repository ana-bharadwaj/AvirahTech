import streamlit as st
st.set_page_config(layout="wide")

def admin_login():
    st.subheader("Admin Login")
    admin_id = st.text_input("Admin ID", key="admin_id_input")
    admin_password = st.text_input("Admin Password", type="password", key="admin_password_input")
    if st.button("Login as Admin", key="admin_login_button"):
        # Check credentials and perform login logic her
        if admin_id == "admin" and admin_password == "admin_password":
            st.success(st.switch_page("pages/admin_entry.py"))
            # Redirect to admin dashboard or perform necessary actions
        else:
            st.error("Invalid admin credentials")

def user_login():
    st.subheader("User Login")
    user_id = st.text_input("User ID", key="user_id_input")
    user_password = st.text_input("User Password", type="password", key="user_password_input")
    if st.button("Login as User", key="user_login_button"):
        # Check credentials and perform login logic here
        # Example: query database or check against predefined credentials
        if user_id == "user" and user_password == "user_password":
            st.success("User login successful")
            # Redirect to user dashboard or perform necessary actions
        else:
            st.error("Invalid user credentials")

def main():
    # Add a blue header with the logo
    st.markdown(
        """
        <style>
        .header {
            background-color: #0078FF;
            padding: 10px;
            border-radius: 5px;
            color: white;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-top: 0px; /* Adjust margin-top to make header topmost */
            width: 100%; /* Ensure header occupies entire width */
            display: flex; /* Enable flexbox layout */
            align-items: center; /* Center content vertically within the header */
            justify-content: flex-start; /* Align content to the start (left) of the header */
        }
        .logo {
            max-width: 50px;
            margin-right: 10px;
        }
        }

        .stApp {

            background-color: white;

            color: black;

        }
        .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 5rem;
        padding-right: 5rem;
                }
        </style>
        """
    , unsafe_allow_html=True)

    st.markdown('<div class="header"><img src="ins_logo.png" class="logo">Login Page</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        admin_login()
    with col2:
        user_login()

if __name__ == "__main__":
    main()
