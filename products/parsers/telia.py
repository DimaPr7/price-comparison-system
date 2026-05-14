import re
from bs4 import BeautifulSoup
from .base import BaseProductParser


class TeliaParser(BaseProductParser):

    def extract_price(self, soup: BeautifulSoup) -> float | None:
        if not soup:
            return None

        # 1. Поиск основного контейнера цены Telia по дата-атрибуту
        container = soup.select_one('div[data-test="price_with_monthly_payment"]')

        # Запасной селектор контейнера (по частичному совпадению сгенерированного класса)
        if not container:
            container = soup.select_one('div[class*="PriceContainer"]')

        if container:
            # Ищем блок, где написано "Iš viso" (Полная стоимость)
            # На скриншоте это родитель тега strong, у которого прописан aria-label="Iš viso 669 €"
            price_element = container.find(lambda tag: tag.has_attr('aria-label') and "Iš viso" in tag['aria-label'])

            if price_element:
                raw_text = price_element['aria-label']
                # Очищаем атрибут от текста, пробелов и знака валюты
                clean_text = raw_text.replace("Iš viso", "").replace("\xa0", "").replace("€", "").strip()
                clean_text = clean_text.replace(",", ".")

                match = re.search(r"\d+(?:\.\d+)?", clean_text)
                if match:
                    try:
                        return float(match.group(0))
                    except ValueError:
                        pass

            # Если через атрибут aria-label забрать не удалось, собираем ТЕКСТ изнутри тега strong
            strong_tag = container.select_one("strong")
            if strong_tag:
                # Берем чистый текст внутри strong (он вернет "669")
                strong_text = strong_tag.get_text().strip()
                # Удаляем пробелы-разделители тысяч, если цена больше 1000 евро
                strong_text = strong_text.replace("\xa0", "").replace(" ", "").replace(",", ".")

                match = re.search(r"\d+(?:\.\d+)?", strong_text)
                if match:
                    try:
                        return float(match.group(0))
                    except ValueError:
                        pass

        # 2. Запасной текстовый поиск по регулярному выражению на случай изменения структуры блоков
        # Ищет подстроки "Iš viso 669", "Iš viso 1249" или аналогичные текстовые блоки на странице
        page_text = soup.get_text()
        match_text = re.search(r"Iš\s+viso\s*(\d[\d\s]*,?\d*)", page_text)
        if match_text:
            clean_p = match_text.group(1).replace(" ", "").replace("\xa0", "").replace(",", ".")
            try:
                return float(clean_p)
            except ValueError:
                pass

        return None
