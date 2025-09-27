# streamlit_app.py
import streamlit as st
import pandas as pd
from supabase import create_client
import plotly.express as px
import plotly.graph_objects as go

@st.cache_resource
def init_supabase():
    return create_client(
        ["https://duawsrbpkgwpytnyjkvu.supabase.co"],
        ["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR1YXdzcmJwa2d3cHl0bnlqa3Z1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg3MzUyNDcsImV4cCI6MjA3NDMxMTI0N30.R1a4zZGgtll2T7cvS_p9CQK4dDkZ8q0pUSsGAoedRig"]
    )

def get_funko_pops():
    supabase = init_supabase()
    response = supabase.table('funko_pops').select('*').order('extracted_at', desc=True).execute()
    return pd.DataFrame(response.data)

# Streamlit app
st.set_page_config(page_title="Funko Pop Variety", layout="wide")
st.title("Funko Pop Wiki - Variety Editions")

# Fetch data
df = get_funko_pops()

if not df.empty:
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Pops", len(df))
    with col2:
        st.metric("Unique Characters", df['character'].nunique())
    with col3:
        avg_price = df['price_numeric'].mean() if 'price_numeric' in df.columns else 0
        st.metric("Average Price", f"${avg_price:.2f}")
    with col4:
        st.metric("Rarest", df['rarity'].mode().iloc[0] if not df['rarity'].mode().empty else "N/A")
    
    # Latest products table
    st.subheader("Funko Pops")
    display_cols = ['title', 'character', 'variant', 'rarity', 'price', 'estimated_value']
    st.dataframe(df[display_cols].head(15))
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Characters Distribution")
        char_counts = df['character'].value_counts()
        fig = px.pie(values=char_counts.values, names=char_counts.index, 
                    title="Funko Pops by Character")
        st.plotly_chart(fig)
    
    with col2:
        st.subheader("Rarity Analysis")
        rarity_counts = df['rarity'].value_counts()
        fig = px.bar(x=rarity_counts.index, y=rarity_counts.values,
                    title="Pops by Rarity", color=rarity_counts.index)
        st.plotly_chart(fig)
    
    # Price analysis
    if 'price_numeric' in df.columns:
        st.subheader("Price Distribution")
        fig = px.box(df, y='price_numeric', x='rarity', 
                    title="Price by Rarity Level", color='rarity')
        st.plotly_chart(fig)
    
    # Character value analysis
    st.subheader("Character Value Analysis")
    if 'price_numeric' in df.columns and 'character' in df.columns:
        char_avg_prices = df.groupby('character')['price_numeric'].mean().sort_values(ascending=False)
        fig = px.bar(x=char_avg_prices.index, y=char_avg_prices.values,
                    title="Average Price by Character")
        st.plotly_chart(fig)

else:
    st.info("No Funko Pop data available. Run the pipeline first.")
    
    # Show sample of what the LLM will analyze
    st.subheader("What we'll analyze from funko.com:")
    st.write("""
    - Character identification (Tanjiro, Nezuko, Zenitsu, Inosuke, etc.)
    - Variant types (Standard, Chase, Exclusive, Special Edition)
    - Rarity classification based on pricing and availability
    - Estimated collector value
    - Price trends and distributions
    """)