from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/<int:pk>/", views.post_detail, name="post_detail"),
    path("category/<slug:slug>/",
         views.category_posts, name="category_posts"),
    path("location/<int:pk>/",
         views.location_posts, name="location_posts"),
    path("author/<int:pk>/",
         views.author_posts, name="author_posts"),
]
