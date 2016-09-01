# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from accounts.models import Profile
from django.contrib import auth
from django.db import models
from django.conf import settings
import datetime
from django.core.files import File
from django.db.models.signals import pre_save
from tobusan.pil_image import thumbnail,square_image
from django.core.urlresolvers import reverse


'''
class Category(models.Model):
    name = models.CharField(max_length=40)
    parent = models.ForeignKey('self')
'''


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=40, choices=(), default='')
    base_category = models.ForeignKey(Category)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=40)
    content = models.TextField()
    image = models.ImageField(upload_to='post_image')
    category = models.ForeignKey(SubCategory)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    min_member_counts = models.SmallIntegerField()
    max_member_counts = models.SmallIntegerField()
    deadline = models.SmallIntegerField()

    def __str__(self):
        return self.title

    def add_tags(self, tag_names,pk):
        for tag_name in tag_names.split(','):
            tag_name = tag_name.strip()
            if tag_name:
                tag, is_created = Tag.objects.get_or_create(name=tag_name)
                post = Post.objects.get(pk=pk)
                tag.post.add(post)


class Tag(models.Model):
    name = models.CharField(max_length=40)
    post = models.ManyToManyField(Post)

    def __str__(self):
        return self.name

    def list_of_post(self):
        return "\n"+", ".join(p.title for p in self.post.all())


def pre_on_post_save(sender,**kwargs):
    post = kwargs['instance']
    if post.image:
        max_height=300
        if post.image.width>max_height or post.image.height>max_height:
            processsed_file =square_image(post.image.file,max_height)
            post.image.save(post.image.name,File(processsed_file))
pre_save.connect(pre_on_post_save, sender=Post)

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.CharField(max_length=100)
    create_at = models.DateTimeField(default=datetime.datetime.now())
    post = models.ForeignKey(Post)

class Apply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)

    def __str__(self):
        return self.user.username









# Create your models here.
