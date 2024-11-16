from django import forms
from .models import Articles, Comment

class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['full_text', 'date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            "text": forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш комментарий'
            }),
        }
        labels = {
            'text': ''  # Убираем метку для поля text
        }
