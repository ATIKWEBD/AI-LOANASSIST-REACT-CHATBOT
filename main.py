from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Import the RAG chain creation function from our other file
from pipeline import create_rag_chain

app = FastAPI(
    title="LoanAssist API",
    description="API for the L&T Finance Loan Inquiry Chatbot",
    version="0.1.0"
)
# --- Add CORS Middleware ---
origins = [
    "*", # This allows requests from all origins during development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- KEY OPTIMIZATION ---
# Create the RAG chain once when the application starts up.
# This avoids reloading the model and data for every single request,
# which would be very slow.
rag_chain = create_rag_chain()

# Define the request model using Pydantic
# This ensures that any request to our /chat endpoint must have a "query" field which is a string.
class ChatRequest(BaseModel):
    query: str

@app.get("/")
async def read_root():
    """
    Root endpoint with a welcome message.
    """
    return {"message": "Welcome to the LoanAssist API! Go to /docs to interact."}

@app.post("/chat")
async def chat_handler(request: ChatRequest):
    """
    This endpoint receives a user's query, passes it to the RAG chain,
    and returns the AI-generated response.
    """
    # The .invoke() method runs the RAG chain with the user's query
    response = rag_chain.invoke(request.query)
    return {"response": response}