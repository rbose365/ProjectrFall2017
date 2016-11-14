from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import LoginForm, RegisterForm, ProjectSubmissionForm
from models import User, Project
from samples import *

user_type_logged_in = None
def redirect_user_to_homepage(user):
    if user.user_type == 'S':
        return HttpResponseRedirect("/student/")
    elif user.user_type == 'I':
        return HttpResponseRedirect("/instructor/")
    elif user.user_type == 'C':
        return HttpResponseRedirect("/client/")
    else:
        assert False, "Invalid user type for user " + user.email


# Create your views here.
def index(request):
    global user_type_logged_in
    user_type_logged_in = None
    return render(request, "index.html")

def login(request):
    if request.method == "POST":
        blank_form = LoginForm() # Used only if the login fails
        form = LoginForm(request.POST)
        form.is_valid()
        print "Login Sumbitted:", form.cleaned_data
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        # useful stuff
        # https://docs.djangoproject.com/en/1.10/topics/db/queries/
        # Retrieve user from the database:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Re-render the login with a failure message
            return render(request, "login.html", { "invalid_email": True, "form": blank_form })

        # Check that the passwords match
        if user.password == password:
            # Redirect the user to their home page
            return redirect_user_to_homepage(user)
        else:
            # Reject the login and notify that the password was wrong
            return render(request, "login.html", { "invalid_password": True, "form": blank_form })
    else: # GET request
        form = LoginForm()
    return render(request, "login.html", { "form": form })

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        form.is_valid()
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user_type = form.cleaned_data["user_type"]
        print "Register Submitted:", form.cleaned_data

        new_user = User(email=email, password=password, user_type=user_type)
        new_user.save() # save the new user to the database

        return redirect_user_to_homepage(new_user)
    else:
        form = RegisterForm()
    return render(request, "register.html", { "form": form })

def instructor(request):
    return render(request, "instructor.html", test_instructor)

def client(request):
    if request.method == "POST":
        # User submitted a project, add this project to the database (first ask an instructor?)
        form = ProjectSubmissionForm(request.POST)
        form.is_valid()

        name = form.cleaned_data["name"]
        requirements = form.cleaned_data["requirements"]
        keywords = form.cleaned_data["keywords"]
        description = form.cleaned_data["description"]

        new_project = Project(name=name,
                              requirements=requirements,
                              keywords=keywords,
                              description=description)

        new_project.save()
    else:
        form = ProjectSubmissionForm()
        test_client["form"] = form
    return render(request, "client.html", test_client)

def student(request):
    return render(request, "student.html", test_student)

def projects(request):
    # PSEUDO
    # map to a dictionary for rendering
    # return render(request, "projects.html",  projects)

    # Read in all projects from the database, maybe we want to limit this to projects that are not awarded (or just remove projects that are awarded)
    projects = Project.objects.all()
    return render(request, "projects.html", { "projects": projects })

def project(request, project_id):
    print project_id
    proj = Project.objects.get(id=int(project_id))
    return render(request, "project.html", { "project": proj })

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
