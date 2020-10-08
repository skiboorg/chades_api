from rest_framework import serializers
from .models import *

class PuzzleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuzzleImage
        fields = '__all__'



class PuzzleVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuzzleVideo
        fields = '__all__'
