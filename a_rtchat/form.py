from django.forms import ModelForm
from django import forms
from .models import *


class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={
                'class': 'p-4 text-black',
                'maxlength': 300,
                'autofocus': True,
                'placeholder': 'Type your message here...',
            }),
        }
    
