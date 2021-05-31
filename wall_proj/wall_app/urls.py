from django.urls import path, include
from . import views

urlpatterns = [
     path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('wall', views.wall),
    path('add-message', views.add_message),
    path('add-comment', views.add_comment),
    path('delete/<int:message_ID>', views.delete_message),
    path('edit/<int:message_ID>', views.edit_message),
    path('modify-message', views.modify_message),
]