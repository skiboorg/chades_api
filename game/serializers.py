from rest_framework import serializers
from .models import *




class PuzzleVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuzzleVideo
        fields = '__all__'
