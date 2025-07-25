# from django.shortcuts import render

# posts = [
#     {
#         "id": 0,
#         "name": "Исаакиевский собор",
#         "location": "Санкт-Петербург",
#         "date": "30 сентября 2004 года",
#         "category": "churchs",
#         "text": """Самый крупный собор Северной столицы строился на протяжении
#             40 лет. Современное здание — четвертое по счету, построенное в духе
#             позднего классицизма по проекту архитектора Огюста Монферрана.
#             Храм возведен в честь преподобного Исаакия Далматского.
#             Снаружи собор украшают более 350 скульптур,
#             посвященных Иисусу Христу.""",
#     },
#     {
#         "id": 1,
#         "name": "Красная площадь",
#         "location": "Москва",
#         "date": "1 октября 2010 года",
#         "category": "intresting_places",
#         "text": """Кра́сная пло́щадь — главная площадь Москвы и России,
#             расположена между Московским Кремлём (к западу)
#             и Китай-городом (на восток). Выходит к берегу Москвы-реки
#             через пологий Васильевский спуск. Площадь тянется вдоль
#             северо-восточной стены Кремля, от Кремлёвского проезда и проезда
#             Воскресенские Ворота до Васильевского спуска, выходящего
#             к Кремлёвской набережной. На восток от Красной площади отходят
#             Никольская улица, Ильинка и Варварка. Вдоль западной стороны
#             площади расположен Московский Кремль, вдоль восточной —
#             Верхние торговые ряды и Средние торговые ряды.
#             Входит в единый ансамбль с Московским Кремлём, однако исторически
#             является частью Китай-города.""",
#     },
#     {
#         "id": 2,
#         "name": "Золотой мост",
#         "location": "Владивосток",
#         "date": "25 октября 2012 года",
#         "category": "intresting_places",
#         "text": """Золотой мост — вантовый мост через бухту Золотой Рог
#             во Владивостоке. Он является одной из главных
#             достопримечательностей города. Был построен в рамках
#             программы подготовки города к проведению саммита АТЭС.
#             Открыт 11 августа 2012 года.""",
#     },
# ]


# def index(request):
#     template_name = "posts/index.html"
#     context = {
#         "posts": posts,
#     }
#     return render(request, template_name, context)


# def post_detail(request, id):
#     template_name = "posts/detail.html"
#     context = {
#         'post': posts[id]
#     }
#     return render(request, template_name, context)


# def category_posts(request, category):
#     template_name = "posts/category.html"
#     context = {
#         'category': category,
#     }
#     return render(request, template_name, context)

import datetime
# from urllib import request
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import (CreateView,
                                  DeleteView,
                                  DetailView,
                                  ListView,
                                  UpdateView)
from django.urls import reverse, reverse_lazy

from .models import (Advice,
                     Category,
                     Comment,
                     Country,
                     Favorite,
                     Post,
                     Tag,
                     Town)
from .forms import AdviceForm, CommentForm, PostCreateForm

User = get_user_model()


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/create.html'
    success_url = reverse_lazy('posts:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form'] = CommentForm()
        # context['comments'] = (
        #     self.object.comments.select_related('author')
        # )
        context['comments'] = self.get_comments()
        if self.request.user.is_authenticated:
            # context['form'] = CommentForm()
            context['form'] = CommentForm

            context['added_to_favorite'] = Favorite.objects.filter(
                post=self.object, user=self.request.user).exists()
        return context
    
    def get_comments(self):
        queryset = self.object.comments.all()
        paginator = Paginator(queryset, settings.OBJECTS_COUNT_ON_PAGES)
        page = self.request.GET.get('page')
        posts = paginator.get_page(page)
        return posts


class PostListView(ListView):
    model = Post
    queryset = Post.objects.prefetch_related(
        'tags').select_related('author', 'category', 'category', 'town')
    template_name = 'posts/index.html'
    paginate_by = settings.OBJECTS_COUNT_ON_PAGES


