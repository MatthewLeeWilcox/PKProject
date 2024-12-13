import cv2
import mediapipe as mp

# Initialize MediaPipe holistic
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Initialize Video Capture (webcam or video file)
cap = cv2.VideoCapture("../")  # Change 0 to your video file path if needed

# Set up the video writer to save the output as an MP4 file
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Specify the codec
out = cv2.VideoWriter('../Cut Clips Renamed/PKClips00000180R.mp4', fourcc, 30.0, (640, 480))  # Adjust the frame size as needed

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame for a mirror effect
        frame = cv2.flip(frame, 1)

        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False

        # Process the frame
        results = holistic.process(rgb_frame)

        # Convert RGB back to BGR
        rgb_frame.flags.writeable = True
        frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

        # Check if any landmarks are detected
        if results.pose_landmarks:
            # Get the bounding box coordinates from landmarks
            x_min, y_min = float('inf'), float('inf')
            x_max, y_max = -float('inf'), -float('inf')

            # Loop through the pose landmarks
            for landmark in results.pose_landmarks.landmark:
                x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                x_min, y_min = min(x_min, x), min(y_min, y)
                x_max, y_max = max(x_max, x), max(y_max, y)

            # Draw the bounding box around the person
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(frame, 'Person Detected', (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Write the frame to the video file
        out.write(frame)

        # Display the frame with bounding boxes
        cv2.imshow('MediaPipe Bounding Box', frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture and writer objects
cap.release()
out.release()
cv2.destroyAllWindows()
