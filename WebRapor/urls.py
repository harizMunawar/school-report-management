from django.contrib import admin
from django.urls import path, include
from REST.routers import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('django.contrib.auth.urls')),
    path('', include('User.urls')),
]
