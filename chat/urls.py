from django.urls import path
from django.urls.conf import include

from .views import *
app_name = 'chat'

urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('chat/', chat, name='chat'),
    path('inbox/<str:user>', login_required(InboxView.as_view()), name='chat'),
    path('signup/', signup, name='signup'),
    path('friends/', FriendListView.as_view(), name='friends'),
    path('friend/accept/', FriendRequestAcceptAPIView.as_view()),
    # path('notification/<str:room_name>/', room, name='room'),
    path('notify/<str:user_id>/', notify_friend, name='notify_friend'),
    path('lead_data/', LeadAPIView.as_view(), name='lead_data'),
    ]
