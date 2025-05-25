from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import *
from .form import *
# Create your views here.
@login_required 
def chat_view(request , chatroom_name='public-chat'):
    chat_groups = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_groups.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    other_user = None
    if chat_groups.is_private:
        if request.user not in chat_groups.members.all():  
            raise Http404()
        for member in chat_groups.members.all():
            if member != request.user:
                other_user = member
                break

    if chat_groups.group_name:
        if request.user not in chat_groups.members.all():
            chat_groups.members.add(request.user)


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

    context = {
        'chatroom_name': chatroom_name,
        'chat_messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'chat_groups': chat_groups,
    }


    return render(request, 'a_rtchat/chat.html', context)


@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')
    other_user = User.objects.get(username=username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                chatroom = chatroom
                break
            else:
                chatroom = ChatGroup.objects.create(is_private=True)
                chatroom.members.add( other_user,request.user)
    else:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)
    
    return redirect('chatroom', chatroom.group_name)

@login_required
def create_groupchat(request):
    form = NewGroupForm()
    if request.method == 'POST':
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect('chatroom', new_groupchat.group_name)
    context = {
        'form': form,
    }
    return render(request, 'a_rtchat/create_groupchat.html', context)
           
@login_required
def chatroom_edit_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()
    form = ChatroomEditForm(instance=chat_group)

    if request.method == 'POST':
        form = ChatroomEditForm(request.POST, instance=chat_group)
        if form.is_valid():
            form.save()
            
            remove_members = request.POST.getlist('remove_members')
            for member_id in remove_members:
                member = User.objects.get(id=member_id)
                chat_group.members.remove(member)
            
            return redirect('chatroom', chatroom_name)



    context = {
        'form': form,
        'chat_group': chat_group,
    }
    return render(request, 'a_rtchat/chatroom_edit.html',context)

@login_required
def chatroom_delete_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()
    
    if request.method == 'POST':
        chat_group.delete()
        return redirect('home')

    context = {
        'chat_group': chat_group,
    }
    return render(request, 'a_rtchat/chatroom_delete.html', context)


