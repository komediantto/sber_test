import calendar
from rest_framework import serializers
from dataclasses import dataclass
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta
from dateutil.relativedelta import relativedelta


@dataclass
class Application():
    date: str
    periods: int
    amount: int
    rate: float

    def calc_deposit(self):
        profits = {}

        if self.is_last_day_of_month():
            for _ in range(self.periods):
                self.amount *= (1 + self.rate/12/100)
                next_month = (self.date + relativedelta(months=1))
                next_date = next_month.replace(day=calendar.monthrange(
                    next_month.year, next_month.month)[1])
                response_date = str(self.date.strftime("%d.%m.%Y"))
                profits[response_date] = round(self.amount, 2)
                self.date = next_date
            return profits
        else:
            start_day = self.date.day
            for _ in range(self.periods):
                self.amount *= (1 + self.rate/12/100)
                if self.date.month == 2:
                    wrong_next_date = self.date + relativedelta(months=1)
                    next_date = wrong_next_date.replace(
                        day=self.date.day + (start_day - self.date.day))
                else:
                    next_date = self.date + relativedelta(months=1)
                response_date = str(self.date.strftime("%d.%m.%Y"))
                profits[response_date] = round(self.amount, 2)
                self.date = next_date
            return profits

    def is_last_day_of_month(self):
        next_day = self.date + timedelta(days=1)
        return next_day.month != self.date.month


class ApplicationSerializer(serializers.Serializer):
    date = serializers.DateField(format='%d.%m.%Y', input_formats=['%d.%m.%Y'])
    periods = serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(60)])
    amount = serializers.IntegerField(
        validators=[MinValueValidator(10000), MaxValueValidator(3000000)])
    rate = serializers.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(8)])

    def create(self, validated_data):
        return Application(**validated_data)
