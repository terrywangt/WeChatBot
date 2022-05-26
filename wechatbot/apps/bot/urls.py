from datetime import datetime
from django.urls import path,re_path
from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [

    url(r'^start/', views.start),
    url(r'^logout/', views.logout),
    url(r'^get_login_info/', views.get_login_info),
    url(r'^get_friend_list/', views.get_friend_list),
    url(r'^get_chat_room_members/', views.get_chat_room_members),
    url(r'^send_text/', views.send_text),
    url(r'^send_link_card/', views.send_link_card),
    url(r'^send_img/', views.send_img),
    #url(r'^send_file/', views.send_file),

]