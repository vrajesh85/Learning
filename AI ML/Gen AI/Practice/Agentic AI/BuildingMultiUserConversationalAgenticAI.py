from IPython.display import Image
Image(filename='./Data/conversational_agent.png')

import json
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain_core.tools import tool
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import SystemMessage, HumanMessage, trim_messages
from langchain_core.messages.utils import count_tokens_approximately
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from IPython.display import display, Image, Markdown
from langgraph.checkpoint.memory import MemorySaver

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
    api_version=OPENAI_API_VERSION,
    azure_deployment = MODEL_DEPLOYMENT_NAME,
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
    collection_name='web_search_db_demo4',    # Collection name
    embedding=embeddings_client,              # Embedding model for vectorization
)

# Create a vector database from simulated PubMed documents.
# Enables semantic search over clinical research content.
pubmed_db = Chroma.from_texts(
    search_docs['pubmed_pages'],              # List of PubMed-style document texts
    collection_name='pubmed_db_demo4',        # Collection name
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

# Load the doctor appointment slots database with availability details
doctor_slots_db = {
    "Dr. Janet Dyne": {"slots": [
        {"time": "10:00 AM", "available": True}, {"time": "10:30 AM", "available": True},
        {"time": "11:00 AM", "available": True}, {"time": "11:30 AM", "available": True},
        {"time": "12:00 PM", "available": True}
    ]},
    "Dr. Don Blake": {"slots": [
        {"time": "2:00 PM", "available": True}, {"time": "2:30 PM", "available": True},
        {"time": "3:00 PM", "available": True}, {"time": "3:30 PM", "available": True},
        {"time": "4:00 PM", "available": True}
    ]},
    "Dr. Susan D'Souza": {"slots": [
        {"time": "11:00 AM", "available": True}, {"time": "11:30 AM", "available": True},
        {"time": "12:00 PM", "available": True}, {"time": "12:30 PM", "available": True},
        {"time": "1:00 PM", "available": True}
    ]},
    "Dr. Matt Murdock": {"slots": [
        {"time": "4:00 PM", "available": True}, {"time": "4:30 PM", "available": True},
        {"time": "5:00 PM", "available": True}, {"time": "5:30 PM", "available": True},
        {"time": "6:00 PM", "available": True}
    ]},
    "Dr. Dinah Lance": {"slots": [
        {"time": "9:00 AM", "available": True}, {"time": "9:30 AM", "available": True},
        {"time": "10:00 AM", "available": True}, {"time": "10:30 AM", "available": True},
        {"time": "11:00 AM", "available": True}
    ]}
}

# Load the appointment bookings database — initially empty (no bookings yet)
bookings_db = []

# Tool for simulating a web search on general health topics
@tool
def search_web(query: str) -> list:
    """Search the web for a query. Useful for retrieving general or up-to-date healthcare information."""
    # Perform semantic similarity search over the web search vector database
    results = web_search_db.similarity_search(query, k=5)
    docs = [doc.page_content for doc in results]
    return docs


# Tool for simulating a PubMed-style academic search
@tool
def search_pubmed(query: str) -> list:
    """Search PubMed for scientific articles related to the query."""
    # Perform semantic similarity search over the PubMed vector database
    results = pubmed_db.similarity_search(query, k=5)
    docs = [doc.page_content for doc in results]
    return docs


# Tool for recommending a doctor based on user symptoms or query
@tool
def recommend_doctor(query: str) -> dict:
    """Recommend the most suitable doctor based on the user's symptoms."""
    doctors_list = str(doctors_db)

    # Use LLM reasoning to select the most appropriate doctor based on the query
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


# Tool to list all doctors in the clinic from the doctors database
@tool
def list_all_doctors() -> str:
    """Return the list of all doctors in the clinic along with their details."""
    return str(doctors_db)


# Tool to retrieve all available appointment slots for a specific doctor
@tool
def show_available_slots(doctor_name: str) -> list:
    """Retrieve and return available appointment slots for a given doctor."""
    if doctor_name not in doctor_slots_db:
        return ["Doctor not found."]

    # Filter for slots that are still available
    available = [slot["time"] for slot in doctor_slots_db[doctor_name]["slots"] if slot["available"]]
    return available or ["No available slots for this doctor."]


# Tool to book an appointment with a doctor based on patient details and selected time slot
@tool
def book_appointment(doctor_name: str, slot_time: str, patient_name: str, email: str, phone: str) -> str:
    """Book an appointment with a specific doctor for a selected time slot and store it in the bookings database."""

    # Check if the doctor exists in the slots database
    if doctor_name not in doctor_slots_db:
        return "Doctor not found."

    # Find and book the specified time slot if available
    for slot in doctor_slots_db[doctor_name]["slots"]:
        if slot["time"] == slot_time:
            if slot["available"]:
                slot["available"] = False  # Mark the slot as booked
                booking = {
                    "patient_name": patient_name,
                    "email": email,
                    "phone": phone,
                    "doctor_name": doctor_name,
                    "slot": slot_time
                }
                bookings_db.append(booking)
                return f"Appointment booked for {patient_name} with {doctor_name} at {slot_time}."
            else:
                return "The selected slot is no longer available."

    return "Requested slot not found for this doctor."

# List of all tools that the LLM should be aware of
# These tools were defined earlier using the @tool decorator
tools = [
    search_web,
    search_pubmed,
    recommend_doctor,
    show_available_slots,
    book_appointment,
    list_all_doctors
]

# Bind the tools to the LLM so it can invoke tool calls when needed
# Enables tool-calling functionality in LangChain
llm_with_tools = chat_client.bind_tools(tools=tools)

# Instruction prompt for the overall Agent
AGENT_PROMPT_TXT = """You are an agent designed to act as an expert in researching medical symptoms,
recommending relevant doctors for booking appointments, and assisting with the booking process.

Given a user query, call the relevant tools and provide the most appropriate response.
Follow these guidelines to make more informed decisions:

  - For researching information:
    - If the user is researching specific aspects such as symptoms, treatments, or other healthcare-related topics,
      use both search_web and search_pubmed to gather detailed information and provide a well-structured response.
    - If the user is looking for general healthcare information, search_web alone is sufficient.
    - Use search_pubmed only if the query relates to information likely found in PubMed articles.
    - The response should include cited source links from the web search and PubMed article titles and publication dates, if available.

  - For doctor recommendations:
    - If the user's query explicitly asks for a doctor recommendation, use the recommend_doctor tool.
    - If the user asks to see all available doctors, use the list_all_doctors tool and display the list.
    - When recommending a doctor, present the information in a clear, structured format.

  - For viewing doctor slots:
    - If the user wants to see slots for a specific doctor, follow this flow:
      - First, use the list_all_doctors tool to match the name provided by the user.
      - If no match is found, inform the user and show available doctors using the list_all_doctors tool.
        Ask if they would like to book an appointment with a specific doctor.
      - If a doctor match is found, use the show_available_slots tool and display the available slots in a well-structured format.
      - If no slots are available, apologize and ask the user to try again tomorrow.

    - If the user wants to see slots based on a symptom or problem, follow this flow:
      - First, use the recommend_doctor tool to identify the most relevant doctor and show the recommendation to the user.
        Ask if they would like to book an appointment.
      - If the doctor is accepted, use the show_available_slots tool and display the available slots in a well-structured format.
      - If no slots are available, apologize and ask the user to try again tomorrow.

  - For booking appointments:
    - If the user has already booked a slot, show the appointment details and avoid double booking.
    - If the user wants to book a specific recommended doctor, follow this flow:
      - First, get the exact name of the doctor (matching the name field) and use the show_available_slots tool
        to display available slots. Ask the user to choose a preferred slot.
      - If the slot is invalid, inform the user and ask them to enter a valid slot.
      - Ensure the slot time is properly formatted (e.g., 9:00 AM, 10:00 PM).
      - Then ask for the user's name, email, and phone number.
      - Use the book_appointment tool with the correct arguments to finalize the booking.
      - Present the confirmed appointment details in a clear, structured format.
      - If no slots are available, apologize and ask the user to try again tomorrow.

    - If the user has already viewed slots (as described above), follow this flow:
      - If the user hasn’t specified a preferred slot, prompt them to do so.
      - If the slot is invalid, explain why and request a valid one.
      - Ensure the slot time is formatted correctly (e.g., 9:00 AM, 10:00 PM).
      - Then ask for the user's name, email, and phone number.
      - Use the book_appointment tool with the appropriate arguments to book the appointment.
      - Display the confirmed appointment details in a structured format.
      - If no slots are available, apologize and ask the user to try again tomorrow.

  - Politely decline to answer any queries not related to medical or healthcare information.
"""

AGENT_SYS_PROMPT = SystemMessage(content=AGENT_PROMPT_TXT)

# Define the agent's state schema for storing the message history
class State(TypedDict):
    messages: Annotated[list, add_messages]

    # Create the node function that handles reasoning and planning using the LLM
def tool_calling_llm(state: State) -> State:
    # Extract the current conversation history from the state
    current_state = state["messages"]

    # Trim the message history to fit within the model's token limit
    trimmed_state = trim_messages(
        state["messages"],
        max_tokens=127000,              # GPT-4o-mini supports up to ~128K tokens
        strategy="last",                # Retain the most recent messages
        token_counter=count_tokens_approximately,  # Use approximate token counting
        include_system=True,            # Keep the system prompt intact
        allow_partial=True              # Allow partial trimming of messages if needed
    )

    # Prepend the system instruction to the trimmed message history
    state_with_instructions = [AGENT_SYS_PROMPT] + trimmed_state

    # Call the LLM to generate a new message (either a direct response or a tool call)
    response = [llm_with_tools.invoke(state_with_instructions)]

    # Return the updated state including the new message
    return {"messages": response}


# Build the agent execution graph
builder = StateGraph(State)

# Add nodes to the graph
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode(tools=tools))

