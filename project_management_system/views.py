from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def client(request):
    return render(request, "client.html")

def student(request):
    return render(request, "student.html")
