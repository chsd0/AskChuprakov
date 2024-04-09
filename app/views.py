from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

from app.models import *

# Create your views here.

QUESTIONS = Question.objects.order_by('-created_at')

best_tags = Tag.objects.get_best_tags()[:5]

user_is_logged = True

def index(request):
    page_obj = paginate(QUESTIONS, request.GET.get('page', 1))
    return render(request, "index.html", {"questions": page_obj, "best_tags": best_tags, "user_is_logged": user_is_logged})

def ask(request):
    return render(request, "ask.html", {"user_is_logged": user_is_logged, "best_tags": best_tags})

def hot(request):
    page_obj = paginate(Question.objects.get_hot_questions(), request.GET.get('page', 1))
    return render(request, "hot.html", {"questions":page_obj, "best_tags": best_tags, "user_is_logged": user_is_logged})

def question(request, question_id):
    item = QUESTIONS.get(id=question_id)
    ANSWERS = Answer.objects.filter(question=question_id).order_by('-likes')
    page_obj = paginate(ANSWERS, request.GET.get('page', 1), 3)
    return render(request, "question_detail.html", {"question":item, "answers":page_obj, "best_tags": best_tags, "user_is_logged": user_is_logged})

def tag(request, tag_name):
    QUESTIONS = Question.objects.get_questions_by_tag(tag_name).order_by('-likes')
    page_obj = paginate(QUESTIONS ,request.GET.get('page', 1))
    return render(request, "tag.html", {"questions": page_obj, "tag_name": tag_name, "best_tags": best_tags, "user_is_logged": user_is_logged})

def settings(request):
    return render(request, "settings.html", {"best_tags": best_tags, "user_is_logged": user_is_logged})

def login(request):
    return render(request, "login.html", {"best_tags": best_tags})

def signup(request):
    return render(request, "signup.html", {"best_tags": best_tags})

def paginate(obj_list, page, per_page=5):
    page = int(float(page)) #handle PageNotAnInteger
    if(len(obj_list) < 1): #handle EmptyPage
        return 
    if(page < 1):
        page = 1
    paginator = Paginator(obj_list, per_page)
    return paginator.page(page)
