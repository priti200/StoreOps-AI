from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class StoreRAG:
    def __init__(self, products_path: str = "app/data/products.json", orders_path: str = "app/data/orders.json"):
        self.products_path = products_path
        self.orders_path = orders_path
        self.embedding_function = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vector_store = None
        self._initialize_knowledge_base()

    def _initialize_knowledge_base(self):
        """Indexes products and orders if not already indexed."""
        # For FAISS (in-memory by default for this MVP), we rebuild on startup.
        # In production, we would load_local().
        
        documents = []
        
        # Index Products
        try:
            with open(self.products_path, "r") as f:
                products = json.load(f)
                for p in products:
                    content = f"Product: {p['name']}. Category: {p['category']}. Price: ${p['price']}. Stock: {p['stock']}. Description: {p['description']}"
                    doc = Document(page_content=content, metadata={"type": "product", "id": p['id']})
                    documents.append(doc)
        except FileNotFoundError:
            print(f"Warning: {self.products_path} not found.")

        # Index Orders (Summarized)
        try:
            with open(self.orders_path, "r") as f:
                orders = json.load(f)
                for o in orders:
                    content = f"Order ID: {o['order_id']}. Product ID: {o['product_id']}. Quantity: {o['quantity']}. Date: {o['date']}. Revenue: ${o['revenue']}."
                    doc = Document(page_content=content, metadata={"type": "order", "id": o['order_id']})
                    documents.append(doc)
        except FileNotFoundError:
            print(f"Warning: {self.orders_path} not found.")
            
        # Index Policies (Hardcoded for MVP)
        policies = [
            "Return Policy: Items can be returned within 30 days of purchase if they are in original condition.",
            "Shipping Policy: Free shipping on orders over $50. Standard shipping takes 3-5 business days.",
            "Support Policy: Customer support is available 24/7 via email at support@examplestore.com."
        ]
        for policy in policies:
            doc = Document(page_content=policy, metadata={"type": "policy"})
            documents.append(doc)

        if documents:
            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(documents, self.embedding_function)
            else:
                self.vector_store.add_documents(documents)
            print(f"Indexed {len(documents)} documents into Store Knowledge Base (FAISS).")

    def retrieve(self, query: str, k: int = 3) -> List[Document]:
        """Retrieves relevant documents for a given query."""
        return self.vector_store.similarity_search(query, k=k)

    def answer_query(self, query: str) -> str:
        """Simple retrieval-based answer (simulate RAG agent logic)."""
        docs = self.retrieve(query)
        context = "\n".join([d.page_content for d in docs])
        return f"Context retrieved:\n{context}"

if __name__ == "__main__":
    # Test the RAG setup
    try:
        rag = StoreRAG()
        print("\n--- Test Retrieval ---")
        query = "What is the return policy?"
        results = rag.retrieve(query)
        for doc in results:
            print(f"- {doc.page_content}")
            
        print("\n--- Test Product Search ---")
        query = "headphones"
        results = rag.retrieve(query)
        for doc in results:
            print(f"- {doc.page_content}")

    except Exception as e:
        print(f"Error during RAG initialization or test: {e}")
        print("Ensure OpenAI API Key is set in .env")
