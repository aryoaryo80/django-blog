from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
        }


class NestedCommentForm(forms.Form):
    body = forms.CharField(max_length=300, widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': '3'}))
    comment_id = forms.IntegerField()


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': '10'}),
        }
