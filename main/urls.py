from django.urls import path
from main import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login', views.loginview, name='login'),
    path('register', views.registerview, name='register'),
    path('logout', views.logout, name='logout'),
    path('record', views.create_lecture, name='record'),
    # path('contact', views.contactform, name='contact'),
]