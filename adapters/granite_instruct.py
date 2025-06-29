"""Granite Instruct adapter for meeting request parsing."""

import json
import re
import os
import requests
from dotenv import load_dotenv
from config.prompt_template import meeting_prompt
load_dotenv()

API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
MODEL_ID = "ibm/granite-3-8b-instruct"

def get_iam_token():
    """Get IBM Cloud IAM token using API key."""
    api_key = os.getenv("WATSONX_API_KEY")
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception("Failed to obtain IAM token: " + response.text)
    return response.json()["access_token"]

def extract_first_json(text):
    """Extract the first JSON object from text using regex."""
    match = re.search(r'\{.*?\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            print("[!] JSON found but invalid:", match.group(0))
            return {}
    print("[!] No JSON object found in output")
    return {}

def parse_meeting_request(request: str):
    """Parse natural language meeting request using Granite model."""
    token = get_iam_token()
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    prompt = meeting_prompt.format(request=request)
    payload = {
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 200,
            "min_new_tokens": 0,
            "repetition_penalty": 1
        },
        "model_id": MODEL_ID,
        "project_id": PROJECT_ID,
        "moderations": {
            "hap": {
                "input": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                },
                "output": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                }
            },
            "pii": {
                "input": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                },
                "output": {
                    "enabled": True,
                    "threshold": 0.5,
                    "mask": {
                        "remove_entity_value": True
                    }
                }
            },
            "granite_guardian": {
                "input": {
                    "threshold": 1
                }
            }
        }
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        raise Exception("API call failed: " + str(response.text))
    
    output_text = response.json()["results"][0]["generated_text"]

    parsed = extract_first_json(output_text)

    required_keys = ["participants", "date", "time", "topic"]
    for key in required_keys:
        if key not in parsed:
            raise KeyError(f"Missing key in parsed output: {key}")
    return parsed


