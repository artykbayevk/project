# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Document(models.Model):
    document = models.FileField(upload_to='img/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ExampleModel(models.Model):
    model_pic = models.ImageField(upload_to = 'img/')
