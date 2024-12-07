import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose

def extract_landmarks(video_path):
    cap = cv2.VideoCapture(video_path)
    landmarks_all_frames = []

    # Set up the Pose estimation model
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to RGB, as MediaPipe works with RGB images
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame for pose estimation
            results = pose.process(rgb_frame)

            # If pose landmarks are detected
            if results.pose_landmarks:
                landmarks_frame = []
                for landmark in results.pose_landmarks.landmark:
                    landmarks_frame.append([landmark.x, landmark.y, landmark.z])
                landmarks_all_frames.append(landmarks_frame)

    cap.release()
    return np.array(landmarks_all_frames)

# Extract landmarks from two videos
landmarks_clip1 = extract_landmarks('Final Clips/PKClips00001099R.mp4')  # Replace with your video paths
landmarks_clip2 = extract_landmarks('Final Clips/PKClips00001099R.mp4')
print(landmarks_clip1.shape, landmarks_clip2.shape)
print(landmarks_clip1)
# Select a frame to compare (e.g., first frame for simplicity)
frame_idx = 0
pose1 = landmarks_clip1[frame_idx]
pose2 = landmarks_clip2[frame_idx]

# Convert landmarks to pixel coordinates (for better visualization)
def normalize_to_pixel_coords(landmarks, image_width, image_height):
    return np.array([[int(lm[0] * image_width), int(lm[1] * image_height)] for lm in landmarks])

# Create a blank image for drawing the poses (800x800 pixel canvas)
canvas = np.ones((800, 800, 3), dtype=np.uint8) * 255

# Define connections between landmarks for plotting
mp_connections = mp_pose.POSE_CONNECTIONS

# Drawing function for the pose on the canvas
def draw_pose(pose_2d, color, canvas):
    # Draw landmarks as circles
    for point in pose_2d:
        cv2.circle(canvas, tuple(point), 5, color, -1)

    # Draw connections as lines
    for connection in mp_connections:
        start_idx = connection[0]
        end_idx = connection[1]
        cv2.line(canvas, tuple(pose_2d[start_idx]), tuple(pose_2d[end_idx]), color, 2)

# Get canvas size
canvas_height, canvas_width, _ = canvas.shape

# Normalize both poses to fit the canvas size
pose1_2d = normalize_to_pixel_coords(pose1, canvas_width, canvas_height)
pose2_2d = normalize_to_pixel_coords(pose2, canvas_width, canvas_height)

# Draw the first pose in red
draw_pose(pose1_2d, (0, 0, 255), canvas)

# Draw the second pose in blue
draw_pose(pose2_2d, (255, 0, 0), canvas)

# Show the image with the two poses
cv2.imshow('Pose Comparison', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()

