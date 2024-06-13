import streamlit as st
import psycopg2

# Function to handle form submission and insert data into the database
def handle_submit(engine_type, engine_name, tech_assemblies, num_parts):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname="avirahtech",
            user="postgres",
            password="1020",
            host="localhost",
            port="5432"
        )
        # Create a cursor object
        cur = conn.cursor()

        # Check if the engine_type already exists in engine_config
        cur.execute("SELECT 1 FROM engine_config WHERE engtype = %s", (engine_type,))
        if cur.fetchone() is None:
            # Insert data into the engine_config table
            cur.execute("INSERT INTO engine_config (engtype, engname) VALUES (%s, %s)",
                        (engine_type, engine_name))

        # Generate the techassembly values
        tech_assemblies_list = [f"{engine_name[:3]}T{i}" for i in range(1, tech_assemblies + 1)]

        # Insert data into the engine_techassembly_map table
        for tech_assembly in tech_assemblies_list:
            cur.execute("INSERT INTO engine_techassembly_map (engtype, techassembly) VALUES (%s, %s)",
                        (engine_type, tech_assembly))

        # Insert data into the part_details table
        for tech_assembly in tech_assemblies_list:
            for i in range(num_parts):
                part = f"{tech_assembly}P{i+1}"
                cur.execute(
                    "INSERT INTO part_details (engtype, part, techassembly, serial_presence, radial_presence, axial_tolerance, radial_tolerance) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (engine_type, part, tech_assembly, False, False, 0.0, 0.0)
                )

        # Commit changes
        conn.commit()
        st.write("Data inserted successfully!")
    except (Exception, psycopg2.Error) as error:
        st.error(f"Error inserting data: {error}")
    finally:
        # Close connection
        if conn:
            cur.close()
            conn.close()

# Function to handle search and display results
def handle_search(engine_type, engine_name):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname="avirahtech",
            user="postgres",
            password="1020",
            host="localhost",
            port="5432"
        )
        # Create a cursor object
        cur = conn.cursor()

        # Search for engine configurations
        cur.execute("SELECT pd.part, pd.techassembly, pd.serial_presence, pd.radial_presence, pd.axial_tolerance, pd.radial_tolerance FROM part_details pd WHERE pd.engtype = %s", (engine_type,))
        rows = cur.fetchall()

        if rows:
            st.subheader("Search Results:")
            table_content = "<table><tr><th>Tech Assembly</th><th>Part</th><th>Serial Presence</th><th>Radial Presence</th><th>Serial Tolerance</th><th>Radial Tolerance</th></tr>"
            prev_tech_assembly = None
            for row in rows:
                tech_assembly = row[1]
                part = row[0]
                serial_presence = row[2]
                radial_presence = row[3]
                serial_tolerance = row[4]
                radial_tolerance = row[5]

                # Display the data in the table
                if prev_tech_assembly == tech_assembly:
                    tech_assembly_display = ""
                else:
                    tech_assembly_display = tech_assembly
                    prev_tech_assembly = tech_assembly

                table_content += f"<tr><td>{tech_assembly_display}</td><td>{part}</td><td><input type='radio' name='serial_presence_{tech_assembly}_{part}' {'checked' if serial_presence else ''}></td><td><input type='radio' name='radial_presence_{tech_assembly}_{part}' {'checked' if radial_presence else ''}></td><td><input type='number' step='0.1' name='serial_tolerance_{tech_assembly}_{part}' value='{serial_tolerance}'></td><td><input type='number' step='0.1' name='radial_tolerance_{tech_assembly}_{part}' value='{radial_tolerance}'></td></tr>"
            table_content += "</table>"
            st.markdown(table_content, unsafe_allow_html=True)

            if st.button("Submit"):
                # Update values in the table based on user input
                for row in rows:
                    tech_assembly = row[1]
                    part = row[0]
                    serial_presence = bool(st.radio(f"Serial Presence for {tech_assembly} {part}", options=[False, True], index=1 if row[2] else 0))
                    radial_presence = bool(st.radio(f"Radial Presence for {tech_assembly} {part}", options=[False, True], index=1 if row[3] else 0))
                    serial_tolerance = st.number_input(f"Serial Tolerance for {tech_assembly} {part}", value=row[4], step=0.1)
                    radial_tolerance = st.number_input(f"Radial Tolerance for {tech_assembly} {part}", value=row[5], step=0.1)

                    # Update values in the database (Replace this with your actual update logic)
                    cur.execute("UPDATE part_details SET serial_presence = %s, radial_presence = %s, axial_tolerance = %s, radial_tolerance = %s WHERE engtype = %s AND part = %s", (serial_presence, radial_presence, serial_tolerance, radial_tolerance, engine_type, part))

                conn.commit()
                st.write("Values updated successfully!")


        else:
            st.write("No matching records found.")

    except (Exception, psycopg2.Error) as error:
        st.error(f"Error searching data: {error}")
    finally:
        # Close connection
        if conn:
            cur.close()
            conn.close()

# Create the option containers
option = st.sidebar.radio("Choose an option:", [ "Create New", "Search"])

# Display content based on the selected option

if option == "Create New":
    st.subheader("Create New")
    engine_type = st.text_input("Engine Type:")
    engine_name = st.text_input("Engine Name:")
    tech_assemblies = st.number_input("Number of Tech Assemblies:", step=1, min_value=3, value=3)
    num_parts = st.number_input("Number of Parts:", step=1, min_value=1)

    if st.button("Submit"):
        handle_submit(engine_type, engine_name, tech_assemblies, num_parts)
elif option == "Search":
    st.subheader("Search")
    engine_type_search = st.text_input("Enter Engine Type to search:")
    engine_name_search = st.text_input("Enter Engine Name to search:")

    if st.button("Search"):
        handle_search(engine_type_search, engine_name_search)
