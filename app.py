import streamlit as st
from PIL import Image
from detectors.clip_aligner import get_alignment_score
from core.explainer import generate_explanation

st.set_page_config(page_title="🛡️ Echelon Misinfo Detector", layout="wide")

st.title("🛡️ Multi-Modal Misinformation Detector")
st.markdown("Detecting cross-modal inconsistencies and AI-generated content.")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    user_text = st.text_area("Enter Caption/News Text")

if st.button("Analyze Content"):
    if uploaded_file and user_text:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=400)
        
        with st.spinner('Analyzing...'):
            # 1. Run CLIP Alignment
            score = get_alignment_score(image, user_text)
            
            # 2. Get Explanation
            explanation = generate_explanation(user_text, score)
            
        # 3. Display Results
        st.subheader("Analysis Results")
        
        # Color coding the score
        if score < 18:
            st.error(f"⚠️ High Inconsistency Detected (Score: {score})")
        else:
            st.success(f"✅ Content Appears Aligned (Score: {score})")
            
        st.info(f"**Expert Explanation:**\n\n{explanation}")
    else:
        st.warning("Please upload both an image and text.")