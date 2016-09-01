#-*- coding: utf-8 -*-


from .models import *
from django import forms


class PostForm(forms.ModelForm):
    user_tag = forms.CharField(max_length=100,help_text='태그는 해쉬태그로 구분하여 입력해주세요. 예) #야구 #아침운동 #관악구')
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        category_choices = []
        for category in Category.objects.all():
            sub_choices = []
            for sc in category.subcategory_set.all():
                sub_choices.append((sc.id, sc.name))
            category_choices.append((category.name, sub_choices))

        self.fields['category'].choices = category_choices

        # ('value', 'label')
        # ('male', '남자')
        # ('female, '여자'')

    class Meta:
        model = Post
        fields = ['title', 'content','image','category','min_member_counts','max_member_counts','deadline']

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='')
    class Meta:
        model = Comment
        fields = ['content']


class TagForm(forms.ModelForm):


    class Meta:
        model = Tag
        fields = ['name']

