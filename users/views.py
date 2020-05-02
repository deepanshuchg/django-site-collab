from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'users/index.html')

def login(request):
    return render(request,'users/login.html')

def logout(request):
    return render(request,'users/logout.html')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f'Your account has been created, please Log in.')
            return redirect('login')
    else:
        form=UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def youtube(request):
    return render(request, 'users/youtube.html')