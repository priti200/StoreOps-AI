from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field

class SafetyDecision(BaseModel):
    decision: str = Field(description="APPROVED or REVIEW_REQUIRED")
    reasoning: str = Field(description="Explanation for the decision")

class SafetyAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.system_message = SystemMessage(content="""You are the Safety Officer for an autonomous store manager.
        Your job is to review the proposed actions of the Operations Agent.
        
        Rules for Approval:
        1. Read-only actions (checking stock, analyzing data) are ALWAYS APPROVED.
        2. Proposing a price change is REVIEW_REQUIRED (financial impact).
        3. Proposing a stock order is REVIEW_REQUIRED (financial impact).
        4. Any action that modifies data (mocked or real) is REVIEW_REQUIRED.
        
        Output your decision structured as JSON with 'decision' and 'reasoning'.
        """)
        self.structured_llm = self.llm.with_structured_output(SafetyDecision)

    def call(self, state):
        messages = state['messages']
        last_message = messages[-1]
        
        # Simple heuristic: Check the last message content or tool calls
        # But conceptually, the safety agent reviews the *plan* or *tool usage*.
        # In this graph, strictly speaking, we might want to check what the Operations agent *said* or *did*.
        
        # If the Operations agent just called a read-only tool, it's safe.
        # If it proposed an action in text, we review it.
        
        # Construction context for review
        review_input = f"Review this latest message/action:\n{last_message}"
        
        decision = self.structured_llm.invoke([self.system_message, review_input])
        
        # Append safety decision to state (conceptually, or just return it as a message)
        # We'll return it as a structured message or just text for now.
        return {"safety_decision": decision.decision, "safety_reasoning": decision.reasoning}

safety_agent = SafetyAgent()
