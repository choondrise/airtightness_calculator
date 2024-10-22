import streamlit as st
import requests
import pandas as pd
import io

# URL for FastAPI backend
FASTAPI_URL = "http://fastapi:8000/upload-and-process-csv/"

# Function to convert uploaded file to CSV
def convert_to_csv(uploaded_file):
    # Read the uploaded file into a DataFrame
    try:
        # Assuming the uploaded file can be read as CSV
        df = pd.read_csv(uploaded_file)
        st.write("Data:")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error reading the uploaded file: {e}")
        return None

    # Convert DataFrame to CSV
    csv = df.to_csv(index=False)
    return csv

# Streamlit app
st.title("Airtightness Calculator")

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "txt"])

if uploaded_file is not None:
    # Convert the uploaded file to CSV format
    csv_data = convert_to_csv(uploaded_file)

    if csv_data is not None:
        # Sending the CSV data to the FastAPI endpoint
        response = requests.post(FASTAPI_URL, files={"file": ("data.csv", io.StringIO(csv_data), "text/csv")})

        # Handle the response from the FastAPI server
        if response.status_code == 200:
            result = response.json()
            st.success("File processed successfully!")
            st.write("Air Changes per Hour (ACH):", result['ach'])
            st.write("Insulation Category:", result['insulation'])
        else:
            st.error("Error processing file: " + response.text)