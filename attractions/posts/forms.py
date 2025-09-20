from django import forms

from .models import Advice, Comment, Post


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
