from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True)
    users_online = models.ManyToManyField(User, blank=True, related_name='online_in_groups')

    def __str__(self):
        return self.group_name

class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='chat_messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} : {self.body}"
    
    class Meta:
        ordering = ['-created']