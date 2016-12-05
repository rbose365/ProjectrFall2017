from django.contrib.auth.decorators import login_required
from views_utils import redirect_user_to_homepage
from models import Bid, Notification, Project

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
    proj.delete()
    return redirect_user_to_homepage(request.user.profile.user_type)
