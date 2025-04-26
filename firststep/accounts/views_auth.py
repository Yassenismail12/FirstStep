from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import User
from cvbuilder.models import CV

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Change this to your dashboard URL name

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')  # Redirect to main app/dashboard
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                firstname=firstname,
                lastname=lastname
            )
            login(request, user)
            return redirect('dashboard')

    return render(request, 'register.html')

@login_required
def dashboard(request):
    cvs = CV.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'cvs': cvs})