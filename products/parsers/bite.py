import re
from bs4 import BeautifulSoup
from .base import BaseProductParser


class BiteParser(BaseProductParser):

    def extract_price(self, soup: BeautifulSoup) -> float | None:
        if not soup:
            return None

        target_block = None

        accordion_items = soup.select(".product-details_accordion") or soup.select("[class*='accordion']")

        for item in accordion_items:
            item_text = item.get_text()
            if "Mokant iš karto" in item_text or "Be įsipareigojimų" in item_text:
                target_block = item
                break

        price_tag = None

        if target_block:
            price_tag = target_block.select_one(".product-device__prices-price")
            if not price_tag:
                price_tag = target_block.select_one("[class*='prices-price'], [class*='price-new']")

        if not price_tag:
            all_prices = soup.select(".product-device__prices-price") or soup.select("[class*='prices-price']")
            for tag in all_prices:
                tag_text = tag.text
                if "/mėn" not in tag_text and "mėn" not in tag_text:
                    price_tag = tag
                    break

        if price_tag:
            raw_text = price_tag.text.replace("\xa0", "").replace("€", "").strip()
            raw_text = raw_text.replace(",", ".")
            clean_text = "".join(char for char in raw_text if char.isdigit() or char == ".")

            if clean_text:
                try:
                    return float(clean_text)
                except ValueError:
                    return None

        return None