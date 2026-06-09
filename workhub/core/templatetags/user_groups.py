from django import template

register = template.Library()

@register.filter
def has_group(user, group_name):
    """Проверяет, состоит ли пользователь в указанной группе."""
    return user.groups.filter(name=group_name).exists()
