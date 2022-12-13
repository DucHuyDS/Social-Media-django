from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from Accounts.models import Account
from .models import Profile,FriendRequest
from Post.models import Post
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from Socket.models import Notifications
# Create your views here.

def posts(request,username):
    user=get_object_or_404(Account,username=username)
    posts=Post.objects.filter(author=user).order_by('-created_at')[0:5]
    context={
        'posts':posts
      
    }
    return render(request,'profile/posts.html',context)

def about(request,username):
    url=request.META.get('HTTP_REFERER')
    user=get_object_or_404(Account,username=username)
    userprofile=Profile.objects.get(user=user)
    if request.method == 'POST':
        form=ProfileForm(request.POST,request.FILES,instance=userprofile)
        if form.is_valid():
            form.save()

            messages.success(request,'Profile updated!')
            return redirect(url)
    else:
        form=ProfileForm(instance=userprofile)

    context={
        'form':form,
        
    }
    return render(request,'profile/about.html',context)

def friends(request,username):
    return render(request,'profile/friends.html')

def media(request,username):
    user=get_object_or_404(Account,username=username)
    posts=Post.objects.filter(author=user)     
    context={
        'posts':posts
    }
    return render(request,'profile/media.html',context)

@login_required(login_url='login')
def send_friend_request(request,user_id):
    user=get_object_or_404(Account,id=user_id)
    exist=FriendRequest.objects.filter(sender=request.user,receiver=user).exists()
    if exist:
        friend_request=FriendRequest.objects.filter(sender=request.user,receiver=user)
        Notifications.objects.filter(generator=request.user,user=user,type='send').delete()
        friend_request.delete()
    else:
        friend_request=FriendRequest.objects.create(sender=request.user,receiver=user)
        Notifications.objects.create(generator=request.user,user=user,type='send',link=request.user.profile.get_url())

    data={
        'exist':exist,
        'user_id':user.id,
    }
    return JsonResponse(data)

def accept_friend_request(request,user_id):
    user=get_object_or_404(Account,id=user_id)
    try:
        friend_request=FriendRequest.objects.get(sender=user,receiver=request.user)
        accept=True
        if friend_request.receiver == request.user:
            friend_request.sender.profile.friends.add(friend_request.receiver)
            friend_request.receiver.profile.friends.add(friend_request.sender)
            friend_request.delete()
            Notifications.objects.create(generator=request.user,user=user,type='accept',link=request.user.profile.get_url())
         
    except FriendRequest.DoesNotExist:
        friend_request=None
        accept=False

    data={
        'accept':accept,
        'user_id':user.id,
    }
    return JsonResponse(data)



def remove_friend(request,user_id):
    user=get_object_or_404(Account,id=user_id)
    request.user.profile.friends.remove(user)
    user.profile.friends.remove(request.user)

    return JsonResponse({'user_id':user.id})


def contact(request):
    check=request.user.is_anonymous
    if check == False:
        user=request.user
        friends=Profile.objects.get(user=user).friends.all() 
        if request.method=='GET':
            try:
                keyword=request.GET['search_contact']
                if keyword:
                    user=request.user
                    profile=Profile.objects.get(user=user)
                    friends=profile.friends.all().filter(Q(first_name__icontains=keyword)|Q(last_name__icontains=keyword))
            except :
                pass
        html=render_to_string('profile/contact.html',{'friends':friends})
        return JsonResponse({'html':html})
    return HttpResponse()
