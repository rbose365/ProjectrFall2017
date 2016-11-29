from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import LoginForm, RegisterForm, ProjectSubmissionForm, MessageForm, BidSubmissionForm, NewSectionForm
from models import Project, Message, Bid, Section, Notification
from views_utils import redirect_user_to_homepage


def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.user.is_authenticated():
        return redirect_user_to_homepage(request.user.profile.user_type)

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


def logout_view(request):
    logout(request) # doesn't throw if user not logged in, just silently does nothing
    return HttpResponseRedirect("/")


def register(request):
    if request.user.is_authenticated():
        return redirect_user_to_homepage(request.user.profile.user_type)

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

            if user_type == 'I' or user_type == 'S':

                # Create an introduction notification
                subject = "Welcome to Groupr"
                body = "Anything is possible at Groupr. The infinite is possible at Groupr. The unattainable is unknown at Groupr. This Groupr. This is Groupr."
                new_notif = Notification(recipient=user, subject=subject, text=body)
                new_notif.save()

                # When an instructor is made, allow them to register a section
                return HttpResponseRedirect("/makesection/")
            else:
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
    bids = Bid.objects.filter(instructors__id=request.user.id)
    notifications = Notification.objects.filter(recipient__id=request.user.id)
    return render(request, "instructor.html", { "notifications":notifications, "inbox": messages, "bids": bids })


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
    projects = Project.objects.filter(client_id=request.user.id)
    context = {
            "bids": bids,
            "form": form,
            "projects": projects
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
    notifications = reversed(Notification.objects.filter(recipient__id=request.user.id))
    form = MessageForm()
    context = {
            "projects": projects,
            "inbox": messages,
            "form": form,
            "notifications": notifications
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
            team_members = form.cleaned_data["team_members"]
            description = form.cleaned_data["description"]
            section = Section.objects.get(students__id=request.user.id)

            new_bid = Bid(team_members=team_members, description=description, project=proj, is_approved=False, student=request.user)
            new_bid.save()
            new_bid.instructors.set(section.instructors.all())

            bid_success = True # TODO notify the user on the UI that the bid was submitted

            new_notification = Notification(recipient=request.user, subject="Bid on \"{}\" submitted.".format(proj.name),
                                            text="You submitted a bid with team members {}.  \
                                                  If the bid is awarded, you will receive \
                                                  another notification here.".format(team_members))
            new_notification.save()
    form = BidSubmissionForm()
    context = {
            "project": proj,
            "form": form,
            "success": bid_success # For showing a message that the bid was successfully saved
    }
    return render(request, "project.html", context)

def messages(request):
    return render(request, "messages.html")


@login_required
def make_a_section(request, section_id):
    if section_id != "":
        # User is choosing to join an existing section
        section = Section.objects.get(id=int(section_id))
        if request.user.profile.user_type == 'S':
            section.students.add(request.user)
        elif request.user.profile.user_type == 'I':
            section.instructors.add(request.user)
        else:
            assert False, "Invalid user type"
        return redirect_user_to_homepage(request.user.profile.user_type)

    if request.method == "POST":
        # Class is being submitted
        form = NewSectionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            new_section = Section(name=name)
            new_section.save()
            new_section.instructors.add(request.user)
            return redirect_user_to_homepage(request.user.profile.user_type)

    form = NewSectionForm()
    sections = Section.objects.all()
    context = {
            "form": form,
            "sections": sections
    }
    return render(request, "makesection.html", context)
