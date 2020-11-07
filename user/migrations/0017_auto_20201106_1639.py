# Generated by Django 3.1.1 on 2020-11-06 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_user_expiry_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='vi_chat',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='vichat'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Эл. почта'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Ник'),
        ),
    ]