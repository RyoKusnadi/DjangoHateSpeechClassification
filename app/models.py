# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255)
    sentiment = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)

    def __str__(self):
        return self.message
