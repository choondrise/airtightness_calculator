import streamlit as st
import requests
import pandas as pd
import io

# URL for FastAPI backend
FASTAPI_URL = "http://fastapi:8000/upload-and-process-csv/"


def calculate_ach(df):
    csv_data = df.to_csv(index=False)
    response = requests.post(FASTAPI_URL, files={"file": ('data.csv', io.StringIO(csv_data), "text/csv")})

    # Handle the response from the FastAPI server
    if response.status_code == 200:
        result = response.json()
        st.success("File processed successfully!")
        st.write("Air Changes per Hour (ACH):", result['ach'])
        st.write("Insulation Category:", result['insulation'])
    else:
        st.error("Error processing file: " + response.text)


# Function to convert uploaded file to CSV
def show_data(uploaded_file):
    # Read the uploaded file into a DataFrame
    try:
        # Assuming the uploaded file can be read as CSV
        df = pd.read_csv(uploaded_file)
        df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time
        min_time = df['Time'].min()
        max_time = df['Time'].max()

        st.write("Data:")
        st.dataframe(df.head())

        # Interactivity: Select a range of time to zoom in
        st.subheader("Select Time Interval for ACH Calculation")
        filtered_df = df.copy()
        # Update the chart with the filtered data
        time_selection = st.slider(label="Select Time Range", min_value=min_time, max_value=max_time,
                                    value=(min_time, max_time))

        # Filter the DataFrame based on the selected time range
        filtered_df = df[(df['Time'] >= time_selection[0]) & (df['Time'] <= time_selection[1])]
        chart = st.line_chart(filtered_df['CO2 Level (ppm)'])

        # Call calculate_ach function below the graph
        calculate_ach(filtered_df)


    except Exception as e:
        st.error(f"Error reading the uploaded file: {e}")
        return None

    # Convert DataFrame to CSV
    csv = df.to_csv(index=False)
    return csv

# Streamlit app
st.set_page_config(layout="wide")
st.title("CO₂ Level Visualization and ACH Calculation")

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "txt"])

if uploaded_file is not None:
    # Convert the uploaded file to CSV format
    csv_data = show_data(uploaded_file)