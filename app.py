import streamlit as st
from supabase import create_client
import pandas as pd

SUPABASE_URL = "https://duawsrbpkgwpytnyjkvu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR1YXdzcmJwa2d3cHl0bnlqa3Z1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg3MzUyNDcsImV4cCI6MjA3NDMxMTI0N30.R1a4zZGgtll2T7cvS_p9CQK4dDkZ8q0pUSsGAoedRig"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
data = supabase.table("funko_pops").select("*").execute().data
df = pd.DataFrame(data)

st.title("Funko Pop Wiki")
st.dataframe(df)

if "image_url" in df.columns:
    st.image(df["image_url"].dropna().tolist(), width=150)
if "rarity" in df.columns:
    st.bar_chart(df["rarity"].value_counts())
if "estimated_value" in df.columns:
    st.write("Estimated Value Distribution")
    st.bar_chart(df["estimated_value"].value_counts())