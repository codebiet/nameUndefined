from django.urls import path;
from .views import homePage,registerView,loginView,logoutView,createTestView,takeTestView,createQuestionView,displayQuesView,dashboardView,profileView
urlpatterns=[
    path("",homePage),
    path("register/",registerView),
    path("login/",loginView),
    path("logout/",logoutView),
    path("createtest/",createTestView),
    path("taketest/",takeTestView),
    path("createQuestions/",createQuestionView),
    path("updateProfile/",profileView),
    path("displayQuestions/",displayQuesView),
    path("dashboard/",dashboardView),
]
