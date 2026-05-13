import copy
from bs4 import BeautifulSoup
from .base import BaseProductParser


class SenukaiParser(BaseProductParser):

    def extract_price(self, soup: BeautifulSoup) -> float | None:
        price_tag = None

        regular_label = soup.find(string=lambda t: t and "Įprasta kaina" in t)

        if regular_label:
            parent_container = regular_label.find_parent("div", class_="MuiStack-root")
            if not parent_container:
                parent_container = regular_label.find_parent()

            if parent_container:
                price_tag = parent_container.find(
                    "div", {"data-test": "ksd-typography"}
                )

        if not price_tag:
            price_box = soup.find("div", {"data-test": "ksd-price-tag"})
            if price_box:
                price_tag = price_box.find("div", {"data-test": "ksd-typography"})

        if not price_tag:
            price_tag = soup.select_one("div[class*='MuiTypography-h4-bold']")

        if price_tag:
            raw_text = price_tag.text.strip()

            clean_text = (
                raw_text.replace("€", "")
                .replace(" ", "")
                .replace(",", ".")
                .strip()
            )

            final_digits = "".join(c for c in clean_text if c.isdigit() or c == ".")

            if final_digits:
                try:
                    return float(final_digits)
                except Exception:
                    pass

        return None
