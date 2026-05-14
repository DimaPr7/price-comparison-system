import os
import random
import time
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from playwright.sync_api import sync_playwright

from products.models import Price, ProductOffer, PriceHistory
from products.parsers.registry import get_parser_for_store

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]


class Command(BaseCommand):
    help = "Parse product prices using Playwright"

    def handle(self, *args, **kwargs):
        offers = list(ProductOffer.objects.select_related("product", "store"))

        if not offers:
            self.stdout.write("No product offers found")
            return

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            for offer in offers:
                product = offer.product
                store = offer.store
                url = offer.url

                if not url:
                    self.stdout.write(f"Skip {product.title}: no URL")
                    continue

                parser = get_parser_for_store(store.name)
                if not parser:
                    self.stdout.write(f"Skip {product.title}: no parser for {store.name}")
                    continue

                context = browser.new_context(
                    user_agent=random.choice(USER_AGENTS),
                    viewport={"width": 1920, "height": 1080},
                )
                page = context.new_page()

                try:
                    page.goto(url, timeout=30000, wait_until="domcontentloaded")
                    page.wait_for_timeout(4000)
                    html = page.content()
                except Exception as e:
                    self.stdout.write(f"Error loading {product.title}: {e}")
                    context.close()
                    continue

                soup = BeautifulSoup(html, "html.parser")
                price = parser.extract_price(soup)

                if price is None:
                    self.stdout.write(f"Price not found for {product.title} @ {store.name}")
                    context.close()
                    continue

                # -----------------------
                # CURRENT PRICE (FIXED)
                # -----------------------
                current_price, created = Price.objects.get_or_create(
                    offer=offer,
                    defaults={
                        "price": price,
                        "currency": "EUR",
                    },
                )

                if not created and float(current_price.price) != float(price):
                    old_price = current_price.price
                    current_price.price = price
                    current_price.save()

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"[UPDATED] {product.title}: {old_price}€ → {price}€"
                        )
                    )

                elif created:
                    self.stdout.write(
                        self.style.SUCCESS(f"[NEW] {product.title} → {price}€")
                    )

                else:
                    self.stdout.write(f"[NO CHANGE] {product.title} → {price}€")

                # -----------------------
                # HISTORY (FIXED, ONLY OFFER)
                # -----------------------
                last_history = PriceHistory.objects.filter(
                    offer=offer
                ).order_by("-recorded_at").first()

                should_save = False

                if not last_history:
                    should_save = True
                else:
                    price_changed = float(last_history.price) != float(price)
                    time_passed = timezone.now() - last_history.recorded_at > timedelta(hours=6)
                    should_save = price_changed or time_passed

                if should_save:
                    PriceHistory.objects.create(
                        offer=offer,
                        price=price
                    )

                self.stdout.write(f"{product.title} @ {store.name} → {price}€")

                context.close()
                time.sleep(random.uniform(1.5, 3.0))

            browser.close()