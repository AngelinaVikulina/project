from django.shortcuts import render, redirect, get_object_or_404
from .models import Articles, Like, Comment
from .forms import ArticlesForm, CommentForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse

def news_home(request):
    news = Articles.objects.order_by('-date')
    for article in news:
        article.likes_count = article.like_set.filter(is_like=True).count()
        article.dislikes_count = article.like_set.filter(is_like=False).count()
        if request.user.is_authenticated:
            article.user_like = article.like_set.filter(user=request.user, is_like=True).exists()
            article.user_dislike = article.like_set.filter(user=request.user, is_like=False).exists()
    return render(request, 'news/news_home.html', {'news': news})


class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/details_view.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(article=self.object)
        context['comment_form'] = CommentForm()
        context['likes_count'] = self.object.like_set.filter(is_like=True).count()
        context['dislikes_count'] = self.object.like_set.filter(is_like=False).count()
        if self.request.user.is_authenticated:
            context['user_like'] = self.object.like_set.filter(user=self.request.user, is_like=True).exists()
            context['user_dislike'] = self.object.like_set.filter(user=self.request.user, is_like=False).exists()
        return context

class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Articles
    template_name = 'news/create.html'
    form_class = ArticlesForm

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author

class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Articles
    success_url = '/news/'
    template_name = 'news/news-delete.html'

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author

@login_required
def create(request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.title = request.user.username  # Автоматическое задание заголовка
            article.save()
            return redirect('news_home')
        else:
            error = 'Форма заполнена не верно'

    form = ArticlesForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'news/create.html', data)
@login_required
def like_article(request, pk):
    article = get_object_or_404(Articles, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, article=article)
    if not created:
        like.is_like = not like.is_like
        like.save()
    return JsonResponse({'likes': article.like_set.filter(is_like=True).count(), 'dislikes': article.like_set.filter(is_like=False).count()})

@login_required
def add_comment(request, pk):
    article = get_object_or_404(Articles, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()
            return redirect('news-detail', pk=article.pk)
    else:
        form = CommentForm()
    return render(request, 'news/add_comment.html', {'form': form})

@login_required
def like_article(request, pk):
    article = get_object_or_404(Articles, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, article=article)

    if created:
        like.is_like = request.POST.get('is_like') == 'true'
        like.save()
    else:
        if like.is_like == (request.POST.get('is_like') == 'true'):
            like.delete()
        else:
            like.is_like = not like.is_like
            like.save()

    likes_count = article.like_set.filter(is_like=True).count()
    dislikes_count = article.like_set.filter(is_like=False).count()

    return JsonResponse({'likes': likes_count, 'dislikes': dislikes_count})