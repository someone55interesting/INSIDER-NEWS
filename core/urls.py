from django.contrib import admin
from django.urls import path, include
from news import views
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Это подключает стандартные login/logout/password_reset
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # Твои кастомные пути
    path('', views.home, name='home'),
    path('article/<int:pk>/', views.article_detail, name='article'),
    path('category/<slug:slug>/', views.category_detail, name='category'),
    path('register/', views.register, name='register'),
    path('like/<int:pk>/', views.like_view, name='like_article'),
    path('profile/', views.profile, name='profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)