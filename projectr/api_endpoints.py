from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from views_utils import redirect_user_to_homepage
from models import Bid, Notification, Project, Question, Section, Tag
from forms import QuestionForm, ReplyForm, ProfileForm
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

@login_required
def award_bid(request, bid_id):
    bid = Bid.objects.get(id=int(bid_id))
    new_notification = Notification(recipient=bid.student, subject="Bid on {} Awarded!".format(bid.project.name),
                                    text="Your bid on the project {} was awarded by your instructor(s)!" \
                                         "This will be your project.  Contact your client at {}".format(bid.project.name, bid.project.client.email))
    new_notification.save()
    bid.delete()
    return redirect_user_to_homepage(request.user.profile.user_type)


@login_required
def reject_bid(request, bid_id):
    bid = Bid.objects.get(id=int(bid_id))
    new_notification = Notification(recipient=bid.student, subject="Bid on {} Rejected".format(bid.project.name),
                                    text="Your bid on the project {} was rejected by your instructor(s)." \
                                         "Please continue browsing and submitting more bids.")
    new_notification.save()
    bid.delete()
    return redirect_user_to_homepage(request.user.profile.user_type)


@login_required
def approve_project(request, project_id):
    proj = Project.objects.get(id=int(project_id))
    proj.is_approved = True
    proj.save()
    return redirect_user_to_homepage(request.user.profile.user_type)


@login_required
def reject_project(request, project_id):
    proj = Project.objects.get(id=int(project_id))
    new_notification = Notification(recipient=proj.client, subject="Project {} Rejected".format(proj.name),
                                    text="The instructor decided that your project submission was not right for the"
                                          "scope of the class and has decided not to allow students to bid on it.")
    new_notification.save()
    proj.delete()
    return redirect_user_to_homepage(request.user.profile.user_type)


@login_required
def ask_question(request, project_id):
    proj = Project.objects.get(id=int(project_id))
    form = QuestionForm(request.POST)
    if form.is_valid():
        new_question = Question(text=form.cleaned_data["question"],
                                project=proj,
                                asker=request.user,
                                reply="")
        new_question.save()
    return HttpResponseRedirect("/project/{}".format(project_id))


@login_required
def reply_to_question(request, question_id):
    question = Question.objects.get(id=int(question_id))
    form = ReplyForm(request.POST)
    if form.is_valid():
        question.reply = form.cleaned_data["text"]
        question.save()
    return redirect_user_to_homepage(request.user.profile.user_type)

@login_required
def delete_a_section(request, section_id):
    """
    Deletes a section if it is not the last section
    """
    if section_id != "":
        sections = Section.objects
        if sections.count() != 1:
            if sections.get(id=int(section_id)).students.count() == 0:
                sections.get(id=int(section_id)).delete()

    return HttpResponseRedirect("/managesection/")

@login_required
def add_tag(request):
    """
    Adds tags to student's profile
    """
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            tags = form.cleaned_data["tags"]
            tags = [x.strip() for x in tags.split(',')]
            for tag in tags:
                #TODO: tags comma separated
                new_tag = Tag(name=tag)
                try:
                    Tag.objects.get(name=tag)
                    new_tag = Tag.objects.get(name=tag)
                    messages.add_message(request, messages.INFO, 'You cannot add the same tags!')
                    return HttpResponseRedirect("/profile/")
                except ObjectDoesNotExist:
                    new_tag.save()
                new_tag.students.add(request.user)
            return redirect_user_to_homepage(request.user.profile.user_type)
        else:
            # The form data was bad, display an error
            return redirect_user_to_homepage(request.user.profile.user_type)
