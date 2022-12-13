from django.shortcuts import render
from Post.models import Post

from Profile.models import FriendRequest,Profile
from Accounts.models import Account
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.
@login_required(login_url='login')
def home(request):
    posts=Post.objects.all().order_by('-created_at')[0:5]
    try:
        user=request.user
        friends_profile=Profile.objects.get(user=user).friends.all()
        
        friends_request=FriendRequest.objects.filter(receiver=user)[:3]
        values_request=friends_request.values_list('sender__email',flat=True)
        send_request=FriendRequest.objects.filter(sender=user).values_list('receiver__email',flat=True)

        who_to_follow=Profile.objects.all().exclude(user=user).exclude(user__in=friends_profile).exclude(user__email__in=list(send_request)).exclude(user__email__in=list(values_request)).order_by('-user__date_joined')[:5]



    except:
        friends_request=[]
        user=None
        who_to_follow=[]
    context={
        
        'posts':posts,
        'friends_request':friends_request,
        'user':user,
        'who_to_follow':who_to_follow
    }
    return render(request,'home.html',context)

