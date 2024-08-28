import cv2
import time
import torch

# Load YOLOv5 model for vehicle detection
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)  # Use YOLOv5s model
model.classes = [1, 2, 3, 5, 7]  # Include bicycles (1), cars (2), motorbikes (3), buses (5), and trucks (7)

cap = cv2.VideoCapture('static/WhatsApp Video 2024-08-25 at 6.29.14 PM.mp4')

# Initialize variables
start_time = time.time()
last_snapshot_time = start_time
snapshot_interval = 20  # Snapshot every 20 seconds
snapshot_counter = 0
total_vehicle_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    time_remaining = int(snapshot_interval - (current_time - last_snapshot_time))

    # Perform vehicle detection on the current frame
    results = model(frame)
    detections = results.pred[0]
    
    # Dictionary to count vehicles in the current snapshot
    vehicle_count_snapshot = 0

    # Draw bounding boxes and count vehicles
    for detection in detections:
        class_id = int(detection[5])
        if class_id in [1, 2, 3, 5, 7]:  # Vehicle classes
            vehicle_count_snapshot += 1
            bbox = detection[:4].cpu().numpy().astype(int)
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            cv2.putText(frame, 'Vehicle', (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Update total vehicle count only for the snapshot
    if current_time - last_snapshot_time >= snapshot_interval:
        last_snapshot_time = current_time
        snapshot_counter += 1

        # Save the snapshot with bounding boxes
        snapshot_filename = f'snapshot_{snapshot_counter}.jpg'
        cv2.imwrite(snapshot_filename, frame)
        total_vehicle_count += vehicle_count_snapshot
        print(f'Snapshot saved: {snapshot_filename}, Vehicle count: {vehicle_count_snapshot}')

    # Display vehicle counts and time remaining on the frame
    cv2.putText(frame, f'Vehicles: {vehicle_count_snapshot}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f'Time until next snapshot: {time_remaining}s', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Display the frame with bounding boxes
    cv2.imshow('Vehicle Detection', frame)

    # Exit on 'q' key press
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

# Release video capture object and close windows
cap.release()
cv2.destroyAllWindows()

# Print the total number of vehicles detected
print(f'Total vehicles detected: {total_vehicle_count}')
