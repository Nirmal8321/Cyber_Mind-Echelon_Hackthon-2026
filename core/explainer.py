import google.generativeai as genai
import os

def generate_explanation(text, clip_score, context_info="No previous records found."):
    genai.configure(api_key="AIzaSyDu6pvkYc0IswdC8iLfGHV1pNHovCHPWIM")
    # Try the newer, more stable alias for 2026
    model = genai.GenerativeModel('gemini-3-flash-preview')
    
    prompt = f"""
    You are an AI Misinformation Expert. Analyze the following data:
    - User Caption: "{text}"
    - CLIP Alignment Score: {clip_score}/100 (Higher is better)
    - Context Research: {context_info}
    
    Task: Provide a 3-sentence verdict. 
    1. State if it's likely "Authentic" or "Misinformation".
    2. Explain the cross-modal consistency based on the score.
    3. Cite the context evidence.
    """
    
    response = model.generate_content(prompt)
    return response.text