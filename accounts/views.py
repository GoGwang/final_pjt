from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method =="POST":
        form= CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context ={
        'form' : form,
    }
    return render(request, 'accounts/signup.html', context)

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == 'POST':
      form = AuthenticationForm(request, request.POST)
      if form.is_valid():
          auth_login(request, form.get_user())
          return redirect('movies:index') 
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
        'submit': '로그인',
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('accounts:login')

@login_required
@require_http_methods(['GET','POST'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        user = request.user
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', user.username)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)

@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect('movies:index')

@require_http_methods(['GET','POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        user = request.user
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts:profile', user.username)
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form' : form,
    }
    return render(request,'accounts/change_password.html', context)



@login_required
def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)


@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), pk=user_pk)
        user = request.user
        if person != user:
            if person.followers.filter(pk=user.pk).exists():
                person.followers.remove(user)
            else:
                person.followers.add(user)
    return redirect('accounts:profile', person.username)

def followinglist(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/following_list.html', context)

def followerlist(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/follower_list.html', context)

@require_POST
def followerfollow(request, user_pk):
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), pk=user_pk)
        user = request.user
        if person != user:
            if person.followers.filter(pk=user.pk).exists():
                person.followers.remove(user)
            else:
                person.followers.add(user)
    return redirect('accounts:followerlist', person.username)

@require_POST
def followingfollow(request, user_pk):
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), pk=user_pk)
        user = request.user
        if person != user:
            if person.followers.filter(pk=user.pk).exists():
                person.followers.remove(user)
            else:
                person.followers.add(user)
    return redirect('accounts:followinglist', person.username)