import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Set page title
st.set_page_config(page_title="SQL Injection Detector", page_icon=":shield:")

# Load the model and tokenizer
@st.cache_resource
def load_resources():
    model = load_model("./sql_injection_model.h5")
    with open("./tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)
    return model, tokenizer

model, tokenizer = load_resources()

# Set max sequence length
max_sequence_length = 100

# Title and description
st.title("SQL Injection Detection")
st.write("Detect whether an SQL query is safe or potentially malicious.")

# User input
user_query = st.text_input("Enter an SQL query:", "")

# Prediction button
if st.button("Check Query"):
    if user_query:
        # Preprocess user input
        query_tokenized = tokenizer.texts_to_sequences([user_query])
        query_padded = pad_sequences(query_tokenized, maxlen=max_sequence_length, padding='post')

        # Make prediction
        prediction = model.predict(query_padded)[0][0]
        if prediction > 0.5:
            st.error("⚠️ SQL Injection Detected!")
        else:
            st.success("✅ Query is Safe.")
    else:
        st.warning("Please enter an SQL query.")

# Footer
st.write("Developed by Ankit")
