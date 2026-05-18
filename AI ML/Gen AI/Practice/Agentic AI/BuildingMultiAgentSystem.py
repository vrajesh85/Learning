from IPython.display import Image
Image(filename='./Data/multi_agent.png')

import json
from langchain_openai import AzureChatOpenAI
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langgraph.types import Command
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
    api_version=OPENAI_API_VERSION,
    azure_deployment = MODEL_DEPLOYMENT_NAME,
    temperature=0,
    azure_ad_token=get_access_token(),
    default_headers={
        "projectId": PROJECT_ID
    }
)

# Load the SOP documents dictionary from the JSON file
with open("./Data/sop_documents.json", "r") as f:
    sop_documents = json.load(f)

# Access the HR-related Standard Operating Procedures from the loaded dictionary
hr_sops = sop_documents['HR']
print(f'HR SOP Documents:\n {json.dumps(hr_sops, indent=2)}')

# Tool: classify_department
# -----------------------------------------------
# This tool is used by the intent classifier agent to determine which department
# (HR, Finance, or IT) is responsible for handling a given user query. It leverages
# LLM reasoning to map the query to the most relevant department label.
@tool
def classify_department(query: str) -> str:
    """
    Uses an LLM to classify a user's policy-related question into the most appropriate department:
    HR, Finance, or IT. This tool enables the intent classification agent to route the query
    to the correct downstream workflow.

    Parameters:
        query (str): The user's natural language question.

    Returns:
        str: One of the department labels: 'HR', 'Finance', or 'IT'.
    """

    # LLM prompt instructs the model to analyze the user query and choose the correct department
    prompt = f"""
You are a policy assistant responsible for determining which internal department should handle a given employee query.

Available departments and their primary responsibilities:
- HR: Leave policies, remote work, dress code, onboarding, general employee policies
- Finance: Expense reimbursements, salary, travel allowance, WFH equipment, bonuses
- IT: Software access, device issues, VPN setup, password resets, system access

User query:
"{query}"

Instructions:
- Carefully read the query and compare it to department responsibilities above.
- Respond with exactly one word: HR, Finance, or IT.
- Do not include any additional explanation or commentary.
"""

    # Run the prompt through the LLM client and return the result
    return chat_client.invoke(prompt).content.strip()


# Tool: retrieve_sop
# -----------------------------------------------
# This tool is used by the SOP retriever agent to identify the most relevant policy section
# based on a user's query and department. It uses LLM reasoning to match user intent
# against a curated list of SOP entries for that department.
@tool
def retrieve_sop(department: str, query: str) -> str:
    """
    Uses an LLM to retrieve the most relevant Standard Operating Procedure (SOP) section
    based on the user's query and the department it pertains to.

    Parameters:
        department (str): The department the query has been classified under (e.g., HR, Finance, IT).
        query (str): The user's natural language question.

    Returns:
        str: A matched SOP policy text, or a fallback message if no match is found.
    """

    # Fetch SOP entries for the specified department
    department_data = sop_documents.get(department, {})

    # Format the SOP options into a readable string for the LLM
    options = "\n".join([f"- {k}: {v}" for k, v in department_data.items()])

    # LLM prompt to match user intent with the most appropriate SOP section
    prompt = f"""
You are an internal policy retrieval assistant for the {department} department.

Your task is to analyze the employee's query and select the most relevant SOP section from the list below.

User Query:
"{query}"

Available SOPs:
{options}

Instructions:
- Use reasoning to identify the best match, even if exact keywords are not present.
- If no SOP matches the query, respond with: "No relevant SOP found."
- If a match is found, return the full SOP policy text without any extra commentary.
"""

    # Run the prompt through the LLM client and return the result
    return chat_client.invoke(prompt).content.strip()


# Tool: summarize_sop
# -----------------------------------------------
# This tool is used by the answer generator agent to convert an SOP section into a clear,
# user-facing response that directly addresses the user's original question. It uses
# LLM-based reasoning to extract relevant details and communicate them concisely.
@tool
def summarize_sop(query: str, sop_text: str) -> str:
    """
    Uses an LLM to generate a concise, context-aware summary of an SOP section,
    tailored specifically to the user's original question.

    Parameters:
        query (str): The user's original question or concern.
        sop_text (str): The SOP content retrieved by the previous agent.

    Returns:
        str: A 2–4 sentence user-friendly explanation that directly answers the query.
    """

    # Prompt instructs the LLM to tailor the summary to the user's specific question
    prompt = f"""
You are an internal communications assistant helping employees understand policy content.

A user has submitted a question related to a policy. You have access to the relevant SOP section.

Your job is to:
1. Understand what the user is really asking.
2. Extract the parts of the SOP that are most relevant to their concern.
3. Write a short, helpful answer tailored to that concern — not a generic summary.

Guidelines:
- Be clear and concise (3–4 sentences).
- Avoid repeating SOP language verbatim — rephrase for clarity.
- Emphasize any limits, exceptions, approval flows, or timing rules.
- If the SOP does not fully answer the question, acknowledge that transparently.

---

User Query:
{query}

Relevant SOP Content:
{sop_text}
"""

    # Return the LLM-generated response, cleaned of surrounding whitespace
    return chat_client.invoke(prompt).content.strip()


