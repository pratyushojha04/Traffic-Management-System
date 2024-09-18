import cv2
import numpy as np
from tensorflow.keras.models import load_model # type: ignore


def detect_ambulance_in_video(video_path, threshold=0.2):
    """
    Detects if there is any ambulance in the video.

    :param video_path: Path to the video file
    :param model_path: Path to the trained model file
    :param threshold: Confidence threshold for detecting an ambulance
    :return: True if any ambulance is detected, False otherwise
    """
    # Load the trained model
    model = load_model('Interface/mlmodels/best_model.h5')
    
    # Define the video capture object
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return False
    
    # Define the expected input size for the model
    input_size = (128, 128)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Resize and preprocess the frame for the model
        resized_frame = cv2.resize(frame, input_size)
        resized_frame = resized_frame.astype('float32') / 255.0
        resized_frame = np.expand_dims(resized_frame, axis=0)
        
        # Predict using the model
        prediction = model.predict(resized_frame)
        confidence = prediction[0][0]
        
        # Check if the prediction indicates an ambulance
        if confidence > threshold:
            cap.release()  # Release the video capture object
            return True
    
    cap.release()  # Release the video capture object
    return False



