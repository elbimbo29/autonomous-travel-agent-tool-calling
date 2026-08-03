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

## 🏗️ System Architecture

```text
                                  +-----------------------+
                                  |   Streamlit Web UI    |
                                  |      (app.py)         |
                                  +-----------+-----------+
                                              |
                                              | 1. User Prompt
                                              v
                                  +-----------------------+
                                  |    OpenAI API Client  |
                                  |     (gpt-4o-mini)     |
                                  +-----------+-----------+
                                              |
                        +---------------------+---------------------+
                        | 2. Evaluates Tool Schemas & Emits Calls  |
                        v                                           v
            +-----------------------+                   +-----------------------+
            | get_country_info()    |                   | get_current_weather() |
            +-----------+-----------+                   +-----------+-----------+
                        |                                           |
                        v                                           v
            +-----------------------+                   +-----------------------+
            |  REST Countries API   |                   |    Open-Meteo API     |
            +-----------------------+                   +-----------------------+
                                              |
                                              | 3. Tool Results Returned
                                              v
                                  +-----------------------+
                                  | OpenAI Model Synthesis|
                                  +-----------+-----------+
                                              |
                                              | 4. Final Formatted Answer
                                              v
                                  +-----------------------+
                                  |     User Interface    |
                                  +-----------------------+