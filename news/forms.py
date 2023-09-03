from django.forms import ModelForm, widgets, ModelChoiceField, CharField, Select, DateTimeField, ModelMultipleChoiceField, Textarea
from django.forms import ModelForm
from .models import *
from django import forms
from .models import Comment
from django import forms
from .models import Comment
from .models import Comment
from django import forms



class CreateCommentForm(forms.ModelForm):



    class Meta:
        model = Comment
        fields = ['text','user_sender']





class PostForm(ModelForm):
    author = ModelChoiceField(queryset=Author.objects.all(), label='Автор:')

    category = ModelMultipleChoiceField(label='Категория', queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ['photo', 'author', 'title', 'text', 'categoryType', 'category']












