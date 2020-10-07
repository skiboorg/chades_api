# Generated by Django 3.1.1 on 2020-09-09 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shool', '0002_auto_20200909_1503'),
        ('user', '0002_auto_20200909_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='current_lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_lesson', to='shool.lesson'),
        ),
    ]