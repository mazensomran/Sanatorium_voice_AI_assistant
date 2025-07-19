import unittest
from .crm import CRMIntegrator


class TestCRMIntegrator(unittest.TestCase):

    def setUp(self):
        self.crm = CRMIntegrator()

    def test_booking_request_generation(self):
        test_data = {
            "check_in": "20250101",
            "check_out": "20250110",
            "adults": 2,
            "guest_name": "Иванов Иван",
            "phone": "+79101234567"
        }

        request = self.crm.generate_booking_request(test_data)

        self.assertEqual(request["ChekInDate"], "202501011200")
        self.assertEqual(request["Adult"], 2)
        self.assertEqual(request["MainGuestName"], "Иванов Иван")


if __name__ == "__main__":
    unittest.main()