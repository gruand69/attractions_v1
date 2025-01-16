from django.urls import path

from . import views

app_name = "users"


urlpatterns = [
    path("profile/<slug:username>/", views.profile, name="profile"),
    path("edit_profile/<slug:username>/",
         views.edit_profile, name="edit_profile"),
]
