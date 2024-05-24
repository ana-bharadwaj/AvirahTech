import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import pandas as pd

# Initialize session state DataFrame if not already initialized
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        'a': [''],
        'b': [''],
        'c': [''],
        'd': ['']
    })

# Streamlit page configuration
st.set_page_config(page_title="Editable Table with AG Grid", layout="wide")

# Title of the app
st.title("Editable Table with AG Grid")

# Create a GridOptionsBuilder instance
gb = GridOptionsBuilder.from_dataframe(st.session_state.df)
gb.configure_default_column(editable=True, resizable=True)
gb.configure_grid_options(domLayout='autoHeight')

# Add Row and Delete Row configurations
gb.configure_side_bar()
gb.configure_pagination(paginationAutoPageSize=True)
gb.configure_selection(selection_mode="multiple", use_checkbox=True)

# Customize the theme and style
custom_css = """
.ag-theme-streamlit .ag-header-cell-label {
    justify-content: center;
}
.ag-theme-streamlit .ag-header-cell-text {
    color: white;
    font-weight: bold;
}
.ag-theme-streamlit .ag-row-even {
    background-color: #f0f2f6;
}
.ag-theme-streamlit .ag-row-odd {
    background-color: white;
}
.ag-theme-streamlit .ag-cell {
    padding: 10px;
    text-align: center;
}
.ag-theme-streamlit .ag-header {
    background-color: #2c3e50;
}
"""

# Inject custom CSS
st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)

# Build the grid options
gridOptions = gb.build()

# Display the grid
response = AgGrid(
    st.session_state.df,
    gridOptions=gridOptions,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode=DataReturnMode.AS_INPUT,
    enable_enterprise_modules=True,
    fit_columns_on_grid_load=True,
    theme="streamlit"
)

# Update DataFrame with changes made by the user
if response['data'] is not None:
    st.session_state.df = pd.DataFrame(response['data'])

# Display buttons side by side
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Add Row"):
        new_row = pd.DataFrame({'a': [''], 'b': [''], 'c': [''], 'd': ['']})
        st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
        st.experimental_rerun()

with col2:
    if st.button("Delete Selected Rows"):
        selected_rows = response['selected_rows']
        if selected_rows:
            selected_rows_df = pd.DataFrame(selected_rows)
            # Identify the rows in the DataFrame to drop
            indices_to_drop = st.session_state.df.merge(selected_rows_df, how='right', indicator=True).query('_merge == "both"').index
            st.session_state.df.drop(indices_to_drop, inplace=True)
            st.session_state.df.reset_index(drop=True, inplace=True)
            st.experimental_rerun()
