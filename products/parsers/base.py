from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class BaseProductParser(ABC):

    @abstractmethod
    def extract_price(self, soup: BeautifulSoup) -> float | None:
        pass
