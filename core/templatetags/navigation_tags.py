from django import template

from core.models import Navigation

register = template.Library()


@register.inclusion_tag("_navigation.html", takes_context=True)
def navigation(context):
    return {"navigation_items": Navigation.active_objects.all(), "request": context.get("request")}
