# thumbnailer/views.py

import os

from celery import current_app

from django import forms
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .tasks import make_thumbnails

class FileUploadForm(forms.Form):
    image_file = forms.ImageField(required=True)


class HomeView(View):
    def get(self, request):
        form = FileUploadForm()
        return render(request, 'thumbnailer/home.html', { 'form': form })
    
    def post(self, request):
        form = FileUploadForm(request.POST, request.FILES)
        context = {}

        if form.is_valid():
            file_path = os.path.join(settings.IMAGES_DIR, request.FILES['image_file'].name)

            with open(file_path, 'wb+') as fp:
                for chunk in request.FILES['image_file']:
                    fp.write(chunk)

            task = make_thumbnails.delay(file_path, thumbnails=[(128, 128)])

            context['task_id'] = task.id
            context['task_status'] = task.status
            context['media_url'] = settings.MEDIA_URL

            return render(request, 'thumbnailer/home.html', context)

        context['form'] = form

        return render(request, 'thumbnailer/home.html', context)


class TaskView(View):
    def get(self, request, task_id):
        task = current_app.AsyncResult(task_id)
        response_data = {'task_status': task.status, 'task_id': task.id}

        if task.status == 'SUCCESS':
            response_data['results'] = task.get()

        return JsonResponse(response_data)
