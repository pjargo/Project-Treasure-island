from django import forms
from .models import DispImage, MyImage, MyPdf


class DispImageForm(forms.ModelForm):
    class Meta:
        model = DispImage
        fields = ['link', 'description', 'image']


class ImageForm(forms.ModelForm):
    class Meta:
        model = MyImage
        fields = ['Main_Img']


class PdfForm(forms.ModelForm):
    class Meta:
        model = MyPdf
        fields = ['Main_pdf']


class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'webkitdirectory': True, 'directory': True}))