from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import LoginForm, RegisterForm, ProjectSubmissionForm, MessageForm, BidSubmissionForm
from models import Project, Message, Bid

def redirect_user_to_homepage(user_type):
    """
    Redirect a user to a particular home page based on their
    user type (i.e student, instructor, client)
    """
    if user_type == 'S':
        return HttpResponseRedirect("/student/")
    elif user_type == 'I':
        return HttpResponseRedirect("/instructor/")
    elif user_type == 'C':
        return HttpResponseRedirect("/client/")
    else:
        assert False, "Invalid user type for user"


def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == "POST": # User attempting to log in
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(username=email, password=password)
            if user is not None:
                # User was successfully authenticated, redirect them to their home page
                login(request, user)
                return redirect_user_to_homepage(user.profile.user_type)

        # Reject the login and notify that the email / password was wrong
        blank_form = LoginForm()
        return render(request, "login.html", { "invalid": True, "form": blank_form })
    else: # GET request
        form = LoginForm()
        return render(request, "login.html", { "form": form })


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user_type = form.cleaned_data["user_type"]

            new_user = User.objects.create_user(email,
                                                email=email,
                                                password=password)
            new_user.profile.user_type = user_type
            new_user.save() # save the new user to the database

            user = authenticate(username=email, password=password)
            assert user is not None # Considering we just added this entry above, this should never happen
            login(request, user)
            return redirect_user_to_homepage(user_type)
        else:
            blank_form = RegisterForm()
            return render(request, "register.html", { "invalid": True, "form": blank_form })
    else:
        form = RegisterForm()
        return render(request, "register.html", { "form": form })


@login_required
def instructor(request):
    messages = Message.objects.filter(recipient__id=request.user.id)
    return render(request, "instructor.html", { "inbox": messages })


@login_required
def client(request):
    if request.method == "POST":
        # User submitted a project, add this project to the database
        form = ProjectSubmissionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            requirements = form.cleaned_data["requirements"]
            keywords = form.cleaned_data["keywords"]
            description = form.cleaned_data["description"]

            new_project = Project(name=name,
                                  requirements=requirements,
                                  keywords=keywords,
                                  description=description,
                                  client=request.user)

            new_project.save()
        else:
            # TODO indicate some kind of failure
            pass
    form = ProjectSubmissionForm()
    bids = Bid.objects.filter(project__client__id=request.user.id)
    context = {
            "bids": bids,
            "form": form
    }
    return render(request, "client.html", context)


@login_required
def student(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            try:
                sender = request.user
                recipient = User.objects.get(email=form.cleaned_data["recipient"])
                subject = form.cleaned_data["subject"]
                text = form.cleaned_data["text"]

                new_message = Message(sender=sender,
                                      recipient=recipient,
                                      subject=subject,
                                      text=text)

                new_message.save()
            except KeyError:  #TODO Is this the right error?
                # TODO indicate that recipient does not exist
                pass
        else:
            # TODO indicate some kind of failure
            pass

    projects = Project.objects.all()[:5] # This is efficient according to docs, although it doesn't look that way
    messages = Message.objects.filter(recipient__id=request.user.id)
    # TODO notifications
    form = MessageForm()
    context = {
            "projects": projects,
            "inbox": messages,
            "form": form
    }
    return render(request, "student.html", context)


def projects(request):
    # Read in all projects from the database, maybe we want to limit this to projects that are not awarded (or just remove projects that are awarded)
    projects = Project.objects.all()
    return render(request, "projects.html", { "projects": projects })


@login_required
def project_view(request, project_id):
    proj = Project.objects.get(id=int(project_id))
    bid_success = False
    if request.method == "POST":
        # User submitted a bid on this project
        form = BidSubmissionForm(request.POST)
        if form.is_valid():
            # TODO how do we know which instructor to assign to this?
            team_members = form.cleaned_data["team_members"]
            description = form.cleaned_data["description"]
            new_bid = Bid(team_members=team_members, description=description, project=proj, is_approved=False, student=request.user)
            new_bid.save()
            bid_success = True

            # TODO add a notification to this user
    form = BidSubmissionForm()
    context = {
            "project": proj,
            "form": form,
            "success": bid_success # For showing a message that the bid was successfully saved
    }
    return render(request, "project.html", context)

def messages(request):
    return render(request, "messages.html")

def menu(request):
    pass
    # print user_type_logged_in
    # if user_type_logged_in is None:
    #     return render(request, "index.html")
    # elif user_type_logged_in == "student":
    #     return render(request, "student.html", test_student)
    # elif user_type_logged_in == "instructor":
    #     return render(request, "instructor.html", test_instructor)
    # elif user_type_logged_in == "client":
    #     return render(request, "client.html", test_client)
    # else:
    #     assert False, "Should never reach here"
