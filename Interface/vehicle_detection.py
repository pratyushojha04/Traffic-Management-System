import torch
import cv2
import warnings
import os

# Suppress warnings
warnings.filterwarnings('ignore')  # Ignore all warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings

def count_vehicles_in_video(video_path):
    # Load the YOLOv5 model (suppress logs)
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, verbose=False)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Initialize the vehicle count
    vehicle_count = 0

    # Iterate through the video frames without displaying the video
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # Break when no more frames are available

        # Perform vehicle detection on the current frame
        results = model(frame)
        detections = results.xywh[0]  # Get the detection results

        # Filter out only vehicles (YOLO classes for vehicles: car, truck, bus, motorcycle)
        for detection in detections:
            label = int(detection[5])  # Class ID
            if label in [2, 3, 5, 7]:  # YOLO class IDs for car, motorcycle, bus, truck
                vehicle_count += 1

    cap.release()
      # Release the video capture
    return vehicle_count
