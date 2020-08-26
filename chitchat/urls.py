"""chitchat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from django.contrib.auth.views import LoginView, LogoutView


from chat.views import HomeView
from django.conf import settings

app_name = 'chat'
urlpatterns = [
    path('', HomeView.as_view()),
    path('chat/', include('chat.urls')),
    path('accounts/login/', LoginView.as_view(template_name='chat/registration/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('auth-jwt/', obtain_jwt_token),
    path('auth-jwt/refresh/', refresh_jwt_token),
    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

