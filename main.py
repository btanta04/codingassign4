# main.py
from collector import scrape_funko_pops
from structurer import blob_to_json
from loader import clean_and_prepare_df, upsert_to_supabase
import json

def run_pipeline():
    print("🚀 Starting pipeline...")
    
    # 1. Collect data
    print("📥 Scraping...")
    blob_text = scrape_funko_pops()
    
    # 2. Structure with LLM
    print("🤖 Analyzing with LLM...")
    json_data = blob_to_json(blob_text)
    
    if json_data:
        # Save structured data
        with open('data/structured.json', 'w') as f:
            json.dump(json_data, f, indent=2)
        
        # 3. Load to Supabase
        print("📊 Converting to DataFrame...")
        df = clean_and_prepare_df(json_data)
        
        print("💾 Uploading to Supabase...")
        SUPABASE_URL = "https://duawsrbpkgwpytnyjkvu.supabase.co"
        SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR1YXdzcmJwa2d3cHl0bnlqa3Z1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg3MzUyNDcsImV4cCI6MjA3NDMxMTI0N30.R1a4zZGgtll2T7cvS_p9CQK4dDkZ8q0pUSsGAoedRig"
        
        response = upsert_to_supabase(df, SUPABASE_URL, SUPABASE_KEY)
        print("✅ Pipeline completed!")
        return True
    else:
        print("❌ Pipeline failed")
        return False

if __name__ == "__main__":
    run_pipeline()