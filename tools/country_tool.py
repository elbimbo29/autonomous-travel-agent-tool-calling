"""
==============================================================================
MODULE: Country Information Tool (country_tool.py)
DESCRIPTION:
    Interfaces with the public REST Countries API (https://restcountries.com)
    to retrieve metadata for a requested country (e.g., capital city, total
    population, official languages, accepted currencies, and geographic 
    latitude/longitude coordinates).
    
AUTHOR: Autonomous AI Travel Agent Project
==============================================================================
"""

import requests

def get_country_info(country_name: str) -> dict:
    """
    Fetches key geographic, demographic, and financial details about a country.
    
    Args:
        country_name (str): The common English name of the country (e.g., "Japan", "Spain").
        
    Returns:
        dict: Sanitized dictionary containing country metadata or an error message.
    """
    # Construct the API endpoint URL with fullText search to get precise matches
    url = f"https://restcountries.com/v3.1/name/{country_name}?fullText=true"
    
    try:
        # Send an HTTP GET request with a 10-second safety timeout
        response = requests.get(url, timeout=10)
        
        # Check if the HTTP status code indicates a failure (e.g., 404 Not Found)
        if response.status_code != 200:
            return {"error": f"Country '{country_name}' not found. Please check spelling."}
            
        # Parse the JSON response body (REST Countries returns a list of matching country objects)
        data = response.json()[0]
        
        # Safely extract latitude and longitude coordinates for weather tool chaining
        # Fallbacks check capital coordinates first, then general country coordinates
        latlng = data.get("capitalInfo", {}).get("latlng") or data.get("latlng", [0.0, 0.0])
        
        # Extract currency codes (e.g., ['USD', 'EUR']) from the currencies dictionary keys
        currencies = list(data.get("currencies", {}).keys())
        
        # Extract language names (e.g., ['Spanish', 'English']) from the languages dictionary values
        languages = list(data.get("languages", {}).values())
        
        # Return a clean, structured dictionary back to the LLM agent
        return {
            "country_name": data.get("name", {}).get("common"),
            "capital": data.get("capital", ["N/A"])[0],
            "population": data.get("population"),
            "region": data.get("region"),
            "currencies": currencies,
            "languages": languages,
            "latitude": latlng[0],
            "longitude": latlng[1]
        }
        
    except requests.exceptions.RequestException as e:
        # Catch network failures, connection timeouts, or DNS resolution issues gracefully
        return {"error": f"Failed to reach REST Countries API: {str(e)}"}