from django.db import models
from django.contrib.auth.models import AbstractUser
from model_utils.models import TimeStampedModel
from django.db.models.signals import post_save




class CustomUser(AbstractUser, TimeStampedModel):
    username = models.CharField(max_length=250, unique=True)


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        

class Profile(TimeStampedModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username


def create_profile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_profile, sender=CustomUser)






