from fastapi import APIRouter
from app.models.predictor import make_prediction
from app.models.explainer import explain_prediction

router = APIRouter()

@router.post("/")
def predict(input_data: dict):
    prediction, probability = make_prediction(input_data)
    explanation = explain_prediction(input_data)
    return {
        "prediction": "Approved" if prediction == 1 else "Rejected",
        "probability": probability,
        "explanation": explanation
    }