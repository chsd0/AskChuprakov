from django.urls import path

from app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('ask/', views.ask, name='ask'),
    path('hot/', views.hot, name='hot'),
    path('questions/<int:question_id>', views.question, name='question'),
    path('tag/<str:tag_name>', views.tag, name="tag"),
    path('settings/', views.settings, name="settings"),
    path('login/', views.Login, name="login"),
    path('logout/', views.Logout, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('<question_id>/like_async', views.like_async, name="like_async"),
    path('tag/<question_id>/like_async', views.like_async, name="like_async"),
    path('hot/<question_id>/like_async', views.like_async, name="like_async"),
    path('questions/<question_id>/like_async', views.like_async, name="like_async"),
    path('questions/<answer_id>/like_async_answer', views.like_async_answer, name="like_async_answer"),
    path('questions/<answer_id>/correct_async', views.correct_async, name="correct_async"),
]
