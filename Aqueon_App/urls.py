from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    
    # react-native
    path('user_loginnn/', views.user_loginnn, name='user_loginnn'),
    path('show_user/', views.show_user, name='show_user'),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)