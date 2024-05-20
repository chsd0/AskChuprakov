from django import forms
from django.contrib.auth.models import User
from app.models import *

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            self.add_error('username', 'This username does not exist')
            raise forms.ValidationError("")
        return username


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, max_length=30, required=True)
    password_conformation = forms.CharField(widget=forms.PasswordInput, max_length=30, required=True)
    image = forms.ImageField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'This username already exists, please choose another one')
            raise forms.ValidationError("")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'This email is already in use, please choose another one')
            raise forms.ValidationError("")
        return email
    
    def clean_passwords(self):
        passwrd = self.cleaned_data['password']
        if self.cleaned_data.get('password_conformation'):
            passwrd_conf = self.cleaned_data['password_conformation']
        else:
            self.add_error('password_conformation', 'no input')
            passwrd_conf = None

        if passwrd != passwrd_conf:
            self.add_error('password', 'Password do not match')

        return passwrd
    
    def clean(self):
        self.clean_passwords()
        self.clean_username()
        self.clean_email()
        cleaned_data = super().clean()
        return cleaned_data
    
    def save(self):
        self.cleaned_data.pop('password_conformation')
        image = self.cleaned_data.get('image')
        self.cleaned_data.pop('image')
        user = User.objects.create_user(**self.cleaned_data)
        profile = Profile.objects.create_profile(user=user)
        profile.image = image
        profile.save()
        return user
    
class SettingsForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    image = forms.ImageField()

    class Meta:
        model = User
        fields = ('username', 'email')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists() and self.initial['username']!=username:
            self.add_error('username', 'This username already exists, please choose another one')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists() and self.initial['email']!=email:
            self.add_error('email', 'This email is already in use, please choose another one')
        return email
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        profile = Profile.objects.filter(user=self.instance).get()
        profile.image = image
        profile.save()
        return image
    
    def clean(self):
        self.clean_username()
        self.clean_email()
        self.clean_image()
        cleaned_data = super().clean()
        return cleaned_data
    
class AskForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True)
    text = forms.CharField(max_length=300, required=True)
    tags = forms.CharField()

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags')
      
    def create_question(self, profile):
        question = Question.objects.create(title=self.cleaned_data['title'], 
                                           text=self.cleaned_data['text'],
                                           author=profile)
        tags = self.cleaned_data['tags'].split()
        if len(tags) > 5:
            tags = tags[:5]
        tagsModel = []
        for tag in tags:
            if Tag.objects.filter(name=tag).exists():
                tagsModel.append(Tag.objects.filter(name=tag).get())
            else:
                newTag = Tag.objects.create(name=tag)
                tagsModel.append(newTag)
        question.tags.set(tagsModel)
        question.save()
        return question

class AnswerForm(forms.ModelForm):
    text = forms.CharField(max_length=300, required=True)

    class Meta:
        model = Answer
        fields = ('text',)

    def create_answer(self, question, profile):
        answer = Answer.objects.create(question=question, text=self.cleaned_data['text'], author=profile)
        answer.save()
        return answer