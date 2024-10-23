import streamlit as st
import requests
import pandas as pd
import io
import plotly.graph_objects as go

# URL for FastAPI backend
FASTAPI_URL = "http://fastapi:8000/upload-and-process-csv/"


def plot_speedometer(value, min_value, max_value):
    good_range = (0.1, max_value)
    bad_range = (-0.1, 0.1)
    very_bad_range = (min_value, -0.1)

    # Set color and label based on value
    if value > good_range[0]:
        color = "green"
        label = "Good"
    elif value < very_bad_range[1]:
        color = "red"
        label = "Very Bad"
    else:
        color = "yellow"
        label = "Bad"

    # Create the speedometer
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": "ACH (Air Changes per Hour)"},
            gauge={
                "axis": {"range": [min_value, max_value]},
                "bar": {"color": color}
            },
        )
    )

    # Add the label text inside the gauge
    fig.add_annotation(
        text=label,
        font={"size": 40, "color": color},
        showarrow=False,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        bgcolor="rgba(255, 255, 255, 0)",  # Background color for the label
        align="center"
    )

    # Show the speedometer
    st.plotly_chart(fig)



def calculate_ach(df):
    csv_data = df.to_csv(index=False)
    response = requests.post(FASTAPI_URL, files={"file": ('data.csv', io.StringIO(csv_data), "text/csv")})

    # Handle the response from the FastAPI server
    if response.status_code == 200:
        result = response.json()
        # st.write("Air Changes per Hour (ACH):", result['ach'])
        # st.write("Insulation Category:", result['insulation'])
        plot_speedometer(result['ach'], -1, 1)
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
        st.success("File processed successfully!")

        col1, col2 = st.columns(2)

        with col1:
            # Interactivity: Select a range of time to zoom in
            st.subheader("Select Time Interval for ACH Calculation")
            filtered_df = df.copy()
            # Update the chart with the filtered data
            time_selection = st.slider(label="Select Time Range", min_value=min_time, max_value=max_time,
                                        value=(min_time, max_time))

            # Filter the DataFrame based on the selected time range
            filtered_df = df[(df['Time'] >= time_selection[0]) & (df['Time'] <= time_selection[1])]
            chart = st.line_chart(filtered_df['CO2 Level (ppm)'])

        with col2:
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