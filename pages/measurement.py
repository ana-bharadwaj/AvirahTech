import streamlit as st
import psycopg2
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")

# Function to fetch engine types from PostgreSQL table
def fetch_engine_types():
    connection = psycopg2.connect(
        user="postgres",
        password="1020",
        host="localhost",
        port="5432",
        database="avirahtech"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT engtype FROM engine_config")
    engine_types = [row[0] for row in cursor.fetchall()]
    connection.close()
    return engine_types

# Function to fetch tech assemblies for a given engine type from part_details table
def fetch_techassembly_for_engine_type(engine_type):
    connection = psycopg2.connect(
        user="postgres",
        password="1020",
        host="localhost",
        port="5432",
        database="avirahtech"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT techassembly FROM part_details WHERE engtype = %s", (engine_type,))
    tech_assemblies = [row[0] for row in cursor.fetchall()]
    connection.close()
    return tech_assemblies

# Function to fetch parts for a given tech assembly from part_details table
def fetch_parts_for_tech_assembly(tech_assembly):
    connection = psycopg2.connect(
        user="postgres",
        password="1020",
        host="localhost",
        port="5432",
        database="avirahtech"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT part FROM part_details WHERE techassembly = %s", (tech_assembly,))
    parts = [row[0] for row in cursor.fetchall()]
    connection.close()
    return parts

# Function to check part status in processtrack table
def check_part_status(part):
    connection = psycopg2.connect(
        user="postgres",
        password="1020",
        host="localhost",
        port="5432",
        database="avirahtech"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT completed FROM processtrack WHERE part = %s", (part,))
    status = cursor.fetchone()
    connection.close()
    return status[0] if status else None

# Function to plot circle with marked degrees
def plot_circle():
    fig, ax = plt.subplots()
    circle = plt.Circle((0.5, 0.5), 0.4, color='blue', fill=False)
    ax.add_artist(circle)

    # Mark degrees
    for deg in range(0, 361, 90):
        rad = np.deg2rad(deg)
        x = 0.5 + 0.4 * np.cos(rad)
        y = 0.5 + 0.4 * np.sin(rad)
        ax.text(x, y, str(deg), horizontalalignment='center', verticalalignment='center')

    ax.set_aspect('equal')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    st.pyplot(fig)

# Main function to create Streamlit app
def main():
    st.title("Engine Part Details")

    # Fetch engine types from PostgreSQL table
    engine_types = fetch_engine_types()

    # Layout the selection criteria side by side
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_engine_type = st.selectbox("Select Engine Type", engine_types)

    # Fetch tech assemblies for the selected engine type
    tech_assemblies = fetch_techassembly_for_engine_type(selected_engine_type)

    with col2:
        selected_tech_assembly = st.selectbox("Select Tech Assembly", tech_assemblies)

    # Fetch parts for the selected tech assembly
    parts = fetch_parts_for_tech_assembly(selected_tech_assembly)

    with col3:
        selected_part = st.selectbox("Select Part", parts)

    # Button to trigger search
    if st.button("Search"):
        st.subheader("Part Details")
        st.write(f"Selected Part: {selected_part}")

        st.subheader("Process Track")

        # Check part status in processtrack table
        status = check_part_status(selected_part)
        if status is not None:
            if status:
                st.write("✔️ Status: True")
            else:
                if st.button("Measure"):
                    # Plot and display the circle with marked degrees
                    plot_circle()
        else:
            if st.button("Measure"):
                # Plot and display the circle with marked degrees
                plot_circle()

if __name__ == "__main__":
    main()
