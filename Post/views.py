import json
from xml.etree.ElementTree import Comment
from django.shortcuts import render,redirect
from Post.models import Post,Media,CommentPost
from django.http import HttpResponse,JsonResponse
from Socket.models import Notifications
from .forms import PostForm
from django.shortcuts import get_object_or_404

# Create your views here.
def post_data_share(request,post_id):
    post=get_object_or_404(Post,id=post_id)

    return render(request,'post/share_post.html',{'post':post})



def post_data(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    return render(request,'post/post.html',{'post':post})

    
def detail(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    context={
        'post':post,
    }
    return render(request,'post/post_detail.html',context)


def create_post(request):
    if request.method=='POST':
        content=request.POST['content']
        files=request.FILES.getlist('file')  
        post=Post.objects.create(author_id=request.user.id,content=content)
        for file in files:
            Media.objects.create(post=post,img=file)  


    return redirect('/post/get_next_post?offset=0')


def share_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    if request.method=='POST':
        content=request.POST['content_share']
        post =Post.objects.create(root=post,author=request.user,content=content)
    return render(request,'post/post.html',{'post':post})


def update_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    if request.method == 'POST':
        post_form=PostForm(request.POST,instance=post)
        post.edite=True
        if post_form.is_valid():
            post_form.save()

            return render(request,'post/post.html',{'post':post})
            
    else:
        post_form=PostForm(instance=post)   
    context={
        'post_form':post_form,
        'post':post
    }
    return render(request,'post/post_form.html',context)


def delete_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    post.delete()
    return HttpResponse()



def get_next_post(request):
    try:
        offset=int(request.GET['offset'])     
    except:
        offset=5
    url =request.META.get('HTTP_REFERER')
    if 'profile' not in url:
        posts=Post.objects.all().order_by('-created_at')[offset:offset+5]
    else:
        posts=Post.objects.filter(author__username=url.split('/')[4]).order_by('-created_at')[offset:offset+5]
    context={
        'posts':posts,
        'offset':offset+5,
    }
    return render(request,'post/get_next_post.html',context)



def like(request,post_id):
    if request.user.is_anonymous :
        data={
            'content':'You need login!',
            'status':'anonymous'
        }
        return JsonResponse(data)
    post=get_object_or_404(Post,id=post_id)  
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        if post.author != request.user: 
            Notifications.objects.get(generator=request.user,user=post.author,type='likepost',post=post).delete()
        status=False
    else:
        post.likes.add(request.user)
        if post.author != request.user: 
            Notifications.objects.create(generator=request.user,type='likepost',user=post.author,link=post.get_url(),post=post)
        status=True
    data=post.likes.count()
    data={
        'count':post.likes.count(),
        'status':status
    }
    return JsonResponse(data) 


def like_comment(request,comment_id):
    try:
        comment=CommentPost.objects.get(id=comment_id)
        comment.post.id
    except CommentPost.DoesNotExist:
        data={
            'content':'This comment has been deleted',
            'status':'deleted'
        }
        return JsonResponse(data)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        if comment.user != request.user: 
            Notifications.objects.get(generator=request.user,user=comment.user,type='likecmt').delete()
        status=False

    else:
        comment.likes.add(request.user)
        if comment.user != request.user: 
            Notifications.objects.create(generator=request.user,type='likecmt',user=comment.user,link=comment.post.get_url())
        status=True
    data={
        'count':comment.likes.count(),
        'status':status
    }
    return JsonResponse(data)


def comment(request,post_id):
    user=request.user


    if request.method=='POST':
        comment=request.POST['comment']
        parent_comment=request.POST['commentparent']
        post=get_object_or_404(Post,id=post_id)
      
        if parent_comment == "":
            commentpost=CommentPost(post=post,content=comment,user=user)
            commentpost.save()        
            if post.author != request.user:   
                Notifications.objects.create(generator=request.user,user=post.author,type='comment',link=post.get_url())
            
        else:
            try:
                parent=CommentPost.objects.get(id=comment)  
            except CommentPost.DoesNotExist:
                data={
                    'status':'deleted',
                    'content':'This comment has been deleted'
                }
                return JsonResponse(data)      
            commentpost=CommentPost(post=post,content=parent_comment,user=user,parent=parent)
            commentpost.save()   
            if post.author != request.user: 
                Notifications.objects.create(generator=request.user,user=parent.user,type='reply',link=post.get_url()) 

    data={
        'comment_id':commentpost.id,
        'img':request.user.profile.img.url,
        'first_name':request.user.first_name,
        'last_name':request.user.last_name,
        'content':commentpost.content,
        'likes':commentpost.likes.count(),
        'comments':post.commentpost_set.count(),
    
    }
    return JsonResponse(data)
    


def delete_comment(request,comment_id):
    comment=get_object_or_404(CommentPost,id=comment_id)
    comment.delete()
    data={
        'comments':comment.post.commentpost_set.count(),
        'post_id':comment.post.id,
    }
    return JsonResponse(data)
