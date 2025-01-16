from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.PostListView.as_view(), name="index"),
    path(
        "posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path('posts/create/', views.PostCreateView.as_view(),
         name='create_post'),
    path(
        "posts/<int:pk>/edit/", views.PostUpdateView.as_view(
        ), name="edit_post"),
    path(
        "posts/<int:pk>/delete/", views.PostDetailView.as_view(
        ), name="delete_post"),

    # ---------------------------------------------------------------

    path("posts/<int:pk>/comment/", views.CommentCreateView.as_view(

    ), name="add_comment"),
    path(
        "posts/<int:pk>/edit_comment/<int:comment_id>/",
        views.CommentUpdateView.as_view(), name="edit_comment"),
    path("posts/<int:pk>/delete_comment/<int:comment_id>/",
         views.CommentDeleteView.as_view(), name="delete_comment"),

    # -------------------------------------------------------------

    path("category/<slug:slug>/",
         views.CategoryDetailView.as_view(), name="category_posts"),
    path("town/<slug:slug>/",
         views.TownDetailView.as_view(), name="town_posts"),
    path("country/<slug:slug>/",
         views.CountryDetailView.as_view(), name="country_town"),
    path("author/<int:pk>/",
         views.author_posts, name="author_posts"),
]
