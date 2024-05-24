import streamlit as st
import pandas as pd

# Define a session state to persist data across script reruns
session_state = st.session_state

# Initialize component list if it doesn't exist in the session state
if 'component_list' not in session_state:
    session_state.component_list = []

def main():
    st.title("Tech Assembly Counter")

    # Display inputs side by side
    col1, col2 = st.columns([3, 2])

    with col1:
        engine_type = st.text_input("Enter Engine Type")

    with col2:
        num_tech_assemblies = st.number_input("Enter Number of Tech Assemblies", min_value=3, value=3, step=1)

    st.subheader("Parts")
    part_cols = st.columns(num_tech_assemblies)
    for i, col in enumerate(part_cols):
        with col:
            st.button(f"Part {i+1}")

    # Place form and table side by side
    form_col, table_col = st.columns([1, 2])

    with form_col:
        st.subheader("Add Component Details")

        # Text input for component
        component = st.text_input("Component")

        # Radial buttons for axial and radial measurements presence
        with st.expander("Select Measurements"):
            axial_present = st.radio("Axial Measurements", options=["Present", "Not Present"], key="axial_present")
            radial_present = st.radio("Radial Measurements", options=["Present", "Not Present"], key="radial_present")

        # Number inputs for tolerance for axial and radial
        with st.expander("Enter Tolerance"):
            axial_tolerance = st.number_input("Axial Tolerance (microns)", key="axial_tolerance")
            radial_tolerance = st.number_input("Radial Tolerance (microns)", key="radial_tolerance")

        if st.button("Add Component"):
            # Create a dictionary to store component details
            component_details = {
                "Component": component,
                "Axial-Measurements": axial_present,
                "Radial-Measurements": radial_present,
                "Radial-Tolerance(microns)": radial_tolerance,
                "Axial-Tolerance(microns)": axial_tolerance
            }

            # Append the dictionary to the session state component list
            session_state.component_list.append(component_details)

            # Clear the form fields
            st.session_state["Component"] = ""
            st.session_state["axial_present"] = "Present"
            st.session_state["radial_present"] = "Present"
            st.session_state["axial_tolerance"] = 0
            st.session_state["radial_tolerance"] = 0

    with table_col:
        # Convert the session state component list to a DataFrame
        df = pd.DataFrame(session_state.component_list)

        # Display the table using HTML without vertical border lines
        st.subheader("Assembly Details")
        st.write(get_table_html(df), unsafe_allow_html=True)

        # Check if any row is selected for deletion
        row_to_delete = st.selectbox("Select Row to Delete", [None] + list(df.index))

        # Delete the selected row
        if row_to_delete is not None:
            df = df.drop(index=row_to_delete)
            st.write("Row deleted successfully!")

        # Update the session state with the modified DataFrame
        session_state.component_list = df.to_dict(orient="records")

def get_table_html(df):
    # Create HTML table string without vertical border lines
    table_html = """
    <style>
    table {
        border-collapse: collapse;
        width: 100%;
    }
    th, td {
        border: none;
        padding: 8px;
        text-align: left;
    }
    tr:nth-child(even) {
        background-color: #FAF9F6;
        color: black;
    }
    th {
        background-color: #ADD8E6;
        color: black;
    }
    </style>
    <table>
    <tr>"""
    for col in df.columns:
        table_html += f"<th>{col}</th>"
    table_html += "</tr>"

    for index, row in df.iterrows():
        table_html += "<tr>"
        for value in row:
            table_html += f"<td contenteditable='true'>{value}</td>"
        table_html += "</tr>"

    table_html += "</table>"
    return table_html

if __name__ == "__main__":
    main()
