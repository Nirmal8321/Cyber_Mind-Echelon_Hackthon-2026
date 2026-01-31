import google.generativeai as genai
import streamlit as st
import time
import random
import re

def generate_explanation(text, clip_score):
    """
    Analyzes visual forensic data and context using Gemini 3 Flash.
    Includes decision fusion (score extraction) and rate-limit retry logic.
    """
    # Fetch the API key securely from Streamlit Secrets
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except KeyError:
        return 50.0, "Error: GEMINI_API_KEY not found in Streamlit secrets."

    genai.configure(api_key=api_key)
    
    # Using Gemini 3 Flash Preview (Latest 2026 Model)
    model = genai.GenerativeModel('gemini-2.5-flash-lite') 
    
    prompt = f"""
    You are an AI Misinformation Expert. Analyze the following forensic data:
    - User Caption: "{text}"
    - CLIP Visual Alignment Score: {clip_score}/100
    
    Task: 
    1. Provide a 'Gemini Logic Score' (0 to 100) where 100 is perfectly authentic and 0 is complete misinformation. 
       (Consider if the text sounds like typical 'clickbait' or if it logically matches a {clip_score} visual score).
    2. Provide a concise human-readable reason.

    YOU MUST FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
    SCORE: [number]
    REASON: [your explanation]
    """
    
    # --- Exponential Backoff Retry Logic for 429 Quota Errors ---
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            content = response.text
            
            # Use Regex to safely extract the score and reason
            # This 'shield' prevents errors if the AI adds extra conversational text.
            score_match = re.search(r"SCORE:\s*(\d+\.?\d*)", content)
            gemini_score = float(score_match.group(1)) if score_match else 50.0
            
            reason_match = re.search(r"REASON:\s*(.*)", content, re.DOTALL)
            reason = reason_match.group(1).strip() if reason_match else "Analysis complete."
            
            return gemini_score, reason

        except Exception as e:
            # Check for Rate Limit (429) or Overloaded (503) errors
            if "429" in str(e) or "503" in str(e):
                wait_time = (2 ** attempt) + random.uniform(0, 1) # Exponential wait with jitter
                st.warning(f"Rate limit hit. Retrying in {wait_time:.1f}s...")
                time.sleep(wait_time)
            else:
                return 50.0, f"Forensic analysis failed: {str(e)}"
    
    return 50.0, "Error: Max retries exceeded. Please wait a minute and try again."