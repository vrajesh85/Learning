import pandas as pd
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

# Give appropriate file path
filepath = 'Data/SentimentAnalysis/Patient_Reviews.csv'
reviews = pd.read_csv(filepath)
reviews.head()

# Extract the first row
review = reviews['review_text'][0]
print(review)

# Wrap the text to readable window width
print("\n".join(textwrap.wrap(review, width=80)))

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

query = """ You are an assistant that analyses customer reviews and identify sentiment. \
            The sentiment can be positive, negative or neutral.\
            Make sure to return the output using the following sample format. \
            {"sentiment": "positive", "confidence": 0.9} \
            The confidence should be a float between 0 and 1.
      """

prompt_messages = [
    {"role": "developer", "content": query},
    {"role": "user", "content": f"Patient review text:\n\n{review}"}
]
response = query_llm(prompt_messages)
print(response['text'])

query  = """ You are a sentiment analysis expert. Please analyze the following text and return a detailed JSON response with the following fields:
            - "sentiment_label": a string "positive", "negative", or "neutral" representing the overall sentiment.
            - "confidence_score": a numeric value between 0 and 1 indicating how confident you are in your sentiment classification.
            - "emotions": an array with the name of the detected emotions (e.g., "joy", "anger", "sadness", "surprise", "fear").
            Return the response in valid JSON format. Do not include the keyword json in the output

        """
prompt_messages = [
    {"role": "developer", "content": query},
    {"role": "user", "content": f"Patient review text:\n\n{review}"}
]

response = query_llm(prompt_messages)
print(response['text'])

results = []
for review in reviews['review_text'].head(3):
    prompt_messages = [
        {"role": "developer", "content": query},
        {"role": "user", "content": f"Patient review text:\n\n{review}"}
    ]
   
    response = query_llm(prompt_messages)
    results.append(response['text'])

# display the results
results

# create a proper list of the output using list-comprehension
results_dict = [json.loads(result) for result in results]
results_dict

# convert the results into dataframe format
df = pd.DataFrame(results_dict)
df

# import the required packages
from pydantic import BaseModel, Field
from typing import List

# create a class defining the attributes that we need in the structured output
# this is known as pydantic model
class SentimentOutput(BaseModel):
    sentiment_label: str = Field(..., description="A string ('positive', 'negative', or 'neutral')")
    confidence_score: float = Field(..., description="A value between 0 and 1")
    emotions: List[str]

# use the previous generated parsed JSON values to model as per the pydantic model created

final_result=[]
for i in range(len(results_dict)):
    validated_response = SentimentOutput(**results_dict[i])   # passing one row at a time
    final_result.append(validated_response.dict())

final_result

# convert to dataframe
df_results = pd.DataFrame(final_result)
df_results

