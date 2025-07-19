import unittest
from dialog_manager import DialogManager


class TestDialogManager(unittest.TestCase):

    def setUp(self):
        self.manager = DialogManager()

    def test_welcome_stage(self):
        context = self.manager.process_input("test1", "Привет")
        self.assertEqual(context["stage"], "приветствие")

    def test_booking_intent(self):
        context = self.manager.process_input("test2", "Хочу забронировать номер")
        self.assertEqual(context["intent"], "booking")


if __name__ == "__main__":
    unittest.main()