from django import template

register = template.Library()


@register.filter('check_liked')
def check_liked(instance, user):
    return instance.votes.filter(user=user).exists()
