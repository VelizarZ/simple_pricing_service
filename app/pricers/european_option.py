# pricers/european_option.py
from __future__ import annotations
import math
from typing import Dict


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
        Volatility (annual, > 0). If sigma == 0, the function uses the T->0 limit.
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
    if option_type not in ("call", "put"):
        raise ValueError("option_type must be 'call' or 'put'")

    # Trivial / boundary cases
    if T == 0:
        # Option at maturity: payoff
        if option_type == "call":
            price = max(S0 - K, 0.0)
            delta = 1.0 if S0 > K else 0.0 if S0 < K else 0.5
        else:  # put
            price = max(K - S0, 0.0)
            delta = -1.0 if S0 < K else 0.0 if S0 > K else -0.5
        vega = 0.0
        return {"price": price, "delta": delta, "vega": vega}

    if sigma <= 0:
        # Zero volatility -> deterministic outcome discounted
        forward = S0 - K * math.exp(-r * T)
        if option_type == "call":
            price = max(forward, 0.0)
            # delta is either 1 (if forward > 0) or 0
            delta = 1.0 if forward > 0 else 0.0
        else:
            price = max(-forward, 0.0)
            delta = -1.0 if forward < 0 else 0.0
        vega = 0.0
        return {"price": price, "delta": delta, "vega": vega}

    # Black-Scholes core
    sqrtT = math.sqrt(T)
    sigma_sqrtT = sigma * sqrtT
    # careful step-by-step with logs and division
    lnS_K = math.log(S0 / K) if S0 > 0 and K > 0 else float("-inf")
    d1 = (lnS_K + (r + 0.5 * sigma * sigma) * T) / sigma_sqrtT
    d2 = d1 - sigma_sqrtT

    Nd1 = _std_normal_cdf(d1)
    Nd2 = _std_normal_cdf(d2)
    nd1 = _std_normal_pdf(d1)

    discK = K * math.exp(-r * T)

    if option_type == "call":
        price = S0 * Nd1 - discK * Nd2
        delta = Nd1
    else:  # put
        # Put-call parity: P = C - S + K e^{-rT}
        call_price = S0 * Nd1 - discK * Nd2
        price = call_price - S0 + discK
        delta = Nd1 - 1.0

    # Vega (same for call/put in Black-Scholes)
    vega = S0 * sqrtT * nd1

    return {"price": price, "delta": delta, "vega": vega}


# Quick demo if run directly
if __name__ == "__main__":
    demo_call = price_european_option(S0=100, K=95, r=0.01, sigma=0.2, T=0.5, option_type="call")
    demo_put = price_european_option(S0=100, K=105, r=0.01, sigma=0.25, T=1.0, option_type="put")
    print("Call demo:", demo_call)
    print("Put demo :", demo_put)
