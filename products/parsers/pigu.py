import copy
import json
from bs4 import BeautifulSoup
from .base import BaseProductParser


class PiguParser(BaseProductParser):

    def extract_price(self, soup: BeautifulSoup) -> float | None:
        price = None

        product_widget = soup.select_one("div[widget-data*='item_id']")
        if product_widget and product_widget.has_attr("widget-data"):
            try:
                widget_json = json.loads(product_widget["widget-data"])
                if "price" in widget_json:
                    return float(widget_json["price"])
            except Exception:
                pass

        regular_price_label = soup.find(string=lambda t: t and "Įprasta kaina" in t)
        price_tag = None

        if regular_price_label:
            parent_block = regular_price_label.find_parent()
            if parent_block:
                price_tag = parent_block.find_next_sibling("span", class_="c-price")
                if not price_tag:
                    price_tag = parent_block.find_parent().select_one("span.c-price")

        if not price_tag:
            price_tag = soup.select_one(
                "span.c-price.h-price--x-large:not(.h-price--loyalty)"
            )

        if not price_tag:
            price_tag = soup.select_one(
                "span.c-price.h-price--x-large.h-price--loyalty"
            )

        if not price_tag:
            price_tag = soup.select_one("span.c-price")

        if price_tag:
            sup_tag = price_tag.find("sup")
            sup_text = sup_tag.text.strip() if sup_tag else "00"

            clean_tag = copy.copy(price_tag)
            for child in clean_tag.find_all(["sup", "sub", "small", "i"]):
                child.decompose()

            main_text = "".join(filter(str.isdigit, clean_tag.text))
            if main_text:
                try:
                    price = float(f"{main_text}.{sup_text}")
                except Exception:
                    price = None

        return price
