import asyncio
from gigachat_integration import GigaChatIntegration
from character1 import CharacterSettings
from dialog_manager import DialogManager
from typing import Dict, List, Optional
from datetime import datetime

class SanatoriumAssistant:
    """Главный класс приложения"""

    def __init__(self):
        self.llm = GigaChatIntegration()
        self.character = CharacterSettings()
        self.dialog = DialogManager()
        self.session_counter = 0

    async def start_cli(self):
        """Запуск интерфейса командной строки"""
        print(f"{self.character.name}: {self.character.get_greeting()}")

        session_id = f"session_{self.session_counter}"
        self.session_counter += 1

        while True:
            user_input = input("Вы: ").strip()

            if user_input.lower() in ["выход", "стоп"]:
                print(f"{self.character.name}: До свидания! Хорошего дня.")
                break

            # Обработка ввода
            context = self.dialog.process_input(session_id, user_input)
            llm_response = await self._generate_response(session_id, context)

            # Вывод ответа
            print(f"\n{self.character.name}: {llm_response}\n")

    async def _generate_response(self, session_id: str, context: Dict) -> str:
        """Генерация ответа через LLM"""
        prompt_name = context.get("next_prompt", "default")

        prompt_context = {
            "character": self.character.get_traits_for_prompt(),
            "dialog_context": context,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        return await self.llm.generate_response(
            session_id=session_id,
            prompt_name=prompt_name,
            context=prompt_context
        )


if __name__ == "__main__":
    assistant = SanatoriumAssistant()
    asyncio.run(assistant.start_cli())