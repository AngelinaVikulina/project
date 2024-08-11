from django.db import models

class Articles(models.Model):
    title = models.CharField('Имя пользователя', max_length=50)
    full_text = models.TextField('Отзыв')
    date = models.DateTimeField('Дата публикации')



    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'