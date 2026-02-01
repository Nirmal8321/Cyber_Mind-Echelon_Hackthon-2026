import google.generativeai as genai
import streamlit as st
import re

def get_logical_verdict(claim, clip_score, search_report, ocr_report):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Immediate penalty for 404 or critical technical failures
        if "404" in search_report or "failed" in search_report.lower():
            return 15.0, "Logical Red Flag: Core verification engine connection failed. Authenticity unverified."

        prompt = f"""
        Act as an Adversarial Auditor. 
        Analyze the consistency between this claim: "{claim}" and the evidence.
        Visual Evidence: CLIP score {clip_score}/100.
        Search Evidence: {search_report}.
        OCR Evidence: {ocr_report}.

        If the claim is absurd (e.g., Calling an image of ice cream an "Ancient Greek Artifact"),
        provide a very low score and explain the contradiction.

        Format: SCORE | CRITIQUE
        """
        
        response = model.generate_content(prompt)
        text = response.text
        
        # Improved parsing: Extract numerical score regardless of formatting
        score_match = re.search(r"(\d+)", text)
        score = float(score_match.group(1)) if score_match else 40.0
        
        # Improved parsing: Safely extract critique text
        report = text.split('|')[1].strip() if '|' in text else text
        
        return score, report
    except Exception as e:
        # Prevents the "Logic synchronization error" UI message
        return 20.0, f"Logic analysis bypassed due to parsing conflict: {str(e)}"