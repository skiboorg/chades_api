from django.urls import path,include
from . import views

urlpatterns = [


    path('stages/', views.GetStages.as_view()),
    path('cources/', views.GetCourses.as_view()),
    path('cource_open/', views.CourseOpen.as_view()),
    path('cource/<int:pk>', views.GetCourse.as_view()),
    path('lessons/', views.GetLessons.as_view()),
    path('avaiable_lessons', views.GetAvaiableLessons.as_view()),
    path('tests/', views.GetTests.as_view()),
    path('lesson_done/', views.LessonDone.as_view()),
    path('testchoices/', views.GetTestChoices.as_view()),
    path('inputtests/', views.GetInputTests.as_view()),
    path('startscript/', views.StartScript.as_view()),
    path('get_banner/', views.GetBanner.as_view()),
    path('new_cb/', views.NewCB.as_view()),
    path('create_pay/', views.CreatePay.as_view()),
    path('pay_notify/', views.PayNotify.as_view()),
]
