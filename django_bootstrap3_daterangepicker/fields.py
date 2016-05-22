from django import forms
from django.core.exceptions import ValidationError
from django.utils import six
from django.utils.encoding import force_text
from django.utils.translation import string_concat

from .widgets import DateRangeWidget


class DateRangeField(forms.Field):
    widget = DateRangeWidget

    def __init__(self, base=forms.DateField(), **kwargs):
        super(DateRangeField, self).__init__(**kwargs)
        self.base = base

    def to_python(self, value):
        # Try to coerce the value to unicode.
        unicode_value = force_text(value, strings_only=True)
        if isinstance(unicode_value, six.text_type):
            value = unicode_value.strip()

        if self.widget.separator in value:
            parts = value.split(self.widget.separator, 2)

            try:
                part1 = self.base.to_python(parts[0])
            except ValidationError as e:
                raise ValidationError(string_concat('Ошибка в начале периода: ', e.message), e.code)

            try:
                part2 = self.base.to_python(parts[1])
            except ValidationError as e:
                raise ValidationError(string_concat('Ошибка в конце периода: ', e.message), e.code)

            return part1, part2
        else:
            return ()
