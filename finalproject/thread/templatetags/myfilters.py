from django import template

register = template.Library()

@register.filter
def add_style(field, style):
    return field.as_widget(attrs={'style': style})

@register.filter
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()