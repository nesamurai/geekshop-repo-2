from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from users.models import ShopUserProfile


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        profile = user.get_profile()
        if profile is None:
            profile = Profile(user_id=user.id)
        profile.gender = response.get('gender')
        # profile.link = response.get('link')
        # profile.timezone = response.get('timezone')
        profile.username = response.get('username')
        profile.first_name = response.get('first_name')
        profile.last_name = response.get('last_name')
        profile.email = response.get('email')
        profile.save()
