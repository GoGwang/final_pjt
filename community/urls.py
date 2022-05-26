from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('tag/<str:slug>/', views.tag_page),
    path('category/<str:slug>/', views.category_page),
    path('', views.ReviewList.as_view(), name='index'),
    # path('', views.ReviewList.as_view()),

    # path('<int:pk>/', views.ReviewDetail.as_view()),
    path('<int:pk>/', views.ReviewDetail.as_view(), name='detail'),
    # path('create/', views.ReviewCreate.as_view()),
    path('create/', views.ReviewCreate.as_view(), name='create'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('update/<int:pk>/', views.ReviewUpdate.as_view(), name='update'),
    path('<int:review_pk>/like/', views.like, name='like'),
    path('<int:pk>/new_comment/', views.new_comment, name="new_comment"),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('delete_comment/<int:pk>/', views.delete_comment), 
    path('search/<str:q>/', views.ReviewSearch.as_view()),
]
