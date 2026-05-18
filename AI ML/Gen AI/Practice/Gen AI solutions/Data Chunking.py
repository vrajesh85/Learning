# Import required libraries
import os
import nltk
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from nltk.tokenize import sent_tokenize

nltk.data.path.append(os.path.join("/Volumes/prod_ai_dojo/nltk/nltk_data"))

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

# Define a function to split text into fixed-size character chunks using LangChain's CharacterTextSplitter.

def fixed_size_chunking(docs, chunk_size=500, chunk_overlap=50):
    
    splitter = CharacterTextSplitter(
        separator=" ",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(docs)

# Apply it
fixed_chunks = fixed_size_chunking(docs)
print(f" Total fixed-size chunks: {len(fixed_chunks)}\n")
print(f" Example:First Chunk \n{fixed_chunks[0].page_content[:]}")

# Splits documents using RecursiveCharacterTextSplitter which preserves context better

def recursive_chunking(docs, chunk_size=500, chunk_overlap=50):
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(docs)

# Apply it
recursive_chunks = recursive_chunking(docs)
print(f" Total recursive chunks: {len(recursive_chunks)}\n")
print(f" Example: First Chunk \n{recursive_chunks[0].page_content[:]}")


# Define a function to split each page into chunks of N sentences.
def sentence_based_chunking(docs, sentences_per_chunk=3):

    chunks = []

    for doc in docs:
        sentences = sent_tokenize(doc.page_content)
        for i in range(0, len(sentences), sentences_per_chunk):
            chunk_text = " ".join(sentences[i:i + sentences_per_chunk])
            chunks.append(chunk_text)

    return chunks

sentence_chunks = sentence_based_chunking(docs)
print(f" Total sentence-based chunks: {len(sentence_chunks)}\n")
print(f" Example:\n{sentence_chunks[0][:]}")


# Define a function to split based on paragraph breaks (using two newlines)

def semantic_chunking(docs):
   
    chunks = []
    for doc in docs:
        paragraphs = doc.page_content.split("\n\n")
        for para in paragraphs:
            cleaned = para.strip()
            if cleaned:
                chunks.append(cleaned)
    return chunks

semantic_chunks = semantic_chunking(docs)
print(f" Total semantic chunks: {len(semantic_chunks)}")
print(f" Example:\n{semantic_chunks[0][:]}")


fixed_chunks = fixed_size_chunking(docs)
#print(f" Total fixed-size chunks : {len(fixed_chunks)}")
print(f" Fixed-size chunk at index 6: \n{fixed_chunks[6].page_content[:]}\n")

recursive_chunks = recursive_chunking(docs)
#print(f" Total recursive chunks: {len(recursive_chunks)}")
print(f" Recursive chunk at index 6: \n{recursive_chunks[6].page_content[:]}\n")

sentence_chunks = sentence_based_chunking(docs)
#print(f" Total sentence-based chunks: {len(sentence_chunks)}")
print(f" Sentence-based chunk at index 6:\n{sentence_chunks[6][:]}\n")

semantic_chunks = semantic_chunking(docs)
#print(f" Total semantic chunks: {len(semantic_chunks)}")
print(f" Semantic chunk at index 6:\n{semantic_chunks[6][:]}")


