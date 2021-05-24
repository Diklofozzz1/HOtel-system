from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('reg.urls')),
    path('', include('client.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
