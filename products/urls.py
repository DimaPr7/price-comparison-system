from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),

    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]