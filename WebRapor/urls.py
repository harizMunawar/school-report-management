from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.conf.urls import handler404
from REST.routers import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    path('', include('django.contrib.auth.urls')),
    path('', include('User.urls')),
    path('', include('Nilai.urls')),
    path('', include('Rapor.urls')),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# handler404 = 'backend.views.error_404'