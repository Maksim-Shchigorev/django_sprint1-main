from django.db import models


class PublishedModel(models.Model):
    """Абстрактная модель. Добвляет флаг is_published."""

    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        abstract = True
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
