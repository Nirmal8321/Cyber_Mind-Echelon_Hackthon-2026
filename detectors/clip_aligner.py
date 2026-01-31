import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image

# Load model once to save time
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def get_alignment_score(image, text):
    """Returns a similarity score between 0 and 100."""
    inputs = processor(text=[text], images=image, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Cosine similarity
    logits_per_image = outputs.logits_per_image 
    score = logits_per_image.item()
    return round(score, 2)