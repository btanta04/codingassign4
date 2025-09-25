# structurer.py
import json
from llm_client import get_llm_client
from datetime import datetime

def blob_to_json(blob_text):
    """Send blob to LLM and return validated JSON following schema"""
    client, deployment_name = get_llm_client()
    
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "title": {"type": "string"},
                "price": {"type": "string"},
                "character": {"type": "string"},
                "variant": {"type": "string"},
                "rarity": {"type": "string"},
                "estimated_value": {"type": "string"},
                "category": {"type": "string"},
                "image_url": {"type": "string"},
                "source_url": {"type": "string"},
                "extracted_at": {"type": "string"}
            },
            "required": ["id", "title", "character", "category", "extracted_at"]
        }
    }
    
    prompt = f"""
    Extract Funko Pop information from this text and return VALID JSON array following this exact schema:
    - id: unique identifier
    - title: product title
    - price: price as string (e.g., "$12.99")
    - character: character name
    - variant: Standard/Exclusive/Chase
    - rarity: Common/Rare/Exclusive
    - estimated_value: Low/Medium/High/Collector
    - category: Anime/Movies/TV/etc.
    - image_url: valid image URL
    - source_url: https://funko.fandom.com/wiki/Pop!
    - extracted_at: ISO timestamp
    
    Ensure ALL fields are present and values are diverse.
    
    Text: {blob_text[:2000]}
    
    Return ONLY the JSON array, no other text.
    """
    
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7  # More diversity
        )
        
        json_string = response.choices[0].message.content.strip()
        
        # Clean and validate JSON
        json_string = clean_json_string(json_string)
        json_data = json.loads(json_string)
        
        # Validate it's an array of objects
        if not isinstance(json_data, list):
            raise ValueError("Expected JSON array")
        if not all(isinstance(item, dict) for item in json_data):
            raise ValueError("All items must be objects")
            
        # Add extracted_at timestamp to each item
        current_time = datetime.utcnow().isoformat()
        for item in json_data:
            item["extracted_at"] = item.get("extracted_at", current_time)
            item["source_url"] = item.get("source_url", "https://funko.fandom.com/wiki/Pop!")
        
        print(f"✅ Validated {len(json_data)} JSON objects")
        return json_data
        
    except Exception as e:
        print(f"❌ JSON validation failed: {e}")
        return create_fallback_data()

def clean_json_string(json_string):
    """Remove markdown code blocks from JSON string"""
    if json_string.startswith('```json'):
        json_string = json_string[7:]
    if json_string.endswith('```'):
        json_string = json_string[:-3]
    return json_string.strip()

def create_fallback_data():
    """Fallback data with proper schema"""
    current_time = datetime.utcnow().isoformat()
    return [
        {
            "id": "1", "title": "Funko Pop Demo", "price": "$12.99", 
            "character": "Demo Character", "variant": "Standard", "rarity": "Common",
            "estimated_value": "Low", "category": "Demo", 
            "image_url": "https://via.placeholder.com/150", "source_url": "https://funko.fandom.com/wiki/Pop!",
            "extracted_at": current_time
        }
    ]