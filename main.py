import pandas as pd
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.preprocessing import StandardScaler
import pickle

app = FastAPI()

ridge_model = pickle.load(open('models/ridge.pkl', 'rb'))
scalar_model = pickle.load(open('models/scaler.pkl', 'rb'))


# Define request schema
class FireData(BaseModel):
    Temperature: float
    RH: float
    Ws: float
    Rain: float
    FFMC: float
    DMC: float
    ISI: float
    Classes: int
    Region: int

@app.post("/predict")
def predict(data: FireData):
    new_data = scalar_model.transform([[data.Temperature, data.RH, data.Ws, data.Rain, data.FFMC, data.DMC, data.ISI, data.Classes, data.Region]])
    fwi = ridge_model.predict(new_data)
    return {"FWI": float(fwi)}
