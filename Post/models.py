from django.db import models
from Accounts.models import Account
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    root=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    author = models.ForeignKey(Account,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    content=models.TextField(max_length=500)
    likes=models.ManyToManyField(Account,related_name='likes',blank=True)
    shares=models.IntegerField(default=0)
    edite=models.BooleanField(default=False)

    def __str__(self):
        return f'post {self.id}'

    def get_url(self):
        return reverse('detail',args=[self.id])


class Media(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)
    img=models.ImageField(upload_to='posts')


class CommentPost(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)
    parent=models.ForeignKey('CommentPost',on_delete=models.CASCADE,null=True,blank=True)
    content=models.CharField(max_length=200)
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(Account,blank=True,related_name='likescomment')

    def children(self):
        return CommentPost.objects.filter(parent=self)
