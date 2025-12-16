from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from users.views import UserCreateView, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('posts.urls')),
    path("pages/", include('pages.urls')),
    path("users/", include('users.urls')),
    path('auth/logout/', logout_view, name='logout'),
    path("auth/", include('django.contrib.auth.urls')),
    path('auth/registration/', UserCreateView.as_view(), name='registration'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__', include(debug_toolbar.urls)),)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
