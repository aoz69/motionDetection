import cv2
import threading
import os
from tkinter import filedialog

# Define global variables to control video recording.
is_recording = False
start_time = 0
video_writer = None

image_directory = 'images'

# Specify the name of the output video file.
output_video_name = 'output_video.avi'




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



counter = 0

# Function to save a cropped image when motion is detected
def save_cropped_image(frame):
    global counter
    
    # Define the absolute directory path where the image will be saved.
    dir = os.path.abspath("./images/")

    # Check if the directory exists, and if not, create it.
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Define a unique filename using the counter or timestamp.
    filename_cropped = f"{dir}/movedImage_{counter}.jpg"
    
    # Increment the counter for the next image
    counter += 1

    # Save the cropped image to the specified file path.
    cv2.imwrite(filename_cropped, frame)
    images_to_video(image_directory, output_video_name)



def images_to_video(image_folder, video_name='output_video.avi', fps=10):
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), fps, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

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