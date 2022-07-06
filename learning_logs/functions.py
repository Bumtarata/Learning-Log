"""Auxiliary functions for learning_logs app."""

from django.http import Http404

def check_topic_owner(topic, user):
    """Returns True if user is owner of particular topic."""
    if topic.visibility == 'private':
        if user != topic.owner:
            raise Http404