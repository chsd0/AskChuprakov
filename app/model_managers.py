import json
from django.db import models
from django.db.models import Count
import app.models 

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
    
    def correct_async(self, request, answer_id):
        body = json.loads(request.body)
        answer = app.models.Answer.objects.filter(id=answer_id).get()
        correct = answer.correct

        if correct:
            answer.correct = False
        else:
            answer.correct = True
        answer.save()
        
        body['correct'] = answer.correct
        return body
    
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
    
    def like_async(self, request, question_id):
        body = json.loads(request.body)
        question = app.models.Question.objects.filter(id=question_id).get()
        profile = app.models.Profile.objects.filter(user=request.user).get()
        try:
            question_like, question_like_created = app.models.LikeQuestion.objects.get_or_create(question=question, author=profile)
        except app.models.LikeQuestion.MultipleObjectsReturned:
            question_like = app.models.LikeQuestion.objects.filter(question=question, author=profile).first()
            question_like_created = 0

        if not question_like_created:
            question_like.delete()
        
        body['likes_count'] = app.models.LikeQuestion.objects.filter(question=question).count()
        question.likes = app.models.LikeQuestion.objects.filter(question=question).count()
        question.save()
        return body

class LikeAnswerManager(models.Manager):
    def get_likes_for_answer(self, exactAnswer):
        return self.filter(answer=exactAnswer)       
    
    def like_async(self, request, answer_id):
        body = json.loads(request.body)
        answer = app.models.Answer.objects.filter(id=answer_id).get()
        profile = app.models.Profile.objects.filter(user=request.user).get()
        answer_like, answer_like_created = app.models.LikeAnswer.objects.get_or_create(answer=answer, author=profile)

        if not answer_like_created:
            answer_like.delete()
        
        body['likes_count'] = app.models.LikeAnswer.objects.filter(answer=answer).count()
        answer.likes = app.models.LikeAnswer.objects.filter(answer=answer).count()
        answer.save()
        return body