from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from forms import LoginForm, RegisterForm, ProjectSubmissionForm, MessageForm, \
        BidSubmissionForm, NewSectionForm, QuestionForm, ReplyForm, ProfileForm, \
        SearchForm, FilteredSearchForm
from django.db.models import Q
from models import Project, Message, Bid, Section, Notification, Question, InstructorKey, Tag
from views_utils import redirect_user_to_homepage
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def index(request):
    """
    Authenticated users will be sent to their home pages,
    unauthenticated users will be sent to the Login / Register home screen
    """
    if request.user.is_authenticated():
        if request.user.is_superuser:
            return HttpResponseRedirect("/admin/")
        return redirect_user_to_homepage(request.user.profile.user_type)
    else:
        return render(request, "index.html")


def login_view(request):
    """
    Endpoint for logins.
    Logged in users will be redirected to their homepage.
    If login fails, they will be redirected to /login to try again.
    Successful login will authenticate them and send them to their homepage
    """
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
    """
    Log the user out and return them to the Login/Register splash screen
    """
    logout(request) # doesn't throw if user not logged in, just silently does nothing
    return HttpResponseRedirect("/")


def register(request):
    """
    Endpoint for new users registering.
    Authenticated users will just be redirected to their homepage.
    If registration fails, the user is redirected to /register and an error appears
    """
    if request.user.is_authenticated():
        return redirect_user_to_homepage(request.user.profile.user_type)

    blank_form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user_type = form.cleaned_data["user_type"]

            currKey = InstructorKey.objects.filter(key = form.cleaned_data["key"]).first()

            if user_type == "I" and currKey is None:
                messages.add_message(request, messages.INFO, 'The Instructor key was incorrect')
                return render(request, "register.html", { "form": form })

            try: # Try and create the new user object
                new_user = User.objects.create_user(email, email=email, password=password)
                new_user.profile.user_type = user_type
                if user_type == 'I':
                    currKey.delete()
                new_user.save() # save the new user to the database
            except IntegrityError:
                # Duplicate email: notify the user and bail on registering
                return render(request, "register.html", { "duplicate_email": True, "form": blank_form })


            user = authenticate(username=email, password=password)
            login(request, user)

            welcome_notification = Notification(recipient=user, subject="Welcome to Projectr", text="")
            welcome_notification.save()

            if user_type == 'S':
                # Allow instructors to join/create a section, students to join a section
                return HttpResponseRedirect("/joinsection/")
            else:
                return redirect_user_to_homepage(user_type)
        else:
            # The form data was bad, display an error
            return render(request, "register.html", { "invalid": True, "form": blank_form })
    else:
        # The user did not try and register, and just needs to see the register form
        return render(request, "register.html", { "form": blank_form })


@login_required
def instructor(request):
    """
    Get all the information from the database to display an instructor's homepage (messages, notifications, bids etc.)
    and then render the page
    """
    messages = Message.objects.filter(recipient__id=request.user.id)
    bids = Bid.objects.all()
    notifications = Notification.objects.filter(recipient__id=request.user.id)
    projs_to_approve = Project.objects.filter(is_approved=False)
    sections = Section.objects.all()

    context = {
        "notifications": notifications.order_by('-id')[:1],
        "notifications_count": notifications.count,
        "messages": messages.order_by('-id')[:1],
        "messages_count": messages.count,
        "bids": bids.order_by('-id')[:1],
        "bids_count": bids.count,
        "projects_to_approve": projs_to_approve.order_by('-id')[:1],
        "projects_count": projs_to_approve.count
    }

    return render(request, "instructor.html", context)


@login_required
def client(request):
    """
    Render the client homepage.
    Grabs what is needed for the client: their projects / bids, notifications, and any questions
    on their projects
    """
    reply_form = ReplyForm()
    bids = Bid.objects.filter(project__client__id=request.user.id).order_by('-id')
    projects = Project.objects.filter(client_id=request.user.id).order_by('-id')
    questions = Question.objects.filter(project__client__id=request.user.id).order_by('-id')
    notifications = Notification.objects.filter(recipient__id=request.user.id).order_by('-id')
    context = {
            "bids": bids.order_by('-id')[:4],
            "bids_count": bids.count,
            "projects": projects.order_by('-id')[:],
            "projects_count": projects.count,
            "questions": questions.order_by('-id')[:],
            "questions_count": questions.count,
            "notifications": notifications.order_by('-id')[:1],
            "notifications_count": notifications.count,
            "reply_form": reply_form
    }
    return render(request, "client.html", context)


