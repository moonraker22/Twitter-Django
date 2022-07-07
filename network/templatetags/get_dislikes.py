from django import template
from django.db.models import Count
from ..models import Dislikes

register = template.Library()


@register.filter
def get_dislikes(post):
    return Dislikes.objects.filter(post_id=post.id).count()
