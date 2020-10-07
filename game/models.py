from django.db import models
from django_random_queryset import RandomManager




class PuzzleVideo(models.Model):
    video = models.FileField('Картинка или видео', upload_to='puzzlevideo/', blank=False, null=True)

    objects = RandomManager()

    def __str__(self):
        return f'Файл пазла {self.id}'

    class Meta:
        verbose_name = "Файл пазла"
        verbose_name_plural = "Файлы для пазлов"