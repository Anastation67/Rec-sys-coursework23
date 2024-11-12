from django.shortcuts import render

def about(request):
    return render(request, 'about.html')

def homepage(request):
    return render(request, 'homepage.html')
