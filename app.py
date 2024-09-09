from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import uvicorn
import os

app = FastAPI()

# Load the trained model
model = joblib.load('student_gpa_model.pkl')

# Define the data structure for the input
class StudentData(BaseModel):
    Gender: str
    Age: int
    StudyHoursPerWeek: int
    AttendanceRate: float
    Major: str
    PartTimeJob: str
    ExtraCurricularActivities: str

@app.post("/predict/")
def predict(data: StudentData):
    # Convert input data to dataframe
    input_data = pd.DataFrame([data.dict()])
    
    # Make prediction using the model
    try:
        prediction = model.predict(input_data)
        return {"GPA": prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Entry point to run the FastAPI app with Uvicorn
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # Default to 8080 if PORT is not set
    uvicorn.run(app, host="0.0.0.0", port=port)
