import cv2
import threading
import os
from tkinter import filedialog

# Define global variables to control video recording.
is_recording = False
start_time = 0
video_writer = None




# Function to perform motion detection from a video source
def motion_detection(video_source):
    cap = cv2.VideoCapture(video_source)

    # Initialize previous frames
    prev_frame = None

    while cap.isOpened():
        ret, frame1 = cap.read()
        ret, frame2 = cap.read()

        if not ret:
            break

        # Detect motion between two frames
        motion_detected = detect_motion(frame1, frame2)

        if motion_detected:
            save_cropped_image(frame1)
            # save_frame_to_video(frame1)

        show_video_frame(frame1)

        if cv2.waitKey(50) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to detect motion between two frames
def detect_motion(frame1, frame2):
    # Calculate the absolute difference between the two frames
    diff = cv2.absdiff(frame1, frame2)

    # Convert the difference to grayscale
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the grayscale image
    blur = cv2.GaussianBlur(diff_gray, (5, 5), 0)

    # Threshold the blurred image to create a binary image
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # Dilate the thresholded image to fill gaps in the detected motion
    dilated = cv2.dilate(thresh, None, iterations=3)

    # Find contours in the dilated image
    contours, _ = cv2.findContours(
        dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Flag to track if motion is detected
    motion_detected = False

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 2000: 
            continue
        center_x = x + w // 2
        center_y = y + h // 2
        radius = max(w, h) // 2
        cv2.circle(frame1, (center_x, center_y), radius, (128, 0, 128), 2)  # Purple circle
        motion_detected = True

    return motion_detected

# Function to save a cropped image when motion is detected
def save_cropped_image(frame):
    # Define the absolute directory path where the image will be saved.
    dir = os.path.abspath("./images/")

    # Check if the directory exists, and if not, create it.
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Define the complete file path including the directory and filename.
    filename_cropped = f"{dir}/movedImage.jpg"

    # Save the cropped image to the specified file path.
    cv2.imwrite(filename_cropped, frame)
# Function to display a video frame
def show_video_frame(frame):
    cv2.imshow("Video", frame)

# Function to start motion detection with a given video source
def start_motion_detection(video_source):
    motion_detection_thread = threading.Thread(target=motion_detection, args=(video_source,))
    motion_detection_thread.start()

# Function to use a video file for motion detection
def use_video_file():
    video_source = filedialog.askopenfilename()
    start_motion_detection(video_source)

# Function to use the webcam for motion detection
def use_webcam():
    start_motion_detection(0)  # 0 represents the default webcam index











# # Function to start video recording.
# def start_recording(frame):
#     global is_recording, start_time, video_writer

#     # Define the absolute directory path where the video will be saved.
#     dir = os.path.abspath("./videos")

#     # Check if the directory exists, and if not, create it.
#     if not os.path.exists(dir):
#         os.makedirs(dir)

#     # Define the complete file path including the directory and filename.
#     filename = f"{dir}/motionVideo.mp4"

#     # Get the frame width and height to set up the video writer.
#     frame_height, frame_width, _ = frame.shape

#     # Define the codec and create a VideoWriter object.
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     video_writer = cv2.VideoWriter(filename, fourcc, 30, (frame_width, frame_height))

#     # Set the start time and recording flag.
#     start_time = cv2.getTickCount()
#     is_recording = True

# # Function to stop video recording.
# def stop_recording():
#     global is_recording, video_writer

#     # Release the video writer object.
#     if video_writer is not None:
#         video_writer.release()
#         video_writer = None

#     is_recording = False

# # Function to save a frame to the video file.
# def save_frame_to_video(frame):
#     global is_recording, video_writer

#     # Write the frame to the video file if recording is active.
#     if is_recording:
#         video_writer.write(frame)

# # Function to check if recording duration has reached 2 seconds.
# def has_recorded_enough():
#     global is_recording, start_time

#     # Calculate the elapsed time since recording started.
#     elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()

#     # If 2 seconds have passed, stop recording.
#     if elapsed_time >= 2:
#         stop_recording()

# # Function to save a 2-second video clip when motion is detected.
# def save_video_clip(frame):
#     global is_recording

#     # Check if recording is active.
#     if not is_recording:
#         start_recording(frame)

#     # Save the frame to the video file.
#     save_frame_to_video(frame)

#     # Check if 2 seconds have passed and stop recording.
#     has_recorded_enough()

