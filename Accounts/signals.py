from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save
from .models import Account
from Profile.models import Profile
from Socket.models import Message,Thread,Notifications
from Profile.models import FriendRequest

@receiver(post_save,sender=Account)
def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile=Profile()
        user_profile.user=instance
        user_profile.img='avatar/default-avatar/defaulavatar.jpg'
        user_profile.cover_img='avatar/default-avatar/cover-img.jpg'
        user_profile.save()
        admin=Account.objects.filter(is_admin=True).first()
        try:
            user=Account.objects.get(username='sibitrung4')
            FriendRequest.objects.create(sender=user,receiver=instance)
            Notifications.objects.create(generator=user,user=instance,type='send',link=user.profile.get_url())
            user_profile.friends.add(admin)
            admin.profile.friends.add(instance)
            thread=Thread.objects.get_or_create_personal_thread(admin,instance)
            Message.objects.create(thread=thread,sender=admin,text='Welcome to Hello World!')
        except:
            pass