# django-bootstrap3-daterangepicker

This is django field wrapper for http://www.daterangepicker.com/ . Useful for reporting services.

Field data format is tuple (start_date, end_date).

Installation:
---

1. ```pip install django_bootstrap3_daterangepicker```
2. add `'django_bootstrap3_daterangepicker'` to `INSTALLED_APPS`


Usage:
----
* jQuery, Bootstrap are required on target page

```python
class PeriodFilter(forms.Form):
    range = DateRangeField(widget=DateRangeWidget(picker_options={
        'ranges': common_dates()
    }))

# ...    
form = PeriodFilter(initial={'range': (date.today(), date.today())})
# ...
(from_date, to_date) = form.cleaned_data['range']
```

Template - don't forget media:
```html
{% block extracss %}
    {{ filter.media['css'] }}
{% endblock %}
{% block endscripts %}
    {{ super() }}
    {{ filter.media['js'] }}
{% endblock %}

{% block content %}
{{ filter.range }}
{% endblock %}
```

Special thanks to https://github.com/nkunihiko/django-bootstrap3-datetimepicker/ for guidance in creating custom fields.
