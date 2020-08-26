from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import File
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from django.db.models.signals import post_save


class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_thread(self, username, other_username):
        qlookup1 = Q(first__username=username) & Q(second__username=other_username)
        qlookup2 = Q(first__username=other_username) & Q(second__username=username)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.exists() and qs.count() == 1:
            return qs.first()

    def get_or_new(self, user, other_username):  # get_or_create
        username = user.username
        print(username)
        if username == other_username:
            return None
        qlookup1 = Q(first__username=username) & Q(second__username=other_username)
        qlookup2 = Q(first__username=other_username) & Q(second__username=username)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            Klass = user.__class__
            user2 = Klass.objects.get(username=other_username)
            if user != user2:
                obj = self.model(
                    first=user,
                    second=user2
                )
                obj.save()
                return obj, True
            return None, False


class Channel(models.Model):
    channel_id = models.CharField(max_length=100)
    user = models.ForeignKey('User', blank=True, related_name='channels', null=True, on_delete=models.SET_NULL)
    thread = models.ForeignKey('Thread', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.channel_id


image_storage = FileSystemStorage(
    # Physical file location ROOT
    location=f'{settings.MEDIA_ROOT}/my_sell',  # u'{0}/my_sell/'.format(settings.MEDIA_ROOT),
    # Url for file
    base_url=f'{settings.MEDIA_URL}/my_sell',  # u'{0}my_sell/'.format(settings.MEDIA_URL)

)


def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/my_sell/picture/<filename>
    return u'picture/{0}'.format(filename)


class User(AbstractUser):
    image = models.ImageField(upload_to=image_directory_path, storage=image_storage, default='user.jpg')
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=True, default="100")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=True, default="100")
    friends = models.ManyToManyField('self', blank=True, related_name='friends')
    friend_requests = models.ManyToManyField('self', blank=True, related_name='friend_requests')
    is_active = models.BooleanField(default=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Thread(models.Model):
    first = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_thread_first')
    second = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_thread_second')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()

    @property
    def room_group_name(self):
        return f'room_{self.id}'

    def broadcast(self, msg=None):
        if msg is not None:
            # broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
            return True
        return False


class Notification(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    opened = models.BooleanField(default=False)
    sender = models.CharField(max_length=30)
    timestamp = models.DateTimeField(blank=True, default=timezone.now)

    def __str__(self):
        return self.message

    def check_notification(self):
        self.opened = True


class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def __str__(self):
        return self.question


class Message(models.Model):
    thread = models.ForeignKey(Thread, null=True, related_name='messages', on_delete=models.CASCADE)
    sender = models.TextField(null=True)
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return self.message


# @receiver(post_save, sender=User)
# def set_image(sender, instance, created, **kwargs):
#     if created:
#         if instance.image is None:
#             f = open('media/user.jpg', 'r')
#             myf = File(f)
#             instance.image.save('user.jpg', myf.read(), True)
#

