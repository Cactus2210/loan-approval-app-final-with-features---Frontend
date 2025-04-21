from fastapi import APIRouter
import json

router = APIRouter()

@router.get("/")
def get_dashboard_data():
    try:
        with open("data/feedback_log.json", "r") as f:
            logs = [json.loads(line) for line in f.readlines()]
    except FileNotFoundError:
        logs = []

    overrides = [log for log in logs if log["model_decision"] != log["user_decision"]]
    return {
        "total_feedbacks": len(logs),
        "overrides": len(overrides),
        "override_rate": len(overrides) / len(logs) if logs else 0.0
    }