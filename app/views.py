from django.http import HttpResponse, QueryDict
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django import forms
from app.forms import *
from app.models import *

# Create your views here.

QUESTIONS = Question.objects.order_by('-created_at')

best_tags = Tag.objects.get_best_tags()[:5]


def index(request):
    page_obj = paginate(QUESTIONS, request.GET.get('page', 1))
    return render(request, "index.html", {"questions": page_obj, "best_tags": best_tags})

@login_required(login_url="login")
def ask(request):
    if request.method == "GET":
        ask_form = AskForm()
    if request.method == "POST":
        ask_form = AskForm(data=request.POST)
        if ask_form.is_valid():
            question = ask_form.create_question(Profile.objects.filter(user=request.user).get())
            question.save()
            return redirect(reverse('question', kwargs={'question_id': question.id}))
    return render(request, "ask.html", {"best_tags": best_tags, "form":ask_form})

def hot(request):
    page_obj = paginate(Question.objects.get_hot_questions(), request.GET.get('page', 1))
    return render(request, "hot.html", {"questions":page_obj, "best_tags": best_tags})

def question(request, question_id):
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
    return render(request, "question_detail.html", {"question":item, "answers":page_obj, "best_tags": best_tags, "form":ans_form})

def tag(request, tag_name):
    QUESTIONS = Question.objects.get_questions_by_tag(tag_name).order_by('-likes')
    page_obj = paginate(QUESTIONS ,request.GET.get('page', 1))
    return render(request, "tag.html", {"questions": page_obj, "tag_name": tag_name, "best_tags": best_tags})

@login_required(login_url="login")
def settings(request):
    if request.method == 'GET':
        settings_form = SettingsForm()
    if request.method == 'POST':
        settings_form = SettingsForm(data=request.POST, instance=request.user)
        if settings_form.is_valid():
            settings_form.save()
            return redirect(reverse('settings'))
    return render(request, "settings.html", {"best_tags": best_tags, "form": settings_form})

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
        register_form = RegisterForm(request.POST)
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
