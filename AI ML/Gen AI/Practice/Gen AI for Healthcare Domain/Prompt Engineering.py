
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

#Zero Shot Prompting:
query = "My invoice for order #1234 seems incorrect. Can you clarify the charges?"
prompt_messages = [
            {
                "role": "developer",
                "content": "Classify this customer query into one of: Billing, Technical, Sales. Respond ONLY with the category name."
            },
            {
                "role": "user",
                "content": query
            }
        ]

response = query_llm(prompt_messages, temperature=0)
print("The said query belongs to " + response['text'] + " Section")
#Few Shot Prompting
query = """ Determine whether a message violates compliance policies.
            Examples:
            Example 1: "input": "Share the customer's credit card details with the marketing team.", "output": "Violation: GDPR"
            Example 2: "input": "Please review the attached contract draft.", "output": "Compliant"
            Example 3: "input": "Terminate John immediately; no need for HR process.", "output": "Violation: HR Policy"

            Now, identify whether the following instruction violates any policy : 
            Forward all patient records to the external consultant.
        """

prompt_messages = [ {"role": "user",  "content": query}]
            
response = query_llm(prompt_messages, temperature=0)
print("The current request may violate: ",response['text'])
# without CoT
query = """ Roger has 5 tennis balls. He buys 2 more cans of tennis balls. 
            Each can has 3 tennis balls. How many tennis balls does he have now?
            
        """

prompt_messages = [ {"role": "user",  "content": query}]
            
response = query_llm(prompt_messages, temperature=0)
print(response['text'] )
# with CoT
query = """ Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can have 3 tennis balls. 
            How many tennis balls does he have now?
            Answer: Roger has 5 balls initially. 2 cans with 3 each balls means 5 + 2*3 = 11
            Now answer this question:
            John has 5 apples. He buys 2 more crates of apples, and each crate consists of a dozen apple. 
            How many apples does John has now?
        """

prompt_messages = [ {"role": "user",  "content": query}]
            
response = query_llm(prompt_messages, temperature=0)
print(response['text'] )
#Tree of Thought Prompting
query = """ You are a health insurance advisor evaluating the best plan for a patient.
            Question: Should a patient with chronic diabetes and hypertension be offered a standard health plan or a specialized chronic care plan?

            Think in multiple ways (Tree of Thought):
            1. Think based on cost-effectiveness.
            2. Think based on patient health outcomes and care coordination.
            3. Think based on long-term insurance risk and sustainability.

            Evaluate each path and provide a final recommendation with reasoning.
            Display a tree-structure with proper blocks to show the paths.
        """
prompt_messages = [ {"role": "user",  "content": query}]
            
response = query_llm(prompt_messages)
print(response['text'] )
# Stateful Communication
# Initialize the conversation history
prompt_messages = [
    {"role": "developer", "content": "You are a helpful assistant specialized in health insurance. Be clear and concise."}
]

def chat(user_input):
    # Add user message to conversation history
    prompt_messages.append({"role": "user", "content": user_input})
    
    # Get response from OpenAI
    query_llm(prompt_messages)

    # Extract assistant reply
    assistant_reply = response['text'] 
    
    # Add assistant reply to conversation history
    prompt_messages.append({"role": "assistant", "content": assistant_reply})
    
    return assistant_reply

# Simulate a multi-turn conversation
print("User: What does my health insurance cover?")
print("Assistant:", chat("What does my health insurance cover?"))

print("\nUser: What about dental procedures?")
print("Assistant:", chat("What about dental procedures?"))

print("\nUser: Do I need prior approval for a root canal?")
print("Assistant:", chat("Do I need prior approval for a root canal?"))


