# collector.py
import requests
from bs4 import BeautifulSoup
import os

def scrape_funko_pops():
    url = "https://funko.fandom.com/wiki/Pop!"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Just get the text content
        text = soup.get_text()
        blob_text = text[:3000]  # First 3000 chars
        
        # Save it
        os.makedirs('data', exist_ok=True)
        with open('data/raw_blob.txt', 'w', encoding='utf-8') as f:
            f.write(blob_text)
        
        return blob_text
        
    except Exception as e:
        print(f"Error: {e}")
        # Simple fallback
        return "Funko Pop vinyl figures information from wiki."

def save_raw_blob(blob_text):
    os.makedirs('data', exist_ok=True)
    with open('data/raw_blob.txt', 'w', encoding='utf-8') as f:
        f.write(blob_text)