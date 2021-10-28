import os
import cv2
import math


def video_to_frames(video_path, save_folder_path):
    video_path_patterns = video_path.split('/')
    video_filename = video_path_patterns[-1].split('.')[0]
    print('[WRITE] Extract frames from ', video_path_patterns[-1])

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS) # Frame rate
    # print("Frames per second: {}".format(fps))
    fps = math.floor(fps) # Lam tron frame rate
    cap_frames_per_second = 1 # Cap 3 frame/second

    while cap.isOpened():
        frameId = cap.get(cv2.CAP_PROP_POS_FRAMES)
        ret, frame = cap.read()

        if not ret:
            break

        if frameId % fps < cap_frames_per_second:
            frame_filename = save_folder_path + video_filename + '-' + str(int(frameId)) + '.png'
            cv2.imwrite(frame_filename, frame)

    cap.release()
    cv2.destroyAllWindows()


def load_videos_from_folder(folder_path):
    print('[INFO] Loading images from ', folder_path)
    filenames = os.listdir(folder_path)
    allowed_extensions = ['mp4', 'mov', 'MP4', 'MOV']
    videos = []
    for filename in filenames:
        # get a full file path
        file_path = os.path.join(folder_path, filename)
        # check whether a file path is a file or a directory
        if os.path.isfile(file_path):
            # check whether a file is a video
            filename_patterns = filename.split('.')
            if filename_patterns[-1] in allowed_extensions:
                # add file name to videos list
                videos.append(filename)
    return videos

video_folder = 'D:/Thesis/MyData/Videos/with_shield/'
frame_folder = 'D:/Thesis/Mydata/Frames/with_shield/'

videos = load_videos_from_folder(video_folder)
for video in videos:
    video_to_frames(os.path.join(video_folder, video), frame_folder)

