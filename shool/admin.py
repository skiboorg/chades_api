from django.contrib import admin
from .models import *

class TestInline(admin.TabularInline):
    model = Test
    extra = 0

class InputTestInline(admin.TabularInline):
    model = InputTest
    extra = 0

class LessonAdmin(admin.ModelAdmin):
    inlines = [TestInline,InputTestInline]
    list_filter = ("course",)
    class Meta:
        model = Lesson

class TestChoiceInline(admin.TabularInline):
    model = TestChoice
    extra = 0

class TestAdmin(admin.ModelAdmin):
    inlines = [TestChoiceInline]
    list_filter = ("lesson",)
    class Meta:
        model = Test

class TestChoiceAdmin(admin.ModelAdmin):
    list_filter = ("test",)
    class Meta:
        model = TestChoice

class AvaiableLessonsAdmin(admin.ModelAdmin):
    list_filter = ("user",)
    class Meta:
        model = AvaiableLessons

admin.site.register(Stage)
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(TestChoice,TestChoiceAdmin)
admin.site.register(InputTest)
admin.site.register(Banner)
admin.site.register(CallBackForm)
admin.site.register(AvaiableLessons,AvaiableLessonsAdmin)
