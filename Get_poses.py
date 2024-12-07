import re
import cv2
import mediapipe as mp
import pandas as pd


def get_label(string):
    match = re.search(r'PKClips(\d+)([A-Za-z])', string)

    if match:
        number = match.group(1)  # Extract '00000129'
        label = match.group(2)   # Extract 'L'
        return number, label

def get_pose_df(file_path, frame_flip = False,  show_img = False):
    # Initialize MediaPipe Pose and Drawing utilities
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    # Open a video file (replace 'your_video.mp4' with the path to your video)
    cap = cv2.VideoCapture(file_path)  # Use 0 for webcam or provide the video file path

    # Check if the video was opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    # Create an empty list to store the data
    pose_data = []

    # Use MediaPipe Pose
    with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.7) as pose:
        frame_num = 0
        while cap.isOpened():
            success, image = cap.read()

            # Break the loop if the video has ended (i.e., no more frames to read)
            if not success:
                print("Video ended or cannot be read.")
                break

            if frame_flip == True:
                image = cv2.flip(image, 1)
            
            # Convert the image color (OpenCV uses BGR, MediaPipe uses RGB)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Perform pose detection
            result = pose.process(image_rgb)

            # Draw pose landmarks on the frame
            if result.pose_landmarks:
                mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # Extract and save pose landmarks
                for idx, landmark in enumerate(result.pose_landmarks.landmark):
                    pose_data.append([frame_num, idx, landmark.x, landmark.y, landmark.z, landmark.visibility])

            # Display the frame with pose landmarks
            if show_img == True:
                cv2.imshow('Pose Estimation', image)

            # Exit loop by pressing 'q'
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

            frame_num += 1

    # Release the capture and close the windows
    cap.release()
    cv2.destroyAllWindows()


 
    print(file_path)
    labs = get_label(file_path)
    # Convert the collected data into a DataFrame
    df = pd.DataFrame(pose_data, columns=['frame', 'landmark', 'x', 'y', 'z', 'visibility'])
    df = df[df['landmark']>10]
    
    if frame_flip == True:
        if labs[1] == "R":
            df['shot_loc'] = "L"
        elif labs[1] == "L":
            df['shot_loc'] = "R"
        else:
            df['shot_loc'] = labs[1]
    else:
        df['shot_loc'] = labs[1]
    df['clip'] = labs[0]
    df['frame_modified'] = df['frame'] - min(df['frame'])
    # Now you can work with the DataFrame
    # print(df.head())

    return df



file_name = 'PkClips00000178R.mp4'
import os

all_pose_dfs = []

for file in os.listdir("TestClips"):
    print(file)
    pose_df = get_pose_df("TestClips/"+file, show_img= True)
    all_pose_dfs.append(pose_df)
    pose_df_flip = get_pose_df("TestClips/"+file,frame_flip=True, show_img= True)
    all_pose_dfs.append(pose_df_flip)

final_pose_df = pd.concat(all_pose_dfs, ignore_index=True)
final_pose_df.to_csv('test_final_pose_data.csv', index = False)


final_pose_df.to_csv('output.txt', sep='\t', index=False)