from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class Achive(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    icon = models.ImageField('Фото', upload_to='achives', blank=True, null=True)
    rules = models.TextField(blank=True,null=True)

class User(AbstractUser):
    username = None
    # tarif = models.ForeignKey(Tarif,blank=True,null=True,on_delete=models.SET_NULL,
    #                           related_name='Тариф')
    # own_partner_code = models.ForeignKey(ParnterCode,blank=True,null=True,
    #                                      on_delete=models.SET_NULL,
    #                                      related_name='own_partner_code',
    #                                      verbose_name='Персональный портнерский код')
    achives = models.ManyToManyField(Achive, blank=True)
    avatar = models.ImageField('Фото', upload_to='user',blank=True,null=True)
    nickname = models.CharField('Ник', max_length=50, blank=True, null=True, default='Иван')
    name = models.CharField('Имя', max_length=50, blank=True, null=True, default='Иван')
    email = models.EmailField('Эл. почта', blank=True, null=True, unique=True)
    score = models.IntegerField('Баллы', default=0)
    is_vip = models.BooleanField('VIP?', default=False)
    title = models.CharField('Титул', max_length=255, blank=True, null=True)
    bg_image = models.ImageField('Картинка', upload_to='user',blank=True,null=True)
    avaiable_courses = models.ManyToManyField('shool.Course',blank=True,verbose_name='Доступные курсы',
                                              related_name='avaiable_courses')
    finished_courses = models.ManyToManyField('shool.Course',blank=True,verbose_name='Завершенные курсы',
                                              related_name='finished_courses')
    progress_courses = models.ManyToManyField('shool.Course', blank=True, verbose_name='В процессе курсы',
                                              related_name='progress_courses')



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

def user_post_save(sender, instance, created, **kwargs):
    if created:
        from shool.models import Course
        first_course = Course.objects.all().first()
        instance.avaiable_courses.add(first_course.id)
        instance.save()

post_save.connect(user_post_save, sender=User)



