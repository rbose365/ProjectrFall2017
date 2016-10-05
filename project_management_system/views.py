from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import LoginForm, RegisterForm
from samples import *

user_type_logged_in = None

# Create your views here.
def index(request):
    global user_type_logged_in
    user_type_logged_in = None
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
        global user_type_logged_in
        if email == test_student["email"]:
            user_type_logged_in = "student"
            return HttpResponseRedirect("/student/")
        elif email == test_instructor["email"]:
            user_type_logged_in = "instructor"
            return HttpResponseRedirect("/instructor/")
        elif email == test_client["email"]:
            user_type_logged_in = "client"
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

def messages(request):
    return render(request, "messages.html", test_messages)

def menu(request):
    print user_type_logged_in
    if user_type_logged_in is None:
        return render(request, "index.html")
    elif user_type_logged_in == "student":
        return render(request, "student.html", test_student)
    elif user_type_logged_in == "instructor":
        return render(request, "instructor.html", test_instructor)
    elif user_type_logged_in == "client":
        return render(request, "client.html", test_client)
    else:
        assert False, "Should never reach here"
