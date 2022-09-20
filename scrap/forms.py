from django.forms import ModelForm
from django import forms
from .models import RelatedFile

class RelatedFileForm(ModelForm):
    image = forms.FileField(label='File')    
    class Meta:
        model = RelatedFile
        fields = ('file', )            