from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

class QueryForm(forms.Form):
    city = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)
