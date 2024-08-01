from django.db import models
from core.models import PublishedModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Location(PublishedModel):
    name = models.CharField('Название места', max_length=256)
    is_published = models.BooleanField('Опубликовано', default=True)
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.title


class Category(PublishedModel):
    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание', )
    slug = models.SlugField('Идентификатор', unique=True,
                            help_text='Идентификатор страницы для URL; '
                            'разрешены символы латиницы, цифры, дефис '
                            'и подчёркивание.')
    is_published = models.BooleanField(
        'Опубликовано', default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Post(PublishedModel):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор публикации')
    title = models.CharField('Заголовок', max_length=256)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации', help_text='Если установить дату и время в'
        ' будущем — можно делать отложенные публикации.')
    is_published = models.BooleanField(
        'Опубликовано', default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='post', verbose_name='Категория',
        help_text='Укажите категорию для публикации.'
    )
    # category = models.ForeignKey(Category, on_delete=models.SET_NULL,
    #                             null=True, blank=False,
    #                             related_name='post', verbose_name='Категория',
    #                             help_text='Укажите категорию для публикации.')

    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Местоположение', help_text='Укажите местоположение '
        'публикации.')

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='post',
        verbose_name='Категория')
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Местоположение')
