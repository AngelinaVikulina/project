from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('main.urls')),
    path('news/', include('news.urls')),
    path('', include('menu.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('menu/', include('menu.urls')),

]

# Добавляем обслуживание медиафайлов в режиме разработки
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