# Add edges
builder.add_edge(START, "tool_calling_llm")

# Conditional routing:
# - If the latest message includes a tool call -> route to "tools"
# - Otherwise -> end the workflow
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition,  # Routing function based on the message
    ["tools", END]
)

# Feedback loop: return to LLM for reasoning after tool execution
builder.add_edge("tools", "tool_calling_llm")

# Compile the agent graph and attach conversational memory for persistence
memory = MemorySaver()
healthbuddy_agent = builder.compile(checkpointer=memory)

from IPython.display import Image
Image(filename='./Data/tool_use_agent_arch.png', height=200, width=300)

# Utility function to call the agent and stream its step-by-step reasoning for a specific user
def call_conversational_agent(agent, prompt, user_session_id, verbose=False):
    # Stream the agent's execution using the given prompt and session ID for memory tracking
    events = agent.stream(
        {"messages": [{"role": "user", "content": prompt}]},   # User input prompt
        {"configurable": {"thread_id": user_session_id}},      # Thread ID for session-based memory (multi-user support)
        stream_mode="values"                                   # Stream messages as the agent processes them
    )

    print('Running Agent. Please wait...')

    # Iterate through each step of the streamed agent output
    for event in events:
        # If verbose mode is enabled, print each intermediate message
        if verbose:
            event["messages"][-1].pretty_print()

    # Display the final response from the agent as formatted Markdown
    print('\n\nAgent Final Response:\n')
    display(Markdown(event["messages"][-1].content))

