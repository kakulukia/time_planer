import pendulum
from django.db.models import Q
from django.shortcuts import render
import pandas as pd
import numpy as np
from django.template.defaultfilters import date

from times.models import Plan, Unit


def time_plan(request):

    # get the start date
    start_date = pendulum.now()
    if 'date' in request.GET:
        start_date = pendulum.parse(request.GET.get('date'))

    # Create the multi-level header
    weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
    units = Unit.objects.all().values_list('name', flat=True)
    header = pd.MultiIndex.from_product([weekdays, units], names=['Weekday', 'Unit'])

    # Create an empty DataFrame with the multi-level header and the correct shape
    unit_count = Unit.objects.count()
    df = pd.DataFrame(np.zeros((48, 7 * unit_count)), columns=header)

    # Create an index with time values for every 30min of a day
    times = []
    current_time = start_date.start_of('day')
    for _ in range(48):
        times.append(current_time.time())
        current_time = current_time.add(minutes=30)
    df.index = times
    df.index.name = "Time"

    df = df.astype(str)
    df = df.replace('0.0', '')

    day = start_date.start_of('week')
    dates = []

    for _ in range(7):
        key = date(day, "l")
        dates.append(date(day, "D. d.m.y"))
        plans = Plan.objects.filter(Q(date=day.date()) | Q(end_datetime__date=day.date()))
        for plan in plans:
            start_index = plan.start_index(day)
            end_index = plan.end_index(day)

            for i in range(start_index, end_index):
                df.at[times[i], (key, plan.unit.name)] = plan.unit.color
        day = day.add(days=1)

    return render(request, 'time_plan.pug', {
        'dates': dates,
        'units': df.columns.get_level_values(1),
        'plan': df,
        'unit_count': unit_count,
        'next_week': date(start_date.add(weeks=1), 'Y-m-d'),
        'previous_week': date(start_date.subtract(weeks=1), 'Y-m-d'),
    })
