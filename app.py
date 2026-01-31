import streamlit as st
from PIL import Image
import os
from core.orchestrator import orchestrator
from utils.video_utils import extract_frames
from utils.report_gen import generate_pdf_report

# --- UI Configuration ---
st.set_page_config(page_title="BUILDEDGE | Multi-Agent Forensic AI", layout="wide")
st.title("🛡️ BUILDEDGE: Multi-Agent Forensic Suite")
st.info("Echelon Hackathon 2026 | Decision Fusion: CLIP + Llama + Gemini")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📤 Input Media")
    uploaded_file = st.file_uploader("Upload Image/Video", type=["jpg", "png", "jpeg", "mp4", "mov"])
    user_text = st.text_area("Context/Headline", placeholder="Enter the claim associated with this media...")
    
if st.button("🚀 Start Multi-Agent Forensic Scan", use_container_width=True):
    if uploaded_file and user_text:
        # 1. Media Pre-processing
        if uploaded_file.name.endswith(('.mp4', '.mov')):
            with open("temp_video.mp4", "wb") as f: f.write(uploaded_file.read())
            frames = extract_frames("temp_video.mp4", interval=1)
            image_to_analyze = Image.open(frames[len(frames)//2])
            with col2: st.video(uploaded_file)
        else:
            image_to_analyze = Image.open(uploaded_file)
            with col2: st.image(image_to_analyze, use_container_width=True)

        # 2. Master Orchestration
        with st.spinner("Master AI is coordinating specialized agents..."):
            results = orchestrator.run_full_forensics(image_to_analyze, user_text)

        # 3. Results Display
        with col2:
            st.divider()
            st.subheader("📊 Integrated Forensic Scorecard")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Vision (CLIP)", f"{results['reports']['Vision']:.1f}")
            m2.metric("Context (OCR)", f"{results['reports']['Context']:.1f}")
            m3.metric("Logic (Thinking)", f"{results['reports']['Logic']:.1f}")

            st.write(f"### Final Confidence: **{results['final_score']:.1f}/100**")
            st.progress(min(results['final_score']/100, 1.0))

            if results['final_score'] < 25:
                st.error("🔴 VERDICT: HIGHLY SUSPICIOUS")
            elif 25 <= results['final_score'] < 35:
                st.warning("🟡 VERDICT: NEEDS VERIFICATION")
            else:
                st.success("🟢 VERDICT: HIGH CONFIDENCE MATCH")

            st.info(f"**Master AI Reasoning:**\n\n{results['reason']}")
            
            # PDF Report Export
            pdf_bytes = generate_pdf_report(results, user_text)
            st.download_button("📥 Download Official Forensic Report (PDF)", pdf_bytes, "Forensic_Report.pdf", "application/pdf")
    else:
        st.error("Missing input data.")