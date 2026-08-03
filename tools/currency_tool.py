"""
==============================================================================
MODULE: Real-Time Currency Conversion Tool (currency_tool.py)
DESCRIPTION:
    Interfaces with the Open Exchange Rate API (https://open.er-api.com)
    to perform live currency conversion calculations between international 
    ISO currency codes (e.g., converting USD to EUR or JPY).
    
AUTHOR: Autonomous AI Travel Agent Project
==============================================================================
"""

import requests

def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """
    Converts a financial amount from one currency to another using real-time rates.
    
    Args:
        amount (float): The monetary value to convert (e.g., 100.0).
        from_currency (str): 3-letter ISO source currency code (e.g., "USD").
        to_currency (str): 3-letter ISO target currency code (e.g., "EUR").
        
    Returns:
        dict: Dictionary containing conversion inputs, rate, and calculated final amount.
    """
    # Normalize currency code inputs to uppercase strings without leading/trailing spaces
    base_curr = from_currency.upper().strip()
    target_curr = to_currency.upper().strip()
    
    # Construct endpoint using the base currency
    url = f"https://open.er-api.com/v6/latest/{base_curr}"
    
    try:
        # Execute HTTP GET request with a 10-second timeout
        response = requests.get(url, timeout=10)
        
        # Check for HTTP errors
        if response.status_code != 200:
            return {"error": f"Could not retrieve exchange rates for base currency '{base_curr}'."}
            
        # Extract the dictionary of exchange rates relative to the base currency
        rates = response.json().get("rates", {})
        
        # Verify that the target currency exists in the retrieved rates dictionary
        if target_curr not in rates:
            return {"error": f"Target currency '{target_curr}' is invalid or unsupported."}
            
        # Get conversion multiplier rate
        rate = rates[target_curr]
        
        # Calculate final converted amount rounded to 2 decimal places
        converted_amount = round(amount * rate, 2)
        
        # Return structured conversion payload back to the LLM agent
        return {
            "original_amount": amount,
            "from_currency": base_curr,
            "to_currency": target_curr,
            "exchange_rate": rate,
            "converted_amount": converted_amount
        }
        
    except requests.exceptions.RequestException as e:
        # Handle connection failures or API downtime gracefully
        return {"error": f"Failed to reach Exchange Rate API: {str(e)}"}