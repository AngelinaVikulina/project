from django.db import models
from django.contrib.auth.models import User

class Articles(models.Model):
    title = models.CharField('Имя пользователя', max_length=50)
    full_text = models.TextField('Отзыв')
    date = models.DateTimeField('Дата публикации')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
