# backend.py

from dotenv import load_dotenv
from typing import TypedDict, Annotated

import requests

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, HumanMessage

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command

load_dotenv()

# ==================================================
# LLM
# ==================================================

llm = ChatOpenAI(model="gpt-4o-mini")

# ==================================================
# TOOLS
# ==================================================

@tool
def get_stock_price(symbol: str) -> dict:
    """
    Get latest stock price.
    """

    url = (
        "https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE&symbol={symbol}&apikey=YOUR_API_KEY"
    )

    response = requests.get(url, timeout=10)

    return response.json()


@tool
def purchase_stock(symbol: str, quantity: int) -> dict:
    """
    Purchase stock after human approval.
    """

    approval = interrupt(
        {
            "action": "purchase_stock",
            "symbol": symbol,
            "quantity": quantity,
            "message": f"Approve purchase of {quantity} shares of {symbol}?"
        }
    )

    if approval["approved"]:

        return {
            "status": "success",
            "symbol": symbol,
            "quantity": quantity,
            "message": f"Successfully purchased {quantity} shares of {symbol}"
        }

    return {
        "status": "cancelled",
        "symbol": symbol,
        "quantity": quantity,
        "message": "Purchase cancelled by reviewer"
    }


tools = [get_stock_price, purchase_stock]

llm_with_tools = llm.bind_tools(tools)

# ==================================================
# STATE
# ==================================================

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# ==================================================
# NODES
# ==================================================

def chatbot_node(state: ChatState):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


tool_node = ToolNode(tools)

# ==================================================
# GRAPH
# ==================================================

builder = StateGraph(ChatState)

builder.add_node("chatbot", chatbot_node)
builder.add_node("tools", tool_node)

builder.add_edge(START, "chatbot")

builder.add_conditional_edges(
    "chatbot",
    tools_condition
)

builder.add_edge(
    "tools",
    "chatbot"
)

graph = builder.compile(
    checkpointer=MemorySaver()
)

# ==================================================
# VISUALIZE GRAPH
# ==================================================

print(graph.get_graph().draw_mermaid())

# ==================================================
# CLI
# ==================================================

if __name__ == "__main__":

    thread_id = "stock-thread"

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        result = graph.invoke(
            {
                "messages": [
                    HumanMessage(content=user_input)
                ]
            },
            config={
                "configurable": {
                    "thread_id": thread_id
                }
            }
        )

        interrupts = result.get("__interrupt__", [])

        if interrupts:

            approval_request = interrupts[0].value

            print("\n===== HUMAN APPROVAL REQUIRED =====")
            print(approval_request)

            choice = input(
                "\nApprove? (y/n): "
            ).strip().lower()

            approved = choice == "y"

            result = graph.invoke(
                Command(
                    resume={
                        "approved": approved
                    }
                ),
                config={
                    "configurable": {
                        "thread_id": thread_id
                    }
                }
            )

        final_message = result["messages"][-1]

        print("\nBot:")
        print(final_message.content)