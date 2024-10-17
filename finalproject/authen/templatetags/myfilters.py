from django import template

register = template.Library()

@register.filter
def add_style(field, style):
    return field.as_widget(attrs={'style': style})
