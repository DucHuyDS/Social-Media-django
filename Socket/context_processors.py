from ast import Raise
from .models import Notifications,Thread

def notifications(request):
    try:
        notifications= Notifications.objects.filter(user=request.user).order_by('-timestamp')
        unread_noti=notifications.filter(seen=False).count()
    except:
        notifications=[]
        unread_noti=0
    data={
        'notifications':notifications[:10],
        'unread_noti':unread_noti,
    }
    return dict(data)

def unread_mess(request,unread_count=0):
    try:
        rooms=Thread.objects.by_user(request.user).order_by('-updated')
        for room in rooms:
            try:
                if room.message_set.last().seen==False and room.message_set.last().sender !=request.user:
                    unread_count+=1
            except:
                pass             
    except:
        rooms=None
    data={
        'unread_mess':unread_count,
        'rooms':rooms,
    }
    return dict(data)

