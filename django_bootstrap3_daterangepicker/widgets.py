import json
import re
from collections import OrderedDict

from datetime import date, datetime, timedelta
from django import forms
from django.utils import formats
from django.utils.safestring import mark_safe

__all__ = ['DateRangeWidget', 'add_month', 'common_dates']

format_to_js = {
    '%m': 'MM',
    '%d': 'DD',
    '%Y': 'YYYY',
    '%y': 'YY',
    '%B': 'MMMM',
    '%b': 'MMM',
}

format_to_js_re = re.compile(r'(?<!\w)(' + '|'.join(format_to_js.keys()) + r')\b')


def add_month(target_date, months):
    year, month = divmod(target_date.month + months, 12)
    if month == 0:
        month = 12
        year -= 1
    return date(target_date.year + year, month, target_date.day)


def common_dates():
    today = date.today()
    one_day = timedelta(days=1)
    return OrderedDict([
        ('Today', (today, today)),
        ('Yesterday', (today - one_day, today - one_day)),
        ('This week', (today - timedelta(days=today.weekday()), today)),
        ('Last week', (today - timedelta(days=today.weekday() + 7), today - timedelta(days=today.weekday() + 1))),
        ('Week ago', (today - timedelta(days=7), today)),
        ('This month', (today.replace(day=1), add_month(today, 1) - one_day)),
        ('Last month', (add_month(today.replace(day=1), -1), today.replace(day=1) - one_day)),
        ('3 months', (add_month(today, -3), today)),
        ('Year', (add_month(today, -12), today)),
    ])


class DateRangeWidget(forms.TextInput):
    format_key = 'DATE_INPUT_FORMATS'

    def __init__(self, picker_options=None, attrs=None, format=None, separator=' - '):
        super(DateRangeWidget, self).__init__(attrs)
        self.separator = separator
        self.format = format
        self.picker_options = picker_options or {}

    def __format(self):
        return self.format or formats.get_format(self.format_key)[0]

    def __format_date(self, value):
        return formats.localize_input(value, self.__format())

    def _format_value(self, value):
        if isinstance(value, tuple):
            return self.__format_date(value[0]) + \
                   self.separator + \
                   self.__format_date(value[1])
        else:
            return value

    script_template = """
        <script type="text/javascript">
        $(function() {{
            $('#{id}').daterangepicker({options});
        }});
        </script>
        """

    date_options = {'startDate', 'endDate', 'minDate', 'maxDate'}

    def render(self, name, value, attrs=None):
        date_format = self.__format()
        js_format = format_to_js_re.sub(lambda m: format_to_js[m.group()], date_format)

        options = {
            'locale': {
                'format': js_format
            }
        }

        def convert_dates(v):
            if callable(v):
                v = v()

            if isinstance(v, date) or isinstance(v, datetime):
                return v.strftime(date_format)
            else:
                return str(v)

        picker_options = self.picker_options if not callable(self.picker_options) else self.picker_options()
        options.update(picker_options)

        options_js = json.dumps(options, default=convert_dates, indent="    ")

        script = self.script_template.format(id=attrs['id'], options=options_js)

        attrs = attrs or {}
        if 'class' not in attrs:
            attrs['class'] = 'form-control'
        return mark_safe(super(DateRangeWidget, self).render(name, value, attrs) + script)

    class Media:
        css = {
            'all': ('daterangepicker/daterangepicker.css',)
        }
        js = ('momentjs/moment.js', 'daterangepicker/daterangepicker.js')
