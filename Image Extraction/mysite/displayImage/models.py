from django.db import models
from django import forms

# Create your models here.
class DispImage(models.Model):
    link = models.TextField()
    description = models.TextField()
    image = models.ImageField()


class MyImage(models.Model):
    Main_Img = models.ImageField(upload_to='images/')


class MyPdf(models.Model):
    Main_pdf = models.FileField(upload_to='files/')


class FileFieldModel(models.Model):
    pass
    # file_field = models.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'webkitdirectory': True, 'directory': True}))