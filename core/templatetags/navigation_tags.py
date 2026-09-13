from django import template

from core.models import Navigation

register = template.Library()


@register.inclusion_tag("_navigation.html", takes_context=True)
def navigation(context):
    context = {
        "navigation_items": Navigation.active_objects.all(),
        "unauthenticated_navigation_items": Navigation.active_unauthenticated_objects.all(),
        "request": context.get("request"),
    }
    return context
