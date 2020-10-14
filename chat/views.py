from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
from django.views.generic.base import View
from django.views.generic.list import ListView
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.response import Response

from chat.forms import SignUpForm
from .models import *

from django.views.generic import TemplateView
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, get_object_or_404

from chat.api.serializers import (FriendRequestSerializer,
                                  FriendListSerializer,)
from .serializers import LeadSerializer


class FriendRequestAcceptAPIView(CreateAPIView):
    serializer_class = FriendRequestSerializer
    queryset = User.objects.all()


class FriendListView(ListView):
    template_name = 'friend_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return user.friends.all()
        else:
            return None


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        user = self.request.user
        friends = None

        if user.is_authenticated:
            friends = user.friends.all()
        context['friends'] = friends
        return context


class InboxView(View):
    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('user')
        obj = None
        context = None
        try:
            obj = User.objects.get(username=username)
        except:
            pass
        if obj:
            user = request.user
            my_name = user.username
            thread_obj = Thread.objects.get_thread(my_name, username)
            messages = Message.objects.filter(thread=thread_obj)
            lm = {}
            friends = user.friends.all()
            for friend in friends:
                t_o = Thread.objects.get_thread(my_name, friend)
                lm[friend] = Message.objects.filter(thread=t_o).last() or 'na'

            print(lm)
            context = {
                'obj': obj,
                'username': username,
                'messages': messages,
                'friends': friends,
                'last_messages': lm
            }
        else:
            # return httpresponse
            pass

        return render(request, template_name='inbox.html', context=context)


@api_view(('GET',))
def notify_friend(request, id):
    channel_layer = get_channel_layer()
    obj = User.objects.safe_get(id=id)

    if obj is not None:
        print('this is my channel')
        challenger = request.user.id
        player_id = obj.id
        group_name = 'room_%s' % player_id
        async_to_sync(channel_layer.group_send)(group_name, {
            "type": "notify",
            "text_data": 'A challenge from %s' % challenger
        })

        # async_to_sync(channel_layer.send)('ch', {
        #     "type": "notify",
        #     "text_data": 'A  from %s' % challenger,
        # })

        return Response({'message': "Challenge sent!"}, status=status.HTTP_200_OK)

    else:
        pass
    return Response({'message': "User does not exist!"}, status=status.HTTP_404_NOT_FOUND)


def chat(request, username):
    return render(request, 'room.html', {'username': username})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('chat:home')
    else:
        form = SignUpForm()
    return render(request, 'chat/registration/signup.html', {'form': form})


# def lead
#     if request.method == 'POST':
#         first_name = request.post.get('first_name')
#         last_name = request.post.get('last_name')
#         email = request.post.get('email')
#
#         LeadData.objects.create(first_name=first_name, last_name=last_name, email=email)
#         return HttpResponseRedirect('lead_data')
#

class LeadAPIView(CreateAPIView):
    queryset = LeadData.objects.all()
    serializer_class = LeadSerializer
    authentication_classes = []
    permission_classes = []


