from django import forms
from .models import Submission
from django.db.models import TextField


class SubmissionForm(forms.ModelForm):
    code = forms.CharField(widget=forms.Textarea)
    language = forms.CharField(max_length=50)

    class Meta:
        model = Submission
        fields = ('problem', 'language', 'code')
