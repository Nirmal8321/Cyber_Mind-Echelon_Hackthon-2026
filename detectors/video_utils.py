import cv2
import os

def extract_frames(video_path, interval=1):
    """
    Extracts frames from a video at a specific interval (e.g., every 1 second).
    Returns a list of image objects.
    """
    # Create a temporary directory for frames if it doesn't exist
    output_folder = "temp_frames"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    
    # Handle case where FPS might be 0 or invalid
    if fps <= 0: fps = 30 
    
    success, image = vidcap.read()
    count = 0
    saved_frame_paths = []
    
    while success:
        # Save frame every 'interval' seconds
        if count % int(fps * interval) == 0:
            frame_path = os.path.join(output_folder, f"frame_{count}.jpg")
            cv2.imwrite(frame_path, image)
            saved_frame_paths.append(frame_path)
            
        success, image = vidcap.read()
        count += 1
        
    vidcap.release()
    return saved_frame_paths