import google.generativeai as genai
import streamlit as st
import re

# Specialist Agent Imports
from agents.consistency_agent import get_clip_score
from agents.ocr_agent import get_ocr_analysis
from agents.logic_agent import get_logical_verdict
from utils.forensic_logger import log_forensic_step

class MasterOrchestrator:
    def __init__(self):
        # Configure Gemini 3 Flash as the Master Reasoning Engine
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            self.master_model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            st.error(f"Master AI Configuration Error: {e}")

    def run_full_forensics(self, image, text):
        """
        Coordinates specialized agents and applies Weighted Decision Fusion.
        """
        # 1. Specialist: CLIP (Visual Alignment) - 30% Weight
        clip_score = get_clip_score(image, text)
        log_forensic_step("CLIP_AGENT", text, clip_score, "Visual alignment check complete.")

        # 2. Specialist: Llama 3.2-Vision (OCR Context) - 30% Weight
        ocr_score, ocr_report = get_ocr_analysis(image, text)
        log_forensic_step("OCR_AGENT", text, ocr_score, ocr_report)

        # 3. Specialist: DeepSeek (Logical Cross-Examination) - 40% Weight
        logic_score, logic_report = get_logical_verdict(text, clip_score, ocr_report)
        log_forensic_step("LOGIC_AGENT", text, logic_score, "Chain-of-thought logic complete.")

        # 4. Integrated Scoring (Fusion)
        # Weighting strategy: 30% Vision, 30% Context, 40% Thinking/Logic
        final_score = (clip_score * 0.3) + (ocr_score * 0.3) + (logic_score * 0.4)
        
        # 5. Master Synthesis: Gemini generates the final expert verdict
        master_prompt = f"""
        Analyze these forensic findings for the claim: "{text}"
        - CLIP Visual Score: {clip_score}/100
        - OCR Context Match: {ocr_score}/100
        - Logical Reasoning Summary: {logic_report}
        
        Provide a final, authoritative expert conclusion for the forensic report.
        """
        try:
            response = self.master_model.generate_content(master_prompt)
            reason = response.text
        except:
            # Fallback to the logic agent's findings if the Master AI hits a quota limit
            reason = logic_report 

        return {
            "final_score": final_score,
            "reports": {
                "Vision": clip_score,
                "Context": ocr_score,
                "Logic": logic_score
            },
            "reason": reason
        }

# Singleton instance to be called by app.py
orchestrator = MasterOrchestrator()