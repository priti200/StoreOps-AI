from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field

class RoutingDecision(BaseModel):
    intent: Literal["inventory", "pricing", "analytics", "content", "general"] = Field(description="User intent classification")
    next_agent: Literal["operations", "store_rag"] = Field(description="The agent to route to")

class CoordinatorAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.system_message = SystemMessage(content="""You are the Coordinator Agent.
        Your job is to classify the user's query and route it to the correct specialist.
        
        Routing Logic:
        - 'inventory', 'pricing', 'analytics' -> Route to 'operations'.
        - 'content' (product info, policies, general questions) -> Route to 'store_rag'.
        - 'general' -> Route to 'store_rag' (default knowledge).
        """)
        self.structured_llm = self.llm.with_structured_output(RoutingDecision)

    def call(self, state):
        messages = state['messages']
        user_query = messages[0].content # Assuming first message is user query
        
        decision = self.structured_llm.invoke([self.system_message, user_query])
        
        return {"intent": decision.intent, "next_agent": decision.next_agent}

coordinator_agent = CoordinatorAgent()
