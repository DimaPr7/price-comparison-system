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
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('favorite/add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorite/remove/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
]