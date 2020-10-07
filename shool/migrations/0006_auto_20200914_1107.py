# Generated by Django 3.1.1 on 2020-09-14 08:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shool', '0005_auto_20200912_1348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='depences_from',
        ),
        migrations.CreateModel(
            name='AvaiableLessons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=0)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shool.course', verbose_name='Курс')),
                ('lesson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shool.lesson', verbose_name='Урок')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Юзер')),
            ],
            options={
                'verbose_name': 'Доступный урок',
                'verbose_name_plural': 'Доступные уроки',
            },
        ),
    ]