@login_required
def student(request):
    """
    Render the student homepage.
    Gets a few projects to display as a sample, and any messages / notifications for the student
    """
    try:
        Section.objects.get(students__id=request.user.id)
    except ObjectDoesNotExist:
        return HttpResponseRedirect("/joinsection/")

    projects = Project.objects.filter(is_approved=True)
    messages = Message.objects.filter(recipient__id=request.user.id)
    notifications = Notification.objects.filter(recipient__id=request.user.id)
    context = {
            "projects": projects.order_by('-id')[:2],
            "projects_count": projects.count,
            "messages": messages.order_by('-id')[:1],
            "messages_count": messages.count,
            "notifications": notifications.order_by('-id')[:1],
            "notifications_count": notifications.count
    }
    return render(request, "student.html", context)


def projects(request):
    """
    Renders the view of the projects page (where users can browse a list of all projects in the system
    """
    projects = Project.objects.filter(is_approved=True).filter(is_assigned=False)
    projects_bid_on = request.user.profile.bids.filter(project__in=projects).values_list('project', flat=True)
    if request.method == "POST":
        form = SearchForm(request.POST)
        searchTerms = form.data["query"].split()
        query = Q()
        for searchTerm in searchTerms:
            query |= Q(name__icontains=searchTerm)
            query |= Q(description__icontains=searchTerm)
            query |= Q(keywords__icontains=searchTerm)
            query |= Q(requirements__icontains=searchTerm)
        projects = Project.objects.filter(is_approved=True).filter(is_assigned=False).filter(query).all()
    else:
        form = SearchForm()
    context = {
            "form": form,
            "projects": projects.order_by('-id'),
            "projects_bid_on": projects_bid_on
    }
    return render(request, "projects.html", context)


@login_required
def project_view(request, project_id):
    """
    Renders an individual project page, where users can ask questions, look at asked questions/responses,
    and submit a bid.
    """
    proj = Project.objects.get(id=int(project_id))
    bid_success = False
    if request.method == "POST":
        # User submitted a bid on this project
        form = BidSubmissionForm(request.POST)
        if form.is_valid():
            team_members = form.cleaned_data["team_members"]
            description = form.cleaned_data["description"]
            section = Section.objects.get(students__id=request.user.id)

            new_bid = Bid(team_members=team_members
                        , description = description
                        , project = proj
                        , is_approved = False
                        , student = request.user)
            new_bid.save()
            request.user.profile.bids.add(new_bid)

            bid_success = True # TODO notify the user on the UI that the bid was submitted

            new_notification = Notification(recipient=request.user, subject="Bid Submitted",
                                            text="You submitted a bid on '{}' with team members {}.\
                                                  If the bid is awarded, you will be \
                                                  notified here.".format(proj.name, team_members))
            new_notification.save()
    bid_on = request.user.profile.bids.filter(project=proj).exists()
    form = BidSubmissionForm()
    questions = Question.objects.filter(project__id=proj.id)
    question_form = QuestionForm()
    context = {
            "project": proj,
            "form": form,
            "bid_success": bid_success, # For showing a message that the bid was successfully saved
            "question_form": question_form,
            "questions": questions,
            "bid_on": bid_on
    }
    return render(request, "project.html", context)
    
def notifications(request):
    """
    Renders the view of the notifications page, where users can browse a list of their notifcations in the system
    """
    # Read in all bids from the database
    bids = Bid.objects.all() 
    bid_count = bids.count()
    sections = Section.objects.all()
    notifications = Notification.objects.filter(recipient__id=request.user.id)
    context = {
            "notifications": notifications
    }
    return render(request, "notifications.html", context)
    
def pendingprojects(request):
    """
    Renders the view of the pending projects page, where users can browse a list of their pending projects in the system
    """
    # Read in all pending projects from the database
    projects_to_approve = Project.objects.filter(is_approved=False)
    context = {
            "projects_to_approve": projects_to_approve
    }
    return render(request, "pendingprojects.html", context)

def bids(request):
    """
    Renders the view of the bids page, where users can browse a list of all bids in the system
    """
    # Read in all bids from the database
    bids = Bid.objects.all() 
    bid_count = bids.count()
    sections = Section.objects.all()
    if request.method == "POST":
        form = FilteredSearchForm(request.POST)
        try:
            filter = form.data["filter"]
            searchTerms = form.data["query"].split()
            query = Q()
            for searchTerm in searchTerms:
                query |= Q(description__icontains=searchTerm)
            bids = Bid.objects.filter(query).all()
        except KeyError:
            pass
        else:
            # TODO indicate some kind of failure
            pass
    else:
        filter = 'all'
        form = FilteredSearchForm()
    context = {
            "form": form,
            "filter": filter,
            "sections": sections,
            "bids": bids.order_by('-id'),
            "bid_count": bid_count
    }
    return render(request, "bids.html", context)

