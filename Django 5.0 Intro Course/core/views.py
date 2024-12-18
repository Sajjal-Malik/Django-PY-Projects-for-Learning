# from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    # return HttpResponse("Hello from home")
    return render(request, 'home.html')

def aboutpage(request):
    # return HttpResponse("Hi from about")
    return render(request, 'about.html')