from typing import Dict, List, Optional
from datetime import datetime


class DialogManager:
    """Управление состоянием диалога и контекстом"""

    def __init__(self):
        self.sessions = {}  # Хранение данных сессий
        self.current_stage = "приветствие"
        self.stages = {
            "приветствие": self._handle_welcome,
            "сбор_данных": self._handle_data_collection,
            "бронирование": self._handle_booking
        }

    def process_input(self, session_id: str, user_input: str) -> Dict:
        """
        Обработка ввода пользователя и обновление состояния

        Args:
            session_id: Уникальный идентификатор сессии
            user_input: Текст сообщения пользователя

        Returns:
            Контекст для генерации ответа
        """
        # Инициализация сессии если новая
        if session_id not in self.sessions:
            self._init_session(session_id)

        session = self.sessions[session_id]
        session["history"].append({
            "time": datetime.now(),
            "user": user_input
        })

        # Определение текущего этапа диалога
        handler = self.stages.get(self.current_stage, self._handle_default)
        context = handler(session, user_input)

        # Обновление истории
        if "assistant_response" in context:
            session["history"][-1]["assistant"] = context["assistant_response"]

        return context

    def _init_session(self, session_id: str):
        """Инициализация новой сессии диалога"""
        self.sessions[session_id] = {
            "created_at": datetime.now(),
            "history": [],
            "collected_data": {
                "даты": None,
                "гости": None,
                "контакты": None
            }
        }

    def _handle_welcome(self, session: Dict, input_text: str) -> Dict:
        """Обработка приветственного этапа"""
        context = {
            "stage": "приветствие",
            "intent": self._detect_intent(input_text),
            "user_profile": None
        }

        if any(word in input_text.lower() for word in ["бронь", "забронировать"]):
            self.current_stage = "сбор_данных"
            context["next_prompt"] = "booking_start"
        else:
            context["next_prompt"] = "general_qa"

        return context

    def _handle_data_collection(self, session: Dict, input_text: str) -> Dict:
        """Сбор информации для бронирования"""
        # Упрощенная логика для примера
        if not session["collected_data"]["даты"]:
            if self._validate_date(input_text):
                session["collected_data"]["даты"] = input_text
                return {"next_prompt": "ask_guests"}
            return {"error": "invalid_date"}

        # Продолжение сбора данных...

    def _handle_booking(self, session: Dict, input_text: str) -> Dict:
        """معالجة مرحلة تأكيد الحجز النهائية"""

        # 1. التحقق من اكتمال البيانات
        if not self._is_booking_data_complete(session):
            return {"error": "incomplete_data", "next_prompt": "ask_missing_data"}

        # 2. معالجة تأكيد الحجز
        if input_text.lower() in ["نعم", "أوافق", "confirm"]:
            return self._process_booking_confirmation(session)

        elif input_text.lower() in ["لا", "إلغاء", "cancel"]:
            return self._process_booking_cancellation(session)

        # 3. حالة الإدخال غير المعروف
        return {
            "assistant_response": "لم أفهم ردك. هل تؤكد الحجز؟ (نعم/لا)",
            "next_prompt": "booking_confirmation"
        }

    def _is_booking_data_complete(self, session: Dict) -> bool:
        """التحقق من وجود جميع بيانات الحجز الضرورية"""
        required_fields = ["даты", "гости", "контакты"]
        return all(session["collected_data"][field] is not None for field in required_fields)

    def _process_booking_confirmation(self, session: Dict) -> Dict:
        """تنفيذ عملية الحجز بعد التأكيد"""

        # 1. إنشاء طلب الحجز
        booking_data = {
            "dates": session["collected_data"]["даты"],
            "guests": session["collected_data"]["гости"],
            "contact": session["collected_data"]["контакты"]
        }

        # 2. إرسال الطلب للنظام الداخلي (وهمي في هذا المثال)
        booking_result = self._send_to_booking_system(booking_data)

        # 3. إعداد الرد للمستخدم
        if booking_result["success"]:
            return {
                "assistant_response": f"تم تأكيد حجزك! رقم الحجز: {booking_result['booking_id']}",
                "booking_confirmed": True,
                "next_stage": "completed"
            }
        else:
            return {
                "assistant_response": "حدث خطأ أثناء معالجة حجزك. يرجى المحاولة لاحقاً.",
                "booking_confirmed": False,
                "next_stage": "booking_failed"
            }

    def _process_booking_cancellation(self, session: Dict) -> Dict:
        """معالجة رفض المستخدم لإتمام الحجز"""

        # 1. تنظيف بيانات الجلسة
        session["collected_data"] = {k: None for k in session["collected_data"]}

        # 2. إعداد الرد والعودة لمرحلة البداية
        return {
            "assistant_response": "تم إلغاء عملية الحجز. هل تريد بدء حجز جديد؟",
            "booking_confirmed": False,
            "next_stage": "welcome"
        }

    def _detect_intent(self, text: str) -> str:
        """Определение намерения пользователя"""
        text = text.lower()
        if any(w in text for w in ["бронь", "забронировать"]):
            return "booking"
        elif any(w in text for w in ["цена", "стоимость"]):
            return "pricing"
        return "general_question"

    def _validate_date(self, date_str: str) -> bool:
        """Валидация формата даты"""
        try:
            datetime.strptime(date_str, "%Y%m%d")
            return True
        except ValueError:
            return False