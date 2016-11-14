from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    USER_TYPES = (
        ('S', 'Student'),
        ('I', 'Instructor'),
        ('C', 'Client')
    )
    email = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_type = models.CharField(max_length=1, choices=USER_TYPES)

class Question(models.Model):
    text = models.CharField(max_length=255)

class Student(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)   # Has a (Student <-> Question) ; one to many

class Bid(models.Model):
    description = models.CharField(max_length=255)
    is_approved = models.BooleanField()

class Group(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)   # Belongs to (Student <-> Group) ; many to one
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE)   # Has (Group <-> Bid) ; one to many

class Project(models.Model):
    name = models.CharField(max_length=255)
    requirements = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE)   # For (Bid <-> Project) ; many to one
    question = models.ForeignKey(Question, on_delete=models.CASCADE)   # About (Question <-> Project) ; many to one

class Section(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)   # Is in (Group <-> Section) ; many to one
    projects = models.ManyToManyField(Project)   # Can be awarded to (Section <-> Project) ; many to many

class Instructor(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    sections = models.ManyToManyField(Section)   # Teaches (Instructor <-> Section) ; many to many

class Client(models.Model):
    email = models.CharField(max_length=255, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)   # Contracted By (Client <-> Project) ; one to many
