"""
==============================================================================
PACKAGE: Tools Package Initializer (__init__.py)
DESCRIPTION:
    Exposes all individual tool functions from country_tool, weather_tool, 
    and currency_tool as a unified Python package interface. Allows app.py 
    to import tools cleanly using:
    
    `from tools import get_country_info, get_current_weather, convert_currency`
    
AUTHOR: Autonomous AI Travel Agent Project
==============================================================================
"""

# Import functions from sibling tool modules within the tools package
from .country_tool import get_country_info
from .weather_tool import get_current_weather
from .currency_tool import convert_currency

# Define explicit list of exported functions when using wildcards (import *)
__all__ = [
    "get_country_info",
    "get_current_weather",
    "convert_currency"
]