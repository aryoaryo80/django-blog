from django import template

register = template.Library()


@register.filter('check_liked')
def check_liked(instance, user):
    if user.is_authenticated:
        return instance.votes.filter(user=user).exists()
