# Agentic AI Store Operations Manager - Detailed Overview

**Status**: ✅ Code Complete & Verified

## 1. Executive Summary
This project is a backend-only **Agentic AI System** designed to simulate the operations of an e-commerce store manager. Unlike a simple chatbot, this system uses **Agents**—autonomous units of logic—to reason about problems, use tools, and make decisions safely.

It demonstrates how modern AI can handle complex workflows like checking inventory, analyzing sales trends, and answering policy questions without human intervention, while maintaining a safety layer for critical actions.

---

## 2. System Architecture

The system is built on **LangGraph**, which treats the AI's thought process as a graph of nodes (agents) and edges (transitions).

### The Four Core Agents

1.  **🤖 Coordinator Agent (The Router)**
    *   **Role**: Traffic Controller.
    *   **Logic**: It receives the raw user query and classifies the *intent*.
    *   **Example**: "How much did we sell?" -> Routes to **Operations**. "What is the return policy?" -> Routes to **Store RAG**.

2.  **📚 Store RAG Agent (Knowledge Base)**
    *   **Role**: Librarian.
    *   **Tech**: Uses **Retrieval Augmented Generation (RAG)** with **FAISS** (Vector Database).
    *   **Logic**: It searches through indexed documents (products.json, orders.json, policies) to find relevant text chunks, then generates an answer.
    *   **Why FAISS?**: We switched to FAISS (Facebook AI Similarity Search) because it is lightweight and runs anywhere without complex C++ build tools, making it perfect for this Python environment.

3.  **🛠️ Operations Agent (The Doer)**
    *   **Role**: Store Manager.
    *   **Capabilities**: It has access to distinct **Tools**:
        *   `check_low_stock(threshold)`: Scans inventory for items running out.
        *   `analyze_sales(product_id)`: Calculates revenue and units sold.
        *   `suggest_price_change(product_id)`: Uses logic to recommend price adjustments based on demand.
    *   **Behavior**: It doesn't just "talk"; it *executes code* to get real data before answering.

4.  **🛡️ Safety Agent (The Guard)**
    *   **Role**: Compliance Officer.
    *   **Logic**: It sits at the end of every action pipeline. It looks at what the other agents proposed.
    *   **Rules**:
        *   If the action is **Read-Only** (e.g., checking stock), it **APPROVES**.
        *   If the action is **Write/Modify** (e.g., changing a price), it flags it as **REVIEW_REQUIRED**.
    *   **Goal**: Prevents the AI from accidentally breaking the store.

---

## 3. Technical Implementation Details

### Workflow Flowchart
```mermaid
User Request -> [Coordinator]
       |
       +---> (Intent: Knowledge) -> [Store RAG] -> [Safety Check] -> Response
       |
       +---> (Intent: Action) -> [Operations] -> {Uses Tools} -> [Safety Check] -> Response
```

### Key Technologies
*   **FastAPI**: The web server that exposes the `POST /query` endpoint, making this a deployable microservice.
*   **LangGraph**: Manages the "State" (conversation history, current agent, tools used) as it passes between agents.
*   **OpenAI GPT-4o**: The brain powering the reasoning of all agents.
*   **FAISS**: The vector database storing semantic embeddings of the store's data.

---

## 4. How to Explain This to Others
*"We built an AI system that doesn't just chat—it works. It has a 'Coordinator' that delegates tasks to specialized experts. One expert knows the store policies (RAG), and another can analyze sales data using Python tools (Operations). Before any answer is sent back, a 'Safety Agent' double-checks it to ensure reliability. It's a scalable architecture for autonomous business automation."*

---

## 5. Future Roadmap (If you want to extend it)
1.  **Real Database Connection**: Replace `products.json` with a real SQL database or Shopify API.
2.  **Frontend UI**: Build a React dashboard to visualize the agent's thought process.
3.  **Human-in-the-Loop**: When the Safety Agent says "REVIEW_REQUIRED", send a notification to a Slack channel for a human to click "Approve".
