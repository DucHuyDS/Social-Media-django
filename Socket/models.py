from django.db import models
from Accounts.models import Account
from django.db.models import Count
from django.dispatch import receiver
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import json

from Post.models import Post

class ThreadManager(models.Manager):
    def get_or_create_personal_thread(self, user1, user2):
        if user1!= user2:
            threads = self.get_queryset().filter(thread_type='personal')
            threads = threads.filter(users__in=[user1, user2]).distinct()
            threads = threads.annotate(u_count=Count('users')).filter(u_count=2)
            if threads.exists():
                return threads.first()
            else:
                thread = self.create(thread_type='personal')
                thread.users.add(user1)
                thread.users.add(user2)
                return thread

    def by_user(self, user):
        return self.get_queryset().filter(users__in=[user])

class Thread(models.Model):

    THREAD_TYPE = (
        ('personal', 'Personal'),
        ('group', 'Group')
    )

    name = models.CharField(max_length=50, null=True, blank=True)
    thread_type = models.CharField(max_length=15, choices=THREAD_TYPE, default='group')
    users = models.ManyToManyField(Account)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    objects = ThreadManager()

    def __str__(self) -> str:
        if self.thread_type == 'personal' and self.users.count() == 2:
            return f'{self.users.first()} and {self.users.last()}'
        return f'{self.name}'



    
class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE,null=True,blank=True)
    media=models.FileField(upload_to='chat',null=True,blank=True)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE,null=True,blank=True)
    text = models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    seen=models.BooleanField(default=False)

    def __str__(self)->str:
        return self.text


class Notifications(models.Model):
    NOTIFICATION_CHOICES = (
    ('likepost','liked your post'),
    ('likecmt','liked your comment'),
    ('comment','commented your post'),
    ('reply','replied your comment'),
    ('send','sent a friend request'),
    ('accept','accepted your friend request'),
    )

    generator=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='generator')
    type=models.CharField(max_length=100,choices=NOTIFICATION_CHOICES,blank=True,null=True)
    user=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='user')
    link=models.CharField(max_length=100,null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,blank=True,null=True)
    seen=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.generator.full_name()}  {self.get_type_display()}'

    def save(self,*args,**kwargs):
        if self.seen== False:
            channel_name=get_channel_layer()
            data={
                'event':'noti',
                'img':self.generator.profile.img.url,
                'current':f'{self.generator.first_name} {self.generator.last_name} {self.get_type_display()}' ,
                'link':f'{self.link}',
                
            }

            async_to_sync(channel_name.group_send)(
                f'noti_{self.user.id}',
                {
                    'type':'send_notification',
                    'value':json.dumps(data)
                }
            )
        super(Notifications, self).save(*args,**kwargs)