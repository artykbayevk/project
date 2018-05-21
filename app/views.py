# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseForbidden
# from models import ExampleModel
import shutil
import glob
import os
import cv2
import numpy as np
import subprocess
import json


from django import forms

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from django.db import models

class Document(models.Model):
    document = models.FileField(upload_to='img/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ExampleModel(models.Model):
    model_pic = models.ImageField(upload_to = 'img/')



def index(request):
    return render(request,'index.html')

def upload_pic(request):

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # os.remove(file) for file in os.listdir('path/to/directory') if file.endswith('.png')
            for file in os.listdir(os.path.join(BASE_DIR, 'media', 'img')):
                if(file.endswith('.jpg')):
                    os.remove(os.path.join(BASE_DIR,'media','img',file))
            for file in os.listdir(os.path.join(BASE_DIR, 'static', 'img')):
                if(file.endswith('.jpg')):
                    os.remove(os.path.join(BASE_DIR,'static','img',file))
            m = ExampleModel()
            m.model_pic = form.cleaned_data['image']
            m.save()
            for file in os.listdir(os.path.join(BASE_DIR, 'media', 'img')):
                if(file.endswith('.jpg')):
                    shutil.move(os.path.join(BASE_DIR,'media','img',file), os.path.join(BASE_DIR,'media','img','main.jpg'))
                    shutil.copy(os.path.join(BASE_DIR,'media','img','main.jpg'),os.path.join(BASE_DIR,'static','img','main.jpg'))
            pathForImage = os.path.join(BASE_DIR, 'static', 'img','main.jpg')
            mainImage = cv2.imread(pathForImage)
            p = subprocess.Popen('alpr -c kz -p kz -j '+pathForImage, stdout = subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p_status = p.wait()
            # main_out = output.split('\n')
            print(output.decode().split('\n'))
            return HttpResponse('NOTHING')
            data = (json.loads(main_out))['results']
            # print(data)
            if(len(data) == 0 ):
                data = {'plateNumber':'НОМЕР БЫЛ НЕ НАЙДЕН'}
                return render(request,'second.html',data)
            else:
                coordinates = data[0]['coordinates']
                top_left = coordinates[1]
                bottom_right = coordinates[3]
                y1 = top_left['y']
                x1 = top_left['x']

                y2 = bottom_right['y']
                x2 = bottom_right['x']

                cv2.rectangle(mainImage,(x1,int(y1)),(x2,int(y2)),(0,255,0),1)
                cv2.imwrite(pathForImage, mainImage)
                plates = data[0]['candidates']
                plate_number = (data[0]['candidates'][0]['plate'])

                best_predicted = data[0]['candidates'][0]['plate']
                best_predicted_by_pattern = []
                for plate in plates:
                    if(plate['matches_template'] == 1):
                        best_predicted_by_pattern.append(plate['plate'])
                if(len(best_predicted_by_pattern)!=0):
                    best_predicted = best_predicted_by_pattern[0]
                data = {'plateNumber':best_predicted}
                return render(request,'second.html',data)
    return HttpResponseForbidden('allowed only via POST')
