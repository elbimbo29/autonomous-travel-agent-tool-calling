"""
==============================================================================
APPLICATION: Autonomous AI Travel & Country Fact Agent (app.py)
DESCRIPTION:
    A Streamlit-based AI agent application built using Python and OpenAI SDK.
    Leverages OpenAI Tool / Function Calling to execute local Python functions
    and render synthesized responses in real-time.
==============================================================================
"""

import os
import json
import inspect
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# ------------------------------------------------------------------------------
# 1. TOOL IMPORTS
# ------------------------------------------------------------------------------
# Import custom local tools responsible for fetching country details,
# weather coordinates, and currency conversions.
from tools import get_country_info, get_current_weather, convert_currency

# Load environment variables from .env file (e.g., OPENAI_API_KEY)
load_dotenv()

# ------------------------------------------------------------------------------
# 2. STREAMLIT PAGE CONFIGURATION & UI HEADER
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Autonomous AI Travel Agent",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Autonomous AI Travel & Country Fact Agent")
st.caption("Powered by **OpenAI API**, **Streamlit**, & **Tool Calling**")

# ------------------------------------------------------------------------------
# 3. API KEY VALIDATION & CLIENT INITIALIZATION
# ------------------------------------------------------------------------------
openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()

# Stop execution gracefully if no API key is set in .env
if not openai_api_key:
    st.error("⚠️ `OPENAI_API_KEY` not found! Please set it in your `.env` file.")
    st.stop()

# Initialize the official OpenAI client
client = OpenAI(api_key=openai_api_key)

# ------------------------------------------------------------------------------
# 4. CHAT HISTORY & SESSION STATE MANAGEMENT
# ------------------------------------------------------------------------------
# Limit chat context history to prevent exceeding model context windows
MAX_MESSAGES = 10

# Initialize message state if running for the first time in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------------------------------------------------------
# 5. OPENAI TOOL SCHEMAS (FUNCTION DEFINITIONS)
# ------------------------------------------------------------------------------
# Define available tools using OpenAI JSON Schema syntax.
# The LLM inspects these descriptions and required parameters to construct calls.
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_country_info",
            "description": "Fetch detailed geographical, political, and demographic data for a given country.",
            "parameters": {
                "type": "object",
                "properties": {
                    "country_name": {
                        "type": "string",
                        "description": "The full name of the country (e.g. Japan, France, Philippines)"
                    }
                },
                "required": ["country_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Fetch live weather data using geographic latitude and longitude coordinates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "Latitude coordinate of the location (e.g. 35.6762 for Tokyo)"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "Longitude coordinate of the location (e.g. 139.6503 for Tokyo)"
                    }
                },
                "required": ["latitude", "longitude"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert monetary amounts using real-time foreign exchange rates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "The numerical amount to convert"
                    },
                    "from_currency": {
                        "type": "string",
                        "description": "3-letter currency code to convert from (e.g. USD)"
                    },
                    "to_currency": {
                        "type": "string",
                        "description": "3-letter currency code to convert to (e.g. JPY, EUR)"
                    }
                },
                "required": ["amount", "from_currency", "to_currency"]
            }
        }
    }
]

# Map tool names (strings from OpenAI responses) directly to Python callable functions
TOOL_MAP = {
    "get_country_info": get_country_info,
    "get_current_weather": get_current_weather,
    "convert_currency": convert_currency
}

# ------------------------------------------------------------------------------
# 6. RENDER EXISTING CHAT HISTORY IN STREAMLIT
# ------------------------------------------------------------------------------
for msg in st.session_state.messages:
    if msg["role"] in ["user", "assistant"] and msg.get("content"):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
            # Re-render tool execution logs stored in session state
            if "tool_logs" in msg and msg["tool_logs"]:
                for log in msg["tool_logs"]:
                    with st.expander(f"⚙️ Tool Executed: `{log['name']}`", expanded=False):
                        st.json({
                            "function_called": log["name"],
                            "arguments": log["args"],
                            "raw_response": log["response"]
                        })

# ------------------------------------------------------------------------------
# 7. USER INPUT & MAIN AGENT EXECUTION LOOP
# ------------------------------------------------------------------------------
if user_prompt := st.chat_input("Ask about any country, weather, or currency conversion..."):
    
    # Display the user's message immediately
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    # Append user prompt to history and trim if over history limit
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.session_state.messages = st.session_state.messages[-MAX_MESSAGES:]

    current_turn_tool_logs = []

    with st.chat_message("assistant"):
        with st.spinner("Agent reasoning & checking available tools..."):
            
            # Build payload of messages for OpenAI API, starting with System Prompt
            openai_messages = [
                {
                    "role": "system",
                    "content": "You are an expert Autonomous Travel & Country Fact Agent. Use the provided tools to answer queries accurately."
                }
            ]
            
            # Append prior user/assistant messages for context
            for m in st.session_state.messages:
                if m.get("content"):
                    openai_messages.append({"role": m["role"], "content": m["content"]})

            # Initial call to OpenAI Chat Completion API with tool schemas
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Fast, highly efficient function-calling model
                messages=openai_messages,
                tools=tools_schema,
                tool_choice="auto"
            )

            response_message = response.choices[0].message

            # ------------------------------------------------------------------
            # 8. RECURSIVE FUNCTION / TOOL CALLING LOOP
            # ------------------------------------------------------------------
            # If the model requests tool execution, process them sequentially
            while response_message.tool_calls:
                # Store the model's tool call request in the message payload
                openai_messages.append(response_message)

                # Loop through each tool call returned in this turn
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    if function_name in TOOL_MAP:
                        st.info(f"🛠️ Executing tool: `{function_name}` with args: `{json.dumps(function_args)}`")
                        
                        # Fetch Python function from map
                        python_fn = TOOL_MAP[function_name]

                        # Safely inspect signature to pass only valid arguments
                        sig = inspect.signature(python_fn)
                        valid_args = {k: v for k, v in function_args.items() if k in sig.parameters}

                        # Execute local Python function with extracted parameters
                        tool_result = python_fn(**valid_args)

                        # Store log entry for display in Streamlit expander
                        current_turn_tool_logs.append({
                            "name": function_name,
                            "args": function_args,
                            "response": tool_result
                        })

                        with st.expander(f"🔍 Tracing: `{function_name}` Output Payload", expanded=False):
                            st.json(tool_result)

                        # Return execution result back to OpenAI model as role="tool"
                        openai_messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": json.dumps(tool_result)
                        })

                # Request model to synthesize a final answer using returned tool outputs
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=openai_messages
                )
                response_message = response.choices[0].message

            # ------------------------------------------------------------------
            # 9. RENDER & STORE FINAL RESPONSE
            # ------------------------------------------------------------------
            final_text = response_message.content
            st.markdown(final_text)

            # Save assistant response and current tool logs to Streamlit state
            st.session_state.messages.append({
                "role": "assistant",
                "content": final_text,
                "tool_logs": current_turn_tool_logs
            })
            st.session_state.messages = st.session_state.messages[-MAX_MESSAGES:]