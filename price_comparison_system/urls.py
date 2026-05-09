from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # auth
    path('accounts/', include('django.contrib.auth.urls')),

    path('', include('products.urls')),
]