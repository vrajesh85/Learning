# import libraries 
import os
from langchain.document_loaders import PyMuPDFLoader
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

# Let's view the first couple of chunks to see what we got
print("\n Sample Extracted Content:")
for i, doc in enumerate(docs[:2]):
    print(f"\n--- Chunk {i + 1} ---")
    print(doc.page_content[:500])  # Show first 500 characters
    print("Metadata:", doc.metadata)

