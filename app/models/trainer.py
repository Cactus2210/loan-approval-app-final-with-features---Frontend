import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

def train_model(data_path: str, model_path: str):
    print("✅ Reading dataset...")
    df = pd.read_excel(data_path)

    print("✅ Preprocessing data...")
    df['previous_loan_defaults_on_file'] = df['previous_loan_defaults_on_file'].map({'Yes': 1, 'No': 0})

    X = df.drop('loan_status', axis=1)._get_numeric_data()
    y = df['loan_status']

    print(f"✅ Shape of X: {X.shape}, y: {y.shape}")

    print("✅ Splitting and training model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    print(f"✅ Saving model to {model_path} ...")
    joblib.dump(model, model_path)

    print("✅ Model trained and saved successfully!")

# Entry point for direct execution
if __name__ == "__main__":
    data_path = os.path.join("data", "loan_data.xlsx")
    model_path = os.path.join("models", "classifier.pkl")
    train_model(data_path, model_path)
