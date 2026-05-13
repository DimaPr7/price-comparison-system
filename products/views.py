from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import OuterRef, Subquery
from django.shortcuts import redirect, render

from .models import Price, Product


@login_required
def home(request):
    cheapest_price_subquery = Price.objects.filter(
        offer__product=OuterRef("pk")
    ).order_by("price")

    products = Product.objects.annotate(
        min_price_value=Subquery(cheapest_price_subquery.values("price")[:1]),
        min_price_store=Subquery(
            cheapest_price_subquery.values("offer__store__name")[:1]
        ),
    )

    return render(request, "home.html", {"products": products})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("/")
