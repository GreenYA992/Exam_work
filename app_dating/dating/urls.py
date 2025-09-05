from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Основные страницы
    path('', views.home, name='home'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),

    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='dating/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),

    # Профиль
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    # Взаимодействия
    path('interact/<str:action>/<int:user_id>/', views.interact_user, name='interact_user'),
    #path('like/<int:user_id>/', views.like_user, name='like_user'),
    #path('dislike/<int:user_id>/', views.dislike_user, name='dislike_user'),
]