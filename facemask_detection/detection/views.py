import os

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
# from .forms import UploadImageForm
from . import detect
from facemask_detection import settings
import time


def clear_temp_folder():
    temp = os.path.join(settings.MEDIA_ROOT, 'temp')
    for filename in os.listdir(temp):
        filepath = os.path.join(temp, filename)
        try:
            if os.path.isfile(filepath) or os.path.islink(filepath):
                os.unlink(filepath)
        except Exception as e:
            print('Failed to delete %s due to %s' % (filepath, e))


def index(request):
    temp = os.path.join(settings.MEDIA_ROOT, 'temp')
    if request.method == 'GET':
        clear_temp_folder()
        return render(request, 'home.html')
    if request.method == 'POST':
        if request.POST['action'] == 'upload':
            # upload
            file = request.FILES['file']
            fs = FileSystemStorage(location=temp)
            fs.save(file.name, file)

            uploaded_file_urls = []
            for filename in os.listdir(temp):
                uploaded_file_urls.append(settings.MEDIA_URL + 'temp/' + filename)

            return render(request, 'home.html', {
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

            return render(request, 'home.html', {
                'detected_file_urls': detected_file_urls,
            })

    return render(request, 'home.html')
