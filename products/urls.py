from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("login/", views.login_view, name="login"),

    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('stores/', views.stores, name='stores'),
    path('contacts/', views.contacts, name='contacts'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms_of_use, name='terms_of_use'),

    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('favorite/add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorite/remove/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
]