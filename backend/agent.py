import os
from typing import Tuple, AsyncGenerator
from langgraph.graph import StateGraph, END
from pydantic import BaseModel

# Define a simple state model for the chat
class ChatState(BaseModel):
    user_message: str = ""
    agent_response: str = ""
    trace: list[str] = []

# Placeholder tool functions (to be expanded later)
async def tool_lookup_faq(question: str) -> str:
    # In a real implementation this would query a vector DB or FAQ store
    return f"[FAQ answer placeholder for: {question}]"

# Define the supervisor node
async def supervisor(state: ChatState) -> Tuple[ChatState, str]:
    # Very simple routing logic: if the message contains "billing" -> billing node, else generic.
    if "billing" in state.user_message.lower():
        next_node = "billing"
    elif "technical" in state.user_message.lower() or "error" in state.user_message.lower():
        next_node = "tech"
    else:
        next_node = "generic"
    state.trace.append(f"Supervisor routed to {next_node}")
    return state, next_node

# Generic specialist node – just echoes back with a placeholder
async def generic(state: ChatState) -> Tuple[ChatState, str]:
    answer = f"I’m the generic support assistant. You said: '{state.user_message}'."
    state.agent_response = answer
    state.trace.append("Generic responded")
    return state, END

# Billing specialist node – uses a placeholder tool
async def billing(state: ChatState) -> Tuple[ChatState, str]:
    answer = await tool_lookup_faq(state.user_message)
    state.agent_response = f"Billing specialist: {answer}"
    state.trace.append("Billing responded")
    return state, END

# Technical specialist node – placeholder
async def tech(state: ChatState) -> Tuple[ChatState, str]:
    answer = f"Technical specialist will investigate your issue: '{state.user_message}'."
    state.agent_response = answer
    state.trace.append("Tech responded")
    return state, END

# Build the graph
workflow = StateGraph(ChatState)
workflow.add_node("supervisor", supervisor)
workflow.add_node("generic", generic)
workflow.add_node("billing", billing)
workflow.add_node("tech", tech)
workflow.set_entry_point("supervisor")
workflow.compile()

# Helper to run the graph and stream the trace
async def get_agent_response(user_msg: str) -> Tuple[str, AsyncGenerator[str, None]]:
    """Runs the LangGraph workflow for a single user message.
    Returns the final response text and an async generator that yields the trace entries.
    """
    initial_state = ChatState(user_message=user_msg)
    result = await workflow.ainvoke(initial_state)
    response = result.agent_response
    async def trace_gen():
        for entry in result.trace:
            yield entry
    return response, trace_gen()
