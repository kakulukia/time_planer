from datetime import datetime, timedelta

from colorfield.fields import ColorField
from django.db import models


class Unit(models.Model):
    name = models.CharField(max_length=20)
    color = ColorField(default='#FF0000')

    class Meta:
        verbose_name = 'Einheit'
        verbose_name_plural = 'Einheiten'
        ordering = ['name']

    def __str__(self):
        return self.name


class Plan(models.Model):
    date = models.DateField(verbose_name="Tag")
    start = models.TimeField(verbose_name="Start")
    end = models.TimeField(verbose_name="Ende")
    end_datetime = models.DateTimeField(null=True, editable=False)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, verbose_name="Einheit")

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Pläne'

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.end_datetime = self.calc_end_datetime()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f"{self.date} ({self.start} - {self.end})"

    def calc_end_datetime(self):
        day = self.date
        end_datetime = datetime.combine(day, self.end)

        if self.end < self.start:
            end_datetime += timedelta(days=1)
        return end_datetime

    def start_index(self, day: datetime):
        start_index = None
        if day.date() == self.date:
            start_index = self.start.hour * 2 + int(self.start.minute > 30)
        elif day.date() == self.end_datetime.date():
            start_index = 0
        return start_index

    def end_index(self, day: datetime):
        end_index = None
        if day.date() == self.end_datetime.date():
            end_index = self.end.hour * 2 + int(self.end.minute > 30)
        elif day.date() == self.date:
            end_index = 48
        return end_index
