#-*- coding: utf-8 -*-


from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django import forms

GENDER_CHOICES=(
    ('남성','남성'),
    ('여성','여성'),
    )

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to="profile")
    gender = models.CharField(max_length=10,choices = GENDER_CHOICES)
    interest = models.TextField()

    def __str__(self):
        return self.user.username