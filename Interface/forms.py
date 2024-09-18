from django import forms

class VideoUploadForm(forms.Form):
    video1 = forms.FileField(required=False)  # Set required=False
    video2 = forms.FileField(required=False)
    video3 = forms.FileField(required=False)
    video4 = forms.FileField(required=False)
