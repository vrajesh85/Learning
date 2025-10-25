import os
import shutil
import random
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyMuPDFLoader
from langchain.schema import Document
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.retrievers import BM25Retriever
import warnings
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
import openai

warnings.filterwarnings("ignore")

# Authentication:
import httpx

auth = "https://api.uhg.com/oauth2/token"
client_id = dbutils.secrets.get(scope = "AIML_Training", key = "client_id")
client_secret = dbutils.secrets.get(scope = "AIML_Training", key = "client_secret")
scope = "https://api.uhg.com/.default"
grant_type = "client_credentials"
async with httpx.AsyncClient() as client:
    body = {
        "grant_type": grant_type,
        "scope": scope,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = await client.post(auth, headers=headers, data=body, timeout=120)
    token = resp.json()["access_token"]




load_dotenv("./Data/UAIS_vars.env")

AZURE_OPENAI_ENDPOINT = os.environ["MODEL_ENDPOINT"]
OPENAI_API_VERSION = os.environ["API_VERSION"]
CHAT_DEPLOYMENT_NAME = os.environ["CHAT_MODEL_NAME"]
PROJECT_ID = os.environ["PROJECT_ID"]
EMBEDDINGS_DEPLOYMENT_NAME = os.environ["EMBEDDINGS_MODEL_NAME"]

chat_client = openai.AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version=OPENAI_API_VERSION,
        azure_deployment=CHAT_DEPLOYMENT_NAME,
        azure_ad_token=token,
        default_headers={
            "projectId": PROJECT_ID
        }
    )

embeddings_client = openai.AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=OPENAI_API_VERSION,
    azure_deployment=EMBEDDINGS_DEPLOYMENT_NAME,
    azure_ad_token=token,
    default_headers={ 
        "projectId": PROJECT_ID
    }
)

# this function returns vector embeddings for the provided text chunks.

@retry(wait=wait_random_exponential(min=45, max=120), stop=stop_after_attempt(6))
def get_embeddings(texts_chunk):
    return embeddings_client.embeddings.create(input=texts_chunk, model=EMBEDDINGS_DEPLOYMENT_NAME).data

# this function retrieves the model's response, and returns the content of the generated message
def get_response(prompt):
    response = chat_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=CHAT_DEPLOYMENT_NAME
    )
    
    return response.choices[0].message.content


# Define a Function to Load and Extract Text from PDF
def load_pdf_with_langchain(pdf_path):
 
    # Use LangChain's built-in loader
    loader = PyMuPDFLoader(pdf_path)

    # Load the PDF into LangChain's document format
    documents = loader.load()

    print(f"Successfully loaded {len(documents)} document chunks from the PDF.")
    return documents

# Path to the uploaded PDF (replace with your actual file path)
pdf_path = "./Data/Healthcare doc for RAG.pdf"  

# Extract the document chunks
docs = load_pdf_with_langchain(pdf_path)

# splitting the text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
texts = text_splitter.split_documents(docs)

embeddings = AzureOpenAIEmbeddings(
    azure_deployment=EMBEDDINGS_DEPLOYMENT_NAME,
    api_version=OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_ad_token=token,
    default_headers={
        "projectId": PROJECT_ID
    }
)
 

 tiktoken_cache_dir = os.path.abspath("./.setup/tiktoken_cache/")
os.environ["TIKTOKEN_CACHE_DIR"] = tiktoken_cache_dir

# Due to UHG policies, we have to disable telemetry to use ChromaDB
# See here for more information: https://docs.trychroma.com/docs/overview/telemetry
os.environ["ANONYMIZED_TELEMETRY"]="False"

# Embed and store the texts
# Supplying a persist_directory will store the embeddings on disk
persist_directory = '/tmp/vector_embeddings_OPENAI'

# Store in Chroma vector DB
vectordb = Chroma.from_documents(documents=texts, 
                            embedding=embeddings,
                            persist_directory=persist_directory)
                            
# Persist the database locally
vectordb.persist()

print("Embeddings stored in ChromaDB.")

