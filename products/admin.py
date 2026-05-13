from django.contrib import admin
from .models import Profile, Category, Product, Store, Price, Favorite, PriceHistory, ProductOffer

admin.site.register(ProductOffer)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Store)
admin.site.register(Price)
admin.site.register(Favorite)
admin.site.register(PriceHistory)
