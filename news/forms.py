from django import forms
from .models import Articles

class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'full_text', 'date']  # Убедитесь, что поле 'author' не включено в форму

        widgets = {
            "title": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
            "date": forms.DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата публикации'
            }),
            "full_text": forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Отзыв'
            }),
        }
