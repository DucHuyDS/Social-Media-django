from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async,async_to_sync
from django.template.loader import render_to_string
from Socket.models import Thread,Message
from Accounts.models import Account
from Profile.models import Profile
import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.me=self.scope['user']
        self.room_id=self.scope['url_route']['kwargs']['room_id']

        self.order_user= await sync_to_async(Account.objects.get, thread_sensitive=True)(id=self.room_id)
        self.thread= await sync_to_async(Thread.objects.get_or_create_personal_thread, thread_sensitive=True)(self.me,self.order_user)
        self.room_group_name='thread_%s' % self.thread.id
    
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()



    async def disconnect(self,clean_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self,text_data):
        self.me=self.scope['user']
        data=json.loads(text_data)
        event=data['event']
        room_id=data['room_id']
        message=data['message']
        sender=data['sender']

        created_at=datetime.datetime.today().strftime('%H:%M, %m-%d-%Y')
        await self.save_message(room_id,message,event)
        data={
            'event':event,
            'message':message,
            'room_id':room_id,
            'sender':sender,
            'created_at':created_at
        }

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'value':json.dumps(data)
            }
        )
    async def chat_message(self,event):
        data=json.loads(event.get('value'))

        await self.send(text_data=json.dumps(data))
        await self.update_mess()

    @sync_to_async
    def save_message(self,room_id,message,event):
        room=Account.objects.get(id=room_id)
        thread=Thread.objects.get_or_create_personal_thread(self.me,room)
        thread.save()
        if event =='mess_media':
            mess=Message.objects.filter(thread=thread).last()
            mess.text=message
            mess.save()
        else:
            Message.objects.create(thread=thread,sender=self.me,text=message)
        data={
            'event':'mess',     
            'mess':message,
            'sender':room_id,
            'user':self.me.id,
            'room_id':self.room_id,
        }

        for user in thread.users.all():
            async_to_sync(self.channel_layer.group_send)(
                f'noti_{user.id}',
                {
                    'type':'send_notification_mess',
                    'value':json.dumps(data)
                }
            )
    @sync_to_async
    def update_mess(self):
        thread= Thread.objects.get(id=self.thread.id)
        messages=Message.objects.filter(thread=thread)
        last_mess=messages.last()
        if last_mess.sender !=self.me:
            last_mess.seen=True     
            last_mess.save()


    
class Notifications(AsyncWebsocketConsumer):

    async def connect(self):
        self.me=self.scope['user']
        self.user_id=self.scope['user'].id
        self.room_name = 'new_consumer'
        self.room_group_name = 'noti_%s' %self.user_id
        await self.update_status(self.user_id,True)
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
  
    async def disconnect(self,clean_code):
        await self.update_status(self.user_id,False)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def send_notification(self , event):
        data=json.loads(event.get('value'))
        await self.send(text_data=json.dumps(data))


    async def send_notification_mess(self , event):
        data=json.loads(event.get('value'))
        room_id,html=await self.get_rooms(data['room_id'])  
        data['room_id']=room_id
        data['html']=html
        await self.send(text_data=json.dumps(data))

    @sync_to_async
    def get_rooms(self,sender):
        html=""
        thread=Thread.objects.by_user(self.me).order_by('-updated')
        room=thread.first() 
        messages=Message.objects.filter(thread=room)
        if len(messages) == 1:
            context={
                'room':room,
                'me':self.me,
                'path':str(sender),
            }
            html=render_to_string('socket/rooms.html',context)
        return room.id,html


    @sync_to_async
    def update_status(self,user_id,event):

        user=Profile.objects.get(user_id=user_id)
        user.status_user=event
        user.save()

        