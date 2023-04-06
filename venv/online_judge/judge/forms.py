# from django import forms
# from .models import CodeSnippet
#
#
# class CodeSnippetForm(forms.ModelForm):
#     code = forms.CharField(widget=forms.Textarea)
#
#     class Meta:
#         model = CodeSnippet
#         exclude = ('question',)
from django import forms
from .models import CodeSnippet


class CodeSnippetForm(forms.ModelForm):
    code = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 40, 'class': 'form-control'}))

    class Meta:
        model = CodeSnippet
        fields = ['language', 'code']