# Define Function to retrieve top_k semantically relevant documents from ChromaDB using vector search.
   
def semantic_retrieval(query, top_k=3):
    results = vectordb.similarity_search(query, k=top_k*2)  # fetch more to be safe
    unique_results = []
    seen_contents = set()

    for doc in results:
        if doc.page_content not in seen_contents:
            unique_results.append(doc)
            seen_contents.add(doc.page_content)
        if len(unique_results) >= top_k:
            break

    return unique_results

# Run test
query = "How does the Integrated Clinical Environment (ICE) platform support MIoT implementation in healthcare settings?"
semantic_results = semantic_retrieval(query)

# Print results
for i, doc in enumerate(semantic_results, 1):
    print(f"\n Semantic Result {i}:\n{doc.page_content}")


# Define a function to combine BM25 keyword matching with vector similarity for hybrid retrieval

def hybrid_retrieval_simple(query, top_k=3):
    """
    Combines semantic and keyword search results for diverse retrieval.
    """
    # Get semantic search results
    semantic_results = vectordb.similarity_search(query, k=top_k*2)
    semantic_contents = [doc.page_content for doc in semantic_results]
    
    # Get keyword search results
    documents = [Document(page_content=doc) if isinstance(doc, str) else doc 
                for doc in vectordb.get()["documents"]]
    bm25_retriever = BM25Retriever.from_documents(documents)
    keyword_results = bm25_retriever.get_relevant_documents(query, k=top_k*2)
    
    # Take half from semantic results
    final_results = semantic_results[:top_k//2]
    
    # Add unique keyword results
    for doc in keyword_results:
        if len(final_results) >= top_k:
            break
        if doc.page_content not in semantic_contents:
            final_results.append(doc)
    
    # Fill remaining spots with semantic results
    remaining_spots = top_k - len(final_results)
    if remaining_spots > 0:
        start_idx = len(final_results) - remaining_spots
        final_results.extend(semantic_results[start_idx:start_idx+remaining_spots])
    
    return final_results

# Test the function
hybrid_results = hybrid_retrieval_simple("How does the Integrated Clinical Environment (ICE) platform support MIoT implementation in healthcare settings?")
for i, doc in enumerate(hybrid_results, 1):
    print(f"\n Hybrid Result {i}:\n{doc.page_content}")


# Define function to use OpenAI GPT (via ChatCompletion) to rerank document chunks based on relevance to a query.
def llm_rerank_with_openai(query, retrieved_docs, top_k=3):
    """
    Args:
        query (str): The user’s input question.
        retrieved_docs (list): List of LangChain Document objects retrieved from ChromaDB.
        top_k (int): Number of top chunks to return.

    Returns:
        list: Sorted list of the most relevant chunks, based on GPT scoring.
    """
    # Step 1: Prepare the ranking prompt
    prompt = f"You are helping rank document chunks based on how well they answer this question:\n\nQuestion: {query}\n\n"
    prompt += "Here are the chunks:\n\n"

    for i, doc in enumerate(retrieved_docs):
        prompt += f"Chunk {i+1}:\n{doc.page_content.strip()}\n\n"

    prompt += f"Please rank the top {top_k} chunks in order of relevance. Respond only like this:\nChunk 3, Chunk 1, Chunk 5"

    # Step 2: Call GPT for reranking
    
    gpt_output=get_response(prompt)
    print("GPT Rerank Output:\n", gpt_output)

    # Step 3: Extract chunk numbers from the output
    chunk_order = [int(s.strip().split()[-1]) - 1 for s in gpt_output.split(',') if s.strip().startswith("Chunk")]

    # Step 4: Return sorted chunk objects
    reranked_docs = [retrieved_docs[i] for i in chunk_order if i < len(retrieved_docs)]
    return reranked_docs


# Run the reranker
reranked_results = llm_rerank_with_openai(query, hybrid_results )

# Display the reranked chunks
for i, doc in enumerate(reranked_results, 1):
    print(f"\n Reranked Chunk {i}:\n{doc.page_content[:300]}")


