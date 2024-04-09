from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from app.model_managers import *

class Tag(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TagManager()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(default=user.name ,max_length=30)
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=300)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuestionManager()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AnswerManager()


class LikeQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    objects = LikeQuestionManager()

class LikeAnswer(models.Model):
    answer = models.ForeignKey(Answer, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    objects = LikeAnswerManager()

