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

from django.shortcuts import get_object_or_404, render

from .models import Category, Location, Post, User


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


def location_posts(request, pk):
    template = 'posts/location.html'
    location = get_object_or_404(
        Location.objects.values('town', 'country', 'description'), pk=pk)
    post_list = Post.objects.select_related(
        'location', 'author').filter(
        is_published=True,
        location__id=pk
    )
    context = {'location': location, 'post_list': post_list
               }
    return render(request, template, context)


def author_posts(request, pk):
    template = 'posts/author.html'
    author = get_object_or_404(
        User.objects.values('username',), pk=pk)
    post_list = Post.objects.select_related(
        'location', 'author').filter(
        is_published=True,
        author__id=pk
    )
    context = {'author': author, 'post_list': post_list
               }
    return render(request, template, context)
