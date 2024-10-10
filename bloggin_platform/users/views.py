from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .forms import ProfileForm
from .models import Profile, Follow
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

@login_required
def user_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'profile.html', {'profile': profile})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def profile_view(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    if request.user.is_authenticated:
        check_follow = profile.user.followers.all().intersection(request.user.following.all())
    else:
        check_follow = False
    return render(request, 'profile.html', {'profile': profile, 'check_follow': check_follow})

@login_required
def edit_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect('create_profile')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})

def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profile', username=username)

def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile', username=username)