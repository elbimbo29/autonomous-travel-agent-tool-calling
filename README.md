# 🌍 Autonomous AI Travel & Country Fact Agent
> **Multi-Tool Function Calling & REST API Orchestration in Python**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![SDK](https://img.shields.io/badge/SDK-Google%20GenAI-4285F4.svg)](https://pypi.org/project/google-genai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📌 Overview

An interactive, single-agent system built with **Python**, **Google GenAI SDK (Gemini)**, and **Streamlit**. 

Unlike standard text-prompt wrappers, this application demonstrates how Large Language Models perform **dynamic tool selection**, **parameter extraction**, and **REST API orchestration**. The agent dynamically evaluates natural language queries and determines when and how to call external web services (country metadata, live weather forecasts, and real-time currency exchange rates) to answer complex travel prompts.

---

## 💡 Core Concepts Demonstrated

### 1. LLM Function Calling & Tool Declaration
* **JSON Schema Mapping:** Custom Python function definitions automatically mapped to JSON schemas, allowing the LLM to inspect parameter types, required fields, and tool descriptions.
* **Autonomous Intent Recognition:** The LLM independently determines whether a prompt requires static reasoning or real-time external tool execution without hardcoded `if/else` logic.

### 2. Live REST API Orchestration
* **Multi-Tool Integration:** Integrated 3 independent, live REST APIs:
  * 🌐 **REST Countries API:** Fetches capitals, populations, regions, and currencies.
  * ☀️ **Open-Meteo API:** Retrieves real-time weather metrics using latitude and longitude.
  * 💱 **ExchangeRate API:** Performs live currency conversion calculations.
* **Payload Sanitization & Response Hydration:** Prunes raw API JSON payloads in Python before returning results to the LLM context window, optimizing token usage and reducing latency.

### 3. Multi-Step Execution & Tool Chaining
* Demonstrates **tool chaining**, where output parameters from one tool (e.g., retrieving coordinates from a country query) are dynamically fed as input parameters into another tool (e.g., querying local weather).

### 4. Agent Observability & UI Tracing
* **Real-Time Tool Logs:** A custom Streamlit interface featuring expandable execution logs that expose intermediate function names, generated arguments, execution timing, and raw API responses for full developer visibility.

---

## 🏗️ System Architecture