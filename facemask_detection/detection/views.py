from django.shortcuts import render, redirect
from detection.forms import ImageForm

def index(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            image_obj = form.instance
            return render(request, 'index.html', {'form': form, 'image_obj': image_obj,})
    else:
        form = ImageForm()
    return render(request, 'index.html', {'form': form,})
