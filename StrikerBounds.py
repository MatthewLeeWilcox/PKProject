import os
import cv2

def play_video(file_path):
    """Plays the video file."""
    cap = cv2.VideoCapture(file_path)

    if not cap.isOpened():
        print(f"Unable to open video: {file_path}")
        return False

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Video", frame)

        # Press 'q' to quit the video early
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return True

def rename_file(old_path, new_name):
    """Renames the file with the new name provided by the user."""
    folder = os.path.dirname(old_path)
    new_path = os.path.join(folder, new_name)
    try:
        os.rename(old_path, new_path)
        print(f"Renamed to: {new_path}")
    except Exception as e:
        print(f"Error renaming file: {e}")

def main(folder_path):
    """Main function to cycle through .mp4 files and rename them."""
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return

    mp4_files = [f for f in os.listdir(folder_path) if f.endswith(".mp4")]
    if not mp4_files:
        print("No .mp4 files found in the folder.")
        return

    for file in mp4_files:
        full_path = os.path.join(folder_path, file)
        print(f"Now playing: {file}")
        if play_video(full_path):
            new_name = input(f"Enter new name for '{file}' (or press Enter to skip renaming): ").strip()
            if new_name:
                if not new_name.endswith(".mp4"):
                    new_name += ".mp4"
                rename_file(full_path, new_name)
            else:
                print(f"Skipped renaming for '{file}'.")
        print("-" * 40)

if __name__ == "__main__":
    folder_path = r"F:\PK Penalty Project\test"
    main(folder_path)
