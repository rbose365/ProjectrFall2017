from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from views_utils import redirect_user_to_homepage
from models import Bid, Notification, Project, Question, Section, Tag, Message
from forms import QuestionForm, ReplyForm, ProfileForm
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

@login_required
def award_bid(request, bid_id):
    bid = Bid.objects.get(id=int(bid_id))
    new_notification = Notification(recipient=bid.student, subject="Bid Awarded",
                                    text="Your bid on the project '{}' was awarded by your instructors!" \
                                         " This will be your project. Contact your client at {}".format(bid.project.name, bid.project.client.email))
    new_notification.save()
    bid.project.is_assigned = True
    bid.student.profile.bids.all().delete()
    Bid.objects.filter(project=bid.project).delete()
    bid.project.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def reject_bid(request, bid_id):
    bid = Bid.objects.get(id=int(bid_id))
    new_notification = Notification(recipient=bid.student, subject="Bid Rejected",
                                    text="Your bid on the project '{}' was rejected by your instructors." \
                                         " Please browse and continue submitting more bids.".format(bid.project.name))
    new_notification.save()
    bid.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def approve_project(request, project_id):
    proj = Project.objects.get(id=int(project_id))
    proj.is_approved = True
    proj.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def reject_project(request, project_id):
    proj = Project.objects.get(id=int(project_id))
    new_notification = Notification(recipient=proj.client, subject="Project Rejected",
                                    text="The instructor decided that your project '{}' submission was not right for the" \
                                          " scope of the course and has decided not to allow students to bid on it.".format(proj.name))
    new_notification.save()
    proj.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def reply_to_question(request, question_id):
    question = Question.objects.get(id=int(question_id))
    form = ReplyForm(request.POST)
    if form.is_valid():
        question.reply = form.cleaned_data["text"]
        question.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required
def delete_a_notification(request, notification_id):
    """
    Deletes a notification
    """
    Notification.objects.get(id=notification_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required
def delete_a_message(request, message_id):
    """
    Deletes a message
    """
    Message.objects.get(id=message_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))