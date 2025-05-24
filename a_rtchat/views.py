from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .form import ChatmessageCreateForm
# Create your views here.
@login_required 
def chat_view(request):
    chat_groups = get_object_or_404(ChatGroup, group_name='public-chat')
    chat_messages = chat_groups.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_groups 

            message.save()
            context = {
                'message': message,
                'user': request.user,
                
            }
            return render(request, 'a_rtchat/partials/chat_messages_p.html', context)


    return render(request, 'a_rtchat/chat.html', {
        'chat_messages': chat_messages,
        'form': form
    })