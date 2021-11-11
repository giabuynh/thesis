from django import forms
from .model import Image


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)
        widgets = {'image': forms.HiddenInput()}

# class UploadImageForm(forms.Form):
#     image = forms.ImageField()