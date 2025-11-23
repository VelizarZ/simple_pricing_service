# pricers/forward.py
from __future__ import annotations
import math
from typing import Dict


def price_forward(S0: float, K: float, r: float, T: float) -> Dict[str, float]:
    """
    Price a (long) forward contract on a non-dividend-paying stock.

    Formula (no dividends):
      V0 = S0 - K * exp(-r * T)

    Greeks (simple):
      delta = 1
      vega  = 0

    Parameters
    ----------
    S0 : float
        Spot price (must be >= 0)
    K : float
        Strike/forward price (must be >= 0)
    r : float
        Continuously compounded risk-free rate (e.g., 0.01 for 1%)
    T : float
        Time to maturity in years (must be >= 0)

    Returns
    -------
    dict
        {"price": float, "delta": float, "vega": float}
    """
    # Validate
    if S0 < 0:
        raise ValueError("S0 must be non-negative")
    if K < 0:
        raise ValueError("K must be non-negative")
    if T < 0:
        raise ValueError("T must be non-negative")

    price = S0 - K * math.exp(-r * T)
    # For a forward on a non-dividend-paying stock, instantaneous delta is 1
    delta = 1.0
    vega = 0.0

    return {"price": price, "delta": delta, "vega": vega}


# Quick demo when module run directly
if __name__ == "__main__":
    demo = price_forward(S0=100.0, K=95.0, r=0.02, T=0.5)
    print("Forward demo:", demo)
