from serpapi import GoogleSearch
import google.generativeai as genai
import streamlit as st
import re

def get_search_context(image_url, user_claim):
    # LOCAL IMPORT to break circular dependency
    from core.orchestrator import orchestrator 

    if not image_url or "None" in str(image_url):
        return 30.0, "Search Skip: No public URL available."

    params = {
        "engine": "google_reverse_image",
        "image_url": image_url,
        "api_key": st.secrets["SERPAPI_KEY"]
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        image_results = results.get('image_results', [])
        snippets = [res.get('snippet', '') for res in image_results[:3]]
        combined_snippets = " | ".join(snippets) if snippets else "No web matches."

        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"Claim: {user_claim} | Web Findings: {combined_snippets}. Score 0-100 and explain."
        
        response = model.generate_content(prompt)
        score_match = re.search(r"(\d+)", response.text)
        score = float(score_match.group(1)) if score_match else 50.0
        
        return score, response.text
    except Exception as e:
        return 30.0, f"Search failure: {str(e)}"