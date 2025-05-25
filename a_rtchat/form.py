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
    
class NewGroupForm(ModelForm):  
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name': forms.TextInput(attrs={
                'class': 'p-4 text-black',
                'maxlength': 300,
                'autofocus': True,
                'placeholder': 'Enter group name...',
            }),
          
        }

class ChatroomEditForm(ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name': forms.TextInput(attrs={
                'class': 'p-4 text-xl font-bold mb-4',
                'maxlength': 300,
                'placeholder': 'Edit group name...',
            }),
        } 