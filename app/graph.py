from typing import TypedDict, Annotated, List, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages

from app.agents.coordinator import coordinator_agent
from app.agents.operations import operations_agent
from app.agents.safety import safety_agent
from app.agents.store_rag import StoreRAG

# Define State
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    intent: str
    next_agent: str
    safety_decision: str
    safety_reasoning: str
    final_response: str
    agents_used: Annotated[List[str], lambda x, y: x + y] # Append to list

# Node Functions
def coordinator_node(state: AgentState):
    result = coordinator_agent.call(state)
    return {
        "intent": result["intent"],
        "next_agent": result["next_agent"],
        "agents_used": ["Coordinator"]
    }

def operations_node(state: AgentState):
    # Operations agent returns a dictionary with 'messages'
    result = operations_agent.call(state)
    return {
        "messages": result["messages"],
        "agents_used": ["Operations"]
    }

def store_rag_node(state: AgentState):
    # Initialize RAG on demand (or could be singleton)
    rag = StoreRAG()
    user_query = state['messages'][0].content
    answer = rag.answer_query(user_query)
    
    # Return as an AIMessage
    return {
        "messages": [AIMessage(content=answer)],
        "agents_used": ["StoreRAG"]
    }

def safety_node(state: AgentState):
    # Safety agent inspects the last message/action
    decision = safety_agent.call(state)
    
    # We construct the final response here based on safety
    final_text = ""
    last_msg = state['messages'][-1]
    
    if decision["safety_decision"] == "APPROVED":
        final_text = last_msg.content
    else:
        final_text = f"Action halted. Safety Review: {decision['safety_decision']}. Reason: {decision['safety_reasoning']}"
        
    return {
        "safety_decision": decision["safety_decision"],
        "safety_reasoning": decision["safety_reasoning"],
        "final_response": final_text,
        "agents_used": ["Safety"]
    }

# Build Graph
builder = StateGraph(AgentState)

builder.add_node("coordinator", coordinator_node)
builder.add_node("operations", operations_node)
builder.add_node("store_rag", store_rag_node)
builder.add_node("safety", safety_node)

builder.add_edge(START, "coordinator")

# Conditional Edge from Coordinator
def route_coordinator(state: AgentState):
    if state["next_agent"] == "operations":
        return "operations"
    elif state["next_agent"] == "store_rag":
        return "store_rag"
    else:
        return "store_rag" # Default

builder.add_conditional_edges("coordinator", route_coordinator, {
    "operations": "operations",
    "store_rag": "store_rag"
})

# Both Ops and RAG go to Safety
builder.add_edge("operations", "safety")
builder.add_edge("store_rag", "safety")

builder.add_edge("safety", END)

# Compile
graph = builder.compile()
