import streamlit as st
import requests
import os

API = os.getenv("API", "http://localhost:8000")

st.title("Pricing Service")

S0 = st.number_input("S₀", 0.0, 100000.0, 100.0)
K = st.number_input("K", 0.0, 100000.0, 100.0)
r = st.number_input("r (interest rate)", -1.0, 1.0, 0.01)
T = st.number_input("T (years)", 0.0, 50.0, 1.0)
sigma = st.number_input("σ (volatility)", 0.0, 5.0, 0.2)

# Add option type selector
option_type = st.selectbox("Option Type", ["call", "put"])

if st.button("Price Forward"):
    res = requests.post(f"{API}/price/forward", json={
        "S0": S0, "K": K, "r": r, "T": T
    })
    st.json(res.json())

if st.button("Price Option"):
    res = requests.post(f"{API}/price/european-option", json={
        "S0": S0, "K": K, "r": r, "sigma": sigma, "T": T, "type": option_type
    })
    st.json(res.json())
