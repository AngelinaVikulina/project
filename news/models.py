from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User


class Articles(models.Model):
    title = models.CharField('Заголовок', max_length=50)
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

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'article')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.article.title}'
