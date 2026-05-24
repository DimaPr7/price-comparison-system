from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import OuterRef, Subquery, Q
from django.shortcuts import render, get_object_or_404, redirect

import json

from .forms import UserEditForm, RegisterForm, EmailLoginForm
from .models import Product, PriceHistory, Favorite

def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()
            return redirect("login")

    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {
        "form": form
    })

def login_view(request):

    form = EmailLoginForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            login_input = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.filter(email=login_input).first()
            if not user:
                user = User.objects.filter(username=login_input).first()

            if user and user.check_password(password):
                auth_login(request, user)
                return redirect("home")

            form.add_error(None, "Invalid email or password")

    return render(request, "registration/login.html", {"form": form})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user,
            product=product
        ).exists()

    last_price_subquery = PriceHistory.objects.filter(
        offer=OuterRef("pk")
    ).order_by("-recorded_at").values("price")[:1]

    offers = product.offers.select_related("store").annotate(
        last_price=Subquery(last_price_subquery)
    )

    history_qs = (
        PriceHistory.objects
        .filter(offer__product=product)
        .select_related("offer", "offer__store")
        .order_by("-recorded_at")
    )

    store_data = {}

    for h in history_qs:
        store = h.offer.store.name
        time = h.recorded_at.strftime("%Y-%m-%d %H:%M")

        store_data.setdefault(store, {})
        store_data[store][time] = float(h.price)

    all_dates = sorted({
        h.recorded_at.strftime("%Y-%m-%d %H:%M")
        for h in history_qs
    })

    colors = ["#3b82f6", "#ef4444", "#10b981", "#f59e0b"]

    datasets = []

    for i, (store, data) in enumerate(store_data.items()):
        prices = []
        last = None

        for d in all_dates:
            if d in data:
                last = data[d]
            prices.append(last)

        datasets.append({
            "label": store,
            "data": prices,
            "borderColor": colors[i % len(colors)],
            "fill": False,
            "tension": 0.3,
        })

    return render(request, "product_detail.html", {
        "product": product,
        "offers": offers,
        "history": history_qs,
        "chart_labels": json.dumps(all_dates),
        "chart_datasets": json.dumps(datasets),

        "is_favorite": is_favorite,
    })


def home(request):
    products = Product.objects.prefetch_related(
        "offers__store",
        "offers__history"
    )

    category = request.GET.get("category")
    q = request.GET.get("q", "").strip()

    if category:
        products = products.filter(category__name=category)

    if q:
        products = products.filter(
            Q(title__icontains=q) |
            Q(brand__icontains=q)
        )

    for product in products:
        min_price = None
        min_store = None

        for offer in product.offers.all():
            last_price = offer.history.order_by("-recorded_at").first()
            if not last_price:
                continue

            if min_price is None or last_price.price < min_price:
                min_price = last_price.price
                min_store = offer.store.name

        product.min_price_value = min_price
        product.min_price_store = min_store

    return render(request, "home.html", {"products": products})



def user_logout(request):
    logout(request)
    return redirect("/")


@login_required
def profile_view(request):

    favorites = Favorite.objects.filter(
        user=request.user
    ).select_related("product")

    return render(request, "profile.html", {
        "favorites": favorites
    })

@login_required
def edit_profile(request):

    if request.method == 'POST':
        form = UserEditForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'edit_profile.html', {
        'form': form
    })


@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    Favorite.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def remove_from_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    Favorite.objects.filter(
        user=request.user,
        product=product
    ).delete()

    return redirect(request.META.get("HTTP_REFERER", "/"))

from .models import Store

def stores(request):
    stores = Store.objects.all()

    return render(request, "stores.html", {
        "stores": stores
    })


def contacts(request):
    return render(request, "contacts.html")


def privacy_policy(request):
    return render(request, "privacy_policy.html")


def terms_of_use(request):
    return render(request, "terms_of_use.html")