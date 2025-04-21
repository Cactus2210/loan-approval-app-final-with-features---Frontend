import joblib
import pandas as pd

model = joblib.load("models/classifier.pkl")

def make_prediction(input_data: dict):
    df = pd.DataFrame([input_data])
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0].tolist()
    return prediction, probability