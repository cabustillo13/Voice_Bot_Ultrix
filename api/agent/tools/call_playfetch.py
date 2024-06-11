import requests
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()


def call_llm(url, data):
    """Calling LLM on Playfetch"""

    headers = {
        "x-api-key": os.getenv("PLAYFETCH_API_KEY"),
        "x-environment": "production",
        "content-type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=data)
    output = response.json()["output"]
    
    return output
