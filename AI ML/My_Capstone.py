
import json
import csv
import os
from dotenv import load_dotenv
import httpx
from langchain_openai import AzureChatOpenAI
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from IPython.display import display, Markdown

#from langgraph.checkpoint.memory import MemorySaver
#from langchain_core.messages.utils import count_tokens_approximately
#from langgraph.prebuilt import ToolNode, tools_condition
#from langchain_core.messages import SystemMessage, HumanMessage, trim_messages
#from langgraph.types import Command
#from langgraph.graph import StateGraph, END, START
#from IPython.display import display, Image, Markdown
#from typing import Annotated, Literal

## Setup Authentication and LLM Client

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


AZURE_OPENAI_ENDPOINT = "https://api.uhg.com/api/cloud/api-management/ai-gateway/1.0" #os.environ["AZURE_OPENAI_ENDPOINT"]
OPENAI_API_VERSION ="2025-01-01-preview" #os.environ["OPENAI_API_VERSION"]
EMBEDDINGS_DEPLOYMENT_NAME ="text-embedding-ada-002_2" #os.environ["EMBEDDINGS_DEPLOYMENT_NAME"]
MODEL_DEPLOYMENT_NAME ="gpt-4.1-mini_2025-04-14" #os.environ["MODEL_DEPLOYMENT_NAME"]
PROJECT_ID ="2db8b475-ec3e-468b-b253-058bbe8ff77b" #os.environ['PROJECT_ID']

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
 
# Load the insurance policies data from the JSON file
with open("./Data/insurance_policies.json", "r") as f:
    insurance_policies = json.load(f)
# Load the reference codes data from the JSON file, includes ICD10, CPT codes and their description.
with open("./Data/reference_codes.json", "r") as f:
    reference_codes = json.load(f)
# Load the patient records data from the JSON file for testing and validation purpose.
with open("./Data/validation_records.json", "r") as f:
    patient_records = json.load(f)

## Important !!! Load Test Data for final Submission
# Load final patient records from the JSON file for final submission
with open("./Data/test_records.json", "r") as f:
    test_records = json.load(f)

patient_records=test_records #overriding patient records with test data for final submission

## Patient Data Preprocessing
 
# create age function to calculate age which is mentioned in the Capstone reference document
def calculate_age(date_of_birth, date_of_service):
    age=int(date_of_service[:4])-int(date_of_birth[:4])
    return age


# add patient's age property in the existing patient records
for record in patient_records:
    record.update({'age':calculate_age(record['date_of_birth'], record['date_of_service'])})
#patient_records.update({'age': calculcate_age(patient_records['date_of_birth'], patient_record['date_of_service'])})
 
@tool
def summarize_patient_record(record_str):
    
    """
    Uses an LLM to generate a concise, context-aware summary of an Patient record,
    tailored specifically to the patient records received as input.

    Parameters:
        query (str): patient records.

    Returns:
        str: A 2–4 sentence user-friendly explanation that summarize the patient records.
    """
    
    prompt = f"""
You are an internal communications assistant who is summarizing patient records to help in validating claim coverage.
A claim auditor has submitted a patient record in json or plain text file.
patient record:
"{record_str}"

ICD-10 codes:
"{reference_codes['ICD10']}"

Available CPT codes:"{reference_codes['CPT']}"

Your job is to:
1. Extract the structured summary of patient's insurance claim record that will be used for claim coverage vailidation.
2. Extract the parts of the ICD and CPT codes with description.
3. Write a structured and conscise summary.

Key Expectations:
    Patient Demographics: Include: name, gender, and age (Note: age can be precomputed using Python or LLM reasoning and included in the input record as "age")
    Insurance Policy ID
    Diagnoses and Descriptions: Include ICD-10 codes and their mapped descriptions.
    Procedures and Descriptions: Include CPT codes and their mapped descriptions.
    Preauthorization Status: Clearly mention if preauthorization was required and whether it was obtained.
    Billed Amount (in USD)
    Date of Service

Guidelines:
- Use reasoning to identify exact match of ICD-10 codes with patient record diagnosis codes and use ICD 10 code desciption in the summary.
- User reasoning to identify exact match of procedure codes which is available in patient record and use CPT code desciption in the summary.
- If the patient record does not fully answer the question, acknowledge that transparently.

---
"""
    response=chat_client.invoke(prompt)
    print(f"Calling Tool Patient Summary :\n\n {response.content}")
    return response.content

@tool
def summarize_policy_guideline(policy_id):
    
    """
    Uses an LLM to generate a concise, context-aware summary of a insurance policy document, correspoding to the given policy_id,
    tailored specifically to the policy_id received as input.

    Parameters:
        query (str): policy_id.
"""
    prompt = f"""
You are an internal communications assistant who is summarizing insurance policy document, corresponding to given policy_id.
Returns a well-formatted summary that outlines the specific claim coverage rules for each procedure under that policy. This summary will later be used to determine whether a patient’s claim satisfies the policy’s coverage conditions.
policy_id:
"{policy_id}"
policy_documents:
"{insurance_policies}"
procedure_codes:
"{reference_codes['CPT']}"
diagnosis codes:
"{reference_codes['ICD10']}"
Your job is to:
1. Generate a concise, context-aware summary of the insurance policy document with respect to given policy_id.
2. Use reasoning to identify exact match of policy document with given policy_id and use policy document description in the summary.
3. Write a structured and conscise summary.

Key Expectations: The summary generated by this tool should be clearly formatted and include the following clearly labeled sections, in order:
    - Policy Details: Include: policy ID and plan name
    - Covered Procedures: For each covered procedure listed in the policy, include the following sub-points:
        - Procedure Code and Description (using CPT code mappings)
        - Covered Diagnoses and Descriptions (using ICD-10 code mappings)
        - Gender Restriction
        - Age Range
        - Preauthorization Requirement
        - Notes on Coverage (if any)
Each procedure should be presented as a separate entry under the "Covered Procedures" section, with the required sub-points clearly listed.
"""
    response=chat_client.invoke(prompt)
    print(f"Calling Tool Policy Summary :\n\n {response.content}")
    return response.content

