import streamlit as st
from flask import Flask, request
import threading

app = Flask(__name__)

value = ""

@app.route('/endpoint', methods=['POST'])
def receive_data():
    global value
    value = request.form.get('value')
    return "Data received"

def run_flask():
    app.run(port=8000)

threading.Thread(target=run_flask).start()

st.title("ESP32 Real-Time Data Display")

# Add a dropdown at the top of the page
option = st.selectbox(
    'Select an option',
    ('Option 1', 'Option 2', 'Option 3')
)

st.write('You selected:', option)

st.write("Current Value:")
value_placeholder = st.empty()

iframe_code = """
<iframe src="http://your-esp32-ip-address" width="600" height="400"></iframe>
"""
st.markdown(iframe_code, unsafe_allow_html=True)

while True:
    value_placeholder.text(value)
    st.experimental_rerun()
 