from django.db import models
from django.db.models import Count

class QuestionManager(models.Manager):
    def create_question(self, title1, text1, author1, likes1, tags1 ):
        question = self.model(title=title1, text=text1, tags=tags1, author=author1, likes=likes1)
        question.save()
        return question

    def get_new_questions(self):
        return self.order_by('-created_at')

    def get_hot_questions(self):
        return self.order_by('-likes', '-created_at')
    
    def get_questions_by_tag(self, tag):
        return self.filter(tags__name=tag)

class AnswerManager(models.Manager):
    def create_answer(self, text1, author1, likes1, correct1, question1):
        answer = self.model(question=question1, text=text1, author=author1, likes=likes1, correct=correct1)
        answer.save()
        return answer
    
    def sort_by_likes(self):
        return self.order_by('-likes')

class TagManager(models.Manager):
    def create_tag(self, name1):
        tag = self.model(name=name1)
        tag.save()
        return tag
    
    def get_best_tags(self):
        return self.order_by('created_at')

class ProfileManager(models.Manager):
    def create_profile(self, user):
        profile = self.model(user=user, nickname=user.username)
        profile.save()
        return profile

class LikeQuestionManager(models.Manager):
    def get_likes_for_question(self, exactQuestion):
        return self.filter(question=exactQuestion)

class LikeAnswerManager(models.Manager):
    def get_likes_for_answer(self, exactAnswer):
        return self.filter(answer=exactAnswer)       