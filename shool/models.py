from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_delete
from colorfield.fields import ColorField

from user.models import User


class Banner(models.Model):
    bg = models.ImageField('Бекграунд', upload_to='course', blank=False, null=True)
    top = models.ImageField('Маленькая картинка', upload_to='course', blank=False, null=True)

    def __str__(self):
        return f'Баннер {self.id}'

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"

class Stage(models.Model):
    number = models.IntegerField(blank=False,null=True)
    score_need = models.IntegerField(blank=False,null=True)

    def __str__(self):
        return f'Этап {self.number}'

    class Meta:
        verbose_name = "Этап"
        verbose_name_plural = "Этапы"


class Course(models.Model):
    stage = models.ForeignKey(Stage,on_delete=models.CASCADE,blank=False,null=True,verbose_name='Этап')
    icon = models.ImageField('Иконка белая', upload_to='course', blank=False, null=True)
    bg_color = ColorField(default='#000000')
    bg_image = models.ImageField('Картинка для бекграунда', upload_to='course', blank=False, null=True)
    depence = models.ForeignKey('self',on_delete=models.SET_NULL,blank=True,null=True)
    score_need = models.IntegerField(blank=False, null=True)
    points_to_balance = models.IntegerField(blank=False, null=True)
    description = models.TextField('Описание', blank=True, null=True)

    def __str__(self):
        return f'{self.description}'

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,blank=False,null=True,verbose_name='Курс',related_name='lessons')
    name = models.CharField(max_length=255, blank=True, null=True)
    description = RichTextUploadingField('Описание', blank=True, null=True)
    means = RichTextUploadingField('Определения', blank=True, null=True)
    words = RichTextUploadingField('Слова', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

class AvaiableLessons(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True,verbose_name='Юзер')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,blank=False,null=True,verbose_name='Курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,blank=False,null=True,verbose_name='Урок')
    status = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.email} - {self.lesson.id} - {self.status}'

    class Meta:
        verbose_name = "Доступный урок"
        verbose_name_plural = "Доступные уроки"

class Test(models.Model):
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,blank=False,null=True,verbose_name='Урок',related_name='test')
    order_num = models.IntegerField(default=100)
    description = RichTextUploadingField('Текст', blank=True, null=True)

    def __str__(self):
        return f'Тест к уроку {self.lesson.name}'

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class TestChoice(models.Model):
    test = models.ForeignKey(Test,on_delete=models.CASCADE,blank=False,null=True,verbose_name='Тест',related_name='choices')
    order_num = models.IntegerField(default=100)
    is_right = models.BooleanField('Это верный ответ',default=False)
    description = models.CharField('Текст',max_length=255, blank=True, null=True)
    image=models.ImageField(blank=True,upload_to='tests/')

    def __str__(self):
        return f'Ответ к тесту {self.test.id}'

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class InputTest(models.Model):
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,blank=False,null=True,verbose_name='Урок',related_name='input_test')
    order_num = models.IntegerField(default=100)
    description = RichTextUploadingField('Текст', blank=True, null=True)
    answer = models.TextField('Верный ответ', blank=True, null=True)

    def __str__(self):
        return f'Тест-ввод к уроку {self.lesson.name}'

    class Meta:
        verbose_name = "Тест-ввод"
        verbose_name_plural = "Тесты-ввод"


# def lesson_post_delete(sender, instance, created, **kwargs):
#     avaiable_lesson = AvaiableLessons.objects.get(lesson=instance)
#     avaiable_lesson.delete()
#
# post_delete.connect(lesson_post_delete, sender=Lesson)