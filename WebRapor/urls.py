from django.contrib import admin
from django.urls import path, include, re_path
from REST.routers import router
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('', include('django.contrib.auth.urls')),
    path('', include('User.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
