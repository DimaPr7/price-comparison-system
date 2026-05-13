from .base import BaseProductParser
from .pigu import PiguParser
from .senukai import SenukaiParser

_PARSERS_REGISTRY = {
    "Pigu": PiguParser(),
    "Pigu.lt": PiguParser(),
    "Senukai": SenukaiParser(),
    "senukai": SenukaiParser(),
    "Senukai.lt": SenukaiParser(),
}


def get_parser_for_store(store_name: str) -> BaseProductParser | None:
    return _PARSERS_REGISTRY.get(store_name)
