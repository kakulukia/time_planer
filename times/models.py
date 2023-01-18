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
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, verbose_name="Einheit")

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Pläne'

    def __str__(self):
        return f"{self.date} ({self.start} - {self.end})"



