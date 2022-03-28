from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('index', views.index),
    path('channel/<slug:slug>', views.contents_by_chanel, name="contents_by_chanel"),
    path('contents/<slug:slug>', views.content_details, name="content_details"),
    path('content_detail/<slug:slug>', views.detail, name="detail"),
]