@tool
def check_claim_coverage(record_summary, policy_summary):
    """
    Uses an LLM to determine whether a patient's claim satisfies the policy's coverage conditions.

    Parameters:
        record_summary (str): A summary of the patient's claim record.
        policy_summary (str): A summary of the insurance policy document.
    Returns:
        str: A 2–4 sentence user-friendly explanation that summarizes the claim coverage decision.
    """
    prompt = f"""
You are an Healthcare claim specialist who is validating patient records and insurance policy document to take final decision:
- Either 'Approve' or 'ROUTE FOR REVIEW'
Parameters:
    - patient record: "{record_summary}"
    - insurance policy document: "{policy_summary}"
Your job is to:
1. Determines whether the procedures claimed by a patient are covered under their insurance policy. It takes as input the structured summary of the patient record along with the corresponding policy summary generated by the earlier tools.
2. uses LLM-based reasoning to evaluate each claimed procedure against the applicable policy conditions and returns a coverage eligibility decision, either approval or routing for manual review by a human specialist.

Key Expectations:
    - Procedures should be approved only:
        - The patient's diagnosis code(s) match the policy-covered diagnoses for the claimed procedure.
        - The procedure code is explicitly listed in the policy, and all associated conditions are satisfied.
        - The patient's age falls within the policy's defined age range (inclusive of the lower bound, exclusive of the upper bound).
        - The patient's gender matches the policy’s requirement for that procedure.
        - If preauthorization is required by the policy, it must have been obtained.
    - Only procedures and diagnoses explicitly listed in the patient record should be evaluated.
    - Decision should be made only based on above expectations.
    - Generate a structured response that includes:
        Decision: either 'APPROVE' or 'ROUTE FOR REVIEW'
        Reason: That refers to specific coverage rules and policy conditions which led to the above decision by the agent. Include all satisfied or not satfisfied policy conditions along with their procedure and diagnosis codes description.
    """
    response=chat_client.invoke(prompt)
    print(f"Calling Tool Claim Coverage:\n\n {response.content}")
    return response.content
tools=[summarize_patient_record, summarize_policy_guideline, check_claim_coverage]
llm_with_tools=chat_client.bind_tools(tools=tools)
# Instruction prompt for the overall Agent
AGENT_PROMPT_TXT = f"""You are an Healthcare Claim approval agent designed to act as an expert in researching and summarizing patient claim records, insurance policies, and healthcare information. Your primary tasks to follow the instructions step by step and summarize patient records, policy records and decide final decision.

Given a user patient records, call the relevant tools and provide the most appropriate response.
Follow these guidelines to make more informed decisions:

- Instructions should be followed in sequential order:
  1. Call the summarize_patient_record tool to generate patient summary.
  2. Call the summarize_policy_guideline tool to generate policy summary.
  3. Call check_claim_coverage tool with patient summary and policy summary which is generated from the above 2 steps.

Final output should be in json format, includes:
  patientid: patient_id,
  procedure: procedure description,
  cptcode: procedure code
  Decision: either 'APPROVE' or 'ROUTE FOR REVIEW' received response from check_claim_coverage tool. ,
  Reason: Reason received from check_claim_coverage tool.

"""

AGENT_SYS_PROMPT = SystemMessage(content=AGENT_PROMPT_TXT)

intent_claim_coverage_agent = create_react_agent(
    model=chat_client,
    tools=tools,
    prompt=AGENT_SYS_PROMPT
)

class State(TypedDict):
    messages: Annotated[list, add_messages]


# create function to Start the agent and reeive patient data from the user
def start_node(state:State)-> State:
    return {"input":state["messages"]}
# Function use to receive final output from the user and end the loop.
def end_node(state:State)-> State:
    return {"output":state["messages"]}
# Function use to route to claim agent
def agent_node(state:State)-> State:
    result=intent_claim_coverage_agent.invoke(state)
    return {"messages": [HumanMessage(content=result["messages"][-1].content,
                                          name="claim_specialist_agent")]}

graph_builder = StateGraph(State) # Initialize the graph with the shared message-passing state
# Add nodes
graph_builder.add_node("start", start_node)
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("end", end_node)

# Define edges
graph_builder.set_entry_point("start")
graph_builder.add_edge("start", "agent")
graph_builder.add_edge("agent", "end")

# Compile the graph
workflow = graph_builder.compile()

def call_claim_assistant(agent, query):
    """Execute the Single-agent LangGraph workflow on a given user query and display the final result."""

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

    display(Markdown("### ✅ Final Answer:"))
    output=event["messages"][-1].content
    jsonoutput=json.loads(output)
    display(Markdown(f"**Patient ID:** {jsonoutput['patientid']}  "))
    display(Markdown(f"**Decision:** : '{jsonoutput['Decision']}' for the Claimed procedure - {jsonoutput['procedure']} (CPT code {jsonoutput['cptcode']})  "))
    display(Markdown(f"**Reason:** {jsonoutput['Reason']}"))
    return jsonoutput

##Test with patient data
finallist=[]
for record in patient_records:
    finaldata=call_claim_assistant(workflow, str(record))
    finallist.append({"patient_id":record["patient_id"], "generated_response":f"- Decision: {finaldata['Decision']}\r\n - Reason: {finaldata['Reason']}"})

filename = "./submission.csv"

# Write to CSV
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["patient_id", "generated_response"])
    writer.writeheader()
    writer.writerows(finallist)

