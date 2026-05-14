from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.name or self.user.username


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    brand = models.CharField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )

    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Store(models.Model):
    name = models.CharField(max_length=255)
    website_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to='stores/', null=True, blank=True)

    def __str__(self):
        return self.name

class ProductOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="offers")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="offers")
    url = models.URLField()

    class Meta:
        unique_together = ('product', 'store')

    def __str__(self):
        return f"{self.product.title} @ {self.store.name}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} ♥ {self.product.title}"


class PriceHistory(models.Model):
    offer = models.ForeignKey(
        ProductOffer,
        on_delete=models.CASCADE,
        related_name='history'
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.offer} - {self.price} ({self.recorded_at})"