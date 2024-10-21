from fastapi import FastAPI, File, UploadFile, HTTPException
import pandas as pd
from pandas import DataFrame
import os

app = FastAPI()

# Directory for saving CSV files
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def calculate_ach(df: DataFrame):
    # TODO: add logic to calculating ach
    return 30.0


def categorize_insulation(ach: float):
    # TODO: add logic to categorize insulation based on ach
    return "good"



@app.post("/upload-and-process-csv/")
async def upload_csv(file: UploadFile = File(...)):
    # Check if file is a CSV
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
    
    try:
        # Read the CSV file contents into a pandas DataFrame
        df = pd.read_csv(file.file)
        
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
