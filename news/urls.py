from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_home, name="news_home"),
    path('create', views.create, name="create"),
    path('<int:pk>', views.NewsDetailView.as_view(), name='news-detail'),
    path('<int:pk>/update', views.NewsUpdateView.as_view(), name='news-update'),
    path('<int:pk>/delete', views.NewsDeleteView.as_view(), name='news-delete'),
    path('<int:pk>/like/', views.like_article, name='like-article'),
    path('<int:pk>/comment/', views.add_comment, name='add-comment'),
]
