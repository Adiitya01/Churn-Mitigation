from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import numpy as np
import os

app = FastAPI(title="Financial Intelligence API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models with correct relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHURN_MODEL_PATH = os.path.join(BASE_DIR, "..", "Models", "churn_model.pkl")
ALLOWANCE_MODEL_PATH = os.path.join(BASE_DIR, "..", "Models", "allowance_model.pkl")

with open(CHURN_MODEL_PATH, 'rb') as f:
    churn_model = pickle.load(f)

with open(ALLOWANCE_MODEL_PATH, 'rb') as f:
    allowance_model = pickle.load(f)

# Pydantic Schemas for validation
class ChurnRequest(BaseModel):
    CustomerId: str
    Age: float
    CreditScore: float
    Tenure: float
    TransactionFrequency: float
    AvgTransactionAmount: float
    ComplaintsFiled: float
    CustomerSatisfaction: float
    HasLoan: bool
    Balance: float

class AllowanceRequest(BaseModel):
    CreditScore: float
    Gender: str
    Age: float
    Tenure: float
    Balance: float
    NumOfProducts: float
    HasCrCard: bool
    IsActiveMember: bool
    EstimatedSalary: float

@app.get("/")
async def root():
    return {"message": "Financial Intelligence API is Online", "docs": "/docs"}

@app.post("/predict_churn")
async def predict_churn(data: ChurnRequest):
    try:
        features = [
            data.Age,
            data.CreditScore,
            data.Tenure,
            data.TransactionFrequency,
            data.AvgTransactionAmount,
            data.ComplaintsFiled,
            data.CustomerSatisfaction,
            1.0 if data.HasLoan else 0.0,
            data.Balance
        ]
        
        features_array = np.array(features).reshape(1, -1)
        
        # Get probability of Churn (Class 1)
        prob = churn_model.predict_proba(features_array)[0][1]
        prediction = int(churn_model.predict(features_array)[0])
        
        risk_level = "Critical" if prob > 0.7 else "Moderate" if prob > 0.4 else "Low"

        return {
            "CustomerId": data.CustomerId,
            "probability": round(float(prob) * 100, 2),
            "risk_level": risk_level,
            "prediction": "High chance of churn" if prediction == 1 else "Low chance of churn"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict_allowance")
async def predict_allowance(data: AllowanceRequest):
    try:
        gender_encoded = 1.0 if data.Gender.lower() == 'male' else 0.0
        
        features = [
            data.CreditScore,
            gender_encoded,
            data.Age,
            data.Tenure,
            data.Balance,
            data.NumOfProducts,
            1.0 if data.HasCrCard else 0.0,
            1.0 if data.IsActiveMember else 0.0,
            data.EstimatedSalary
        ]
        
        features_array = np.array(features).reshape(1, -1)
        
        # Get probability of Approval
        prob = allowance_model.predict_proba(features_array)[0][1]
        prediction = int(allowance_model.predict(features_array)[0])
        
        status = "Elite" if prob > 0.8 else "Standard" if prob > 0.4 else "Ineligible"
        
        return {
            "prediction": "Allowance Approved" if prediction == 1 else "Allowance Not Approved",
            "probability": round(float(prob) * 100, 2),
            "status": status
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