# Agent: intent_classifier_agent
# ------------------------------------------------
# This agent is responsible for determining which department (HR, Finance, or IT)
# should handle the user's query. It calls the `classify_department` tool,
# and outputs the department name, which is then used to route the query further.
intent_classifier_agent = create_react_agent(
    model=chat_client,
    tools=[classify_department],
    state_modifier="""
You are acting as an internal query router responsible for directing questions to the correct department (HR, Finance, or IT).

Instructions:
1. Carefully read the user's query.
2. Consider which department is best suited to handle the question based on internal responsibilities.
3. Call the `classify_department` tool and retrieve the department name.
4. Return the department name as the final message.

Important:
- Use sound reasoning to map vague terms to real responsibilities.
- Do NOT guess if unsure — clearly state ambiguity in reasoning before making a decision.
- The output must be a single department name only.

This output will be used to route the query to the SOP retrieval system.
"""
)

# Agent: sop_retriever_agent
# ------------------------------------------------
# This agent retrieves the most relevant SOP section based on the user's query
# and the department identified by the intent classifier. It uses the `retrieve_sop`
# tool and returns the selected policy text, which will then be summarized downstream.
sop_retriever_agent = create_react_agent(
    model=chat_client,
    tools=[retrieve_sop],
    state_modifier="""
You are a policy retriever agent for internal SOPs. Your job is to extract the most relevant policy section from department-specific documents.

Instructions:
1. Use the department classification from the previous agent.
2. Use the user's original query to find the best-matching SOP section.
3. Call the `retrieve_sop` tool with the department and query.
4. Carefully check the result. If it's irrelevant, say "No matching policy found." Otherwise, return the text exactly.

Be thoughtful — many queries will not use exact keywords.
Your reasoning must map intent to the most fitting policy.

This output will be passed to another agent for simplification.
"""
)

# Agent: answer_generator_agent
# ------------------------------------------------
# This agent generates the final user-facing response by summarizing the relevant SOP
# section in context of the original query and identified department. The output includes
# the query, mapped department, and the generated explanation.
answer_generator_agent = create_react_agent(
    model=chat_client,
    tools=[summarize_sop],
    state_modifier="""
You are a communication specialist tasked with creating user-friendly responses to internal SOP queries.

Responsibilities:
1. Use the original user query, the department it was mapped to,
and the relevant SOP passage provided by the SOP retriever agent.
2. Call the `summarize_sop` tool, passing both the query and SOP content.
3. Generate a structured response that includes:
   - The original user query
   - The department that will handle the query (HR, Finance, or IT)
   - A final explanation based on the SOP

Guidelines:
- Clearly address the user's concern using the SOP content
- Highlight any limits, conditions, approval requirements, or deadlines
- Write in plain, professional English
- If the SOP doesn't fully answer the query, note that and recommend escalation

Final output format:
---------------------
**User Query**: <original query>

**Department**: <HR / Finance / IT>

**Response**: <actionable explanation>
---------------------
"""
)

# Define the agent's state schema for storing the message history
class State(TypedDict):
    messages: Annotated[list, add_messages]

    # Supervisor Configuration
# ------------------------------------------------
# The supervisor manages the control flow between agents.
# It decides which agent should act next based on the current conversation state,
# and ensures the system progresses logically through the pipeline.

# List of agent labels the supervisor can route to
members = ["intent_classifier_agent", "sop_retriever_agent", "answer_generator_agent"]

# LLM prompt used to instruct the supervisor to choose the next agent
SUPERVISOR_PROMPT = f"""You are a supervisor managing a multi-agent SOP assistant.

Available agents:
- intent_classifier_agent: Identifies the correct department for the query.
- sop_retriever_agent: Retrieves the relevant SOP section from internal documentation.
- answer_generator_agent: Generates a clear, concise response based on the SOP and query.

Based on the current state of the conversation, select the next agent to act.

Respond with the exact agent name or FINISH if all steps are complete.
"""