class PostUpdateView(LoginRequiredMixin,
                     UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/create.html'
    success_url = reverse_lazy('posts:index')

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CommentUpdateView(LoginRequiredMixin,
                        UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        instance = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        pk = self.kwargs.get('pk')
        return reverse('posts:post_detail', kwargs={'pk': pk})


class AdviceUpdateView(LoginRequiredMixin,
                        UpdateView):
    model = Advice
    form_class = AdviceForm
    template_name = 'posts/advice.html'
    pk_url_kwarg = 'advice_id'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        instance = get_object_or_404(Advice, pk=kwargs['advice_id'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        # pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        return reverse('posts:country_town', kwargs={'slug': slug})
        # return reverse('posts:post_detail', kwargs={'pk': pk})


class PostDeleteView(LoginRequiredMixin,
                     DeleteView):
    model = Post
    success_url = reverse_lazy('posts:index')
    template_name = 'posts/create.html'

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin,
                        DeleteView):
    model = Comment
    template_name = 'posts/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        instance = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        pk = self.kwargs.get('pk')
        return reverse('posts:post_detail', kwargs={'pk': pk})


class AdviceDeleteView(LoginRequiredMixin,
                        DeleteView):
    model = Advice
    template_name = 'posts/advice.html'
    pk_url_kwarg = 'advice_id'
    slug_url_kwarg = 'slug'

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        instance = get_object_or_404(Advice, pk=kwargs['advice_id'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        # pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        return reverse('posts:country_town', kwargs={'slug': slug})


class CommentCreateView(LoginRequiredMixin,
                        CreateView):
    obj = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        self.obj = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.obj
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('posts:post_detail', kwargs={'pk': self.obj.pk})


class AdviceCreateView(LoginRequiredMixin,
                       CreateView):
    obj = None
    model = Advice
    form_class = AdviceForm

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        self.obj = get_object_or_404(Country, slug=kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.country = self.obj
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('posts:country_town', kwargs={'slug': self.obj.slug})


def index(request):
    template_name = 'posts/index.html'
    post_list = Post.objects.select_related(
        'location', 'author').filter(
        is_published=True,
    )[0:5]
    context = {
        'post_list': post_list,
    }
    return render(request, template_name, context)


def post_detail(request, pk):
    template = 'posts/detail.html'
    post = get_object_or_404(Post.objects.select_related(
        'location', 'author').filter(
        is_published=True,
    ), pk=pk)
    context = {'post': post}
    return render(request, template, context)


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'posts/category.html'
    # paginate_by = settings.OBJECTS_COUNT_ON_PAGES
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.get_posts()      
        # context['page_obj'] = (
        #     self.object.posts.select_related('author')
        # )
        context['page_obj'] = posts
        return context

    def get_posts(self):
        # queryset = self.object.posts.select_related('author')
        queryset = self.object.posts.all()

        paginator = Paginator(queryset, settings.OBJECTS_COUNT_ON_PAGES)
        page = self.request.GET.get('page')
        posts = paginator.get_page(page)
        return posts


class TownDetailView(DetailView):
    model = Town
    template_name = 'posts/town.html'
    # paginate_by = settings.OBJECTS_COUNT_ON_PAGES
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.get_posts()        
        context['page_obj'] = posts
        # context['page_obj'] = (
        #     self.object.posts.select_related('author')
        # )
        return context

    def get_posts(self):
        # queryset = self.object.posts.select_related('author')
        queryset = self.object.posts.all()
        paginator = Paginator(queryset, settings.OBJECTS_COUNT_ON_PAGES)
        page = self.request.GET.get('page')
        posts = paginator.get_page(page)
        return posts


class CountryDetailView(DetailView):
    model = Country
    template_name = 'posts/country.html'
    # paginate_by = settings.OBJECTS_COUNT_ON_PAGES
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['towns'] = (
            self.object.towns.all()
        )
        # context['form'] = AdviceForm
        advices = self.get_advices()
        context['page_obj'] = advices
        # context['page_obj'] = self.object.advices.select_related('author')
        if self.request.user.is_authenticated:
            context['form'] = AdviceForm
        return context

    def get_advices(self):
        # queryset = self.object.advices.select_related('author')
        queryset = self.object.advices.all()
        paginator = Paginator(queryset, settings.OBJECTS_COUNT_ON_PAGES)
        page = self.request.GET.get('page')
        advices = paginator.get_page(page)
        return advices
    # def get_queryset(self):
    #     slug = self.kwargs.get('slug')
    #     return Post.objects.select_related('author').filter(
    #         category__slug=slug)
        # return Post.objects.all()


def category_posts(request, slug):
    template = 'posts/category.html'
    category = get_object_or_404(
        Category.objects.values('title', 'description'), slug=slug)
    post_list = Post.objects.select_related(
        'location', 'author').filter(
        is_published=True,
        category__slug=slug
    )
    context = {'category': category, 'post_list': post_list
               }
    return render(request, template, context)


# def location_posts(request, pk):
#     template = 'posts/location.html'
#     location = get_object_or_404(
#         Location.objects.values('town', 'country', 'description'), pk=pk)
#     post_list = Post.objects.select_related(
#         'location', 'author').filter(
#         is_published=True,
#         location__id=pk
#     )
#     context = {'location': location, 'post_list': post_list
#                }
#     return render(request, template, context)


# def author_posts(request, pk):
#     template = 'posts/author.html'
#     author = get_object_or_404(
#         User.objects.values('username',), pk=pk)
#     post_list = Post.objects.select_related(
#         'location', 'author').filter(
#         is_published=True,
#         author__id=pk
#     )
#     context = {'author': author, 'post_list': post_list
#                }
#     return render(request, template, context)


@login_required
def add_advice(request, slug):
    country = get_object_or_404(Country, slug=slug)
    form = AdviceForm(
        request.POST or None, files=request.FILES or None)
    if form.is_valid():
        advice = form.save(commit=False)
        advice.author = request.user
        advice.country = country
        advice.save()
    return redirect('posts:country_town', slug=slug)


@login_required
def add_delite_favorite(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if Favorite.objects.filter(post=post, user=request.user).exists():
        Favorite.objects.filter(post=post, user=request.user).delete()
    else:
        Favorite.objects.create(post=post, user=request.user)
        # post.favoriting.add(request.user)
        # post.favoriting.filter(user=request.user).add()

    return redirect('posts:get_favorite')


@login_required
def get_favorite(request):
    template = 'posts/favorite.html'
    author = get_object_or_404(
        User.objects.values('username',), pk=request.user.pk)
    # favorite_post = Favorite.objects.filter(user=request.user).all()
    # posts = favorite_post.post
    posts = Post.objects.filter(favoriting__user=request.user).order_by('-id')
    paginator = Paginator(posts, settings.OBJECTS_COUNT_ON_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'author': author,
    }
    return render(request, template, context)
