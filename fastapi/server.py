from fastapi import FastAPI, File, UploadFile, HTTPException
import pandas as pd
from pandas import DataFrame
import os

app = FastAPI()

# Directory for saving CSV files
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def calculate_ach(co2_data: DataFrame):
    co2_start = co2_data['CO2 Level (ppm)'].iloc[0]
    co2_end = co2_data['CO2 Level (ppm)'].iloc[-1]
    ach = (co2_start - co2_end) / len(co2_data)
    return ach


def categorize_insulation(ach: float):
    if ach < 0.0:
        return "Very Bad Isolation"
    elif ach < 0.25:
        return "Bad Isolation"
    else:
        return "Good Isolation"



@app.post("/upload-and-process-csv/")
async def upload_csv(file: UploadFile = File(...)):
    # Check if file is a CSV
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
    
    try:
        # Read the CSV file contents into a pandas DataFrame
        df = pd.read_csv(file.file, header=0)
        
        # Perform the ACH calculation
        ach = calculate_ach(df)
        
        # Categorize the airtightness based on ACH value
        insulation_category = categorize_insulation(ach)
        
        # Return results to the user
        return {
            "ach": ach,
            "insulation": insulation_category
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV file: {str(e)}")
