from django import forms
from .models import Post, Comment

class DateInput(forms.DateInput):
    input_type = 'date'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'found_place', 'kept_place', 'item_type', 'found_date')
        widgets = {
            'found_date': DateInput(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
