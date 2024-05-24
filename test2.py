import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

def main():
    # Initialize session state for DataFrame
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=["A", "B", "C", "D"])

    st.title("Interactive Table with AgGrid")

    # AgGrid options
    gb = GridOptionsBuilder.from_dataframe(st.session_state.df)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    grid_options = gb.build()

    # Display the DataFrame using AgGrid
    grid_response = AgGrid(
        st.session_state.df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=True,
        height=400,
        theme='streamlit'
    )

    # Create buttons to add and delete rows
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Add Row"):
            add_row()

    with col2:
        if st.button("Delete Selected Rows"):
            if 'selected_rows' in grid_response and grid_response['selected_rows']:
                selected_indices = [row['_selectedRowNodeInfo']['nodeIndex'] for row in grid_response['selected_rows']]
                delete_rows(selected_indices)

    # Save any changes made through AgGrid back to the session state
    edited_df = pd.DataFrame(grid_response['data'])
    st.session_state.df = edited_df

    # Display the updated DataFrame
    st.write("Current Table Data:")
    st.dataframe(st.session_state.df)

def add_row():
    new_row = pd.Series([None]*len(st.session_state.df.columns), index=st.session_state.df.columns)
    st.session_state.df = pd.concat([st.session_state.df, new_row.to_frame().transpose()], ignore_index=True)

def delete_rows(selected_indices):
    st.session_state.df.drop(selected_indices, inplace=True)
    st.session_state.df.reset_index(drop=True, inplace=True)

if __name__ == "__main__":
    main()
