"""
==============================================================================
MODULE: Live Weather Tool (weather_tool.py)
DESCRIPTION:
    Interfaces with the free Open-Meteo Weather API (https://open-meteo.com)
    to retrieve real-time weather metrics (temperature, wind speed, weather 
    conditions) for any given latitude and longitude coordinates.
    
AUTHOR: Autonomous AI Travel Agent Project
==============================================================================
"""

import requests

def get_current_weather(latitude: float, longitude: float) -> dict:
    """
    Fetches current weather metrics for a specific latitude and longitude coordinate.
    
    Args:
        latitude (float): The geographic latitude (e.g., 40.4168 for Madrid).
        longitude (float): The geographic longitude (e.g., -3.7038 for Madrid).
        
    Returns:
        dict: Dictionary containing temperature, wind speed, condition text, and coordinates.
    """
    # Open-Meteo endpoint URL
    url = "https://api.open-meteo.com/v1/forecast"
    
    # Query parameters required by the Open-Meteo API
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true"  # Flag asking for real-time weather values
    }
    
    try:
        # Send an HTTP GET request with parameters and a 10-second timeout
        response = requests.get(url, params=params, timeout=10)
        
        # Verify the request succeeded (HTTP status 200 OK)
        if response.status_code != 200:
            return {"error": f"Could not retrieve weather for coordinates ({latitude}, {longitude})."}
            
        # Extract the 'current_weather' object from the API response payload
        data = response.json().get("current_weather", {})
        
        # Extract WMO (World Meteorological Organization) weather code
        wmo_code = data.get("weathercode", 0)
        
        # Map raw numeric weather codes to simple human-readable conditions
        if wmo_code == 0:
            condition = "Clear sky"
        elif wmo_code in [1, 2, 3]:
            condition = "Partly cloudy / Overcast"
        else:
            condition = "Rain, Snow, or Thunderstorm"
            
        # Return structured weather data for the agent
        return {
            "temperature_celsius": data.get("temperature"),
            "windspeed_kmh": data.get("windspeed"),
            "weather_condition": condition,
            "latitude": latitude,
            "longitude": longitude
        }
        
    except requests.exceptions.RequestException as e:
        # Catch network or timeout errors without crashing the main application
        return {"error": f"Failed to reach Open-Meteo Weather API: {str(e)}"}