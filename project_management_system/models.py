from __future__ import unicode_literals

from django.db import models

# Test Models (that definitely work)

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

# Real Models (that may work)

class User(models.Model):
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

class Student(models.Model):
    email = models.CharField(max_length=255)

class Instructor(models.Model):
    email = models.CharField(max_length=255)

class Client(models.Model):
    email = models.CharField(max_length=255)

class Group(models.Model):
    name = models.CharField(max_length=255)

class Bid(models.Model):
    description = models.CharField(max_length=255)
    is_approved = models.BooleanField()

class Class(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

"""
class Question(models.Model):
    text = models.CharField(max_length=255)
"""
