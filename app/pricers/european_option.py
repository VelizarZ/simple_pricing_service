# pricers/european_option.py
from __future__ import annotations
import math
from typing import Dict
import numpy as np

SQRT_2PI = math.sqrt(2 * math.pi)


def _std_normal_pdf(x: float) -> float:
    """Standard normal probability density function."""
    return math.exp(-0.5 * x * x) / SQRT_2PI


def _std_normal_cdf(x: float) -> float:
    """Standard normal cumulative distribution function using erf."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def price_european_option(
    S0: float,
    K: float,
    r: float,
    sigma: float,
    T: float,
    option_type: str = "call",
) -> Dict[str, float]:
    """
    Black–Scholes price and Greeks (delta, vega) for a European option on a non-dividend stock.

    Parameters
    ----------
    S0 : float
        Spot price (>= 0)
    K : float
        Strike price (>= 0)
    r : float
        Continuously compounded risk-free rate
    sigma : float
        Volatility (annual, > 0). 
    T : float
        Time to maturity in years (>= 0)
    option_type : str
        "call" or "put"

    Returns
    -------
    dict
        {"price": float, "delta": float, "vega": float}
    """
    # Input validation
    if S0 < 0:
        raise ValueError("S0 must be non-negative")
    if K < 0:
        raise ValueError("K must be non-negative")
    if T < 0:
        raise ValueError("T must be non-negative")
    if sigma <= 0:
        raise ValueError("Sigma must be bigger then 0")    
    if option_type not in ("call", "put"):
        raise ValueError("option_type must be 'call' or 'put'")


    # Black-Scholes 
    d1 = (np.log(S0 / K) + (r + ((sigma**2)/2)) * T) / (sigma * math.sqrt(T))
    d2 = d1 - (sigma * math.sqrt(T))

    Nd1 = _std_normal_cdf(d1)
    Nd2 = _std_normal_cdf(d2)
    phi_d1 = _std_normal_pdf(d1)

    discounted_strike = K * math.exp(-r * T)

    if option_type == "call":
        price = S0 * Nd1 - discounted_strike * Nd2
        delta = Nd1
    else:  # put
        # Put-call parity: P = C - S0 + K e^{-rT}
        call_price = S0 * Nd1 - discounted_strike * Nd2
        price = call_price - S0 + discounted_strike
        delta = Nd1 - 1.0

    # Vega 
    vega = S0 * (sigma * math.sqrt(T)) * phi_d1

    return {"price": price, "delta": delta, "vega": vega}


# Quick demo if run directly
if __name__ == "__main__":
    demo_call = price_european_option(S0=100, K=95, r=0.01, sigma=0.2, T=0.5, option_type="call")
    demo_put = price_european_option(S0=100, K=105, r=0.01, sigma=0.25, T=1.0, option_type="put")
    print("Call demo:", demo_call)
    print("Put demo :", demo_put)
