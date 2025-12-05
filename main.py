from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pickle
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load saved encoders & model
model = pickle.load(open("model.pkl", "rb"))
le_caste = pickle.load(open("le_caste.pkl", "rb"))
le_district = pickle.load(open("le_district.pkl", "rb"))
le_scheme = pickle.load(open("le_scheme.pkl", "rb"))

class InputData(BaseModel):
    age: int
    income: int
    is_farmer: int
    is_woman: int
    is_student: int
    caste: str
    district: str

@app.post("/predict")
def predict(data: InputData):

    caste_num = le_caste.transform([data.caste])[0]
    district_num = le_district.transform([data.district])[0]

    x = np.array([[data.age, data.income, data.is_farmer, data.is_woman,
                   data.is_student, caste_num, district_num]])

    pred_id = model.predict(x)[0]
    pred_name = le_scheme.inverse_transform([pred_id])[0]

    return {"recommended_scheme": pred_name}