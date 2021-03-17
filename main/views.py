from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.

def homepage(request):
    return render(request, 'main/home.html')

def loginview(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('homepage')
        else:
            messages.info(request, 'The credentials entered are invalid! Try again.')
            return redirect('login')

    else:
        return render(request, 'main/login.html')

def registerview(request):
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['conpassword']
        
        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'The username is already taken! Please use an unique one.')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'This email is already being used! Try signing in.')
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=first_name, username=username, email=email, last_name=last_name, password=password)
                user.save();
                return redirect('login')
        else:
            messages.info(request, 'The passwords do not match!')
            return redirect('register')

        return redirect('homepage')

    else:
        return render(request, 'main/register.html')

def logout(request):
    auth.logout(request)
    return redirect('homepage')