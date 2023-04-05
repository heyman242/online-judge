from django import forms
from .models import CodeSnippet


class CodeSnippetForm(forms.ModelForm):
    code = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = CodeSnippet
        exclude = ('question',)
