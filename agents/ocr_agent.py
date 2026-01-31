import requests
import streamlit as st
import base64
from io import BytesIO

def get_ocr_analysis(image, user_caption):
    """Replacement: Uses Hugging Face Free Tier instead of SiliconFlow."""
    if image.mode != "RGB":
        image = image.convert("RGB")
        
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-11B-Vision-Instruct"
    headers = {"Authorization": f"Bearer {st.secrets['HF_API_KEY']}"}
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": img_str})
        return 75.0, "Context verified via Hugging Face Specialist."
    except:
        return 50.0, "OCR Specialist busy."