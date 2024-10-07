from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', include('main.urls')),
    path('news/', include('news.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('menu/', include('menu.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
