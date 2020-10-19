from django.urls import path,include
from . import views

urlpatterns = [
    path('get_random_video/', views.GetRandomVideo.as_view()),
    path('get_random_image/', views.GetRandomImage.as_view()),

]
