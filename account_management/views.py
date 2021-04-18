from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import SignInForm

# Create your views here.
def signup(request):
    return render(request, 'signup.html')

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