from unicodedata import category
# from urllib import response
# from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from requests import post
from .models import Review, Comment, Category, Tag
from .forms import ReviewForm, CommentForm
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.db.models import Q


class ReviewList(ListView):
    model = Review
    ordering = '-pk'

    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super(ReviewList, self).get_context_data()
        context["categories"] = Category.objects.all()

        page = context['page_obj']
        paginator = page.paginator
        print(paginator)
        pagelist = paginator.get_elided_page_range(page.number, on_each_side=3, on_ends=0)
        context['pagelist'] = pagelist

        return context

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    review_list = tag.review_set.all()
    context = {
        'review_list' : review_list,
        'tag' : tag,
        'categories' : Category.objects.all(),
    }
    return render(request, 'community/review_list.html', context)

def category_page(request, slug):
    category = Category.objects.get(slug=slug)
    review_list = Review.objects.filter(category=category)
    context = {
        'review_list' : review_list,
        'categories' : Category.objects.all(),
        'category' : category,
    }
    return render(request, 'community/review_list.html', context)

class ReviewDetail(DetailView):
    model = Review
    def get_context_data(self, **kwargs):
        context = super(ReviewDetail, self).get_context_data()
        context["categories"] = Category.objects.all()
        context['comment_form'] = CommentForm

        return context

class ReviewCreate(LoginRequiredMixin,CreateView):
    model = Review
    template_name = 'community/review_form.html'
    success_url = '/community/'
    fields = ['title', 'content', 'head_image', 'file_upload', 'category']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.user = current_user
            response = super(ReviewCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()

                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t= t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)


            return response
        else:
            return redirect('community/<review.pk>/')
    
    def get_context_data(self, **kwargs):
        context = super(ReviewCreate, self).get_context_data()
        context["categories"] = Category.objects.all()

        return context

class ReviewUpdate(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ['title', 'content', 'head_image', 'file_upload', 'category', 'tags']

    template_name = 'community/review_update_form.html'
    
    def get_context_data(self, **kwargs):
        context = super(ReviewUpdate, self).get_context_data()
        context["categories"] = Category.objects.all()

        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().user:
            return super(ReviewUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
    
    def get_context_data(self, **kwargs):
        context = super(ReviewUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)
        return context
    
    def form_valid(self, form):
        response = super(ReviewUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',',';')
            tags_list = tags_str.split(';')
            
            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name = t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response



@require_POST
def delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user.is_authenticated:
        if request.user == review.user:
            review.delete()
    return redirect('community:index')



# @require_GET
# def detail(request, review_pk):
#     review = get_object_or_404(Review, pk=review_pk)
#     comments = review.comment_set.all()
#     comment_form = CommentForm()
#     context = {
#         'review': review,
#         'comment_form': comment_form,
#         'comments': comments,
#     }
#     return render(request, 'community/detail.html', context)

@require_POST
def new_comment(request, pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
            return redirect('community:detail', pk)
    context = {
        'comment_form': comment_form,
        'review': review,
        'comments': review.comment_set.all(),
    }
    return render(request, 'community/review_detail.html', context)


# @require_POST
# def create_comment(request, review_pk):
#     review = get_object_or_404(Review, pk=review_pk)
#     comment_form = CommentForm(request.POST)
#     if comment_form.is_valid():
#         comment = comment_form.save(commit=False)
#         comment.review = review
#         comment.user = request.user
#         comment.save()
#         return redirect('community:detail', review.pk)
#     context = {
#         'comment_form': comment_form,
#         'review': review,
#         'comments': review.comment_set.all(),
#     }
#     return render(request, 'community/detail.html', context)


@require_POST
def like(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user

        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
        else:
            review.like_users.add(user)
        return redirect('community:detail', review_pk)
    return redirect('accounts:login')

# @require_POST
# def comment_delete(request, community_pk ,comment_pk):
#     if request.user.is_authenticated:
#         comment = get_object_or_404(Comment, pk=comment_pk)
#         if request.user == comment.user:
#             comment.delete()
#     return redirect('community:detail', community_pk)

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    
    def get_context_data(self, **kwargs):
        context = super(CommentUpdate, self).get_context_data()
        context["categories"] = Category.objects.all()


        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().user:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    review = comment.review

    if request.user.is_authenticated and request.user == comment.user:
        comment.delete()
        return redirect('community:detail', review.pk)
    else:
        raise PermissionDenied

class ReviewSearch(ReviewList):
    paginate_by = 5
    def get_queryset(self):

        q = self.kwargs['q']
        review_list = Review.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct()
        return review_list
    
    def get_context_data(self, **kwargs):
        context = super(ReviewSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'
        
        return context

# def Review_search(request):
#     search_word = request.GET['search-word']
#     if search_word:
#         review_list = Review.objects.filter(Q(title__contains=search_word) | Q(tags__name__contains=search_word)).distinct()
#         error = ''

#         if len(movie_list) == 0:
#             # movie_list = random_movies
#             error = '에 해당하는 게시글이 없습니다'

#         context = {
#             'search_word': search_word,
#             'review_list': review_list,
#             'error': error,
#         }

#         return render(request, 'movies/search.html', context)