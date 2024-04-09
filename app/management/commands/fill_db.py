from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker
from random import choice, random, randint
from app.models import *

class Command(BaseCommand):

    help = "Fill db with thrash"

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        fake = Faker()

        profiles = []
        tags = []
        questions = []
        answers = []

        for i in range(ratio):
            username = str(fake.first_name()) + str(i)
            password = fake.password()
            email = fake.email()
            user = User.objects.create_user(username=username, password=password, email=email)
            profile = Profile.objects.create(user=user, nickname=user)
            profiles.append(profile)

            tag_name = fake.unique.word()
            tag = Tag.objects.create(name = tag_name)
            tags.append(tag)

        for _ in range(ratio * 10):
            title = fake.sentence(nb_words=5)
            text = fake.paragraph(nb_sentences=6)
            author = choice(profiles)
            question = Question.objects.create(title=title, text=text, author=author)
            question_tags = [tags[randint(0,len(tags)-1)] for i in range(5)]
            question.tags.set(question_tags)
            questions.append(question)

        for _ in range(ratio * 100):
            text = fake.paragraph(nb_sentences=6)
            author = choice(profiles)
            question = choice(questions)
            answer = Answer.objects.create(text=text, author=author, question=question)
            answers.append(answer)

        for _ in range(ratio * 200):
            user = choice(profiles)
            if(random() > 0.5):
                question = choice(questions)
                LikeQuestion.objects.create(author=user, question=question)
            else:
                answer = choice(answers)
                LikeAnswer.objects.create(author=user, answer=answer)

        self.stdout.write(self.style.SUCCESS('trash is in!'))