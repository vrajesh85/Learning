from IPython.display import Image
Image(filename='./Data/tool_calling.png')

import os
from dotenv import load_dotenv
import httpx
import json
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain_core.tools import tool
from IPython.display import display, Markdown
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

def get_access_token():
    auth = "https://api.uhg.com/oauth2/token"
    scope = "https://api.uhg.com/.default"
    grant_type = "client_credentials"


    with httpx.Client() as client:
        body = {
            "grant_type": grant_type,
            "scope": scope,
            "client_id": dbutils.secrets.get(scope="AIML_Training", key="client_id"),
            "client_secret": dbutils.secrets.get(scope="AIML_Training", key="client_secret"),
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        resp = client.post(auth, headers=headers, data=body, timeout=60)
        access_token = resp.json()["access_token"]
        return access_token


load_dotenv('./Data/UAIS_vars.env')


AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
OPENAI_API_VERSION = os.environ["OPENAI_API_VERSION"]
EMBEDDINGS_DEPLOYMENT_NAME = os.environ["EMBEDDINGS_DEPLOYMENT_NAME"]
MODEL_DEPLOYMENT_NAME = os.environ["MODEL_DEPLOYMENT_NAME"]
PROJECT_ID = os.environ['PROJECT_ID']

chat_client = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=OPENAI_API_VERSION,
    azure_deployment=MODEL_DEPLOYMENT_NAME,
    temperature=0,
    azure_ad_token=get_access_token(),
    default_headers={
        "projectId": PROJECT_ID
    }
)


embeddings_client = AzureOpenAIEmbeddings(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=OPENAI_API_VERSION,
    azure_deployment=EMBEDDINGS_DEPLOYMENT_NAME,
    azure_ad_token=get_access_token(),
    default_headers={
        "projectId": PROJECT_ID
    }
)

# Loading pre-built datasets for web search and PubMed
with open('./Data/search_data.json', 'r') as f:
    search_docs = json.load(f)

# Display the top-level keys in the loaded dataset
print(f"Major Document Types: {list(search_docs.keys())}")

tiktoken_cache_dir = os.path.abspath("./.setup/tiktoken_cache/")
os.environ["TIKTOKEN_CACHE_DIR"] = tiktoken_cache_dir
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# Create a vector database from simulated web search documents.
# Enables semantic search over general health-related content.
web_search_db = Chroma.from_texts(
    search_docs['search_pages'],              # List of web-style document texts
    collection_name='web_search_db_demo1',    # Collection name
    embedding=embeddings_client,              # Embedding model for vectorization
)

# Create a vector database from simulated PubMed documents.
# Enables semantic search over clinical research content.
pubmed_db = Chroma.from_texts(
    search_docs['pubmed_pages'],              # List of PubMed-style document texts
    collection_name='pubmed_db_demo1',        # Collection name
    embedding=embeddings_client,              # Embedding model for vectorization
)

# Load doctor dataset with availability, specialization, and contact details
doctors_db = [
    {"name": "Dr. Janet Dyne", "specialization": "Endocrinology (Diabetes Care)", "available_timings": "10:00 AM - 1:00 PM", "location": "City Health Clinic", "contact": "janet.dyne@healthclinic.com"},
    {"name": "Dr. Don Blake", "specialization": "Cardiology (Heart Specialist)", "available_timings": "2:00 PM - 5:00 PM", "location": "Metro Cardiac Center", "contact": "don.blake@metrocardiac.com"},
    {"name": "Dr. Susan D'Souza", "specialization": "Oncology (Cancer Care)", "available_timings": "11:00 AM - 2:00 PM", "location": "Hope Cancer Institute", "contact": "susan.dsouza@hopecancer.org"},
    {"name": "Dr. Matt Murdock", "specialization": "Psychiatry (Mental Health)", "available_timings": "4:00 PM - 7:00 PM", "location": "Mind Care Center", "contact": "matt.murdock@mindcare.com"},
    {"name": "Dr. Dinah Lance", "specialization": "General Physician", "available_timings": "9:00 AM - 12:00 PM", "location": "Downtown Medical Center", "contact": "dinah.lance@downtownmed.com"}
]

