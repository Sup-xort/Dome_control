from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('open/', views.dopen, name='open'),
    path('close/', views.close, name='close'),
    path('power/', views.power, name='power'),
    path('connect/', views.connect, name='connect'),
    path('disconnect/', views.disconnect, name='disconnect'),
]