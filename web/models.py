from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    image = models.ImageField(upload_to='users_avatars', blank=True, null=True)


class UserInfo(models.Model):
    user = models.ForeignKey(User, related_name='user_info', verbose_name='пользователь', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='имя')
    bio = models.TextField(verbose_name='о себе')
    avatar = models.ImageField(null=True, blank=True, upload_to='image_user_avatars', verbose_name='аватар')
    is_teacher = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Информация о пользователях'
        verbose_name = 'Информация о пользователе'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'

    def __str__(self):
        return self.name


class Course(models.Model):
    user = models.ForeignKey(User, verbose_name='пользователь', related_name='user_courses', on_delete=models.CASCADE)
    tags = TaggableManager()
    price = models.IntegerField(null=True, blank=True, verbose_name='цена',
                                validators=[MinValueValidator(1), MaxValueValidator(150000)])
    title = models.CharField(max_length=50, verbose_name='название')
    created_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=250, verbose_name='слаг', unique_for_date='created_date')
    text = models.TextField(verbose_name='описание')
    image = models.ImageField(null=True, blank=True, upload_to='image_courses', verbose_name='картинка')
    category = models.ManyToManyField(Category)

    class Meta:
        verbose_name_plural = 'Курсы'
        verbose_name = 'Курс'

    def __str__(self):
        return self.title


class Comment(models.Model):
    course = models.ForeignKey(Course, verbose_name='курс', related_name='course_comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='пользователь', related_name='user_comments', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='текст комментария')
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
