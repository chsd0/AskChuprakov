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
        users =[]
        profiles = []
        tags = []
        questions = []
        answers = []
        question_likes = []
        answer_likes = []

        for i in range(ratio):
            username = str(fake.first_name()) + str(i)
            password = fake.password()
            email = fake.email()
            user = User(username=username, password=password, email=email)
            users.append(user)

            profile = Profile(user=user, nickname=user)
            profiles.append(profile)
            
            tag_name = fake.unique.word()
            tag = Tag(name = tag_name)
            tags.append(tag)

        User.objects.bulk_create(users)
        Tag.objects.bulk_create(tags)
        Profile.objects.bulk_create(profiles)

        for _ in range(ratio * 10):
            title = fake.sentence(nb_words=5)
            text = fake.paragraph(nb_sentences=6)
            author = choice(profiles)
            question = Question(title=title, text=text, author=author)
            questions.append(question)

        Question.objects.bulk_create(questions)

        for i in range(ratio * 10):
            question = questions[i]
            question_tags = [tags[randint(0,len(tags)-1)] for j in range(5)]
            question.tags.set(question_tags)

        for _ in range(ratio * 100):
            text = fake.paragraph(nb_sentences=6)
            author = choice(profiles)
            question = choice(questions)
            answer = Answer(text=text, author=author, question=question)
            answers.append(answer)

        Answer.objects.bulk_create(answers)

        for _ in range(ratio * 200):
            user = choice(profiles)
            if(random() > 0.5):
                question = choice(questions)
                question_likes.append(LikeQuestion(author=user, question=question))
            else:
                answer = choice(answers)
                answer_likes.append(LikeAnswer(author=user, answer=answer))

        LikeAnswer.objects.bulk_create(answer_likes)
        LikeQuestion.objects.bulk_create(question_likes)

        self.stdout.write(self.style.SUCCESS('trash is in!'))