# Tool for simulating a web search on general health topics
@tool
def search_web(query: str) -> list:
    """Search the web for a query. Useful for retrieving general or up-to-date healthcare information."""
    # Perform semantic similarity search over the web search vector database
    results = web_search_db.similarity_search(query, k=5)
    docs = [doc.page_content for doc in results]
    return docs


# Tool for simulating a PubMed-style academic literature search
@tool
def search_pubmed(query: str) -> list:
    """Search PubMed for scientific articles related to the query."""
    # Perform semantic similarity search over the PubMed vector database
    results = pubmed_db.similarity_search(query, k=5)
    docs = [doc.page_content for doc in results]
    return docs


# Tool for recommending a doctor based on user symptoms or health-related queries
@tool
def recommend_doctor(query: str) -> dict:
    """Recommend the most suitable doctor based on the user's symptoms."""
    doctors_list = str(doctors_db)

    # Use the LLM to reason over the list and identify the best match for the user's concern
    prompt = f"""You are an assistant helping recommend a doctor based on a patient's health issues.

Here is the list of available doctors:
{doctors_list}

Given the user's query: "{query}"

Choose the most suitable doctor from the list. Only pick one doctor.
Return only the selected doctor's information in JSON format.
If unsure, recommend the General Physician.
"""

    response = chat_client.invoke(prompt)
    return {"recommended_doctor": response.content}

results = search_web.invoke('Recent treatments in Diabetes')
print(f"Total documents: {len(results)}")
print()
display(Markdown((results[0][:3000])))

results = search_pubmed.invoke('Recent treatments in Diabetes')
print(f"Total documents: {len(results)}")
print()
display(Markdown((results[1][:3000])))

result = recommend_doctor.invoke('Treatments for Diabetes')
print(f"Raw Tool Output:\n{json.dumps(result, indent=2)}")
print("-" * 50)
print(f"\nFormatted Tool Output:\n{result['recommended_doctor']}")

# List of all tools that the LLM should be aware of
# These tools were defined earlier using the @tool decorator
tools = [search_web, search_pubmed, recommend_doctor]

# Bind the tools to the LLM so it can invoke them when necessary
# Enables tool-calling functionality in LangChain
llm_with_tools = chat_client.bind_tools(tools=tools)

prompts = [
    "treatments available for diabetes",
    "Research papers on diabetes treatments",
    "What doctor could I visit for diabetes",
    "Explain what is diabetes in simple terms"
]

results = []

for prompt in prompts:
    result = llm_with_tools.invoke(prompt)
    results.append(result)

for prompt, result in zip(prompts, results):
    # If the model provided a direct response without using any tools
    if result.content:
        print('No tool call was needed')
        print(f'Prompt: {prompt}')
        print(f'Direct LLM Response: {result.content}')

    # If the model determined that a tool should be called
    if result.tool_calls:
        print('LLM decided to call tools')
        print(f'Prompt: {prompt}')
        print(f'Tool Call Request: {result.tool_calls}')

    print('-'*50)
    print()

# Create a mapping between tool call names and their corresponding functions
tool_mapper = {
    "search_web": search_web,
    "search_pubmed": search_pubmed,
    "recommend_doctor": recommend_doctor
}

# Inspect the tool call request made
results[0].tool_calls

for result in results:
    tool_call_requests = result.tool_calls
    for tool_call in tool_call_requests:
        # Retrieve the actual tool function based on the tool name from the LLM
        selected_tool = tool_mapper[tool_call["name"]]

        # Invoke the tool using the arguments provided by the LLM
        print(f"Calling tool: {tool_call['name']}")
        tool_output = selected_tool.invoke(tool_call["args"])
        print(f"Tool Output:\n{json.dumps(tool_output, indent=2)}")
        print("-"*50)
        print()


