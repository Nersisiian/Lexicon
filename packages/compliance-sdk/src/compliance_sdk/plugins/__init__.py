from abc import ABC, abstractmethod
from typing import Any, Dict

class BasePlugin(ABC):
    """Базовый класс для всех плагинов обработки."""

    @abstractmethod
    async def process(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Обрабатывает документ и возвращает обновлённый словарь."""
        ...
