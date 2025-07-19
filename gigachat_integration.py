import os
import json
import requests
from typing import Dict, Any, List


class GigaChatIntegration:
    """Класс для интеграции с GigaChat API """

    def __init__(self):
        self.auth_token = self._get_auth_token()
        self.base_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        self.conversation_cache = {}  # Кэш для хранения диалогов

    def _get_auth_token(self) -> str:
        """Получение токена аутентификации для GigaChat API"""
        auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

        # Заголовки запроса
        headers = {
            "Authorization": f"Bearer {os.getenv('GIGACHAT_API_KEY')}",
            "RqUID": os.getenv("GIGACHAT_RQ_UID"),
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            response = requests.post(auth_url, headers=headers, data={"scope": "GIGACHAT_API_PERS"})
            response.raise_for_status()
            return response.json()["access_token"]
        except Exception as e:
            print(f"Ошибка аутентификации: {str(e)}")
            raise

    def generate_response(self, session_id: str, prompt_name: str, context: Dict[str, Any]) -> str:
        """
        Генерация ответа с использованием GigaChat

        Args:
            session_id: Идентификатор сессии пользователя
            prompt_name: Название шаблона промпта
            context: Контекст диалога

        Returns:
            Сгенерированный ответ
        """
        try:
            # Проверка кэша для снижения нагрузки на API
            cache_key = f"{session_id}_{prompt_name}"
            if cache_key in self.conversation_cache:
                return self.conversation_cache[cache_key]

            # Загрузка и форматирование промпта
            prompt = self._load_prompt(prompt_name).format(**context)

            # Подготовка запроса
            headers = {
                "Authorization": f"Bearer {self.auth_token}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "GigaChat",
                "messages": self._prepare_messages(prompt, context),
                "temperature": 0.7,  # Оптимальный баланс креативности/точности
                "max_tokens": 512,
                "n": 1
            }

            # Отправка запроса
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()

            # Извлечение и кэширование ответа
            result = response.json()["choices"][0]["message"]["content"]
            self.conversation_cache[cache_key] = result

            return result

        except requests.exceptions.RequestException as e:
            print(f"Ошибка API: {str(e)}")
            return "Извините, возникли технические трудности. Пожалуйста, повторите позже."
        except Exception as e:
            print(f"Неожиданная ошибка: {str(e)}")
            return "Произошла ошибка при обработке вашего запроса."

    def _prepare_messages(self, prompt: str, context: Dict) -> List[Dict]:
        """Подготовка сообщений для контекста диалога"""
        messages = [
            {"role": "system", "content": "Вы - Саша, виртуальный помощник санатория."}
        ]

        # Добавление истории диалога если есть
        if "history" in context:
            for msg in context["history"][-3:]:  # Берем последние 3 сообщения
                messages.append({"role": "user", "content": msg["user"]})
                messages.append({"role": "assistant", "content": msg["assistant"]})

        messages.append({"role": "user", "content": prompt})
        return messages

    def _load_prompt(self, name: str) -> str:
        """Загрузка шаблона промпта из файла"""
        try:
            with open(f"src/prompts/{name}.json", "r", encoding="utf-8") as f:
                return json.load(f)["prompt"]
        except Exception as e:
            print(f"Ошибка загрузки промпта: {str(e)}")
            return "Ответьте на запрос клиента"