from typing import TypedDict, Literal

from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver


# ================= STATE =================

class EmailState(TypedDict):
    topic: str
    email: str
    decision: str
    feedback: str


# ================= NODES =================

def generate_email(state: EmailState):

    topic = state["topic"]

    email = f"""
Subject: {topic}

Dear Sir/Madam,

This is an email regarding {topic}.

Thank You.
"""

    print("\nGenerated Email:")
    print(email)

    return {"email": email}


def review_email(state: EmailState):

    response = interrupt(
        {
            "email": state["email"],
            "message": "approve / modify / reject"
        }
    )

    return {
        "decision": response["decision"],
        "feedback": response.get("feedback", "")
    }


def modify_email(state: EmailState):

    email = state["email"]

    feedback = state["feedback"]

    modified_email = f"""
{email}

[Modified According To Feedback]
Feedback: {feedback}
"""

    print("\nModified Email:")
    print(modified_email)

    return {"email": modified_email}


def send_email(state: EmailState):

    print("\nEmail Sent Successfully")

    return {}


# ================= ROUTER =================

def review_router(
    state: EmailState
) -> Literal["send_email", "modify_email", END]:

    if state["decision"] == "approve":
        return "send_email"

    elif state["decision"] == "modify":
        return "modify_email"

    return END


# ================= GRAPH =================

builder = StateGraph(EmailState)

builder.add_node("generate_email", generate_email)
builder.add_node("review_email", review_email)
builder.add_node("modify_email", modify_email)
builder.add_node("send_email", send_email)

builder.add_edge(START, "generate_email")
builder.add_edge("generate_email", "review_email")

builder.add_conditional_edges(
    "review_email",
    review_router
)

builder.add_edge("modify_email", "review_email")
builder.add_edge("send_email", END)

graph = builder.compile(
    checkpointer=MemorySaver()
)

print(
    graph.get_graph().draw_mermaid()
)