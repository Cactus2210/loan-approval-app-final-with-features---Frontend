from fastapi import APIRouter
from pydantic import BaseModel
import json

router = APIRouter()

class Feedback(BaseModel):
    input_data: dict
    model_decision: str
    user_decision: str
    reason: str

@router.post("/")
def submit_feedback(feedback: Feedback):
    with open("data/feedback_log.json", "a") as f:
        f.write(json.dumps(feedback.dict()) + "\n")
    return {"status": "Feedback received"}