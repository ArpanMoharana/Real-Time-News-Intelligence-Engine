# ui/app.py
import streamlit as st
import requests

st.set_page_config(page_title="Fake News Detector", layout="wide")
st.title("Fake News Detector — Starter UI")

st.write("Paste an article or a claim below and press Analyze.")

text = st.text_area("Article / Claim text", height=250)

if st.button("Analyze"):
    if not text.strip():
        st.error("Please paste some text to analyze.")
    else:
        # Call the local FastAPI backend
        try:
            resp = requests.post("http://127.0.0.1:8000/analyze", json={"title": "", "text": text})
            resp.raise_for_status()
            data = resp.json()

            st.subheader("Classification")
            st.json(data["classification"])

            st.subheader("Verification (placeholder)")
            st.json(data["verification"])
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to call backend: {e}")
