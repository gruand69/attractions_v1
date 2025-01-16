"""
URL configuration for attractions project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('posts/', include('posts.urls'))
"""

from django import views
from django.conf.global_settings import MEDIA_ROOT, MEDIA_URL
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.conf.urls.static import static
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView

# from attractions import users

from users.views import logout_view, UserCreateView
from users.forms import CustomUserCreationForm


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('posts.urls')),
    path("pages/", include('pages.urls')),
    path("users/", include('users.urls')),
    path('auth/logout/', logout_view, name='logout'),
    path("auth/", include('django.contrib.auth.urls')),
    # path('auth/registration/', CreateView.as_view(
    #     template_name='registration/registration_form.html',
    #     # form_class=UserCreationForm,
    #     form_class=CustomUserCreationForm,
    #     success_url=reverse_lazy('users:profile'),
    # ), name='registration'),
    path('auth/registration/', UserCreateView.as_view(), name='registration'),

]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__', include(debug_toolbar.urls)),)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
