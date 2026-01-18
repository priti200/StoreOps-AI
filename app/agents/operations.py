from typing import Annotated, List
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from app.tools.inventory_tool import check_low_stock
from app.tools.pricing_tool import analyze_sales, suggest_price_change

# Define tools for the agent
@tool
def tool_check_low_stock(threshold: int = 5):
    """Checks for products with low stock."""
    return check_low_stock(threshold)

@tool
def tool_analyze_sales(product_id: str = None):
    """Analyzes sales data for a product or all products."""
    return analyze_sales(product_id)

@tool
def tool_suggest_price_change(product_id: str):
    """Suggests a price change for a product."""
    return suggest_price_change(product_id)

tools = [tool_check_low_stock, tool_analyze_sales, tool_suggest_price_change]

class OperationsAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.llm_with_tools = self.llm.bind_tools(tools)
        self.system_message = SystemMessage(content="""You are an Operations Agent for a store.
        Your goal is to optimize store operations using the provided tools.
        You can check stock, analyze sales, and suggest price changes.
        
        IMPORTANT: You cannot perform write actions directly.
        You must detect issues and suggest ACTIONS to be reviewed.
        
        If you find low stock, report it.
        If you suggest a price change, providing the reasoning.
        """)

    def call(self, state):
        messages = state['messages']
        response = self.llm_with_tools.invoke([self.system_message] + messages)
        return {"messages": [response]}

operations_agent = OperationsAgent()
