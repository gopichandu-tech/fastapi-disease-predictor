from pydantic import BaseModel

class PredictionRequest(BaseModel):
    user_name: str
    email: str
    symptoms: str

class PredictionResponse(BaseModel):
    prediction: str
