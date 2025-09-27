# structurer.py
import json
from llm_client import get_llm_client
from datetime import datetime

def blob_to_json(blob_text):
    client, deployment_name = get_llm_client()
    
    prompt = f"""
    ONLY use information from this text. Do not add outside knowledge.
    
    Extract Funko Pop information from this text and return JSON array.
    
    Text content:
    {blob_text}
    
    Return empty array [] if no products found.
    """
    
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": prompt}]
    )
    
    json_string = response.choices[0].message.content
    return json.loads(json_string)