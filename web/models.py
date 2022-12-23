from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True, null=True)


class UserInfo(models.Model):
    user = models.ForeignKey(User, related_name='user_info', verbose_name='пользователь', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='имя')
    bio = models.TextField(verbose_name='о себе')
    avatar = models.ImageField(null=True, blank=True, upload_to='image_user_avatars', verbose_name='аватар')
    is_teacher = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Информация о пользователях'
        verbose_name = 'Информация о пользователе'


class Course(models.Model):
    user = models.ForeignKey(User, verbose_name='пользователь', related_name='user_courses', on_delete=models.CASCADE)
    tags = TaggableManager()
    title = models.CharField(max_length=50, verbose_name='название')
    slug = models.SlugField(max_length=250, verbose_name='слаг', unique_for_date='created_at')
    text = models.TextField(verbose_name='описание')
    image = models.ImageField(null=True, blank=True, upload_to='image_courses', verbose_name='картинка')
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Курсы'
        verbose_name = 'Курс'


class Comment(models.Model):
    course = models.ForeignKey(Course, verbose_name='курс', related_name='course_comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='пользователь', related_name='user_comments', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='текст комментария')
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'


class RatingStar(models.Model):
    value = models.SmallIntegerField('Значение', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Здезды рейтинга'
        ordering = ['-value']


class Rating(models.Model):
    course = models.ForeignKey(Course, verbose_name='курс', related_name='course_rating', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='пользователь', related_name='user_rating', on_delete=models.CASCADE)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, related_name='rating_star', verbose_name='звезда')

    def __str__(self):
        return f'{self.star} - {self.course}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
