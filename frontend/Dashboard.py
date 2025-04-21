import streamlit as st
import requests

st.title("📊 Feedback Dashboard")

st.markdown("Visualize how often AI decisions are overridden")

res = requests.get("http://localhost:8000/dashboard/")
data = res.json()

st.metric("Total Feedbacks", data["total_feedbacks"])
st.metric("Overrides", data["overrides"])
st.metric("Override Rate", f"{data['override_rate']*100:.2f}%")