import streamlit as st
import psycopg2

st.set_page_config(layout="wide")
showSidebarNavigation = False

def connect_to_database():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="1020",
            host="localhost",
            port="5432",
            database="avirahtech"
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

# Function to check admin credentials against PostgreSQL database
def check_admin_credentials(admin_id, admin_password):
    connection = connect_to_database()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM admin WHERE adminid = %s AND adminpas = %s", (admin_id, admin_password))
            admin = cursor.fetchone()
            if admin:
                return True
            else:
                return False
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
def check_user_credentials(user_id, user_password):
    connection = connect_to_database()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE userid = %s AND userpas = %s", (user_id, user_password))
            user = cursor.fetchone()
            if user:
                return True
            else:
                return False
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()

def admin_login():
    st.subheader("Admin Login")
    admin_id = st.text_input("Admin ID", key="admin_id_input")
    admin_password = st.text_input("Admin Password", type="password", key="admin_password_input")
    if st.button("Login as Admin", key="admin_login_button"):
        # Check credentials against the database
        if check_admin_credentials(admin_id, admin_password):
            st.success("Admin login successful")
            st.session_state['adminT'] = True
            print(st.session_state)
            # Redirect to admin dashboard or perform necessary actions
            st.switch_page("pages/Home.py")
        else:
            st.error("Invalid admin credentials")

def user_login():
    st.subheader("User Login")
    user_id = st.text_input("User ID", key="user_id_input")
    user_password = st.text_input("User Password", type="password", key="user_password_input")
    if st.button("Login as User", key="user_login_button"):
        # Check credentials and perform login logic here
        # Example: query database or check against predefined credentials
        if check_user_credentials(user_id, user_password):
            st.success("User login successful")
            st.session_state['adminT'] = False
            print(st.session_state)
            # Redirect to admin dashboard or perform necessary actions
            st.switch_page("pages/Home.py")
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

    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="header"><img src="ins_logo.png" class="logo">Login Page</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        admin_login()
    with col2:
        user_login()

if __name__ == "__main__":
    main()
