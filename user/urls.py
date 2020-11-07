from django.urls import path, include
from . import views

urlpatterns = [


    path('me/', views.GetUser.as_view()),
    path('update/', views.UserUpdate.as_view()),
    path('getUserEmailbyPhone/', views.getUserEmailbyPhone.as_view()),
    path('getAllAchives/', views.GetAllAchives.as_view()),
    path('add_points/', views.AddPoints.as_view()),
    path('check_email/', views.CheckEmail.as_view()),

]
