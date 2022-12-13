from django.shortcuts import render
from Accounts.models import Account
from .models import Notifications, Thread,Message
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
import asyncio

# Create your views here.
def get_object(request,user):
    obj=Thread.objects.get_or_create_personal_thread(request.user,user)
    return obj


def chat(request,user_id):
    user=get_object_or_404(Account,id=user_id)
    thread=get_object(request,user)  
    messages=Message.objects.filter(thread=thread)
    path=(request.path).split('/')[-2]
    last_mess=messages.last()
    try:
        if last_mess.sender !=request.user  :
            last_mess.seen=True     
            last_mess.save()
    except:
        pass
    context={
        'messages':messages,
        'user':user,
        'me':request.user,
        'path':path,
    }
    
    return render(request,'socket/message.html',context)

def read_noti(request):
    notifications=Notifications.objects.filter(user=request.user,seen=False)

    for noti in notifications:
        noti.seen=True
        noti.save()
    return JsonResponse({'success':'success'})

def mess_img(request):
    if request.method == 'POST':
        files=request.FILES.getlist('file') 
        room_id=request.POST['room_id']
        room=Account.objects.get(id=room_id)
        thread=Thread.objects.get_or_create_personal_thread(request.user,room)
        for file in files:
            mess =Message.objects.create(thread=thread,sender=request.user,media=file)

    return HttpResponse(mess.media.url)