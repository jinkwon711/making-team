from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from .forms import MypageForm
from django.contrib.auth.models import User
# Create your views here.


@login_required
def profile_edit(request):

    # profile = Profile.objects.get(user=request.user)
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
    # print profile.user
    if request.method == "POST":
        form = MypageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('/mypage')
    else:
        form = MypageForm(instance=profile)
        return render(request,'tobusan/mypage_edit.html',{'profile':profile, 'form':form})
