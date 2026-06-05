from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_core.messages import ToolMessage
import requests


# =====================================================
# BLOCK 1: CREATE TOOL
# Creates the actual capability/function.
# LLM can use this later for live exchange rate data.
# =====================================================

@tool
def get_exchange_rate(base: str, target: str):
    """
    Get current exchange rate between currencies
    """

    url = f"https://api.exchangerate-api.com/v4/latest/{base}"

    response = requests.get(url)
    data = response.json()

    return data["rates"][target]


# =====================================================
# BLOCK 2: CREATE LLM
# Starts the model (brain).
# Without this no reasoning happens.
# =====================================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# =====================================================
# BLOCK 3: BIND TOOL TO LLM
# Makes LLM aware of available tools.
# LLM learns:
# - tool name
# - what it does
# - expected args
# NO execution happens here.
# =====================================================

tools = [get_exchange_rate]

llm_with_tools = llm.bind_tools(tools)


# =====================================================
# BLOCK 4: USER QUERY
# Input from user.
# =====================================================

query = "What is current USD to INR exchange rate?"


# =====================================================
# BLOCK 5: TOOL CALLING
# LLM analyzes query.
# Suggests tool + arguments.
# DOES NOT EXECUTE tool.
# =====================================================

response = llm_with_tools.invoke(query)

print("\nSuggested Tool Call:")
print(response.tool_calls)


# =====================================================
# BLOCK 6: TOOL EXECUTION
# Backend executes tool using args
# suggested by LLM.
# Real execution happens here.
# =====================================================

tool_messages = []

for tool_call in response.tool_calls:

    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    print("\nTool Name:", tool_name)
    print("Arguments:", tool_args)

    # actual execution
    result = get_exchange_rate.invoke(tool_args)

    print("Tool Result:", result)

    # sending tool result back to llm
    tool_messages.append(
        ToolMessage(
            content=str(result),
            tool_call_id=tool_call["id"]
        )
    )


# =====================================================
# BLOCK 7: FINAL RESPONSE GENERATION
# LLM receives tool result.
# Converts raw output into human answer.
# =====================================================

final_response = llm_with_tools.invoke(
    [query, response] + tool_messages
)

print("\nFinal Answer:")
print(final_response.content)