import cv2
import numpy as np
from tensorflow.keras.models import load_model
import time

# Load the trained model
model = load_model('best_model.h5')

# Define the video capture object
cap = cv2.VideoCapture('static/WhatsApp Video 2024-08-25 at 6.29.14 PM.mp4')  # Replace with your video file path

# Initialize variables
ambulance_count = 0
snapshot_interval = 10  # Time interval between snapshots in seconds
last_snapshot_time = time.time()
last_snapshot_count = 0  # Store count from last snapshot

# Define the expected input size for the model
input_size = (128, 128)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    time_left = int(snapshot_interval - (current_time - last_snapshot_time))

    # Display the ambulance count from the last snapshot and time left for the next snapshot
    cv2.putText(frame, f'Last Snapshot Count: {last_snapshot_count}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f'Time Left for Next Snapshot: {time_left}s', (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Ambulance Detection', frame)

    # Take a snapshot every 'snapshot_interval' seconds
    if current_time - last_snapshot_time >= snapshot_interval:
        # Resize and preprocess the frame for the model
        snapshot_frame = cv2.resize(frame, input_size)  # Resize to match model input size
        snapshot_frame = snapshot_frame.astype('float32') / 255.0  # Normalize pixel values
        snapshot_frame = np.expand_dims(snapshot_frame, axis=0)  # Add batch dimension

        # Predict using the model
        prediction = model.predict(snapshot_frame)

        confidence = prediction[0][0]
        print(f"Prediction: {prediction}")  # Debugging line to see the raw output

        # Check if the prediction indicates an ambulance
        if confidence > 0.2:  # Lowered the threshold for better detection
            print(f"Ambulance detected with {confidence * 100:.2f}% confidence!")  # Debugging line

            # Create a bounding box around the detected ambulance
            height, width, _ = frame.shape
            bbox = (int(width * 0.1), int(height * 0.1), int(width * 0.8), int(height * 0.8))
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 0, 255), 2)
            cv2.putText(frame, f'Ambulance: {confidence * 100:.2f}%', (bbox[0], bbox[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Increment the count only when adding a new detection
            ambulance_count += 1

        last_snapshot_count = ambulance_count  # Update last snapshot count
        last_snapshot_time = current_time  # Reset the snapshot timer

    # Adjust the delay to match a typical frame rate (e.g., 33 ms for 30 fps)
    if cv2.waitKey(33) & 0xFF == ord('q'):  # 33 ms delay for 30 fps
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()

# Print the total number of ambulances detected
print(f'Total ambulances detected: {ambulance_count}')
