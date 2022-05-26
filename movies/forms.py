from django import forms
from .models import Movie, Movie_Comment

# class MovieForm(forms.ModelForm):
#     class Meta:
#         model = Movie
#         fields = ('title', 'description',)


class MovieCommentForm(forms.ModelForm):
    class Meta:
        model = Movie_Comment
        fields = ('content',)