from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Comment, Advice


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author', 'tags')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class AdviceForm(forms.ModelForm):

    class Meta:
        model = Advice
        fields = ('text', 'image')


class XlsxImportForm(forms.Form):
    xlsx_file = forms.FileField()
