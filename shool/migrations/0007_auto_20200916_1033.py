# Generated by Django 3.1.1 on 2020-09-16 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shool', '0006_auto_20200914_1107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='bg_image',
        ),
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='course', verbose_name='Картинка'),
        ),
    ]
