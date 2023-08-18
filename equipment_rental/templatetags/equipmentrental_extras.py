from datetime import datetime, timedelta

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, field, value):
    dict_ = context["request"].GET.copy()
    dict_.__setitem__(field, value)
    return dict_.urlencode()


@register.filter(name="pages")
def paginator(pages, current, num=8):
    if num >= pages:
        return range(1, pages + 1)
    elif current - num / 2 < 1:
        return range(1, num + 1)
    elif current + num / 2 > pages:
        return range(pages - num + 1, pages + 1)
    else:
        return range(int(current - num / 2) + 1, int(current + num / 2) + 1)


@register.filter(name="getbypk")
def find_by_pk(elements, pk):
    for e in elements:
        if e.pk == pk:
            return e
    return None


@register.filter(name="moredays")
def moredays(basedate, days):
    newdate = datetime.strptime(basedate, "%Y-%m-%d") + timedelta(days=days)
    return newdate.strftime("%Y-%m-%d")


@register.filter(name="substract")
def subtract(value, arg):
    return value - arg