uid = 'john001'
query = 'what doctors are available?'
call_conversational_agent(agent=healthbuddy_agent,
                          prompt=query,
                          user_session_id=uid,
                          verbose=True)

query = 'I need to see a doctor for panic attacks'
call_conversational_agent(agent=healthbuddy_agent,
                          prompt=query,
                          user_session_id=uid,
                          verbose=True)


query = 'yes please I would like to book an appointment immediately'
call_conversational_agent(agent=healthbuddy_agent,
                          prompt=query,
                          user_session_id=uid,
                          verbose=True)

query = 'the 4 pm slot would be good'
call_conversational_agent(agent=healthbuddy_agent,
                          prompt=query,
                          user_session_id=uid,
                          verbose=True)

query = 'John, john@email.com, 1001099'
call_conversational_agent(agent=healthbuddy_agent,
                          prompt=query,
                          user_session_id=uid,
                          verbose=True)

bookings_db

doctor_slots_db['Dr. Matt Murdock']

uid = 'jim007'
query = 'having a lot of stress and depression, what are some ways to tackle it? and also recommend a doctor for me'
call_conversational_agent(agent=healthbuddy_agent,
                          prompt=query,
                          user_session_id=uid,
                          verbose=True)

query = 'yes please'
call_conversational_agent(agent=healthbuddy_agent,
                          prompt=query,
                          user_session_id=uid,
                          verbose=True)

query = '4 pm please'
call_conversational_agent(agent=healthbuddy_agent,
                          prompt=query,
                          user_session_id=uid,
                          verbose=True)

query = 'no can I see the available slots again'
call_conversational_agent(agent=healthbuddy_agent,
                          prompt=query,
                          user_session_id=uid,
                          verbose=True)

query = 'lets do 6'
call_conversational_agent(agent=healthbuddy_agent,
                          prompt=query,
                          user_session_id=uid,
                          verbose=True)

query = 'jim, jim@email.com, 10201221'
call_conversational_agent(agent=healthbuddy_agent,
                          prompt=query,
                          user_session_id=uid,
                          verbose=True)

bookings_db

doctor_slots_db['Dr. Matt Murdock']



