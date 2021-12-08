import os
import time
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http.response import StreamingHttpResponse

from . import detect, detect_rt
from facemask_detection import settings
# from .forms import UploadImageForm

#
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.folder_path = 'D:/Thesis/upload/temp/'
        (self.grabbed, self.frame) = self.video.read()
        self.count = 0
        cv2.imwrite(self.folder_path+str(self.count)+'.jpg', self.frame)
        # detect_rt(source=self.folder_path,
        #           weight='yolov5s.pt',
        #           imgsz=[640, 640],
        #           conf_thres=0.2,
        #           project=settings.MEDIA_ROOT,
        #           nosave=True,
        #           # name=savedir_name,
        #           view_img=False)
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
            self.count += 1
            cv2.imwrite(self.folder_path + str(self.count) + '.jpg', self.frame)
            # detect_rt(source=self.folder_path,
            #           weight='yolov5s.pt',
            #           imgsz=[640, 640],
            #           conf_thres=0.2,
            #           project=settings.MEDIA_ROOT,
            #           nosave=True,
            #           # name=savedir_name,
            #           view_img=False)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livefe(request):
    try:
        temp = os.path.join(settings.MEDIA_ROOT, 'temp')
        detect_rt.run(source=temp,
                      weights='yolov5s.pt',
                      imgsz=[640, 640],
                      conf_thres=0.2,
                      project=settings.MEDIA_ROOT,
                      # name=savedir_name,
                      nosave=False,
                      view_img=False)
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        print('[ERROR]')
        passcam = VideoCamera()
#

def clear_temp_folder():
    temp = os.path.join(settings.MEDIA_ROOT, 'temp')
    for filename in os.listdir(temp):
        filepath = os.path.join(temp, filename)
        try:
            if os.path.isfile(filepath) or os.path.islink(filepath):
                os.unlink(filepath)
        except Exception as e:
            print('Failed to delete %s due to %s' % (filepath, e))


def upload(request):
    temp = os.path.join(settings.MEDIA_ROOT, 'temp')
    if request.method == 'GET':
        clear_temp_folder()
        return render(request, 'upload.html')
    if request.method == 'POST':
        if request.POST['action'] == 'upload':
            # upload
            file = request.FILES['file']
            fs = FileSystemStorage(location=temp)
            fs.save(file.name, file)

            uploaded_file_urls = []
            for filename in os.listdir(temp):
                uploaded_file_urls.append(settings.MEDIA_URL + 'temp/' + filename)

            return render(request, 'upload.html', {
                'uploaded_file_urls': uploaded_file_urls,
            })

        if request.POST['action'] == 'detect':
            savedir_name = time.strftime('%Y%m%d_%H%M%S')
            detect.run(source=temp,
                       weights='yolov5s.pt',
                       imgsz=[640, 640],
                       conf_thres=0.2,
                       project=settings.MEDIA_ROOT,
                       name=savedir_name,
                       view_img=False)

            detected_file_urls = []
            for filename in os.listdir(os.path.join(settings.MEDIA_ROOT, savedir_name)):
                detected_file_urls.append(settings.MEDIA_URL + savedir_name + '/' + filename)

            clear_temp_folder()

            return render(request, 'upload.html', {
                'detected_file_urls': detected_file_urls,
            })

    return render(request, 'upload.html')


def realtime(request):
    return render(request, 'realtime.html')


def display_cam():
    video = cv2.VideoCapture(0)
    while True:
        frame = detection(video)
        frame = cv2.resize(frame, (1000, 700))
        cv2.imwrite('currentframe.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('currentframe.jpg', 'rb').read() + b'\r\n')


def video_feed():
    return StreamingHttpResponse(display_cam(), content_type='multipart/x-mixed-replace; boundary=frame')


def detection(video):
    return detect_rt.run(source=video.read(),
                       weights='yolov5s.pt',
                       imgsz=[640, 640],
                       conf_thres=0.2,
                       project=settings.MEDIA_ROOT,
                       # name=,
                       view_img=False)
