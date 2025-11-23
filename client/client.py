#!/usr/bin/env python3
"""
Client script to demonstrate calling the Pricing Service API endpoints.

This script demonstrates:
- Pricing a stock forward contract
- Pricing a European stock option (both call and put)
- Handling responses and errors
"""

import requests
import json
import sys
from typing import Dict, Any


API_BASE_URL = "http://localhost:8000"


def print_response(response: requests.Response, endpoint: str):
    """Pretty print the API response."""
    print(f"\n{'='*60}")
    print(f"Endpoint: {endpoint}")
    print(f"Status Code: {response.status_code}")
    print(f"{'='*60}")
    
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.status_code}")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=2))
        except:
            print(response.text)
    print()


def price_forward(S0: float, K: float, r: float, T: float):
    """Price a stock forward contract."""
    url = f"{API_BASE_URL}/price/forward"
    payload = {
        "S0": S0,
        "K": K,
        "r": r,
        "T": T
    }
    
    print(f"Pricing Forward Contract:")
    print(f"  Spot Price (S0): {S0}")
    print(f"  Strike Price (K): {K}")
    print(f"  Risk-free Rate (r): {r}")
    print(f"  Time to Maturity (T): {T} years")
    
    try:
        response = requests.post(url, json=payload)
        print_response(response, "/price/forward")
        return response
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error: Could not connect to API at {API_BASE_URL}")
        print("   Make sure the API service is running!")
        return None
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return None


def price_european_option(S0: float, K: float, r: float, sigma: float, T: float, option_type: str):
    """Price a European stock option."""
    url = f"{API_BASE_URL}/price/european-option"
    payload = {
        "S0": S0,
        "K": K,
        "r": r,
        "sigma": sigma,
        "T": T,
        "type": option_type  # "call" or "put"
    }
    
    print(f"Pricing European {option_type.upper()} Option:")
    print(f"  Spot Price (S0): {S0}")
    print(f"  Strike Price (K): {K}")
    print(f"  Risk-free Rate (r): {r}")
    print(f"  Volatility (σ): {sigma}")
    print(f"  Time to Maturity (T): {T} years")
    
    try:
        response = requests.post(url, json=payload)
        print_response(response, f"/price/european-option (type={option_type})")
        return response
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error: Could not connect to API at {API_BASE_URL}")
        print("   Make sure the API service is running!")
        return None
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return None


def main():
    """Run sample API calls."""
    print("="*60)
    print("Pricing Service API Client Demo")
    print("="*60)
    
    # Check if API is reachable
    try:
        health_check = requests.get(f"{API_BASE_URL}/docs")
        if health_check.status_code == 200:
            print(f"✅ API is reachable at {API_BASE_URL}")
        else:
            print(f"⚠️  API returned status {health_check.status_code}")
    except:
        print(f"⚠️  Could not verify API connectivity at {API_BASE_URL}")
        print("   Continuing anyway...\n")
    
    # Sample 1: Forward Contract
    print("\n" + "="*60)
    print("SAMPLE 1: Stock Forward Contract")
    print("="*60)
    price_forward(S0=100.0, K=95.0, r=0.02, T=0.5)
    
    # Sample 2: European Call Option
    print("\n" + "="*60)
    print("SAMPLE 2: European Call Option")
    print("="*60)
    price_european_option(S0=100.0, K=95.0, r=0.01, sigma=0.2, T=0.5, option_type="call")
    
    # Sample 3: European Put Option
    print("\n" + "="*60)
    print("SAMPLE 3: European Put Option")
    print("="*60)
    price_european_option(S0=100.0, K=105.0, r=0.01, sigma=0.25, T=1.0, option_type="put")
    
    # Sample 4: Test caching (call same endpoint twice)
    print("\n" + "="*60)
    print("SAMPLE 4: Testing Cache (Call Forward Twice)")
    print("="*60)
    print("First call (will calculate):")
    price_forward(S0=100.0, K=95.0, r=0.02, T=0.5)
    print("\nSecond call (should be cached):")
    price_forward(S0=100.0, K=95.0, r=0.02, T=0.5)
    
    # Sample 5: Error case - invalid input
    print("\n" + "="*60)
    print("SAMPLE 5: Error Handling (Negative Spot Price)")
    print("="*60)
    price_forward(S0=-10.0, K=95.0, r=0.02, T=0.5)
    
    print("\n" + "="*60)
    print("Demo Complete!")
    print("="*60)


if __name__ == "__main__":
    main()

