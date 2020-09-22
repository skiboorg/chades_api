from rest_framework import serializers
from .models import *



class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'

class CoursesSerializer(serializers.ModelSerializer):
    depence = serializers.SlugRelatedField(slug_field='description', read_only=True)
    class Meta:
        model = Course
        fields = [
            'id',
            'icon_color',
            'icon_white',
            'bg_image',
            'score_need',
            'stage',
            'description',
            'lessons',
            'depence',



        ]

class AvaiableLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvaiableLessons
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class TestChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestChoice
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    choices = TestChoiceSerializer(many=True)
    class Meta:
        model = Test
        fields = [
            'id',
            'order_num',
            'description',
            'choices'
        ]


class InputTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputTest
        fields = '__all__'



class FullLessonSerializer(serializers.ModelSerializer):
    test = TestSerializer(many=True)
    input_test = InputTestSerializer(many=True)
    class Meta:
        model = Lesson
        fields = [
            'id',
            'name',
            'description',
            'means',
            'words',
            'test',
            'input_test',
            'id',
        ]


class CourseSerializer(serializers.ModelSerializer):
    lessons = FullLessonSerializer(many=True)
    depence = serializers.SlugRelatedField(slug_field='description',read_only=True)
    class Meta:
        model = Course
        fields = [
            'id',
            'icon_color',
            'icon_white',
            'bg_image',
            'score_need',
            'stage',
            'description',
            'lessons',
            'depence'
        ]



