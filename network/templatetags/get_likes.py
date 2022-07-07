from django import template
from django.db.models import Count
from ..models import Likes

register = template.Library()


@register.filter
def get_likes(post):
    return Likes.objects.filter(post_id=post.id).count()
