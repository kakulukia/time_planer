from django.contrib import admin
from django.utils.safestring import mark_safe

from times.models import Plan, Unit


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['date', 'unit', 'start', 'end']
    actions = None
    date_hierarchy = 'date'
    list_filter = ['unit']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('unit')
        return qs


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'show_color']
    actions = None

    class Media:
        css = {
            'all': ('sass/admin.css',)
        }

    def show_color(self, unit: Unit):
        html = f"<span class='unit-color-display' style='background-color: {unit.color}'></span>"
        return mark_safe(html)
    show_color.short_description = "Farbe"
