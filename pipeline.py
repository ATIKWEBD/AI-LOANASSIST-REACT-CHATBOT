import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

#  Import Google GenAI components ---
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

# Set up the Google API Key from environment variables
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def create_rag_chain():
    """
    Sets up and returns a Retrieval-Augmented Generation (RAG) chain
    using Google Gemini.
    """
    # 1. Load the documents from our data directory
    loader = DirectoryLoader('./data/')
    docs = loader.load()

    # 2. Split the documents into smaller chunks for processing
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # 3. Create a vector store using FAISS
    # --- CHANGED: Use Google's model for embeddings ---
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
    retriever = vectorstore.as_retriever()

    # 4. Define the LLM and the prompt template
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    prompt = ChatPromptTemplate.from_template("""
    You are an expert assistant for L&T Finance. Answer the user's question based only on the following context:
    {context}

    Question: {question}
    """)

    # 5. Create the RAG chain using LangChain Expression Language (LCEL)
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

if __name__ == '__main__':
    # This allows us to test the chain directly
    chain = create_rag_chain()
    print("RAG Chain with Google Gemini created successfully. Ready to answer questions.")
    
    # Test with a question
    question = "What documents are required for a personal loan?"
    print(f"Asking: {question}")
    response = chain.invoke(question)
    print("Response:", response)