# llm_client.py - FIXED (using real LLM)
import openai 
from openai import OpenAI
import os

def get_llm_client():
    endpoint = "https://cdong1--azure-proxy-web-app.modal.run"
    api_key = "supersecretkey"  
    deployment_name = "gpt-4o"
    
    client = OpenAI(
        base_url=endpoint,
        api_key=api_key
    )
    
    return client, deployment_name