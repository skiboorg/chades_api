from django.shortcuts import render
from rest_framework import generics
from .serializers import *

class GetRandomImage(generics.RetrieveAPIView):
    serializer_class = PuzzleImageSerializer
    def get_object(self):
        return PuzzleImage.objects.all().order_by('?').first()

class GetRandomVideo(generics.RetrieveAPIView):
    serializer_class = PuzzleVideoSerializer
    def get_object(self):
        return PuzzleVideo.objects.all().order_by('?').first()



