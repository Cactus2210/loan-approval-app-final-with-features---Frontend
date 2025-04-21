import streamlit as st
import requests
from utils import call_api

st.title("📝 Provide Your Feedback")

st.markdown("### Revisit the AI's decision and submit your input")

input_data = st.session_state.get("latest_input", None)
result = st.session_state.get("latest_result", None)

if not input_data or not result:
    st.warning("No prediction session found. Please make a prediction first.")
    st.stop()

model_decision = result["prediction"]
st.markdown(f"**AI Decision:** `{model_decision}`")
st.markdown("#### Do you agree with the AI's decision?")

user_decision = st.radio("Your Decision", ["Approved", "Rejected"])
reason = st.text_area("Why do you agree/disagree with the decision?")

if st.button("Submit Feedback"):
    feedback_payload = {
        "input_data": input_data,
        "model_decision": model_decision,
        "user_decision": user_decision,
        "reason": reason
    }
    res = requests.post("http://localhost:8000/feedback/", json=feedback_payload)
    st.success("✅ Feedback submitted successfully!")