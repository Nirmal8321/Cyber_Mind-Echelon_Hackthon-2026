from detectors.clip_aligner import get_alignment_score
from PIL import Image

from detectors.robustness import preprocess_for_robustness

def analyze_video_frames(frame_paths, user_text):
    scores = []
    for path in frame_paths:
        img = Image.open(path)
        # Apply the robustness filter to each frame to "de-blur"
        img = preprocess_for_robustness(img) 
        score = get_alignment_score(img, user_text)
        scores.append(score)
    
    # Use the MAXIMUM score instead of average
    # If even ONE frame clearly looks like a waterfall, it's likely real.
    best_score = max(scores) 
    return best_score