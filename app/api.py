from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from app.graph import graph
import uvicorn

app = FastAPI(title="Agentic AI Store Operations Manager", version="1.0.0")

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def process_query(request: QueryRequest):
    try:
        initial_state = {
            "messages": [HumanMessage(content=request.query)],
            "agents_used": []
        }
        
        # Invoke the graph
        result = graph.invoke(initial_state)
        
        # Extract tool calls (heuristic: check for AIMessage with tool_calls)
        tools_called = []
        for msg in result["messages"]:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    tools_called.append(tc["name"])
        
        # Deduplicate agents_used (graph can append duplicates if nodes visited multiple times)
        # However, our simpler graph visits once.
        agents_used = list(dict.fromkeys(result.get("agents_used", [])))
        
        response = {
            "intent": result.get("intent", "unknown"),
            "agents_used": agents_used,
            "tools_called": list(set(tools_called)),
            "safety_decision": result.get("safety_decision", "N/A"),
            "response": result.get("final_response", "")
        }
        
        # Log to console
        print(f"--- Request Log ---")
        print(f"Query: {request.query}")
        print(f"Intent: {response['intent']}")
        print(f"Agents Trace: {response['agents_used']}")
        print(f"Tools Used: {response['tools_called']}")
        print(f"Safety Decision: {response['safety_decision']}")
        print(f"-------------------")

        return response
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
