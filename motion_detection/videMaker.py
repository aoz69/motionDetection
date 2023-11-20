import cv2
import os

def images_to_video(image_folder, video_name='output_video.avi', fps=10):
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), fps, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

image_directory = 'images'

# Specify the name of the output video file.
output_video_name = 'output_video.avi'

# Call the function to create the video.
images_to_video(image_directory, output_video_name)
