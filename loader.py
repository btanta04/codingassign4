# loader.py
import json
import pandas as pd
import datetime
from supabase import create_client

def load_structured_json(path="data/structured.json"):
    """Load structured JSON from file"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_and_prepare_df(json_data):
    """Convert JSON to DataFrame and ensure schema matches Supabase table"""
    # Define expected columns matching your Supabase table
    expected_columns = [
        "id", "title", "price", "character", "variant", "rarity", 
        "estimated_value", "category", "image_url", "extracted_at", "source_url"
    ]
    
    # Create DataFrame with expected columns
    df = pd.DataFrame(json_data)
    
    # Ensure all expected columns exist
    for col in expected_columns:
        if col not in df.columns:
            df[col] = None
    
    # Select only the expected columns
    df = df[expected_columns]
    
    # Add updated_at timestamp (required by your table schema)
    df["updated_at"] = datetime.datetime.utcnow().isoformat()
    
    print(f"📊 Prepared DataFrame with {len(df)} rows and {len(df.columns)} columns")
    return df

def upsert_to_supabase(df, url, key):
    """Upsert DataFrame to Supabase table"""
    supabase = create_client(url, key)
    
    # Convert DataFrame to records
    records = df.to_dict(orient="records")
    
    # Upsert to funko_pops table
    response = supabase.table('funko_pops').upsert(records).execute()
    
    if response.data:
        print(f"✅ Successfully upserted {len(response.data)} records to Supabase")
    else:
        print("❌ Failed to upsert records")
    
    return response