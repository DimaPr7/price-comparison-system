import re
from bs4 import BeautifulSoup
from .base import BaseProductParser


class TeliaParser(BaseProductParser):

    def extract_price(self, soup: BeautifulSoup) -> float | None:
        if not soup:
            return None

        container = soup.select_one('div[data-test="price_with_monthly_payment"]')

        if not container:
            container = soup.select_one('div[class*="PriceContainer"]')

        if container:
            price_element = container.find(
                lambda tag: tag.has_attr("aria-label") and "Iš viso" in tag["aria-label"]
            )

            if price_element:
                raw_text = price_element["aria-label"]
                clean_text = (
                    raw_text.replace("Iš viso", "")
                    .replace("\xa0", "")
                    .replace("€", "")
                    .strip()
                    .replace(",", ".")
                )

                match = re.search(r"\d+(?:\.\d+)?", clean_text)
                if match:
                    try:
                        return float(match.group(0))
                    except ValueError:
                        pass

            strong_tag = container.select_one("strong")
            if strong_tag:
                strong_text = (
                    strong_tag.get_text()
                    .strip()
                    .replace("\xa0", "")
                    .replace(" ", "")
                    .replace(",", ".")
                )

                match = re.search(r"\d+(?:\.\d+)?", strong_text)
                if match:
                    try:
                        return float(match.group(0))
                    except ValueError:
                        pass

        page_text = soup.get_text()
        match_text = re.search(r"Iš\s+viso\s*(\d[\d\s]*,?\d*)", page_text)

        if match_text:
            clean_p = (
                match_text.group(1)
                .replace(" ", "")
                .replace("\xa0", "")
                .replace(",", ".")
            )

            try:
                return float(clean_p)
            except ValueError:
                pass

        return None