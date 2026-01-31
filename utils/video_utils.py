import cv2
import os

def extract_frames(video_path, interval=1):
    """
    Extracts frames from a video file at a set interval.
    Saves them to a 'temp_frames' folder inside the 'data' directory.
    """
    output_dir = "data/temp_frames"
    os.makedirs(output_dir, exist_ok=True)
    
    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval)
    
    count = 0
    success = True
    frame_paths = []

    while success:
        success, image = vidcap.read()
        if count % frame_interval == 0 and success:
            frame_name = f"frame_{count}.jpg"
            frame_path = os.path.join(output_dir, frame_name)
            cv2.imwrite(frame_path, image)
            frame_paths.append(frame_path)
        count += 1
        
    vidcap.release()
    return frame_paths