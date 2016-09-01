#-*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register
from .forms import *
from django.contrib import messages
from .models import *
from accounts.models import Profile
from django.http import HttpResponse, Http404
# Create your views here.
def index(request):
    categories = Category.objects.all()
    posts = Post.objects.order_by('-created_at')




    return render(request, 'tobusan/main.html',{'range':range(6),'categories':categories, 'posts':posts})

def base(request):
    return render(request, 'tobusan/base.html',{})

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def form(request):
    return render(request, 'tobusan/form.html',{'form':PostForm ,})


def post_list(request,pk):

    one_subcat = SubCategory.objects.get(name=pk)
    posts = Post.objects.order_by('-created_at').filter(category=one_subcat)
    categories = Category.objects.all()


    return render(request, 'tobusan/main.html', {'posts':posts,'categories':categories,'one_subcat':one_subcat,})

@login_required
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    applicants = Apply.objects.filter(post=post, user=request.user)
    print(applicants)
    print(type(applicants))
    applications = Apply.objects.filter(post=post)
    tags = Tag.objects.filter(post=post)


    if request.method == "POST": # Comment Form

        form = CommentForm(request.POST, request.FILES )
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            form.save()

            messages.success(request,'새 댓글이 등록되었습니다.')  #-> 이거하고 html가서 템플릿태그등
            # return redirect('blog:post_detail', post_pk)
            return redirect("/post/{}".format(pk))
            # 일단 겟 앱솔루트 url이 있는 확인하고 호출.
    else:
        form = CommentForm()
        # comment_list = post.objects.comment_set.all()
        comment_list = Comment.objects.filter(post=post)


    return render(request, 'tobusan/post_detail.html', {
        'post':post,
        'form':form,
        'applicants':applicants,
        'applications':applications,
        'comment_list':comment_list,
        'tags':tags,
        })

def post_apply(request, pk):
    post = get_object_or_404(Post,pk=pk)
    applicants = Apply.objects.filter(post=post)
    if Apply.objects.filter(user=request.user, post=post):
        messages.error(request,"이미 이 그룹에 등록하셨습니다.")
        #이 위에거 작동안함.. ㅠㅠㅠㅠ아으아
        return redirect("/post/{}".format(pk))
    if request.user == post.author:
        pass
    else:
        if applicants.count() >= post.max_member_counts:
            messages.error(request,"본 모임은 모집이 완료되었습니다.")
            return redirect("/post/{}".format(pk))

        else:
            messages.success(request,"본 모임의 신청 요청이 완료되었습니다.")
            Apply.objects.create(post=post, user=request.user)
            return redirect("/post/{}".format(pk))
    messages.error(request,"본인이 작성한 모임글에는 등록 할 수 없습니다.")


    return redirect("/post/{}".format(pk))

def apply_delete(request, pk):
    post = get_object_or_404(Post,pk=pk)
    if Apply.objects.filter(post=post, user=request.user):
        Apply.objects.filter(post=post, user=request.user).delete()
        messages.success(request, '성공적으로 해당 팀에서 탈퇴하였습니다.')
        return redirect("/post/{}".format(pk))
    else:
        messages.warning(request,'비정상적인 접근 경로입니다.')
        return redirect("/post/{}".format(pk))

def apply_delete_admin(request, post_pk, user_pk):
    post = get_object_or_404(Post,pk=post_pk)
    if Apply.objects.filter(post=post, user=user_pk):
        Apply.objects.filter(post=post, user=user_pk).delete()
        messages.success(request, '성공적으로 해당 팀원을 탈퇴시켰습니다.')
        return redirect("/post/{}".format(post_pk))
    else:
        messages.warning(request, '팀장만 삭제할 수 있습니다.')
        return redirect("/post/{}".format(post_pk))

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        context =request.POST
        tags = context.get('user_tag', False)
        # print(tags)

        if form.is_valid():

            postform = form.save(commit=False)
            postform.author = request.user
            form.save()

            # fixed_user_tag = tags.replace(" ","")
            # fixed_user_tag = fixed_user_tag.split('#')
            # for tag in fixed_user_tag:
            #     Tag.objects.create(name=tag, post=)


            fixed_user_tag = tags.replace(" ","")
            fixed_user_tag = fixed_user_tag.split('#')[1:]
            for tag in fixed_user_tag:
                t=Tag.objects.create(name=tag)
                t.save()

                p = Post.objects.get(pk=postform.pk)
                # t.name.add(newtag)
                t.post.add(p)
                # Tag.objects.create(name=tag)
                # Tag.objects.add(post=postform)

            # fixed_user_tag = tags.replace(" ","")
            # fixed_user_tag = fixed_user_tag.split('#')
            # for tag in fixed_user_tag:
            #     t = Tag()
            #     t.save()
            #     t.name.add(tag)
            #     t.post.add(postform)



            return redirect('/')

    else:
        form = PostForm()
    return render(request,"tobusan/post_form.html",
        {
        'form':form,
        })

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES ,instance=post)
            if form.is_valid:
                form.save()
                return redirect('/')
        else:
            form = PostForm(instance=post)
    return render(request, 'tobusan/post_form.html', {'form': form, })

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post,pk=pk)
    if post.author == request.user:
        post.delete()
        messages.success(request,"글이 정상적으로 삭제되었습니다.")
        return redirect("/")
    else:
        messages.error(request,"해당 글 작성자만 삭제할 수 있습니다.")
        return redirect("/post/{}".format(pk))

# def comment_edit(request, post_pk, pk):
#     comment = get_object_or_404(Comment, pk=pk)

#     if request.method == "POST":
#         form = CommentForm(request.POST, request.FILES, instance = comment )
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = get_object_or_404(Post, pk = post_pk)
#             form.save()
#             return redirect('blog:post_detail', post_pk)
#     else:
#         form = CommentForm(instance = comment)

#     return render(request, 'comment_form.html', {'form' :form} )

def comment_delete(request,post_pk,pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author == request.user:
        comment.delete()
        messages.success(request,"댓글이 정상적으로 삭제되었습니다.")
        return redirect("/post/{}".format(post_pk))
    else:
        messages.error(request,"해당 댓글 작성자만 삭제할 수 있습니다.")
        return redirect("/post/{}".format(post_pk))


def mypage(request):
    posts = Post.objects.filter(author=request.user)
    applications = Apply.objects.filter(user=request.user)
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    return render(request, 'tobusan/mypage.html', {'posts':posts, 'applications':applications, 'profile':profile})



def main_search(request):
    categories = Category.objects.all()
    if 'q' in request.GET:
        if request.GET['q']=='':
            message = '관심있는 태그를 입력해주세요'
        else :
            # message ='%s 를 검색하셨습니다' %request.GET['q']
            query = request.GET['q']
            tag = Tag.objects.filter(name =query)
            posts =Post.objects.filter(tag__in =tag)
            if posts.exists():
                return render(request, 'tobusan/main.html',{'posts':posts,'categories':categories})
            else:
                return HttpResponse('존재하지 않는 포스트입니다')
    else:
        return HttpResponse('잘못입력하셨습니다')

    # return render(request, 'tobusan/main.html',{'post':post, 'category':category})

def select_search(request,tag):
    categories = Category.objects.all()
    # t = Category.objects.filter(name=tag)

    posts = Post.objects.filter(category__name = tag)

    return render(request, 'tobusan/main.html',{'posts': posts, 'categories':categories})
