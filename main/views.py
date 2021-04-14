from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from main.models import Contact, Lectures
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import subprocess 
import os

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



# def contactform(request):
#     form = Contact.objects.all()
#     return render(request, 'main/contact.html', 
#     {"form":form}
#     )

def create_lecture(request):
    if request.method=='POST':

        apikey = 'wiMX7H_yC9WT-eCVQjVFb4JnsDTTY2Si7bymAKmfg1GQ'
        url = 'https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/cbfc812d-7c73-41a8-b254-83b8fa26a64f'
        authenticator = IAMAuthenticator(apikey)
        stt = SpeechToTextV1(authenticator = authenticator)
        stt.set_service_url(url)
        files = []
        filename= os.path.join(os.path.dirname(os.path.dirname(__file__)),r'NoteMe\output.wav')
        results = []
        with open(filename, 'rb') as f:
            res = stt.recognize(audio=f, content_type='audio/wav', model='en-GB_NarrowbandModel', continuous=True, \
                    inactivity_timeout=360).get_result()
        results.append(res)
        lec_notes = res['results'][0]['alternatives'][0]['transcript']
        lecture = Lectures(notes=lec_notes)
        lecture.save()
        return redirect('homepage')
    else:
        return render(request, 'main/record.html')
