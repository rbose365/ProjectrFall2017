from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    USER_TYPES = (
        ('S', 'Student'),
        ('I', 'Instructor'),
        ('C', 'Client')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=1, choices=USER_TYPES)

# These methods are for linking the Profile model with Django built-in User model for authentication
# Reference: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Project(models.Model):
    name = models.CharField(max_length=255)
    requirements = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField()


class Question(models.Model):
    text = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE) # About (Question <-> Project) ; many to one


class Section(models.Model):
    name = models.CharField(max_length=255)
    instructors = models.ManyToManyField(User, related_name="instructors_for_section")
    students = models.ManyToManyField(User, related_name="students_for_section")


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient")
    subject = models.CharField(max_length=255)
    text = models.TextField()


class Bid(models.Model):
    team_members = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_approved = models.BooleanField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE) # For (Bid <-> Project) ; many to one
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    instructors = models.ManyToManyField(User, related_name="instructors_for_bid")


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_recipient")
    subject = models.CharField(max_length=255)
    text = models.TextField()
