from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('password/', views.change_password, name='change_password'),
    path('<username>/', views.profile, name='profile'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    path('<int:user_pk>/followingfollow/', views.followingfollow, name='followingfollow'),
    path('<int:user_pk>/followerfollow/', views.followerfollow, name='followerfollow'),
    path('<username>/following_list/', views.followinglist, name='followinglist'),
    path('<username>/follower_list/', views.followerlist, name='followerlist'),
]