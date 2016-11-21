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

class Bid(models.Model):
    description = models.CharField(max_length=255)
    is_approved = models.BooleanField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)   # For (Bid <-> Project) ; many to one

class Question(models.Model):
    text = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)   # About (Question <-> Project) ; many to one

class Student(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)   # Has a (Student <-> Question) ; one to many

class Client(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)   # Contracted By (Client <-> Project) ; one to many

class Group(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)   # Belongs to (Student <-> Group) ; many to one
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE)   # Has (Group <-> Bid) ; one to many

class Section(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)   # Is in (Group <-> Section) ; many to one
    projects = models.ManyToManyField(Project)   # Can be awarded to (Section <-> Project) ; many to many

class Instructor(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    sections = models.ManyToManyField(Section)   # Teaches (Instructor <-> Section) ; many to many

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient")
    subject = models.CharField(max_length=255)
    text = models.TextField()
