# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index),
    path('page-detector', views.home, name='home'),
    path('messages/', views.messages, name='messages'),
    path('upload/', views.upload, name='views.upload'),
    path('predict', views.predict),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
]
