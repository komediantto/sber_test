from django.test import TestCase
from rest_framework.test import APIClient
from .serializers import Application
import json
from random import randint


class TestCalc(TestCase):
    """Тестируем методы Application"""

    def setUp(self):
        self.application = Application('31.01.2021', 3, 10000, 6)
        self.guest_client = APIClient()
        self.data = {'periods': self.application.periods,
                     'amount': self.application.amount,
                     'rate': self.application.rate}
        self.endpoint = '/deposite/'

    def test_last_day_of_month(self):
        response = self.guest_client.post(
            self.endpoint,
            {'date': self.application.date} | self.data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"31.01.2021": 10050.0,
                                         "28.02.2021": 10100.25,
                                         "31.03.2021": 10150.75})

    def test_day_more_february(self):
        self.application.date = '30.01.2021'
        response = self.guest_client.post(
            self.endpoint,
            {'date': self.application.date} | self.data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"30.01.2021": 10050.0,
                                         "28.02.2021": 10100.25,
                                         "30.03.2021": 10150.75})

    def test_another_days(self):
        self.application.date = '5.01.2021'
        response = self.guest_client.post(
            self.endpoint,
            {'date': self.application.date} | self.data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"05.01.2021": 10050.0,
                                         "05.02.2021": 10100.25,
                                         "05.03.2021": 10150.75})

    def test_year(self):
        self.application.date = '31.12.2021'
        response = self.guest_client.post(
            self.endpoint,
            {'date': self.application.date} | self.data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"31.12.2021": 10050.0,
                                         "31.01.2022": 10100.25,
                                         "28.02.2022": 10150.75})

    def test_invalid_date(self):
        self.application.date = '2021-12-31'
        response = self.guest_client.post(
            self.endpoint,
            {'date': self.application.date} | self.data, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            content['date'][0],
            'Date has wrong format. '
            'Use one of these formats instead: DD.MM.YYYY.')

    def test_invalid_periods_more(self):
        self.application.periods = 70
        self.data['periods'] = self.application.periods
        response = self.guest_client.post(
            self.endpoint,
            {'date': self.application.date} | self.data, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            content['periods'][0],
            'Ensure this value is less than or equal to 60.')

    def test_invalid_periods_less(self):
        self.application.periods = -1
        self.data['periods'] = self.application.periods
        response = self.guest_client.post(
            self.endpoint,
            {'date': self.application.date} | self.data, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            content['periods'][0],
            'Ensure this value is greater than or equal to 1.')

    def test_invalid_amount_more(self):
        self.application.amount = 5000000
        self.data['amount'] = self.application.amount
        response = self.guest_client.post(
            self.endpoint,
            {'date': self.application.date} | self.data, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            content['amount'][0],
            'Ensure this value is less than or equal to 3000000.')

    def test_invalid_amount_less(self):
        self.application.amount = 9000
        self.data['amount'] = self.application.amount
        response = self.guest_client.post(
            self.endpoint,
            {'date': self.application.date} | self.data, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            content['amount'][0],
            'Ensure this value is greater than or equal to 10000.')

    def test_invalid_rate_more(self):
        self.application.rate = 9.5
        self.data['rate'] = self.application.rate
        response = self.guest_client.post(
            self.endpoint,
            {'date': self.application.date} | self.data, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            content['rate'][0],
            'Ensure this value is less than or equal to 8.')

    def test_invalid_rate_less(self):
        self.application.rate = -1
        self.data['rate'] = self.application.rate
        response = self.guest_client.post(
            self.endpoint,
            {'date': self.application.date} | self.data, format='json')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            content['rate'][0],
            'Ensure this value is greater than or equal to 1.')
