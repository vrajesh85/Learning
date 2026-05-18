import numpy as np
import os
import httpx
import openai
from dotenv import load_dotenv
import nltk
from nltk.tokenize import sent_tokenize
from gensim.models import Word2Vec
from langchain_openai import AzureOpenAIEmbeddings
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
import warnings
warnings.filterwarnings("ignore")

nltk.data.path.append(os.path.join("/Volumes/prod_ai_dojo/nltk/nltk_data"))

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
EMBEDDINGS_DEPLOYMENT_NAME = os.environ["EMBEDDINGS_MODEL_NAME"]
PROJECT_ID = os.environ["PROJECT_ID"]

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

# Define a function to load and extract text from PDF
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

def sentence_based_chunking(docs, sentences_per_chunk=3):
    chunks = []
    for doc in docs:
        sentences = sent_tokenize(doc.page_content)
        for i in range(0, len(sentences), sentences_per_chunk):
            chunk = " ".join(sentences[i:i + sentences_per_chunk])
            chunks.append(chunk)
    return chunks

# Generate sentence chunks
text_chunks = sentence_based_chunking(docs)

    # Define a function to train Word2Vec on the given chunks and returns vector averages for each chunk.
    def word2vec_embedding(chunks):
       
        # Tokenize each chunk into words
        tokenized = [chunk.split() for chunk in chunks]
    
        # Train a Word2Vec model
        model = Word2Vec(sentences=tokenized, vector_size=100, window=5, min_count=1, workers=2)
    
        embeddings = []
        for words in tokenized:
            vectors = [model.wv[word] for word in words if word in model.wv]
            # Take average vector for each chunk
            chunk_vector = np.mean(vectors, axis=0) if vectors else np.zeros(100)
            embeddings.append(chunk_vector)
    
        return embeddings
    
    # Run Word2Vec embeddings
    w2v_embeddings = word2vec_embedding(text_chunks)
    print(f" Generated {len(w2v_embeddings)} Word2Vec chunk embeddings")
    print(f" Generated Word2Vec first chunk embeddings dimension {w2v_embeddings[0].shape} ")

w2v_embeddings[0][0:10]

# Step 1: Load and chunk using RecursiveCharacterTextSplitter
def get_recursive_chunks(pdf_path, chunk_size=500, chunk_overlap=50):
    loader = PyMuPDFLoader(pdf_path)
    raw_docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_documents(raw_docs)

    # Extract just the text part for embedding
    return [chunk.page_content for chunk in chunks]


# Example: Running it all together
pdf_path = "./Data/Healthcare doc for RAG.pdf"  # Update this if needed
text_chunks = get_recursive_chunks(pdf_path)
openai_embeddings = get_embeddings(text_chunks)

print(f"Generated {len(openai_embeddings)} OpenAI embeddings.")
print(f"First chunk embedding size: {len(openai_embeddings[0].embedding)}")
print (f"First chunk embedding : {openai_embeddings[0].embedding[0:10]}")

