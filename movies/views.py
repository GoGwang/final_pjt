from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe, require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from movies.forms import MovieCommentForm
from .models import Movie, Genre, Movie_Comment, Score
from django.views.generic import UpdateView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
import random
from django.db.models import Q

# Create your views here.
@require_safe
def index(request):
    movies = Movie.objects.all()
    favorite_movies = movies.order_by('-vote_average')[:50]
    if request.user.is_authenticated:
        like_lst=[]
        mv_lst=[]
        for mv in request.user.movie_like_reviews.all():
            
            for like_genre in mv.genres.all():
                if like_genre not in like_lst:
                    like_lst.append(like_genre)
            
            if len(like_lst)>3:
                random_genre = random.sample(like_lst,3)
                for movie in movies:
                    for genre in movie.genres.all():
                        for random_gr in random_genre:
                            if genre == random_gr:
                                if movie not in mv_lst:
                                    mv_lst.append(movie)
                random_movies = random.sample(mv_lst,7) 
                context = {
                    'movies' : movies,
                    'favorite_movies' : favorite_movies,
                    'random_movies' : random_movies,
                }
                return render(request, 'movies/index.html', context)
    random_movies = random.sample(list(movies),20) 
    context = {
        'movies' : movies,
        'favorite_movies' : favorite_movies,
        'random_movies' : random_movies,
    }
    return render(request, 'movies/index.html', context)



@require_safe
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie_comment_form = MovieCommentForm()
    movie_comments = movie.movie_comment_set.all()
    ratings = 0
    for score in movie.score_set.all():
        ratings += score.rating
    if ratings == 0:
        ratingAvg = 0
    else:
        ratingAvg = ratings/movie.score_set.all().count()
        ratingAvg = round(ratingAvg, 2)
    # genre = Genre.objects.get()
    context = {
        'movie' : movie ,
        'movie_comment_form' : movie_comment_form,
        'movie_comments' : movie_comments,
        'ratingAvg' : ratingAvg,

    }
    return render(request, 'movies/detail.html', context)



# @require_POST
# def movie_comments_create(request, movie_pk):
#     if request.user.is_authenticated:
#         movie = get_object_or_404(Movie,pk=movie_pk)
#         movie_comment_form = MovieCommentForm(request.POST)
#         if movie_comment_form.is_valid():
#             movie_comment = movie_comment_form.save(commit=False)
#             movie_comment.movie = movie
#             movie_comment.user = request.user
#             movie_comment.save()
#         return redirect('movies:detail', movie.pk)
#     return redirect('accounts:login')

@require_POST
def movie_comments_delete(request, movie_pk, movie_comment_pk):
    if request.user.is_authenticated:
        movie_comment = get_object_or_404(Movie_Comment, pk=movie_comment_pk)
        if request.user == movie_comment.user:
            movie_comment.delete()
    return redirect('movies:detail', movie_pk)


# def movie_comments_update(request, movie_pk, movie_comment_pk):
#     if request.user.is_authenticated:
#         if request.method == "POST":
#             movie_comment = get_object_or_404(Movie_Comment, pk=movie_comment_pk)
#             if request.user == movie_comment.user:
#                 form = MovieCommentForm(request.POST)
#                 if form.is_valid():
#                     movie_comment = form.save()
#                     return redirect('movies:detail', movie_pk)
#     else:
#         return redirect('movies:datail', movie_pk)
#     context = {
#         'form' : form,
#         'movie' : movie_comment,
#     }
#     return render(request, 'movies/update.html', context, movie_pk, movie_comment_pk)

class MovieCommentUpdate(LoginRequiredMixin, UpdateView):
    model = Movie_Comment
    form_class = MovieCommentForm
    
    def get_context_data(self, **kwargs):
        context = super(MovieCommentUpdate, self).get_context_data()


        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().user:
            return super(MovieCommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

@require_POST
def new_movie_comment(request, pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=pk)
        movie_comment_form = MovieCommentForm(request.POST)
        if movie_comment_form.is_valid():
            movie_comment = movie_comment_form.save(commit=False)
            movie_comment.movie = movie
            movie_comment.user = request.user
            movie_comment.save()
            return redirect('movies:detail', pk)
    context = {
        'movie_comment_form': movie_comment_form,
        'movie': movie,
        'movie_comments': movie.movie_comment_set.all(),
    }
    return render(request, 'movies/detail.html', context)


def delete_movie_comment(request, pk):
    movie_comment = get_object_or_404(Movie_Comment, pk=pk)
    movie = movie_comment.movie

    if request.user.is_authenticated and request.user == movie_comment.user:
        movie_comment.delete()
        return redirect('movies:detail', movie.pk)
    else:
        raise PermissionDenied

@require_POST
def movie_like(request, pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=pk)
        user = request.user

        if movie.movie_like_users.filter(pk=user.pk).exists():
            movie.movie_like_users.remove(user)
        else:
            movie.movie_like_users.add(user)
        return redirect('movies:detail', movie.pk)
    return redirect('accounts:login')

@login_required
def scoreCreate(request,id):
    rating = request.POST.get('rating')
    user = request.user
    movie = Movie.objects.get(id=id)
    score_list = Score.objects.filter(user=user,movie=movie)
    
    if score_list:
        score = score_list.update(rating=rating)
    else:
        score = Score.objects.create(user=user, movie=movie, rating=rating)

    return redirect('movies:detail',id)


def search(request):
    search_word = request.GET['search-word']
    if search_word:
        movie_list = Movie.objects.filter(Q(title__icontains=search_word) | Q(overview__icontains=search_word)).distinct()
        message = ''
        error = ''

        if len(movie_list) == 0:
            movie_list = random.sample(list(Movie.objects.all()),10)
            # movie_list = random_movies
            error = '에 해당하는 영화가 없습니다'
            message = '이런 영화는 어떠세요?'

        context = {
            'search_word': search_word,
            'movie_list': movie_list,
            'message': message,
            'error': error,
        }

        return render(request, 'movies/search.html', context)
