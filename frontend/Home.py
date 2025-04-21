import streamlit as st
import requests
from utils import call_api

st.title("🤖 AI-Powered Loan Approval System")

st.markdown("Fill the form below to get AI prediction for loan approval:")

form_data = {
    "person_age": st.slider("Age", 18, 100, 30),
    "person_income": st.number_input("Income (₹)", 10000, 1000000, 50000),
    "person_emp_exp": st.number_input("Experience (Years)", 0, 40, 5),
    "loan_amnt": st.number_input("Loan Amount (₹)", 500, 50000, 10000),
    "loan_int_rate": st.slider("Interest Rate (%)", 5.0, 20.0, 10.5),
    "loan_percent_income": st.slider("Loan % of Income", 0.0, 1.0, 0.2),
    "cb_person_cred_hist_length": st.slider("Credit History (Years)", 1, 10, 3),
    "credit_score": st.slider("Credit Score", 300, 850, 650),
    "previous_loan_defaults_on_file": st.radio("Previous Defaults", ['Yes', 'No']) == "Yes"
}

if st.button("🔍 Predict"):
    result = call_api("/predict", form_data)

    if "error" in result:
        st.error(f"API Error: {result['error']}")
    else:
        st.session_state.latest_input = form_data
        st.session_state.latest_result = result

        st.subheader("📌 Prediction Result")
        st.success(f"Loan Status: **{result['prediction']}**")

        st.markdown(f"**Probability:**")
        st.write(f"- Approved: **{result['probability'][1]*100:.2f}%**")
        st.write(f"- Rejected: **{result['probability'][0]*100:.2f}%**")

        st.markdown("### 💡 Key Feature Impacts:")
        explanation = result.get("explanation", {})
        sorted_exp = sorted(explanation.items(), key=lambda x: abs(x[1][0]), reverse=True)

        for feature, impact in sorted_exp:
            st.write(f"- **{feature.replace('_', ' ').title()}**: {impact[0]:+.3f}")

        # Bias detection (inline simple logic)
        if explanation:
            max_feature = max(explanation, key=lambda k: abs(explanation[k][0]))
            max_impact = explanation[max_feature][0]
            if abs(max_impact) > 0.1:
                st.warning(f"⚠️ Bias Alert: Model relied heavily on **{max_feature}** (impact: {max_impact:.2f})")
