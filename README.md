# django-bootstrap3-daterangepicker

This is django field wrapper for http://www.daterangepicker.com/ . Usefull for some reporting services.

Field data format is tuple (startdate, enddate).

Usage:
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

