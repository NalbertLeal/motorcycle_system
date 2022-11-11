import argparse

# import numpy as np
import cv2

parser = argparse.ArgumentParser(description='Send media file (video) to the backend identify motorcycles.')
parser.add_argument('--path', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
parser.add_argument('--frames', type=int, required=True)
args = parser.parse_args()

video_reader = cv2.VideoCapture(args.path)
video_width = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_fps = video_reader.get(cv2.CAP_PROP_FPS)

video_writer = cv2.VideoWriter(
    #f'{args.output}.avi',
    #cv2.VideoWriter_fourcc(*'MJPG'),
    f'{args.output}.mp4',
    cv2.VideoWriter_fourcc(*'mp4v'),
    video_fps,
    (video_width, video_height)
)

count = 0
if not video_reader.isOpened():
    print(f'File {args.output} could not be open')

while video_reader.isOpened() and count < args.frames:
    has_frame, frame = video_reader.read()
    if not has_frame:
        break
    
    cv2.imshow('Frame', frame)

    video_writer.write(frame)
    count += 1

    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

video_reader.release()
video_writer.release()
cv2.destroyAllWindows()