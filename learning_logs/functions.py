"""Auxiliary functions for learning_logs app."""

from django.http import Http404
from django.db.models import Q

from .models import Topic

def check_topic_owner(topic, user):
    """Returns True if user is owner of particular topic."""
    if user.is_authenticated:
        if topic.visibility == 'private' and user != topic.owner:
            raise Http404
            
    else:
        if topic.visibility == 'private':
            raise Http404

def check_topic_duplicity(topic, user):
    """Returns True if topic is not duplicit."""
    if topic.visibility == 'private':
        # search for duplicity only among users private topics
        users_private_topics = Topic.objects.filter(owner=user, text=topic.text)
            
    elif topic.visibility == 'public':
        # search for duplicity in user's private topics and also in all public topics
        users_private_topics = Topic.objects.filter(
            Q(owner=user, text=topic.text)| Q(visibility='public', text=topic.text)
        )
        
    if users_private_topics.exists():
            # result is negative because there is already topic with this name
            return False
    elif users_private_topics.exists() == False:
            return True