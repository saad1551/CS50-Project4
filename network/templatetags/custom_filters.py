from django import template

register = template.Library()

@register.filter(name='user_has_not_liked')
def user_has_not_liked(user, post):
    return user.id not in post.likers.values_list('user', flat=True)