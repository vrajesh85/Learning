from IPython.display import Image
Image(filename='./Data/tool_use_agent.png')

import json
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from IPython.display import display, Image, Markdown

import os
from dotenv import load_dotenv
import httpx

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
    api_version=OPENAI_API_VERSION,  # or your api version
    azure_deployment=MODEL_DEPLOYMENT_NAME,  # or your deployment
    temperature=0,
    azure_ad_token=get_access_token(),
    default_headers={
        "projectId": PROJECT_ID
    }
)


embeddings_client = AzureOpenAIEmbeddings(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=OPENAI_API_VERSION,  # or your api version
    azure_deployment=EMBEDDINGS_DEPLOYMENT_NAME,  # or your deployment
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
    collection_name='web_search_db_demo2',    # Collection name
    embedding=embeddings_client,              # Embedding model for vectorization
)

# Create a vector database from simulated PubMed documents.
# Enables semantic search over clinical research content.
pubmed_db = Chroma.from_texts(
    search_docs['pubmed_pages'],              # List of PubMed-style document texts
    collection_name='pubmed_db_demo2',        # Collection name
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

# List of all tools that the LLM should be aware of
# These tools were defined earlier using the @tool decorator
tools = [search_web, search_pubmed, recommend_doctor]

# Instruction prompt for the overall Agent
AGENT_PROMPT_TXT = """You are an agent designed to act as an expert in researching medical symptoms
and recommending relevant doctors for booking appointments. Also, remember the current year is 2025.

Given a user query, call the relevant tools and provide the most appropriate response.
Follow these guidelines to help you make more informed decisions:
  - If the user's query specifically asks for a doctor recommendation, recommend an appropriate doctor.
  - If the user is researching specific aspects related to symptoms, treatments, or other areas of healthcare,
    use both the search_web and search_pubmed tools to gather detailed information and provide a well-structured response.
  - If the user is just looking for general healthcare information, web search alone is sufficient.
  - Use the search_pubmed tool only if the query relates to information typically found in PubMed articles.
  - Responses should include cited source links and/or PubMed article titles and publication dates, if available.
  - If recommending doctors, use the recommend_doctor tool and display detailed information in a clear, structured format.
    Also, encourage the user to book an appointment via email.
  - Politely decline to answer any queries that are not related to medical or healthcare information.

The final response should contain the following:
- The main output content.
- At the end, include an Agent Reasoning: section that covers the following in bullet points:
    - Your step-by-step reasoning process for arriving at the final response.
    - The tools you called, in the specific order, with their names.
    - Observations from the tool call results that helped you construct the final response.
"""

AGENT_SYS_PROMPT = SystemMessage(content=AGENT_PROMPT_TXT)

# Create the agent using tools, LLM, and the system instruction prompt
healthbuddy_agent = create_react_agent(
    model=chat_client,
    tools=tools,
    state_modifier=AGENT_SYS_PROMPT
)

from IPython.display import Image
Image(filename='./Data/tool_use_agent_arch.png', height=200, width=300)

# Utility function to call the agent and stream its step-by-step reasoning
def call_agent(agent, query, verbose=False):

    # Stream the agent's execution for the given query
    for event in agent.stream(
        {"messages": [HumanMessage(content=query)]},  # Input prompt
        stream_mode='values'  # Stream output as intermediate values
    ):
        # If verbose is enabled, print each intermediate message
        if verbose:
            event["messages"][-1].pretty_print()

    # Display the final response from the agent as Markdown
    print('\n\nFinal Response:\n')
    display(Markdown(event["messages"][-1].content))

    # Return the final message content for optional downstream use
    return event["messages"][-1].content

# Example usage
query = "what are the latest methods for diabetes management and recommend a doctor please"
result = call_agent(healthbuddy_agent, query, verbose=True)

# Example usage
query = "I am having panic attacks, what could I do?"
result = call_agent(healthbuddy_agent, query, verbose=True)

# Agent limitation
query = "Great can you book an appointment please"
result = call_agent(healthbuddy_agent, query, verbose=True)

