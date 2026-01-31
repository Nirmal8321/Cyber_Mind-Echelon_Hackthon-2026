import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# Load model once to save memory
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def get_clip_score(image, text):
    """Specialist task: Measure how well the image matches the caption."""
    try:
        inputs = processor(text=[text], images=image, return_tensors="pt", padding=True)
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)
        
        # Scale to 0-100 for our dashboard
        score = logits_per_image.item()
        normalized_score = max(0, min(100, score * 2.5)) 
        return normalized_score
    except Exception:
        return 25.0 # Default fallback