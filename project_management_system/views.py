from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import LoginForm, RegisterForm
from samples import *

# Create your views here.
def index(request):
    return render(request, "index.html")

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        form.is_valid()
        print "Login Sumbitted:", form.cleaned_data
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        # DEMO check for hard-coded user for demo
        print email, password
        print test_student["email"] == email
        if email == test_student["email"]:
            return HttpResponseRedirect("/student/")
        elif email == test_instructor["email"]:
            return HttpResponseRedirect("/instructor/")
        elif email == test_client["email"]:
            return HttpResponseRedirect("/client/")
        # ENDDEMO
    else:
        form = LoginForm()
    return render(request, "login.html", { "form": form })

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        form.is_valid()
        print "Register Submitted:", form.cleaned_data
    else:
        form = RegisterForm()
    return render(request, "register.html", { "form": form })

def instructor(request):
    return render(request, "instructor.html", test_instructor)

def client(request):
    return render(request, "client.html", test_client)

def student(request):
    return render(request, "student.html", test_student)

def projects(request):
    return render(request, "projects.html", test_projects)

def project(request):
    return render(request, "project.html", test_project)
