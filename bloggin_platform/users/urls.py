from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import register, profile_view, edit_profile, follow_user, unfollow_user, user_profile

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='post-list'), name='logout'),
    path('profile/', user_profile, name='profile'),
    path('<str:username>/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit-profile'),
    path('profile/<str:username>/follow/', follow_user, name='follow'),
    path('profile/<str:username>/unfollow/', unfollow_user, name='unfollow'),
]
