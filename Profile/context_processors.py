from multiprocessing import context
from .models import FriendRequest, Profile
from Post.models import Post    
from Accounts.models import Account
from django.shortcuts import get_object_or_404

def friend_request(request):
    try:
        friend_request=FriendRequest.objects.filter(receiver=request.user).values_list('sender__id',flat=True)
        recveiver=FriendRequest.objects.filter(sender=request.user).values_list('receiver__id',flat=True)
    except:
        friend_request=None
        recveiver=None
    data={
        'friend_request':friend_request,
        'recveiver':recveiver,
    }
    return dict(data)


def profile(request):
    try:
        username=(request.path).split('/')[-2]
        user=get_object_or_404(Account,username=username)
        profile=Profile.objects.get(user=user)
        posts=Post.objects.filter(author=user)
        media_preview=[]
        for post in posts:
            for media in post.media_set.all():
                media_preview.append(media.img.url)
                if len(media_preview) == 4:
                    break
            if len(media_preview) == 4:
                break 
    except:
        profile=[]
        media_preview=[]
        user=None
    data={
        'user':user,
        'profile':profile,
        'media_preview':media_preview
    }
    return dict(data)