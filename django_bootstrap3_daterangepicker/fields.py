from django import forms
from django.core.exceptions import ValidationError
from django.utils import six
from django.utils.encoding import force_str
from django.utils.translation import string_concat, gettext_lazy as _

from .widgets import DateRangeWidget


class DateRangeField(forms.Field):
    widget = DateRangeWidget

    def __init__(self, base=forms.DateField(), input_formats=None, **kwargs):
        """
        :param base: can be either DateField or DateTimeField, which will be used to do conversions for beginning and end of interval.
        :param input_formats: is passed into base if present
        """
        super(DateRangeField, self).__init__(**kwargs)
        self.base = base
        if input_formats is not None:
            self.base.input_formats = input_formats

    def to_python(self, value):
        # Try to coerce the value to unicode.
        unicode_value = force_str(value, strings_only=True)
        if isinstance(unicode_value, six.text_type):
            value = unicode_value.strip()
        else:
            raise ValidationError(
                _("Date range value given was not able to be converted to unicode.")
            )

        if self.widget.separator in value:
            str_dates = value.split(self.widget.separator, 2)

            try:
                beginning = self.base.to_python(str_dates[0])
            except ValidationError as e:
                raise ValidationError(string_concat('Error in period beginning: ', e.message), e.code)

            try:
                end = self.base.to_python(str_dates[1])
            except ValidationError as e:
                raise ValidationError(string_concat('Error in period end: ', e.message), e.code)

            return beginning, end
        else:
            raise ValidationError(
                _("Invalid date range format."),
                code='invalid'
            )
