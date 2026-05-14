from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import OuterRef, Subquery
from django.shortcuts import render, get_object_or_404, redirect
import json

from .models import Product, PriceHistory


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # 🔥 последняя цена по каждому offer
    last_price_subquery = PriceHistory.objects.filter(
        offer=OuterRef("pk")
    ).order_by("-recorded_at").values("price")[:1]

    offers = product.offers.select_related("store").annotate(
        last_price=Subquery(last_price_subquery)
    )

    # история для графика
    history_qs = (
        PriceHistory.objects
        .filter(offer__product=product)
        .select_related("offer", "offer__store")
        .order_by("recorded_at")
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
    })


def home(request):
    products = Product.objects.prefetch_related(
        "offers__store",
        "offers__history"
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


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("/")