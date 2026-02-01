import google.generativeai as genai
import streamlit as st
from agents.consistency_agent import get_clip_score
from agents.ocr_agent import get_ocr_analysis
from agents.logic_agent import get_logical_verdict
from agents.search_agent import get_search_context 

class MasterOrchestrator:
    def __init__(self):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            # Standardizing on Gemini 2.5 Flash for 2026 stable performance
            self.master_model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            st.error(f"Master AI Configuration Error: {e}")

    def run_full_forensics(self, image, text, image_url=None):
        """
        Coordinates specialized agents and applies Balanced Weighted Fusion.
        Ensures resilience against system failures and extreme claim mismatches.
        """
        # 1. Specialist Agent Execution
        clip_score = get_clip_score(image, text)
        ocr_score, ocr_report = get_ocr_analysis(image, text)
        
        # Ground Truth check: Avoids neutral 50-score fallback if hosting fails
        if not image_url:
            search_score, search_report = 25.0, "Reverse image search unavailable: No Public URL provided."
        else:
            search_score, search_report = get_search_context(image_url, text)

        # Logic Agent Execution (weighted at 10% to prevent overconfident AI speculation)
        logic_score, logic_report = get_logical_verdict(text, clip_score, search_report, ocr_report)

        # 2. Weighted Fusion Calculation
        # Prioritizes Ground Truth (40%) and Visual Alignment (30%)
        final_score = (search_score * 0.4) + (clip_score * 0.3) + (ocr_score * 0.2) + (logic_score * 0.1)
        
        # 3. Master Synthesis: Expert verdict generation for the Clean UI
        master_prompt = f"""
        Analyze this claim: "{text}" 
        Forensic findings show: Vision Match ({clip_score}/100), Search context ({search_report}), OCR data ({ocr_report}), and Logic critique ({logic_report}).

        Even if the claim is highly contradictory to the visual evidence (e.g., calling ice cream an artifact), 
        maintain a professional tone and provide a clear logical breakdown.

        Response Format EXACTLY:
        SUMMARY: [Provide a concise 2-sentence verdict summary]
        MASTER EXPLAINER: [Provide a detailed bulleted logical breakdown of the evidence]
        """
        
        try:
            response = self.master_model.generate_content(master_prompt)
            reason = response.text
        except:
            # High-resilience fallback if synthesis fails
            reason = f"SUMMARY: Audit completed with an authenticity index of {final_score:.1f}%. \nMASTER EXPLAINER: {logic_report}"

        return {
            "final_score": final_score,
            "reports": {
                "Vision": clip_score, 
                "Context": ocr_score, 
                "Ground Truth": search_score, 
                "Logic": logic_score
            },
            "reason": reason
        }

orchestrator = MasterOrchestrator()