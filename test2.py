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

def rename_file_append(old_path, append_text):
    """Appends text to the file name while retaining the original name."""
    folder = os.path.dirname(old_path)
    file_name, file_ext = os.path.splitext(os.path.basename(old_path))
    new_name = f"{file_name}{append_text}{file_ext}"
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
            append_text = input(f"Enter text to append to '{file}' (or press Enter to skip): ").strip()
            if append_text:
                rename_file_append(full_path, append_text)
            else:
                print(f"Skipped renaming for '{file}'.")
        print("-" * 40)

if __name__ == "__main__":
    folder_path = r"F:\PK Penalty Project\test"
    main(folder_path)
