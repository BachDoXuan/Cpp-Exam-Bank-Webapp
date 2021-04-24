from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import SignInForm, SignUpForm

# Create your views here.
def signup(request):
    email_existed = False
    username_existed = False
    if request.method == 'POST':
        print(request.POST)
        form = SignUpForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).count() > 0:
                email_existed = True
            elif User.objects.filter(username=form.cleaned_data['username']).count() > 0:
                username_existed = True
            else:
                user = User.objects.create_user(form.cleaned_data['username'],
                                                form.cleaned_data['email'],
                                                form.cleaned_data['passwd'])
                user.is_active = False
                user.first_name = form.cleaned_data['firstname']
                user.last_name = form.cleaned_data['lastname']
                user.save()
                return redirect('index')
    else:
        form = SignUpForm()
    context = {
        'form':form,
        'email_existed': email_existed,
        'username_existed': username_existed
    }
    return render(request, 'signup.html', context)

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('index')

    return render(request, 'signin.html')

def signout(request):
    logout(request)
    return redirect('index')