from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

API_PREFIX = 'api/v1/'


def is_admin(user):
    return user.is_authenticated and user.is_staff


urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', user_passes_test(is_admin)(SpectacularAPIView.as_view()), name='schema'),
    path('swagger/', user_passes_test(is_admin)(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger'),

    path(API_PREFIX, include([
        path('', include('auths.urls')),
        path('', include('objects.urls')),
        path('', include('generators.urls')),
        path('', include('statements.urls')),
        path('', include('chats.urls')),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_URL
    )
