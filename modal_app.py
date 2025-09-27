# modal_app.py
import modal

app = modal.App("funko-pop-analyzer")

image = modal.Image.debian_slim().pip_install(
    "streamlit",
    "pandas", 
    "supabase",
    "plotly",
    "requests",
    "beautifulsoup4",
    "openai",
    "python-dotenv"
)

@app.function(image=image)
@modal.web_server(8000)
def run_streamlit():
    import subprocess
    subprocess.run([
        "streamlit", "run", "app.py",
        "--server.port=8000", 
        "--server.address=0.0.0.0"
    ])