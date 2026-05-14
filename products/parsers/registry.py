from .base import BaseProductParser
from .bite import BiteParser
from .pigu import PiguParser
from .senukai import SenukaiParser
from .telia import TeliaParser


_PARSERS_REGISTRY = {
    "Pigu": PiguParser(),
    "Pigu.lt": PiguParser(),
    "Senukai": SenukaiParser(),
    "senukai": SenukaiParser(),
    "Senukai.lt": SenukaiParser(),
    "Bite": BiteParser(),
    "bite": BiteParser(),
    "Bite.lt": BiteParser(),
    "Telia": TeliaParser(),
    "telia": TeliaParser(),
    "Telia.lt": TeliaParser(),
}


def get_parser_for_store(store_name: str) -> BaseProductParser | None:
    return _PARSERS_REGISTRY.get(store_name)