from .models import Post
from django import forms

class PostForm(forms.ModelForm):
    content = forms.CharField(required=False,widget=forms.Textarea(attrs={
        'class': 'form-control',
        'style':'height:100px'
        }), label='')
    class Meta:
        model=Post
        fields=['content']