# LangGraph supervisor node function
def supervisor_node(state: State) -> Command[Literal[
    "intent_classifier_agent",
    "sop_retriever_agent",
    "answer_generator_agent",
    "__end__"
]]:
    # Loads message history for the Agent including the system prompt
    messages = [{"role": "system", "content": SUPERVISOR_PROMPT}] + state["messages"]
    # Ask the LLM to choose the next worker agent based on Agent context
    response = chat_client.invoke(messages)
    goto = response.content

    # Terminate if the workflow is complete
    if goto == "FINISH":
        goto = END

    # Instructs LangGraph to move to the next worker agent and update state with routing decision
    return Command(goto=goto, update={"next": goto})

# Node: intent_classifier_node
# ------------------------------------------------
# Executes the intent_classifier_agent, which classifies the user's query
# into a department (HR, Finance, or IT). The agent's output message is
# appended to the conversation state, and control is returned to the supervisor.
def intent_classifier_node(state: State) -> Command[Literal["supervisor"]]:
    result = intent_classifier_agent.invoke(state)
    return Command(
        update={"messages": [HumanMessage(content=result["messages"][-1].content,
                                          name="intent_classifier_agent")]},
        goto="supervisor"  # Return control to the supervisor for next routing decision
    )

# Node: sop_retriever_node
# ------------------------------------------------
# Executes the sop_retriever_agent, which fetches the relevant SOP section
# based on the classified department and the user's query. The retrieved policy
# is appended to the message history and control returns to the supervisor.
def sop_retriever_node(state: State) -> Command[Literal["supervisor"]]:
    result = sop_retriever_agent.invoke(state)
    return Command(
        update={"messages": [HumanMessage(content=result["messages"][-1].content,
                                          name="sop_retriever_agent")]},
        goto="supervisor"  # Return control to the supervisor for next routing decision
    )

# Node: answer_generator_node
# ------------------------------------------------
# Executes the answer_generator_agent, which summarizes the SOP section into
# a clear and concise answer tailored to the user query. The generated response
# is appended to the message history and control returns to the supervisor.
def answer_generator_node(state: State) -> Command[Literal["supervisor"]]:
    result = answer_generator_agent.invoke(state)
    return Command(
        update={"messages": [HumanMessage(content=result["messages"][-1].content,
                                          name="answer_generator_agent")]},
        goto="supervisor"  # Return control to the supervisor to evaluate completion
    )

# LangGraph Multi-Agent Graph
# ------------------------------------------------
# This section defines the multi-agent execution graph using LangGraph.
# Each node in the graph represents an agent function, and the supervisor
# dynamically controls the flow between them based on conversation state.

graph_builder = StateGraph(State)  # Initialize the graph with the shared message-passing state

# Define the starting point of the workflow
graph_builder.add_edge(START, "supervisor")

# Register all nodes (agents and supervisor) in the graph
graph_builder.add_node("supervisor", supervisor_node)
graph_builder.add_node("intent_classifier_agent", intent_classifier_node)
graph_builder.add_node("sop_retriever_agent", sop_retriever_node)
graph_builder.add_node("answer_generator_agent", answer_generator_node)

# Compile the graph into an executable object that can process user inputs
multi_agent = graph_builder.compile()

from IPython.display import Image
Image(filename='./Data/multi_agent_arch.png', height=300, width=400)

def call_sop_assistant(agent, query):
    """Execute the multi-agent LangGraph workflow on a given user query and display the final result."""

    # Stream the execution of the graph with the user's query as input
    events = agent.stream(
        {"messages": [("user", query)]},  # Initial input message from the user
        {"recursion_limit": 150},         # Max number of node steps to prevent infinite loops
        stream_mode="values"              # Stream each intermediate value for debugging or visibility
    )

    # Print each intermediate message (from agent invocations)
    for event in events:
        event["messages"][-1].pretty_print()
        print()

    # Display the final message from the last agent in formatted Markdown
    display(Markdown("### ✅ Final Answer:"))
    display(Markdown(event["messages"][-1].content))

# Run the full multi-agent flow for a HR query
call_sop_assistant(multi_agent,
                   "How many vacation days can I carry over to next year?")

# Run the full multi-agent flow for a Finance query
call_sop_assistant(multi_agent,
                   "Is there a deadline to submit expense reports after a trip?")

# Run the full multi-agent flow for an IT query
call_sop_assistant(multi_agent,
                   "I dropped my laptop — can I request a replacement?")

