import shap
import pandas as pd
import joblib

model = joblib.load("models/classifier.pkl")

def explain_prediction(input_data: dict):
    df = pd.DataFrame([input_data])
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(df)

    # Handle both binary and multi-class scenarios
    if isinstance(shap_values, list) and len(shap_values) > 1:
        shap_vals = shap_values[1][0]  # class 1
    else:
        shap_vals = shap_values[0] if isinstance(shap_values, list) else shap_values[0]

    return dict(zip(df.columns, shap_vals.tolist()))
