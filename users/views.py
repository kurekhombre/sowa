from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm


# Create your views here.
def login_user(request):

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You're in :)")
            return redirect(request.GET['next'] if next in request.GET else 'index')
        else:
            messages.error(request, "Username or password is incorrect")

    return render(
        request,
        'users/login_register.html'
    )


def logout_user(request):
    logout(request)
    messages.info(request, "User was logged out")
    return redirect('login')


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was created")

            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "An error has occurred during registration")

    return render(
        request,
        'users/login_register.html',
        context={
            'page': page,
            'form': form,
        }
    )


@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile
    topics = profile.topic_set.all()

    return render(
        request,
        'users/account.html',
        context={
            'profile': profile,
            'topics': topics
        }
    )

@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    return render(
        request,
        'users/profile_form.html',
        context={
            'form': form
        }
    )