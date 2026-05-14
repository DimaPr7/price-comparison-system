import re
from bs4 import BeautifulSoup
from .base import BaseProductParser


class BiteParser(BaseProductParser):

    def extract_price(self, soup: BeautifulSoup) -> float | None:
        if not soup:
            return None

        # 1. Находим конкретный блок опции "Mokant iš karto" (Оплата сразу)
        target_block = None

        # Перебираем все элементы аккордеона вариантов оплаты
        accordion_items = soup.select(".product-details_accordion") or soup.select("[class*='accordion']")

        for item in accordion_items:
            item_text = item.get_text()
            # Проверяем, что этот блок отвечает за полную оплату без обязательств
            if "Mokant iš karto" in item_text or "Be įsipareigojimų" in item_text:
                target_block = item
                break

        # 2. Если нашли нужный блок, извлекаем цену только из него
        price_tag = None
        if target_block:
            # Ищем тег цены конкретно внутри изолированного блока полной оплаты
            price_tag = target_block.select_one(".product-device__prices-price")
            if not price_tag:
                price_tag = target_block.select_one("[class*='prices-price'], [class*='price-new']")

        # 3. Резервный вариант, если общая структура блоков аккордеона изменилась
        if not price_tag:
            # Ищем все теги цен на странице
            all_prices = soup.select(".product-device__prices-price") or soup.select("[class*='prices-price']")
            for tag in all_prices:
                tag_text = tag.text
                # Игнорируем цены рассрочки (содержащие /mėn.)
                if "/mėn" not in tag_text and "mėn" not in tag_text:
                    price_tag = tag
                    break

        # 4. Форматирование строки в число (float)
        if price_tag:
            # Очищаем строку от неразрывных пробелов, знака евро и лишних символов
            raw_text = price_tag.text.replace("\xa0", "").replace("€", "").strip()
            # Превращаем десятичную запятую в точку
            raw_text = raw_text.replace(",", ".")
            # Оставляем только цифры и разделительную точку
            clean_text = "".join(char for char in raw_text if char.isdigit() or char == ".")

            if clean_text:
                try:
                    return float(clean_text)
                except ValueError:
                    return None

        return None

