from django.shortcuts import render, redirect
from django import *
from .forms import AdminLoginForm

# Create your views here.
def index(req):
    return render(req,'index.html')

def adhome(req):
    return render(req,'ad`home.html')
from django.contrib import messages

def adminlogin(req):
    if req.method == 'POST':
        form = AdminLoginForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if username == "admin" and password == "ad@1234":
                messages.success(req, "Admin login successful!")
                return redirect('index')   
            else:
                messages.error(req, "Invalid credentials")
    else:
        form = AdminLoginForm()

    return render(req, 'adhome.html', {'form': form})
