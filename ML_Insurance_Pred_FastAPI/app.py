from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pickle
import uvicorn
import numpy as np
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

model = pickle.load(open("model.pkl","rb"))

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

class InsuranceInput(BaseModel):
    age:int
    sex:str
    bmi:float
    children:int
    smoker:str
    region:str

region_map={'Northwest':0,'Northeast':1,'Southeast':2,'Southwest':3}
sex_map={'Male':0,'Female':1}
smoker_map={'Yes':1,'No':0}

@app.get("/")
def home(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})

@app.post("/predict")
def predict_charges(input_data: InsuranceInput):
    new_data=pd.DataFrame({
        'age':[input_data.age],
        'sex':[input_data.sex],
        'bmi':[input_data.bmi],
        'children':[input_data.children],
        'smoker':[input_data.smoker],
        'region':[input_data.region],
    })

    new_data['smoker']=new_data['smoker'].map(smoker_map)
    new_data.drop(columns=['sex','region'],inplace=True)

    prediction=model.predict(new_data)[0]
    return {'predicted_charges':round(float(prediction),2)}

if __name__=="__main__":
    uvicorn.run(app, port=8000)