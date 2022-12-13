from django.db import models
from django.urls import reverse
from Accounts.models import Account


# Create your models here.
class Profile(models.Model):
    STATUS_CHOICE=(
        ('Single','Single'),
        ('In a relationship','In a relationship'),
        ('Married','Married'),
        ('Engaged','Engaged'),
    )
    GENDER_CHOICE=(
        ('Male','Male'),
        ('Female','Female')
    )
    user=models.OneToOneField(Account,on_delete=models.CASCADE)
    friends=models.ManyToManyField(Account,related_name='friends')
    img=models.ImageField(upload_to='avatar')
    cover_img=models.ImageField(upload_to='cover')
    overview=models.CharField(max_length=300,blank=True,null=True)
    born=models.DateField(blank=True,null=True)
    about=models.CharField(max_length=100,blank=True,null=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICE,blank=True,null=True)
    current_city=models.CharField(max_length=100,blank=True,null=True)
    work = models.CharField(max_length=100,blank=True,null=True)
    education=models.CharField(max_length=100,blank=True,null=True)
    hometown=models.CharField(max_length=100,blank=True,null=True)
    gender=models.CharField(max_length=20,choices=GENDER_CHOICE,blank=True,null=True)
    status_user=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.email

    def get_url(self):
        return reverse('posts',args=[self.user.username])

class FriendRequest(models.Model):
    sender=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='sender')
    receiver=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='receiver')

    def __str__(self):
        return self.receiver.email
    
  