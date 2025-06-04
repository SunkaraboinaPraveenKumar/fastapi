from fastapi import FastAPI

import pandas as pd
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from model.predict import predict_output, model, MODEL_VERSION
from schema.prediction_response import PredictionResponse

app = FastAPI()


#human readable.
@app.get("/")
def home():
    return JSONResponse(status_code=200, content={
        "message": "Welcome to the Health Insurance Premium Prediction API"
    })


#services like aws, kubernetes, load balancer etc. use this endpoint to check if the service is up and running.
@app.get("/health")
def health_check():
    return JSONResponse(status_code=200, content={
        "status": "OK",
        "version":MODEL_VERSION,
        'model_loaded': model is not None,
    })
        
@app.post("/predict", response_model=PredictionResponse)
def predict_premium(data: UserInput):
    user_input = data.dict()

    try:
        prediction = predict_output(user_input)
        return PredictionResponse(**prediction)
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "message": "An error occurred while processing the prediction."
        })
