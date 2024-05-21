from django.core.management.base import BaseCommand
from random import choice, random
from app.models import *

class Command(BaseCommand):

    help = "TEST FUNCTION"

    def handle(self, *args, **kwargs):
        profiles = Profile.objects.all()
        questions = Question.objects.all()
        answers = Answer.objects.all()
        question_likes = []
        answer_likes = []
        for _ in range(profiles.count() * 200):
                    user = choice(profiles)
                    if(random() > 0.5):
                        question = choice(questions)
                        question_likes.append(LikeQuestion(author=user, question=question))
                    else:
                        answer = choice(answers)
                        answer_likes.append(LikeAnswer(author=user, answer=answer))

        LikeAnswer.objects.bulk_create(answer_likes)
        LikeQuestion.objects.bulk_create(question_likes)