@login_required
def messages(request):
    """
    Render the inbox of the user sending the request
    """
    messages = Message.objects.filter(recipient__id=request.user.id)
    context = {
        "messages": messages
    }
    return render(request, "messages.html", context)
    
@login_required
def send_message(request, message_id):
    """
    Render page where students / instructors can go to send a message to other users
    """
    if (message_id != ''):
        message = Message.objects.get(id=message_id)
        form_init = {'recipient': message.sender,'subject': 'RE: ' + message.subject, 'text': message.reply_text}
    else:
        form_init = {}

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            sender = request.user
            recipient = User.objects.get(email=form.data["recipient"])
            subject = form.data["subject"]
            text = form.data["text"].split('\n     >')[0]
            
            old_reply_text = message.reply_text if message_id != '' else '';
            reply_text = '\n\n'
            reply_lines = ('From: ' + sender.email + '\n' + text + old_reply_text).split('\n')
            for line in reply_lines:
                reply_text = reply_text + '     > ' + line + '\n'

            new_message = Message(sender=sender,
                                  recipient=recipient,
                                  subject=subject,
                                  text=text,
                                  reply_text=reply_text)

            new_message.save()
            return redirect_user_to_homepage(request.user.profile.user_type)
    form = MessageForm(initial=form_init)
    context = {
            "form": form,
    }
    return render(request, "sendmessage.html", context)


@login_required
def join_a_section(request, section_id):
    """
    Render the page where instructors can go to make a new section and
    students can go to join a section
    """
    # Join section
    if section_id != "":
        # If User already belongs to a section, remove them from the original
        if request.user.profile.section != None:
            old_section = Section.objects.get(id=int(request.user.profile.section.id))
            if request.user.profile.user_type == 'S':
                old_section.students.remove(request.user.id)
            else:
                assert False, "Invalid user type"
        section = Section.objects.get(id=int(section_id))
        if request.user.profile.user_type == 'S':
            section.students.add(request.user)
            request.user.profile.section = section
            request.user.profile.save()
        else:
            assert False, "Invalid user type"
        return redirect_user_to_homepage(request.user.profile.user_type)
    sections = Section.objects.all()

    context = {
            "sections": sections
    }
    return render(request, "joinsection.html", context)
    
@login_required
def manage_sections(request):
    """
    Render the page where instructors can go to make a new section or
    edit existing ones.
    """

    if request.method == "POST":
        # Class is being submitted
        form = NewSectionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            new_section = Section(name=name)
            new_section.save()
            return HttpResponseRedirect("/managesection/")

    form = NewSectionForm()
    sections = Section.objects.all()
    context = {
            "form": form,
            "sections": sections,
            "listSize": sections.count()
    }
    return render(request, "managesection.html", context)

@login_required
def edit_a_section(request, section_id):
    """
    Render the page where instructors can go to make a new section and
    students can go to join a section
    """
    if section_id != "":
        # User is choosing to edit the section's name
        form = NewSectionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            section = Section.objects.get(id=int(section_id))
            setattr(section, "name", name)
            section.save()
            return HttpResponseRedirect("/managesection/")

    form = NewSectionForm()
    sections = Section.objects.all()
    context = {
            "form": form,
            "section_id": section_id
    }
    return render(request, "editsection.html", context)
    
@login_required
def submit_project(request, project_id):
    """
    Render page where clients can create/edit a project
    """
    if request.method == "POST":
        print("MADE IT 1");
        form = ProjectSubmissionForm(request.POST)
        if (project_id != ""):
            existing_project = Project.objects.get(id=int(project_id))
            existing_project.name = form.data["name"]
            existing_project.requirements = form.data["requirements"]
            existing_project.keywords = form.data["keywords"]
            existing_project.description = form.data["description"]
            existing_project.save()
        else:
            print("MADE IT 2");
            name = form.data["name"]
            requirements = form.data["requirements"]
            keywords = form.data["keywords"]
            description = form.data["description"]

            new_project = Project(name=name,
                                  requirements=requirements,
                                  keywords=keywords,
                                  description=description,
                                  client=request.user,
                                  is_approved=False)

            new_project.save()
        return HttpResponseRedirect("/client/")
        
    form = ProjectSubmissionForm()
    context = {
            "form": form,
            "project_id": project_id
    }
    return render(request, "submitproject.html", context)

@login_required
def profile(request):
    """
    Endpoint for new users registering.
    Authenticated users will just be redirected to their homepage.
    If registration fails, the user is redirected to /register and an error appears
    """
    form = ProfileForm()
    tags = Tag.objects.filter(students__id=request.user.id)
    context = {
            "tags": tags,
            "form": form
    }
    return render(request, "profile.html", context)
