from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, UserUpdate, upgrade_me, subscribe_me


urlpatterns = [

    path('login/',
         LoginView.as_view(template_name = 'sign/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name = 'sign/logout.html'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name='sign/signup.html'),
         name='signup'),
    path('profile/<int:pk>', UserUpdate.as_view(template_name='sign/edit_user.html'),
         name='updateuser'),
    #path('profile/<int:pk>/subscribe', UserUpdate.as_view(template_name='sign/subscibe.html'),
     #    name='subscribe'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path ('subscribe/', subscribe_me, name='subscribe')

]