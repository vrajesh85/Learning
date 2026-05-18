import textwrap
import openai
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

# Use appropriate file path
filepath = "Data/TextSummarization/conversation_498.txt"

with open(filepath, 'r') as file:
    conversation = file.read()
print(conversation)

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

prompt_messages = [
    {"role": "developer", "content": "You are an assistant that summarizes conversations between Doctor and Patient"},
    {"role": "user", "content": f"Please summarize the following text:\n\n{conversation}\n\nSummary:"}
]

response = query_llm(prompt_messages)

print("\n".join(textwrap.wrap(response['text'], width=80)))

# print no. of words in the summary
print(f"Number of words in summary: {len(response['text'].split())}")

prompt_messages = [
    {"role": "developer", "content": "You are an assistant that summarizes conversations \
      between Doctor and Patient. Make sure to provide concise summary in 100 words."},
    {"role": "user", "content": f"Please summarize the following text:\n\n{conversation}\n\nSummary:"}
]

response = query_llm(prompt_messages)
print(response['text'])

# print no. of words in summary
print(f"Number of words in summary: {len(response['text'].split())}")

prompt_messages = [
    {"role": "developer", "content": "You are an AI assistant specializing in summarizing conversations between a doctor and a patient. \
     Your task is to generate a clear, concise, and structured summary in 150 words or less. \
     Ensure that the summary captures the key points, including the patient's symptoms, \
     diagnosis, prescribed treatment, and follow-up instructions. \
     Present the summary in bullet points for easy readability"},
    {"role": "user", "content": f"Please summarize the following text:\n\n{conversation}\n\nSummary:"}
]

response = query_llm(prompt_messages)
print(response['text'])

# print no. of words in summary
print(f"Number of words in summary: {len(response['text'].split())}")
