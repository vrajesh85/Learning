
import os
import json
import httpx
from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

 # Authentication:
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

endpoint = os.environ.get("MODEL_ENDPOINT")
model_name = os.environ.get("MODEL_NAME")
project_id = os.environ.get("PROJECT_ID")
api_version = os.environ.get("API_VERSION")

chat_client = openai.AzureOpenAI(
        azure_endpoint=endpoint,
        api_version=api_version,
        azure_deployment=model_name,
        azure_ad_token=get_access_token(),
        default_headers={
            "projectId": project_id
        }
    )

# We use an exponential backoff decorator in the event too 
# many users are using the model at once and rate limit is reached
@retry(wait=wait_random_exponential(min=45, max=120), stop=stop_after_attempt(6))
def query_llm(prompt_messages, max_tokens=4096, temperature=1.0, top_p=1.0):
    
    response = chat_client.chat.completions.create(
        messages=prompt_messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        model=model_name
    )

    return {'text': response.choices[0].message.content}

query = "List top 5 commonly used classification models used in machine learning"
prompt_messages = [
    {"role": "user", "content": query}
]

response = query_llm(prompt_messages)
print(response['text'])

sample_text = """
Reasoned about discharge summary sample for 11 seconds
Patient admitted with community-acquired pneumonia received IV antibiotics with marked clinical improvement.
Fever resolved and oxygenation normalized over a 5-day hospital stay.
Discharge medications include oral azithromycin and supportive care instructions.
Follow-up is scheduled in 1 week to reassess recovery.
"""
prompt_messages=[
        {"role": "developer", "content": "You will be provided with a patient discharge summary, and your task is to extract keywords from it"},
        {"role": "user", "content": f"Extract keywords from this patient discharge summary:{sample_text}"},  
    ]

response = query_llm(prompt_messages)
print(response['text'])

sample_text = """
After reviewing the applicant’s recent medical records, lab results, and physician reports, 
the risk assessment indicates a low-risk profile with no significant pre-existing conditions. 
Standard coverage with typical premium rates is recommended. 
Final approval is contingent upon adherence to annual health monitoring requirements.
"""
prompt_messages = [
        {"role": "developer", "content": "You will be provided with unstructured data, and your task is to parse it into proper JSON format."},
        {"role": "user", "content": f"Under-writing text:{sample_text}"},        
    ]

response = query_llm(prompt_messages)
print(response['text'])
