import google.generativeai as genai
import streamlit as st
import re

def get_logical_verdict(text, clip_score, ocr_report):
    """
    FREE REPLACEMENT: Uses Gemini 1.5 Flash instead of paid DeepSeek.
    """
    # 1. Setup Gemini
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash') 
    
    # 2. The Logic Prompt
    prompt = f"""
    Analyze this forensic evidence for contradictions:
    - Claim: "{text}"
    - Vision Match: {clip_score}/100
    - OCR Context: {ocr_report}
    
    Return your verdict in this EXACT format:
    SCORE: [0-100]
    REASON: [Short explanation]
    """
    
    try:
        response = model.generate_content(prompt)
        result = response.text
        
        # 3. Extract results
        score_match = re.search(r"SCORE:\s*(\d+)", result)
        score = float(score_match.group(1)) if score_match else 70.0
        reason = result.split("REASON:")[1].strip() if "REASON:" in result else result
        
        return score, reason
    except Exception as e:
        # If this returns 50, it means the API itself failed
        return 50.0, f"Logic Agent Error: {str(e)}"