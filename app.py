import streamlit as st
import requests
from frontend.utils import call_api
from app.utils.bias_checker import detect_bias

st.set_page_config(page_title="Loan Approval AI System", layout="centered")

base_url = "https://web-production-8a84a.up.railway.app"

menu = st.sidebar.selectbox("📌 Select Page", ["🔍 Prediction", "📝 Feedback", "📊 Dashboard"])

# ------------------ 🔍 Prediction Page ------------------ #
if menu == "🔍 Prediction":
    st.title("Loan Approval Predictor")

    form_data = {
        "person_age": st.slider("Age", 18, 100, 30),
        "person_income": st.number_input("Income", 10000, 1000000, 50000),
        "person_emp_exp": st.number_input("Experience (Years)", 0, 40, 5),
        "loan_amnt": st.number_input("Loan Amount", 500, 50000, 10000),
        "loan_int_rate": st.slider("Interest Rate", 5.0, 20.0, 10.5),
        "loan_percent_income": st.slider("Loan % of Income", 0.0, 1.0, 0.2),
        "cb_person_cred_hist_length": st.slider("Credit History (Years)", 1, 10, 3),
        "credit_score": st.slider("Credit Score", 300, 850, 650),
        "previous_loan_defaults_on_file": st.radio("Previous Defaults", ['Yes', 'No']) == 'Yes'
    }

    if st.button("Predict"):
        try:
            response = requests.post(f"{base_url}/predict", json=form_data)
            result = response.json()

            if response.status_code != 200 or "prediction" not in result:
                raise ValueError("Prediction failed or malformed response.")

            st.subheader("🔍 Prediction Result")
            st.success(f"Loan Status: {result['prediction']}")

            st.markdown("**Probability:**")
            st.write(f"- Approved: {result['probability'][1]*100:.2f}%")
            st.write(f"- Rejected: {result['probability'][0]*100:.2f}%")

            st.markdown("### 💡 Key Feature Impacts:")
            for feature, value in result["explanation"].items():
                impact = value[1] if isinstance(value, list) else value
                st.markdown(f"- **{feature.replace('_', ' ').title()}**: {impact:+.3f}")

            # Bias warning
            bias_result = detect_bias({k: v[1] if isinstance(v, list) else v for k, v in result["explanation"].items()})
            if bias_result["biased"]:
                st.warning(f"⚠️ Bias Alert: Model relied heavily on **{bias_result['top_feature']}** (impact: {bias_result['impact']:.2f})")

        except Exception as e:
            st.error(f"Prediction failed. Reason: {e}")

# ------------------ 📝 Feedback Page ------------------ #
elif menu == "📝 Feedback":
    st.title("Model Decision Feedback")

    with st.form("feedback_form"):
        input_data = {
            "person_age": st.slider("Age", 18, 100, 30),
            "person_income": st.number_input("Income", 10000, 1000000, 50000),
            "person_emp_exp": st.number_input("Experience (Years)", 0, 40, 5),
            "loan_amnt": st.number_input("Loan Amount", 500, 50000, 10000),
            "loan_int_rate": st.slider("Interest Rate", 5.0, 20.0, 10.5),
            "loan_percent_income": st.slider("Loan % of Income", 0.0, 1.0, 0.2),
            "cb_person_cred_hist_length": st.slider("Credit History (Years)", 1, 10, 3),
            "credit_score": st.slider("Credit Score", 300, 850, 650),
            "previous_loan_defaults_on_file": st.radio("Previous Defaults", ['Yes', 'No']) == 'Yes'
        }

        model_response = requests.post(f"{base_url}/predict", json=input_data)

        try:
            model_data = model_response.json()
            st.subheader("Model Prediction")
            st.json(model_data)

            user_decision = st.selectbox("Do you agree with the model's decision?", ["Agree", "Disagree"])
            reason = st.text_area("If you disagree, explain why (required):", max_chars=200)

            submitted = st.form_submit_button("Submit Feedback")
            if submitted:
                feedback_payload = {
                    "input_data": input_data,
                    "model_decision": model_data["prediction"],
                    "user_decision": model_data["prediction"] if user_decision == "Agree" else (
                        "Approved" if model_data["prediction"] == "Rejected" else "Rejected"),
                    "reason": reason
                }

                res = requests.post(f"{base_url}/feedback", json=feedback_payload)
                if res.status_code == 200:
                    st.success("Feedback submitted successfully!")
                else:
                    st.error("Failed to submit feedback.")
        except Exception:
            st.error("Failed to fetch model prediction.")

# ------------------ 📊 Dashboard Page ------------------ #
elif menu == "📊 Dashboard":
    st.title("Feedback Dashboard")

    try:
        res = requests.get(f"{base_url}/dashboard")
        if res.status_code == 200:
            data = res.json()
            st.metric("Total Feedbacks", data.get("total_feedbacks", 0))
            st.metric("Overrides", data.get("overrides", 0))
            st.metric("Override Rate", f"{data.get('override_rate', 0) * 100:.2f}%")
        else:
            st.error("Failed to fetch dashboard data.")
    except Exception as e:
        st.error(f"Dashboard load failed: {e}")
