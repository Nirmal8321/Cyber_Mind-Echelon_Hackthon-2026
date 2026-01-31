import streamlit as st
from PIL import Image
import os

# Custom module imports
from detectors.clip_aligner import get_alignment_score
from core.explainer import generate_explanation
from detectors.robustness import preprocess_for_robustness
from detectors.video_utils import extract_frames

st.set_page_config(page_title="BUILDEDGE | Multi-Model Forensic AI", layout="wide")

st.title("🛡️ BUILDEDGE: Multi-Model Forensic Suite")
st.info("Decision Fusion: Integrating CLIP (Vision) + Gemini 3 (Logic)")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📤 Input Media")
    uploaded_file = st.file_uploader("Upload Image/Video", type=["jpg", "png", "jpeg", "mp4", "mov"])
    user_text = st.text_area("Context/Headline", placeholder="Enter the claim associated with this media...")
    use_robustness = st.checkbox("Enable Adversarial Filter", value=True)

if st.button("🚀 Run Multi-Model Analysis", use_container_width=True):
    if uploaded_file and user_text:
        # --- PHASE 1: Media Processing ---
        if uploaded_file.name.endswith(('.mp4', '.mov')):
            with open("temp_video.mp4", "wb") as f: f.write(uploaded_file.read())
            frames = extract_frames("temp_video.mp4", interval=1)
            image_to_analyze = Image.open(frames[len(frames)//2])
            with col2: st.video(uploaded_file)
        else:
            image_to_analyze = Image.open(uploaded_file)
            with col2: st.image(image_to_analyze, use_container_width=True)

        if use_robustness:
            image_to_analyze = preprocess_for_robustness(image_to_analyze)

        # --- PHASE 2: Multi-Model Decision Fusion ---
        with st.spinner("Calculating Multi-Model Scores..."):
            # Model 1: CLIP (Visual Alignment)
            clip_score = get_alignment_score(image_to_analyze, user_text)
            
            # Model 2: Gemini (Contextual Reasoning)
            gemini_score, reason = generate_explanation(user_text, clip_score)
            
            # FUSION LOGIC: 60% Vision + 40% Logic
            final_score = (clip_score * 0.6) + (gemini_score * 0.4)

        # --- PHASE 3: Calibrated Forensic Report ---
        with col2:
            st.divider()
            st.subheader("📊 Integrated Forensic Report")
            
            # Gauge Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("CLIP (Vision)", f"{clip_score:.1f}")
            c2.metric("Gemini (Logic)", f"{gemini_score:.1f}")
            c3.metric("FINAL SCORE", f"{final_score:.1f}/100")

            # Final Verdict
            if final_score < 25:
                st.error("🔴 VERDICT: HIGHLY SUSPICIOUS")
            elif 25 <= final_score < 35:
                st.warning("🟡 VERDICT: NEEDS VERIFICATION (Potential Motion/Context Gap)")
            else:
                st.success("🟢 VERDICT: HIGH CONFIDENCE MATCH")

            st.progress(min(final_score/100, 1.0))
            st.write(f"**Expert Analysis:** {reason}")
    else:
        st.error("Please provide both media and a caption.")