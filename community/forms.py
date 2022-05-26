from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ['title', 'content', 'head_image', 'file_upload', 'category', 'tags']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ['review', 'user']
