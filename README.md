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
    
    subgraph Local Tools
        CountryTool[🌐 country_tool.py]:::tool
        WeatherTool[☀️ weather_tool.py]:::tool
        CurrencyTool[💱 currency_tool.py]:::tool
    end

    subgraph External REST APIs
        RESTCountries[REST Countries API]:::api
        OpenMeteo[Open-Meteo Weather API]:::api
        Frankfurter[Frankfurter Exchange API]:::api
    end

    %% Flow Execution
    UI -->|1. User Prompt| LLM
    LLM -->|2. Inspects Schema & Emits Tool Call Intent| Router
    
    Router -->|Call get_country_info| CountryTool
    Router -->|Call get_current_weather| WeatherTool
    Router -->|Call convert_currency| CurrencyTool

    CountryTool <-->|Fetch Metadata & Coordinates| RESTCountries
    WeatherTool <-->|Fetch Live Weather via Lat/Long| OpenMeteo
    CurrencyTool <-->|Fetch Live FX Rates| Frankfurter

    CountryTool -->|Sanitized JSON| LLM
    WeatherTool -->|Sanitized JSON| LLM
    CurrencyTool -->|Sanitized JSON| LLM

    LLM -->|3. Synthesized Natural Language Response| UI



## 💡 Core Concepts Demonstrated

### 1. OpenAI Function / Tool Calling
* **JSON Schema Mapping:** Custom Python function definitions automatically mapped to JSON schemas, allowing the LLM to inspect parameter types, required fields, and descriptions.
* **Autonomous Intent Recognition:** The LLM independently determines whether a prompt requires static reasoning or real-time external tool execution without hardcoded `if/else` logic.
* **Safe Argument Parsing:** Inspects and validates parameter signatures dynamically prior to local execution to prevent runtime parameter mismatches.

### 2. Live REST API Orchestration
* **Multi-Tool Integration:** Integrates 3 independent, live REST APIs:
  * 🌐 **REST Countries API:** Fetches capitals, populations, regions, currencies, and geographic coordinates.
  * ☀️ **Open-Meteo API:** Retrieves live weather metrics using latitude and longitude coordinates without requiring API keys.
  * 💱 **Frankfurter Exchange API:** Performs real-time currency conversions across global currency codes.
* **Payload Sanitization:** Prunes and formats raw API JSON payloads in Python before returning results to the LLM context window, optimizing token usage and lowering latency.

### 3. Multi-Step Execution & Tool Chaining
* Demonstrates **tool chaining**, where output parameters from one tool (e.g., retrieving latitude and longitude coordinates from a country query) are dynamically passed as input arguments into another tool (e.g., querying local weather metrics).

### 4. Agent Observability & UI Tracing
* **Real-Time Tool Logs:** A custom Streamlit interface featuring expandable execution logs that expose intermediate function names, arguments passed, execution timing, and raw API responses for full visibility.

---

## 📂 Project Structure


## 🏗️ System Architecture


## 🚀 Quick Start Guide

Follow these steps to set up and run the Autonomous AI Travel Agent locally on your machine.

### 1. Prerequisites
Ensure you have the following installed and configured before starting:
* **Python 3.10+** — [Download Python](https://www.python.org/downloads/)
* **Git** — [Download Git](https://git-scm.com/downloads)
* **OpenAI API Key** — Obtain an API key from your [OpenAI Platform Account](https://platform.openai.com/api-keys)

---

### 2. Clone the Repository
Clone the repository to your local machine and navigate into the project directory:

```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/autonomous-travel-agent-tool-calling.git](https://github.com/YOUR_GITHUB_USERNAME/autonomous-travel-agent-tool-calling.git)
cd autonomous-travel-agent-tool-calling