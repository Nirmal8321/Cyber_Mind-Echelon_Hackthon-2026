# detectors/robustness.py
import cv2
import numpy as np
from PIL import Image

def preprocess_for_robustness(image):
    # Convert PIL Image to a NumPy array for OpenCV
    img_array = np.array(image)
    # Apply Bilateral Filter to reduce noise while keeping edges sharp
    cleaned = cv2.bilateralFilter(img_array, 9, 75, 75)
    # Convert back to PIL format for compatibility with other models
    return Image.fromarray(cleaned)