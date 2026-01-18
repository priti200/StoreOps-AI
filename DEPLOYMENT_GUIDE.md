# Deployment Guide: Agentic AI Store Operations Manager

You have a production-ready **FastAPI** application. The best way to deploy this is using **Docker** on a cloud platform like **Railway**, **Render**, or **Fly.io**.

## Option 1: The Easiest Way (Railway.app or Render)

These platforms connect directly to your GitHub repository and build it automatically.

### Steps:
1.  **Push your latest code to GitHub** (We already did this!).
2.  **Sign up** for [Railway](https://railway.app) or [Render](https://render.com).
3.  **New Project** -> **Deploy from GitHub repo**.
4.  **Select your repository**: `StoreOps-AI`.
5.  **Environment Variables**:
    *   The platform will ask for "Environment Variables".
    *   Add `OPENAI_API_KEY` and paste your key `sk-...`.
6.  **Deploy**: Click deploy. The platform will detect the `Dockerfile` or `requirements.txt` and start the server.
7.  **URL**: You will get a public URL (e.g., `https://storeops-ai.up.railway.app`).

---

## Option 2: Docker (Standard Industry Practice)

I have successfully created a `Dockerfile` in your project root. This allows you to run the app anywhere (AWS, Azure, Google Cloud).

### How to Build & Run Locally with Docker:
1.  **Build the image**:
    ```bash
    docker build -t store-ops-agent .
    ```
2.  **Run the container**:
    ```bash
    docker run -p 8000:8000 store-ops-agent
    ```

---

## Important Considerations for Production

1.  **Persisting Data**: 
    *   Currently, the system uses in-memory FAISS for the knowledge base. If the server restarts, it rebuilds the index from `products.json`.
    *   **Action**: For a real scaling store, you would want to use **Pinecone** or a persistent **ChromaDB** instance instead of local FAISS.

2.  **API Security**:
    *   Currently, the API is open. Anyone with the URL can query it.
    *   **Action**: Add API Key authentication or OAuth to your FastAPI implementation to protect your `POST /query` endpoint.

3.  **Rate Limiting**:
    *   You might hit OpenAI limits if too many people use it. Consider adding rate limiting middleware to FastAPI.
