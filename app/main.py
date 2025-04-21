from fastapi import FastAPI
from app.routes import predict, feedback, dashboard

app = FastAPI(title="Loan Approval Transparency System")

app.include_router(predict.router, prefix="/predict")
app.include_router(feedback.router, prefix="/feedback")
app.include_router(dashboard.router, prefix="/dashboard")

@app.get("/")
def root():
    return {"message": "Loan Approval AI system is up"}