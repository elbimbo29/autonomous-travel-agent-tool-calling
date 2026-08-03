# 🌍 Autonomous AI Travel & Country Fact Agent
> **Multi-Tool Function Calling & REST API Orchestration in Python using OpenAI API**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![SDK](https://img.shields.io/badge/SDK-OpenAI-000000.svg)](https://pypi.org/project/openai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Overview

An interactive, single-agent application built with **Python**, **OpenAI API (`gpt-4o-mini`)**, and **Streamlit**. 

Unlike static text-prompt wrappers, this application demonstrates how Large Language Models perform **dynamic tool selection**, **parameter extraction**, and **REST API orchestration**. The agent dynamically evaluates natural language queries and determines when and how to call external web services (country metadata, live weather forecasts via coordinates, and real-time currency exchange rates) to answer complex travel queries.

---
## 📂 Project Structure

* 📁 **`autonomous-travel-agent-tool-calling/`**
  * 📄 **`app.py`** — Main Streamlit interface & OpenAI agent execution loop
  * 📄 **`tools.py`** — Central module re-exporting local tool functions
  * 📄 **`country_tool.py`** — REST Countries API handler & coordinate extractor
  * 📄 **`weather_tool.py`** — Open-Meteo API handler for live weather data
  * 📄 **`currency_tool.py`** — Frankfurter Exchange Rate API integration module
  * 📄 **`.env.example`** — Environment variable template (`OPENAI_API_KEY`)
  * 📄 **`.gitignore`** — Excludes virtual environments and sensitive keys
  * 📄 **`requirements.txt`** — Python package dependencies
  * 📄 **`README.md`** — Comprehensive project documentation
---

### 🧩 Component Breakdown

* **User Interface (`app.py`):** Built with Streamlit, manages persistent session state for chat history and real-time execution logs.
* **OpenAI Agent Core:** Processes user intent against JSON schemas defined in `tools_schema`, deciding whether to reply directly or issue tool function calls.
* **Execution Safety Layer:** Uses Python's `inspect` module to match arguments strictly against local function signatures before calling `country_tool.py`, `weather_tool.py`, or `currency_tool.py`.
* **External REST Services:**
  * **REST Countries API:** Geographical metadata & coordinates.
  * **Open-Meteo API:** Live weather via latitude/longitude without API key friction.
  * **Frankfurter API:** Real-time currency conversions.
* **Observability & Tracing:** Displays expandable JSON UI traces showing function names, arguments, execution timing, and returned payloads.
---

## 🏗️ System Architecture

```mermaid
flowchart TD
    %% Styling
    classDef ui fill:#4F46E5,stroke:#312E81,color:#ffffff,stroke-width:2px;
    classDef agent fill:#059669,stroke:#065F46,color:#ffffff,stroke-width:2px;
    classDef router fill:#D97706,stroke:#92400E,color:#ffffff,stroke-width:2px;
    classDef tool fill:#2563EB,stroke:#1E40AF,color:#ffffff,stroke-width:2px;
    classDef api fill:#0891B2,stroke:#155E75,color:#ffffff,stroke-width:2px;

    %% Nodes
    UI[🖥️ Streamlit Web Interface<br>app.py]:::ui
    LLM[🧠 OpenAI API Client<br>gpt-4o-mini]:::agent
    Router[⚙️ Dynamic Tool Router<br>inspect.signature]:::router
    
    subgraph Local_Tools [Local Tools]
        CountryTool[🌐 country_tool.py]:::tool
        WeatherTool[☀️ weather_tool.py]:::tool
        CurrencyTool[💱 currency_tool.py]:::tool
    end

    subgraph External_APIs [External REST APIs]
        RESTCountries[REST Countries API]:::api
        OpenMeteo[Open-Meteo Weather API]:::api
        Frankfurter[Frankfurter Exchange API]:::api
    end

    %% Flow Execution
    UI -->|1. User Prompt| LLM
    LLM -->|2. Inspects Schema & Emits Intent| Router
    
    Router -->|Call get_country_info| CountryTool
    Router -->|Call get_current_weather| WeatherTool
    Router -->|Call convert_currency| CurrencyTool

    CountryTool <-->|Fetch Metadata & Coordinates| RESTCountries
    WeatherTool <-->|Fetch Live Weather via Lat/Long| OpenMeteo
    CurrencyTool <-->|Fetch Live FX Rates| Frankfurter

    CountryTool -->|Sanitized JSON| LLM
    WeatherTool -->|Sanitized JSON| LLM
    CurrencyTool -->|Sanitized JSON| LLM

    LLM -->|3. Final Answer| UI

    