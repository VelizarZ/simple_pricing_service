import streamlit as st
import requests
import os

API = os.getenv("API", "http://localhost:8000")

st.title("Simple Pricing Service")

# Financial parameters 
S0 = st.number_input(
    "S₀ (Spot Price)", 
    0.0, 100000.0, 100.0,
    help="Current market price of the underlying asset"
)
K = st.number_input(
    "K (Strike/Forward Price)", 
    0.0, 100000.0, 100.0,
    help="For forwards: delivery price. For options: strike price"
)
r = st.number_input(
    "r (Risk-Free Interest Rate)", 
    -1.0, 1.0, 0.01,
    help="Continuously compounded annual rate (0.01 = 1%)"
)
T = st.number_input(
    "T (Time to Maturity in Years)", 
    0.0, 50.0, 1.0,
    help="Time until expiration (0.5 = 6 months, 1.0 = 1 year)"
)
sigma = st.number_input(
    "σ (Volatility)", 
    0.0, 5.0, 0.2,
    help="Annual volatility as decimal (0.2 = 20%). Used only for options."
)

# European option type 
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
