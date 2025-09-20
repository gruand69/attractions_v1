from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.PostListView.as_view(), name="index"),
    path(
        "posts/<int:pk>/", views.PostDetailView.as_view(),
        name="post_detail"),
    path('posts/create/', views.PostCreateView.as_view(),
         name='create_post'),
    path(
        "posts/<int:pk>/edit/", views.PostUpdateView.as_view(
        ), name="edit_post"),
    path(
        "posts/<int:pk>/delete/", views.PostDeleteView.as_view(
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
    path(
        "country/<slug:slug>/edit_advice/<int:advice_id>/",
        views.AdviceUpdateView.as_view(), name="edit_advice"),
    path("country/<slug:slug>/delete_advice/<int:advice_id>/",
         views.AdviceDeleteView.as_view(), name="delete_advice"),
    path("country/<slug:slug>/advice",
         views.AdviceCreateView.as_view(), name="add_advice"),

    # ------------------------------------------------------------------

    path("posts/<int:pk>/add_favorite/", views.add_delite_favorite,
         name="add_favorite"),
    path("posts/<int:pk>/delite_favorite/", views.add_delite_favorite,
         name="delete_favorite"),
    path("get_favorite/",
         views.get_favorite, name="get_favorite"),
]
