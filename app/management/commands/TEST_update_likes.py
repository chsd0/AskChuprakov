from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker
from random import choice, random, randint
from app.models import *
from django.db.models import Count

class Command(BaseCommand):

    help = "TEST FUNCTION"

    def handle(self, *args, **kwargs):
        for i in LikeAnswer.objects.all():
            like_count = LikeAnswer.objects.filter(answer=i.answer).count()
            i.answer.likes = like_count
            i.answer.save()
        for i in LikeQuestion.objects.all():
            i.question.likes = LikeQuestion.objects.filter(question=i.question).count()
            i.question.save()
        self.stdout.write(self.style.SUCCESS('done'))