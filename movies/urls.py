from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    # path('<int:movie_pk>/movie_comments_create/', views.movie_comments_create, name='movie_comments_create'),
    path('<int:movie_pk>/movie_comments/<int:movie_comment_pk>/delete/', views.movie_comments_delete,name='movie_comments_delete'),
    # path('<int:movie_pk>/movie_comments/<int:movie_comment_pk>/update/', views.movie_comments_update,name='movie_comments_update'),
    path('<int:pk>/update/', views.MovieCommentUpdate.as_view()),
    path('<int:pk>/new_comment/', views.new_movie_comment, name="new_movie_comment"),
    path('<int:pk>/delete/', views.delete_movie_comment), 
    path('<int:pk>/movie_like/', views.movie_like, name='movie_like'),
    path('<int:id>/score/create/',views.scoreCreate, name="scoreCreate"),
    path('search/', views.search, name='search'),
]
