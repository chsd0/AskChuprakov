from django.http import HttpResponse, JsonResponse, QueryDict
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django import forms
import json
from app.forms import *
from app.models import *

# Create your views here.

QUESTIONS = Question.objects.order_by('-created_at')

best_tags = Tag.objects.get_best_tags()[:5]


def index(request):
    if request.user.is_authenticated:
        profilePic = Profile.objects.filter(user=request.user).get().image
    else:
        profilePic = None
    page_obj = paginate(Question.objects.order_by('-created_at'), request.GET.get('page', 1))
    return render(request, "index.html", {"questions": page_obj, "best_tags": best_tags, "profilePic": profilePic})

@login_required(login_url="login")
def ask(request):
    if request.user.is_authenticated:
        profilePic = Profile.objects.filter(user=request.user).get().image
    else:
        profilePic = None

    if request.method == "GET":
        ask_form = AskForm()
    if request.method == "POST":
        ask_form = AskForm(data=request.POST)
        if ask_form.is_valid():
            question = ask_form.create_question(Profile.objects.filter(user=request.user).get())
            question.save()
            return redirect(reverse('question', kwargs={'question_id': question.id}))
    return render(request, "ask.html", {"best_tags": best_tags, "form":ask_form, "profilePic": profilePic})

def hot(request):
    if request.user.is_authenticated:
        profilePic = Profile.objects.filter(user=request.user).get().image
    else:
        profilePic = None

    page_obj = paginate(Question.objects.get_hot_questions(), request.GET.get('page', 1))
    return render(request, "hot.html", {"questions":page_obj, "best_tags": best_tags, "profilePic": profilePic})

def question(request, question_id):
    if request.user.is_authenticated:
        profilePic = Profile.objects.filter(user=request.user).get().image
    else:
        profilePic = None

    item = QUESTIONS.get(id=question_id)
    ANSWERS = Answer.objects.filter(question=question_id).order_by('-likes')
    page_obj = paginate(ANSWERS, request.GET.get('page', 1), 3)

    if request.method=="GET":
        ans_form = AnswerForm()
    if request.method == "POST":
        ans_form = AnswerForm(data=request.POST)
        if ans_form.is_valid():
            answer = ans_form.create_answer(item, Profile.objects.filter(user=request.user).get())
            answer.save()
            ind = list(Answer.objects.filter(question=question_id).order_by('-likes')).index(answer)
            return redirect('{}?{}'.format(reverse('question', kwargs={'question_id': answer.question.id}), 'page='+str(ind//3+1)))
    return render(request, "question_detail.html", {"question":item, "answers":page_obj, "best_tags": best_tags, "form":ans_form, "profilePic": profilePic})

def tag(request, tag_name):
    if request.user.is_authenticated:
        profilePic = Profile.objects.filter(user=request.user).get().image
    else:
        profilePic = None

    QUESTIONS = Question.objects.get_questions_by_tag(tag_name).order_by('-likes')
    page_obj = paginate(QUESTIONS ,request.GET.get('page', 1))
    return render(request, "tag.html", {"questions": page_obj, "tag_name": tag_name, "best_tags": best_tags, "profilePic": profilePic})

@login_required(login_url="login")
def settings(request):
    if request.user.is_authenticated:
        profilePic = Profile.objects.filter(user=request.user).get().image
    else:
        profilePic = None

    if request.method == 'GET':
        settings_form = SettingsForm()
    if request.method == 'POST':
        settings_form = SettingsForm(data=request.POST, instance=request.user, files=request.FILES)
        if settings_form.is_valid():
            settings_form.save()
            return redirect(reverse('settings'))
    return render(request, "settings.html", {"best_tags": best_tags, "form": settings_form, "profilePic": profilePic})

def Login(request):
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                login_form.add_error('password', 'Wrong password')
        else:
            login_form.add_error('username', 'This login does not exist')
                
    return render(request, "login.html", {"best_tags": best_tags, "form": login_form})

def signup(request):
    if request.method == 'GET':
        register_form = RegisterForm()
    if request.method == "POST":
        register_form = RegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                register_form.add_error(None, "Error saving user")
        else:
            register_form.add_error(None, 'Data is invalid')

    return render(request, "signup.html", {"best_tags": best_tags, "form": register_form})

@login_required(login_url="login")
def Logout(request):
    logout(request)
    return redirect(reverse('login'))

def paginate(obj_list, page, per_page=5):
    page = int(float(page)) #handle PageNotAnInteger
    if(len(obj_list) < 1): #handle EmptyPage
        return 
    if(page < 1):
        page = 1
    paginator = Paginator(obj_list, per_page)
    return paginator.page(page)

@login_required(login_url="login")
@require_http_methods(["POST"])
@csrf_protect
def like_async(request, question_id):
    body = json.loads(request.body)
    question = Question.objects.filter(id=question_id).get()
    profile = Profile.objects.filter(user=request.user).get()
    try:
        question_like, question_like_created = LikeQuestion.objects.get_or_create(question=question, author=profile)
    except LikeQuestion.MultipleObjectsReturned:
        question_like = LikeQuestion.objects.filter(question=question, author=profile).first()
        question_like_created = 0

    if not question_like_created:
        question_like.delete()
    
    body['likes_count'] = LikeQuestion.objects.filter(question=question).count()
    question.likes = LikeQuestion.objects.filter(question=question).count()
    question.save()

    return JsonResponse(body)

@login_required(login_url="login")
@require_http_methods(["POST"])
@csrf_protect
def like_async_answer(request, answer_id):
    body = json.loads(request.body)
    answer = Answer.objects.filter(id=answer_id).get()
    profile = Profile.objects.filter(user=request.user).get()
    answer_like, answer_like_created = LikeAnswer.objects.get_or_create(answer=answer, author=profile)

    if not answer_like_created:
        answer_like.delete()
    
    body['likes_count'] = LikeAnswer.objects.filter(answer=answer).count()
    answer.likes = LikeAnswer.objects.filter(answer=answer).count()
    answer.save()

    return JsonResponse(body)

@login_required(login_url="login")
@require_http_methods(["POST"])
@csrf_protect
def correct_async(request, answer_id):
    body = json.loads(request.body)
    answer = Answer.objects.filter(id=answer_id).get()
    profile = Profile.objects.filter(user=request.user).get()
    correct = answer.correct

    if correct:
        answer.correct = False
    else:
        answer.correct = True
    answer.save()
    
    body['correct'] = answer.correct

    return JsonResponse(body)